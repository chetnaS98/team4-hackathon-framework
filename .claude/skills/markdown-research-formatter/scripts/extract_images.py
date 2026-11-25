#!/usr/bin/env python3
"""Extract every meaningful image from a source so it can be embedded in the .md and transcribed.

Usage: python extract_images.py <input> <work_dir> [--render-pages]
  .png/.jpg/.jpeg/.gif/.webp  copied as fig01
  .pptx   pictures (incl. inside groups), slide order, with 'slide' number
  .docx   word/media in document order
  .pdf    embedded raster images (pdfimages), with 'page' number
  .xlsx   xl/media (no location info)
  --render-pages  also render whole pages/slides to PNG (pdf, pptx via soffice). Use for charts,
                  SmartArt, native shapes and vector diagrams, which are not embedded images.
Writes <work_dir>/images/figNN.<ext> and <work_dir>/images.json.
Skips (listed under "skipped") images <48px on a side and exact duplicates (logos, bullets, icons).
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
MIN_SIDE = 48


def size_of(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


class Collector:
    def __init__(self, work):
        self.dir = Path(work) / "images"
        shutil.rmtree(self.dir, ignore_errors=True)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.items, self.skipped, self.seen = [], [], {}

    def add(self, blob, ext, **where):
        ext = ext.lower().lstrip(".")
        ext = "jpg" if ext == "jpeg" else ext
        h = hashlib.sha1(blob).hexdigest()
        loc = ", ".join(f"{k} {v}" for k, v in where.items()) or "n/a"
        if h in self.seen:
            self.skipped.append({"where": loc, "reason": f"duplicate of {self.seen[h]}"})
            return
        tmp = self.dir / f"_tmp.{ext}"
        tmp.write_bytes(blob)
        sz = size_of(tmp)
        if sz and min(sz) < MIN_SIDE:
            tmp.unlink()
            self.skipped.append({"where": loc, "reason": f"tiny {sz[0]}x{sz[1]} (icon/bullet)"})
            return
        fid = f"fig{len(self.items) + 1:02d}"
        dest = self.dir / f"{fid}.{ext}"
        tmp.rename(dest)
        self.seen[h] = fid
        item = {"id": fid, "file": str(dest), **where}
        if sz:
            item["size"] = f"{sz[0]}x{sz[1]}"
        self.items.append(item)

    def add_file(self, path, **where):
        p = Path(path)
        self.add(p.read_bytes(), p.suffix, **where)


def from_pptx(src, col):
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE

    def walk(shapes, n):
        for sh in shapes:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                walk(sh.shapes, n)
                continue
            try:
                img = sh.image  # pictures and picture placeholders
            except Exception:
                continue
            col.add(img.blob, img.ext, slide=n)

    for n, s in enumerate(Presentation(src).slides, 1):
        walk(s.shapes, n)


def from_docx(src, col):
    z = zipfile.ZipFile(src)
    rels = z.read("word/_rels/document.xml.rels").decode("utf-8")
    target = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    target.update({k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="([^"]+)"', rels)})
    doc = z.read("word/document.xml").decode("utf-8")
    for rid in re.findall(r'r:(?:embed|id)="([^"]+)"', doc):
        t = target.get(rid, "")
        if t.startswith("media/"):
            col.add(z.read("word/" + t), Path(t).suffix, order=len(col.items) + len(col.skipped) + 1)


def from_xlsx(src, col):
    z = zipfile.ZipFile(src)
    for n in sorted(x for x in z.namelist() if x.startswith("xl/media/")):
        col.add(z.read(n), Path(n).suffix)


def from_pdf(src, col):
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdfimages", "-png", "-p", str(src), f"{td}/i"], check=True)
        for f in sorted(Path(td).glob("i-*.png")):
            m = re.match(r"i-(\d+)-\d+\.png", f.name)
            col.add(f.read_bytes(), "png", page=int(m.group(1)) if m else "?")


def render_pages(src, col):
    src = Path(src)
    with tempfile.TemporaryDirectory() as td:
        pdf = src
        if src.suffix.lower() == ".pptx":
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", td, str(src)],
                           check=True, stdout=subprocess.DEVNULL)
            pdf = Path(td) / (src.stem + ".pdf")
        subprocess.run(["pdftoppm", "-png", "-r", "110", str(pdf), f"{td}/pg"], check=True)
        for f in sorted(Path(td).glob("pg-*.png")):
            n = int(re.search(r"-(\d+)\.png$", f.name).group(1))
            col.add(f.read_bytes(), "png", **{"slide" if src.suffix.lower() == ".pptx" else "page": n,
                                              "kind": "rendered-page"})


def main(a):
    args = [x for x in a[1:] if x != "--render-pages"]
    render = "--render-pages" in a
    if len(args) != 2:
        print(__doc__)
        return 2
    src, work = Path(args[0]), Path(args[1])
    ext = src.suffix.lower()
    col = Collector(work)
    if ext in IMG_EXT:
        col.add_file(src)
    elif ext == ".pptx":
        from_pptx(src, col)
    elif ext == ".docx":
        from_docx(src, col)
    elif ext in (".xlsx", ".xlsm"):
        from_xlsx(src, col)
    elif ext == ".pdf":
        from_pdf(src, col)
    else:
        print(f"No image extraction for {ext}; if the input has none, skip this step.")
    if render:
        render_pages(src, col)
    out = Path(work) / "images.json"
    out.write_text(json.dumps({"source": src.name, "figures": col.items, "skipped": col.skipped},
                              indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(col.items)} image(s) kept, {len(col.skipped)} skipped -> {out}")
    for it in col.items:
        print(" ", {k: v for k, v in it.items() if k != "file"}, Path(it["file"]).name)
    for s in col.skipped:
        print("  skipped:", s)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
