#!/usr/bin/env python3
"""Per-user output-location config for markdown-research-formatter.

The skill is shared, so no path is baked into it. Each user stores their own locations once, here:
  ~/.config/markdown-research-formatter/config.json   (override the file with env MRF_CONFIG)

Usage:
  python config.py show                          # print config as JSON ({"configured": false} if none)
  python config.py check                         # exit 0 if the local folder is set and writable, else 1
  python config.py set --local PATH [--sharepoint PATH]
  python config.py set --sharepoint PATH         # change one value, keep the other
  python config.py set --clear-sharepoint        # remove the SharePoint location

Keys: local_output_dir (required), sharepoint_output_dir (optional; a SharePoint/OneDrive-synced folder
that must already exist; this script never creates it). `set` creates the local folder if it is missing.
Output is always one JSON object on stdout.
"""
import argparse
import json
import os
import sys
from pathlib import Path


def cfg_path():
    return Path(os.environ.get("MRF_CONFIG") or Path.home() / ".config" / "markdown-research-formatter" / "config.json")


def load():
    p = cfg_path()
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def writable(d):
    return d.is_dir() and os.access(d, os.W_OK | os.X_OK)


def status(c):
    local = c.get("local_output_dir")
    sp = c.get("sharepoint_output_dir")
    return {
        "configured": bool(local),
        "config_file": str(cfg_path()),
        "local_output_dir": local,
        "local_writable": bool(local) and writable(Path(local)),
        "sharepoint_output_dir": sp,
        "sharepoint_available": bool(sp) and writable(Path(sp)),
    }


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show")
    sub.add_parser("check")
    s = sub.add_parser("set")
    s.add_argument("--local")
    s.add_argument("--sharepoint")
    s.add_argument("--clear-sharepoint", action="store_true")
    a = ap.parse_args(argv[1:])

    c = load()
    if a.cmd == "show":
        print(json.dumps(status(c), indent=2))
        return 0
    if a.cmd == "check":
        st = status(c)
        print(json.dumps(st, indent=2))
        return 0 if st["configured"] and st["local_writable"] else 1

    # set
    if a.local:
        d = Path(a.local).expanduser()
        if not d.is_absolute():
            print(json.dumps({"error": "--local must be an absolute path"}))
            return 2
        try:
            d.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(json.dumps({"error": f"cannot create local folder: {e}"}))
            return 1
        if not writable(d):
            print(json.dumps({"error": f"local folder is not writable: {d}"}))
            return 1
        c["local_output_dir"] = str(d)
    if a.sharepoint:
        d = Path(a.sharepoint).expanduser()
        if not d.is_dir():
            print(json.dumps({"error": f"SharePoint folder does not exist (it must be an existing synced folder): {d}"}))
            return 1
        c["sharepoint_output_dir"] = str(d)
    if a.clear_sharepoint:
        c.pop("sharepoint_output_dir", None)
    if not c.get("local_output_dir"):
        print(json.dumps({"error": "a local output folder is required: pass --local PATH"}))
        return 2
    p = cfg_path()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(c, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        print(json.dumps({"error": f"cannot save config: {e}"}))
        return 1
    print(json.dumps(status(c), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
