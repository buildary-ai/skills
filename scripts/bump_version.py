#!/usr/bin/env python3
"""Writes the next version into VERSION, every plugin manifest, every skill and CHANGELOG.md.

    python3 scripts/bump_version.py <patch|minor|major> "<changelog line>"

The next version is the latest vX.Y.Z git tag raised by the given part; with no tag yet, the VERSION file is the
base. While the top CHANGELOG entry is newer than that base it is still unreleased, so a second run renumbers it
instead of adding another entry. Prints the version it wrote. Adapted from eachlabs/plugin
scripts/bump-version.sh (MIT; see THIRD_PARTY_NOTICES.md).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFESTS = [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json", "plugin.json"]


def as_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(x) for x in version.split("."))


def base_version() -> str:
    tags = subprocess.run(["git", "tag", "-l", "v*"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    released = sorted((t[1:] for t in tags if re.fullmatch(r"v\d+\.\d+\.\d+", t)), key=as_tuple)
    return released[-1] if released else (ROOT / "VERSION").read_text().strip()


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("patch", "minor", "major"):
        sys.exit('usage: scripts/bump_version.py <patch|minor|major> "<changelog line>"')
    part, line = sys.argv[1], sys.argv[2]
    base = base_version()
    major, minor, patch = as_tuple(base)
    nxt = {"major": f"{major + 1}.0.0", "minor": f"{major}.{minor + 1}.0", "patch": f"{major}.{minor}.{patch + 1}"}[part]

    (ROOT / "VERSION").write_text(nxt + "\n")
    for path in MANIFESTS:
        data = json.loads((ROOT / path).read_text())
        data["version"] = nxt
        (ROOT / path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    market_path = ROOT / ".claude-plugin/marketplace.json"
    market = json.loads(market_path.read_text())
    for plugin in market["plugins"]:
        plugin["version"] = nxt
    market_path.write_text(json.dumps(market, indent=2, ensure_ascii=False) + "\n")
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill.read_text()
        skill.write_text(re.sub(r'(\nmetadata:\n  version: )"[^"]*"', rf'\1"{nxt}"', text, count=1))

    changelog = ROOT / "CHANGELOG.md"
    text = changelog.read_text()
    top = re.search(r"^## (\d+\.\d+\.\d+)$", text, re.MULTILINE)
    if top and as_tuple(top.group(1)) > as_tuple(base):
        # The top entry is not released yet, so it belongs to this change: renumber it.
        text = text[:top.start()] + f"## {nxt}" + text[top.end():]
    else:
        entry = f"## {nxt}\n\n- {line or 'No description.'}\n\n"
        text = text[:top.start()] + entry + text[top.start():] if top else text.rstrip() + "\n\n" + entry
    changelog.write_text(text)
    print(nxt)


if __name__ == "__main__":
    main()
