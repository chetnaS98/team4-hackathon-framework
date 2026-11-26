#!/usr/bin/env python3
"""Validate a research Markdown file: front matter schema, filename, and body basics.

Usage: python validate_md.py <file.md> [<file2.md> ...] [--source original.txt] [--profile research-profile.json]
--source (transcripts): verifies every source line survives unchanged and in order.
--profile: project profile with allowed products/lifecycle stages. If omitted, the nearest
           research-profile.json above each .md is used; with none, only formats are checked (warning).
Exit code 0 = no errors (warnings allowed), 1 = at least one error.
Requires PyYAML.
"""
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from research_profile import load_profile  # noqa: E402
RESEARCH_TYPES = {"discovery", "design-feedback", "both"}
CONTENT_TYPES = {"transcript", "synthesis", "workflow-map", "spreadsheet",
                 "guide", "deck", "notes", "persona"}
STATUS = {"raw", "cleaned", "synthesized", "final"}
CONFIDENTIALITY = {"internal", "customer-confidential", "public"}
REQUIRED = ["title", "description", "product", "personas", "lifecycle", "workflow",
            "research_type", "content_type", "date"]
OPTIONAL = ["customer", "participants", "status", "source_file", "related", "jira_confluence",
            "tags", "confidentiality", "schema_version"]
JIRA_KEY = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FILENAME = re.compile(
    r"^(?P<product>[a-z]+)_(?P<workflow>[a-z0-9]+(?:-[a-z0-9]+)*)_"
    r"(?P<ctype>[a-z0-9]+(?:-[a-z0-9]+)*)_v(?P<ver>\d+)\.md$"
)


def norm(text):
    """Lowercase and collapse non-alphanumerics to single hyphens."""
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def split_front_matter(text):
    if text.startswith("\ufeff"):
        return None, None, "File starts with a BOM; remove it so '---' is the first characters."
    if not text.startswith("---\n"):
        return None, None, "File must start with '---' on line 1."
    end = text.find("\n---", 4)
    if end == -1:
        return None, None, "Closing '---' for front matter not found."
    raw = text[4:end]
    body = text[end + 4:].lstrip("\n")
    return raw, body, None


def check_verbatim(out_text, source_path):
    """Every source line must appear in the output, unchanged, in the original order.
    Returns (error_or_None, set_of_matched_output_line_indexes)."""
    src = Path(source_path).read_bytes().decode("utf-8").splitlines(keepends=True)
    out = out_text.splitlines(keepends=True)
    i, matched = 0, set()
    for n, line in enumerate(src, 1):
        while i < len(out) and out[i] != line:
            i += 1
        if i == len(out):
            return f"Source line {n} missing or altered/reordered: {line.rstrip()[:70]!r}", matched
        matched.add(i)
        i += 1
    return None, matched


IMG_LINK = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def check_images(p, body, source_lines, errors, warnings):
    """Every image we added must resolve, have alt text, and be followed by its transcription.
    Image refs that came verbatim from the source are only warned about when they do not resolve."""
    blines = body.splitlines()
    used = set()
    for i, l in enumerate(blines):
        for alt, target in IMG_LINK.findall(l):
            from_source = l in source_lines and l.strip() != ""
            ok = not re.match(r"^(https?:|/|[A-Za-z]:)", target) and (p.parent / target).is_file()
            if from_source:
                if not ok:
                    warnings.append(f"Source image reference does not resolve (kept verbatim): {target}; "
                                    "embed the real image as a figure block next to it.")
                continue
            if not ok:
                errors.append(f"Image link does not resolve to a file next to the .md (use a relative path "
                              f"under assets/): {target}")
                continue
            used.add((p.parent / target).resolve())
            if not target.startswith("assets/"):
                warnings.append(f"Image {target} is not under assets/.")
            if not alt.strip():
                errors.append(f"Image {target} has empty alt text.")
            tail = []
            for nxt in blines[i + 1:]:
                if re.match(r"^#{1,6} ", nxt) or IMG_LINK.search(nxt):
                    break
                tail.append(nxt)
            text = " ".join(t for t in tail if t.strip())
            m = re.match(r"^\**Transcription:?\**:?\s*(.*)$", text.strip(), re.S)
            if not m or len(m.group(1).strip()) < 10:
                errors.append(f"Image {target} is not followed by a '**Transcription:**' block with its "
                              "full text (every visible element, or [illegible: where]).")
    stem = p.stem
    adir = p.parent / "assets"
    if adir.is_dir():
        for f in adir.glob(f"{stem}_fig*"):
            if f.resolve() not in used:
                warnings.append(f"assets/{f.name} is not referenced by {p.name}.")


def validate(path, source=None, profile_path=None):
    errors, warnings = [], []
    p = Path(path)
    text = p.read_bytes().decode("utf-8")
    try:
        prof, prof_path = load_profile(profile_path, start=p.parent)
    except (ValueError, OSError) as e:
        return [f"Project profile invalid: {e}"], warnings
    if prof is None:
        warnings.append("No research-profile.json found above this file (and no --profile); "
                        "product/lifecycle values were only format-checked.")
    products = set(prof["products"]) if prof else None
    lifecycle = (set(prof["lifecycle"]) | {"multi"}) if prof and prof.get("lifecycle") else None

    raw, body, err = split_front_matter(text)
    if err:
        return [err], warnings
    if "\t" in raw:
        errors.append("Front matter contains tab characters; use spaces.")
    try:
        fm = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return [f"Front matter is not valid YAML: {e}"], warnings
    if not isinstance(fm, dict):
        return ["Front matter must be a YAML mapping of key: value pairs."], warnings

    for k in REQUIRED:
        if k not in fm or fm[k] in (None, "", []):
            errors.append(f"Missing required field: {k}")
    for k in fm:
        if k not in REQUIRED + OPTIONAL:
            errors.append(f"Unknown field '{k}' (not in schema; see the Front matter section of SKILL.md)")

    def enum(field, allowed):
        v = fm.get(field)
        if v is not None and v not in allowed:
            errors.append(f"{field}='{v}' not in {sorted(allowed)}")

    def list_of(field, allowed=None, kebab=False):
        v = fm.get(field)
        if v is None:
            return
        if not isinstance(v, list):
            errors.append(f"{field} must be a list, e.g. [a, b]")
            return
        for item in v:
            if not isinstance(item, str):
                errors.append(f"{field} items must be strings")
            elif allowed and item not in allowed:
                errors.append(f"{field} value '{item}' not in {sorted(allowed)}")
            elif kebab and not KEBAB.match(item):
                errors.append(f"{field} value '{item}' must be lowercase kebab-case")

    if products is not None:
        enum("product", products)
    elif fm.get("product") is not None and not KEBAB.match(str(fm.get("product"))):
        errors.append("product must be lowercase kebab-case")
    enum("research_type", RESEARCH_TYPES)
    enum("content_type", CONTENT_TYPES)
    if "status" in fm:
        enum("status", STATUS)
    if "confidentiality" in fm:
        enum("confidentiality", CONFIDENTIALITY)
    list_of("lifecycle", lifecycle, kebab=lifecycle is None)
    list_of("personas", kebab=True)
    list_of("workflow", kebab=True)
    if prof:
        for field, key in (("personas", "personas"), ("workflow", "workflows")):
            known = prof.get(key)
            vals = fm.get(field) if isinstance(fm.get(field), list) else []
            new = [v for v in vals if known is not None and v not in known]
            if new:
                warnings.append(f"{field} value(s) {new} not in profile {key}; confirm and add to {prof_path.name}.")
    if "tags" in fm:
        list_of("tags", kebab=True)
        if isinstance(fm["tags"], list) and len(fm["tags"]) > 6:
            warnings.append("More than 6 tags; trim to the most useful.")
    if "related" in fm and not isinstance(fm["related"], list):
        errors.append("related must be a list of filenames")
    if "jira_confluence" in fm:
        jc = fm["jira_confluence"]
        if not isinstance(jc, list) or not jc:
            errors.append("jira_confluence must be a non-empty list of Jira/Confluence URLs; omit the field if none were confirmed")
        else:
            for item in jc:
                if not isinstance(item, str) or not (re.match(r"^https://\S+$", item) or JIRA_KEY.match(item)):
                    errors.append(f"jira_confluence entry {item!r} must be an https URL (or a Jira key like IT-482)")
            if len(set(map(str, jc))) != len(jc):
                warnings.append("jira_confluence has duplicate entries.")

    d = fm.get("date")
    if d is not None and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(d)):
        errors.append("date must be ISO format YYYY-MM-DD")

    desc = fm.get("description")
    if isinstance(desc, str):
        if len(desc) > 300:
            errors.append(f"description is {len(desc)} chars; keep it ≤300.")
        if len(desc) < 40:
            warnings.append("description is very short; say what the file contains and what it can answer.")
    if "customer" in fm:
        c = fm["customer"]
        vals = c if isinstance(c, list) else [c]
        if not vals or not all(isinstance(x, str) and x.strip() for x in vals):
            errors.append("customer must be a non-empty string (or list of strings); omit the field if no customer applies")
        elif any(x.strip().lower() in {"none", "n/a", "na", "null", "unknown", "tbd"} for x in vals):
            errors.append("customer must be a real customer name; omit the field when research is not customer-specific")
    if "participants" in fm and not isinstance(fm["participants"], int):
        errors.append("participants must be an integer")

    title = fm.get("title")
    # Title format: Product | Workflow | Content type [Qualifier] | vN
    title_parts = None
    if isinstance(title, str):
        title_parts = [x.strip() for x in title.split("|")]
        if len(title_parts) != 4:
            errors.append("title must have 4 pipe-delimited segments: "
                          "Product | Workflow | Content type [Qualifier] | vN")
            title_parts = None
        else:
            if norm(title_parts[0]) != str(fm.get("product")):
                errors.append("title product segment does not match product field")
            wf0 = fm.get("workflow")[0] if isinstance(fm.get("workflow"), list) and fm.get("workflow") else None
            if wf0 and norm(title_parts[1]) != wf0:
                errors.append(f"title workflow '{title_parts[1]}' does not match primary workflow '{wf0}'")
            ct = fm.get("content_type")
            if ct and not norm(title_parts[2]).startswith(str(ct)):
                errors.append(f"title content type segment '{title_parts[2]}' must start with content_type '{ct}'")
            if not re.match(r"^v\d+$", title_parts[3]):
                errors.append("title's last segment must be a version like v1")

    # Filename: product_workflow_content-type[-qualifier]_vN.md
    m = FILENAME.match(p.name)
    if not m:
        errors.append("Filename does not match product_workflow_content-type[-qualifier]_vN.md "
                      "(four underscore-separated segments, lowercase, hyphens inside segments)")
    else:
        g = m.groupdict()
        if fm.get("product") != g["product"]:
            errors.append(f"Filename product '{g['product']}' != front matter product '{fm.get('product')}'")
        wf = fm.get("workflow")
        if isinstance(wf, list) and wf and g["workflow"] != wf[0]:
            errors.append(f"Filename workflow '{g['workflow']}' != primary workflow '{wf[0]}'")
        ct = fm.get("content_type")
        if ct and not (g["ctype"] == ct or g["ctype"].startswith(ct + "-")):
            errors.append(f"Filename content-type segment '{g['ctype']}' must be '{ct}' or '{ct}-<qualifier>'")
        if title_parts:
            if norm(title_parts[2]) != g["ctype"]:
                errors.append(f"Title content-type/qualifier '{title_parts[2]}' != filename segment '{g['ctype']}'")
            if title_parts[3] != f"v{g['ver']}":
                errors.append(f"Title version '{title_parts[3]}' != filename version 'v{g['ver']}'")
        if len(p.name) > 60:
            warnings.append("Filename is over ~60 characters; shorten the workflow name.")

    # Body checks (verbatim source lines are excluded: they may legitimately start with '#')
    skip = set()
    verbatim_msg = None
    if source:
        verbatim_msg, matched = check_verbatim(text, source)
        skip = {out_line.rstrip("\r\n") for k, out_line in enumerate(text.splitlines(keepends=True)) if k in matched}
    lines = [l for l in body.splitlines() if l not in skip or not l.strip()]
    h1 = [l for l in lines if re.match(r"^# [^#]", l)]
    if len(h1) != 1:
        errors.append(f"Body must have exactly one H1; found {len(h1)}.")
    elif isinstance(title, str) and "|" in title:
        expected_h1 = "# " + " | ".join(x.strip() for x in title.split("|")[:-1])
        if h1[0].strip() != expected_h1:
            warnings.append("H1 should equal the title without the trailing version segment.")
    first_content = next((l for l in lines if l.strip() and not l.startswith("# ")), "")
    if not (first_content.startswith("*") and first_content.rstrip().endswith("*")):
        warnings.append("No italic context line right after the H1 (one sentence naming product, "
                        "workflow, stage, research type, and what the file is).")
    prev = 0
    in_code = False
    for l in body.splitlines():  # all lines, incl. verbatim source headings, for level order
        if l.startswith("```") or l.startswith("~~~"):
            in_code = not in_code
        if in_code:
            continue
        hm = re.match(r"^(#{1,6}) ", l)
        if hm:
            lvl = len(hm.group(1))
            if prev and lvl > prev + 1:
                warnings.append(f"Heading level jumps from H{prev} to H{lvl}: '{l[:50]}'")
            prev = lvl
    check_images(p, body, skip, errors, warnings)
    if re.search(r"<(div|span|table|img)\b", body, re.I):
        warnings.append("Inline HTML found in body; prefer plain Markdown.")
    if "TODO" in body or "<Body follows" in body:
        errors.append("Placeholder text left in body.")
    if source:
        if verbatim_msg:
            errors.append("Transcript not verbatim: " + verbatim_msg)
    elif fm.get("content_type") == "transcript":
        warnings.append("Transcript: re-run with --source <original> to prove nothing was altered or deleted.")
    return errors, warnings


def main(argv):
    args = argv[1:]
    source = None
    if "--source" in args:
        k = args.index("--source")
        source = args[k + 1] if k + 1 < len(args) else None
        args = args[:k] + args[k + 2:]
    profile_path = None
    if "--profile" in args:
        k = args.index("--profile")
        profile_path = args[k + 1] if k + 1 < len(args) else None
        args = args[:k] + args[k + 2:]
    if not args:
        print(__doc__)
        return 2
    failed = False
    for f in args:
        errs, warns = validate(f, source, profile_path)
        status = "FAIL" if errs else "OK"
        print(f"[{status}] {f}")
        for e in errs:
            print(f"  ERROR: {e}")
        for w in warns:
            print(f"  warn:  {w}")
        failed = failed or bool(errs)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
