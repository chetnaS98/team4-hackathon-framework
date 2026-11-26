#!/usr/bin/env python3
"""SessionStart hook: if the session opens on a koru engagement, put its status and the core rules in context.

Prints nothing when there is no engagement under the working folder, so other projects are not affected.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _koru as k  # noqa: E402

RULES = """koru rules (koru-core v1): every assertion has a confidence and a source; never fabricate; sources and final files are never edited (new version instead);
a different named person checks every AI-led step; only final files become project knowledge (the context keeper uploads them); log decisions, breaks and playbook changes as you go;
run the stale-check before any sign-off. Start or continue with /koru:next; update step status with the plugin's scripts/step.py, never by editing the tracker table."""


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    cwd = Path(data.get("cwd") or ".").resolve()
    found = k.find_engagements(cwd)
    if not found:
        return
    if len(found) > 1:
        print("koru: several engagements here: " + ", ".join(str(f.relative_to(cwd)) for f in found) + ". /koru:next will ask which one.")
        print(RULES)
        return
    r = subprocess.run([sys.executable, "-I", str(ROOT / "scripts" / "route.py"), "--engagement", str(found[0])],
                       capture_output=True, text=True, timeout=60)
    lines = [l for l in r.stdout.splitlines() if l and not l.startswith("  ")]
    print("koru engagement status:\n" + "\n".join(lines[:8]))
    print(RULES)


if __name__ == "__main__":
    main()
