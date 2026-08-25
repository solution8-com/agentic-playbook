#!/usr/bin/env python3
"""Check that the plugin manifest and the skills directories agree, both ways.

The manifest is the only file that decides what a fresh install ships. On 2026-08-20 a commit
moved skills around and correctly updated README, CATALOG and ATTRIBUTION - the three files a
human reads - while missing the manifest. The repo described a skill set it would not have
shipped, and nothing looked at it. This looks at it.

Exit 0 when they agree, 1 when they do not.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / ".claude-plugin" / "plugin.json"
SKILLS_DIR = REPO / "skills"


def main() -> int:
    if not MANIFEST.exists():
        print(f"FAIL: no manifest at {MANIFEST.relative_to(REPO)}")
        return 1

    manifest = json.loads(MANIFEST.read_text())
    entries = manifest.get("skills", [])
    if not isinstance(entries, list):
        print(f"FAIL: manifest 'skills' is {type(entries).__name__}, expected a list of paths")
        return 1

    listed = {Path(p).name for p in entries}
    listed_paths = [REPO / Path(p) for p in entries]
    on_disk = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()} if SKILLS_DIR.exists() else set()

    problems = []

    for name in sorted(on_disk - listed):
        problems.append(f"skills/{name}/ exists on disk but is not in the manifest - it will not ship")

    for name in sorted(listed - on_disk):
        problems.append(f"manifest lists '{name}' but skills/{name}/ does not exist - dead path")

    for path in listed_paths:
        if path.exists() and not (path / "SKILL.md").exists():
            rel = path.relative_to(REPO)
            problems.append(f"{rel}/ is in the manifest but has no SKILL.md")

    if problems:
        print(f"FAIL: manifest and skills/ disagree ({len(problems)} problem(s))")
        for p in problems:
            print(f"  - {p}")
        return 1

    print(f"OK: manifest and skills/ agree - {len(listed)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
