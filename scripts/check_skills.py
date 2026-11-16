#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml==6.0.2"]
# ///
"""Validates every skill in skills/. Run: python3 scripts/check_skills.py (needs PyYAML; `uv run` installs it).

Frontmatter, line limit, references and self-containment follow the rules in .claude/CLAUDE.md. On top of those,
the tool contract check compares every Buildary tool, field, enum value and model a skill mentions with
contracts/buildary-tools.json, the snapshot of the live server: MCP clients cache tool lists and the server never
renames a tool or field, so a name the snapshot lacks is a skill bug, not a server change.
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MAX_SKILL_LINES = 300
MAX_DESCRIPTION = 1024
SPEC_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TURKISH_RE = re.compile(r"[çğıöşüÇĞİÖŞÜ]")

# Fields that appear in Buildary tool results rather than inputs (docs/guides/buildary-mcp-basvuru.md).
RESULT_FIELDS = {"balanceCredits", "createdAt", "elapsedSeconds", "expiresInSeconds", "retryAfterSeconds",
                 "runningJobs", "maxRunningJobs", "nextCursor", "promptReferences", "promptReference",
                 "durationsSeconds", "defaultResolution", "defaultQuality", "startFrame", "endFrame",
                 "creditsPerSecond", "firstSourceSeconds", "isError", "jobId", "requiredFile", "logoFileId",
                 "publishedUrl", "panelUrl", "previewReady", "lastBuild", "buildId", "waitingForOwner",
                 "unpublishedChanges", "minStartCredits"}
TOOL_VERBS = {"list", "get", "create", "complete", "import", "generate", "remake", "upload", "cancel", "wait",
              "start", "run", "delete", "update", "set"}
MODEL_RE = re.compile(r"^(omni|pixverse|seedance|wan|flux|grok|veo|kling|h3|happyhorse|heygen|sunburst|flare|gpt-image"
                      r"|nano-banana|seedream)\b")


def load_contract():
    data = json.loads((ROOT / "contracts" / "buildary-tools.json").read_text())
    tools = {t["name"]: t for t in data["tools"]}
    fields, enums, enum_by_key = set(), set(), {}

    def walk(node, key=None):
        if isinstance(node, dict):
            for name, sub in node.get("properties", {}).items():
                fields.add(name)
                walk(sub, name)
            if "items" in node:
                walk(node["items"], key)
            for value in node.get("enum", []):
                enums.add(value)
                enum_by_key.setdefault(key, set()).add(value)
    for tool in tools.values():
        walk(tool["inputSchema"])
    models = enum_by_key.get("model", set())
    return tools, fields, enums, enum_by_key, models


TOOLS, FIELDS, ENUMS, ENUM_BY_KEY, MODELS = load_contract()
errors: list[str] = []


def fail(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def strip_comments(text: str) -> str:
    """HTML comments are not shown to the agent, so links and names inside them do not count."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def check_frontmatter(skill: Path, version: str) -> None:
    path = skill / "SKILL.md"
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return fail(path, "no YAML frontmatter")
    fm = yaml.safe_load(match.group(1))
    for key in set(fm) - SPEC_KEYS:
        fail(path, f"frontmatter key '{key}' is not in the Agent Skills spec; put it under metadata")
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != skill.name:
        fail(path, f"name '{name}' != directory '{skill.name}'")
    if not NAME_RE.match(name) or len(name) > 64:
        fail(path, "name must be lowercase words joined by '-' and at most 64 characters")
    if not desc:
        fail(path, "description missing")
    if len(desc) > MAX_DESCRIPTION:
        fail(path, f"description exceeds {MAX_DESCRIPTION} characters ({len(desc)})")
    for phrase in ("Use when", "NOT for"):
        if phrase not in desc:
            fail(path, f"description missing '{phrase}'")
    if not TURKISH_RE.search(desc):
        fail(path, "description has no Turkish trigger phrase")
    if not fm.get("license"):
        fail(path, "license missing")
    if str((fm.get("metadata") or {}).get("version")) != version:
        fail(path, f"metadata.version {fm.get('metadata', {}).get('version')} != VERSION {version}")
    lines = text.count("\n")
    if lines > MAX_SKILL_LINES:
        fail(path, f"{lines} lines; the limit is {MAX_SKILL_LINES} (move detail to references/)")


def check_references(skill: Path) -> None:
    skill_md = skill / "SKILL.md"
    text = strip_comments(skill_md.read_text())
    for ref in sorted(set(re.findall(r"references/[A-Za-z0-9_.-]+\.md", text))):
        if not (skill / ref).is_file():
            fail(skill_md, f"links {ref}, which does not exist")
    for ref in sorted((skill / "references").glob("*.md")):
        if f"references/{ref.name}" not in text:
            fail(ref, "orphaned reference (not linked from SKILL.md)")
    for md in skill.rglob("*.md"):
        if re.search(r"(^|[^./])\.\./", md.read_text(), re.MULTILINE):
            fail(md, "contains a ../ path; a skill must be self-contained")


def check_codex_metadata(skill: Path) -> None:
    path = skill / "agents" / "openai.yaml"
    if not path.is_file():
        return fail(path, "missing (Codex shows this skill's name and starter prompt from it)")
    interface = (yaml.safe_load(path.read_text()) or {}).get("interface", {})
    for key in ("display_name", "short_description", "default_prompt"):
        if not interface.get(key):
            fail(path, f"interface.{key} missing")
    if f"${skill.name}" not in interface.get("default_prompt", ""):
        fail(path, f"default_prompt should invoke ${skill.name}")


def check_contract(skill: Path) -> None:
    for md in skill.rglob("*.md"):
        text = strip_comments(md.read_text())
        # Field names are only checked in files that drive Buildary tools: a canvas or CSS recipe has its own
        # camelCase API (strokeText, fillText) that is not about the MCP.
        about_mcp = any(f"`{tool}" in text for tool in TOOLS)
        for token in re.findall(r"`([^`\n]+)`", text):
            check_token(md, token, about_mcp)
        for block in re.findall(r"```json\n(.*?)```", text, re.DOTALL):
            try:
                check_json(md, json.loads(block))
            except json.JSONDecodeError as exc:
                fail(md, f"json example does not parse: {exc}")


def check_token(md: Path, token: str, check_fields: bool) -> None:
    head = token.split(" ", 1)[0]
    if re.fullmatch(r"[a-z]+(_[a-z0-9]+)+", head) and head.split("_")[0] in TOOL_VERBS:
        if head not in TOOLS and head not in ENUMS:
            fail(md, f"`{head}` is not a Buildary tool or enum value")
    for part in head.split(".") if check_fields else ():
        if re.fullmatch(r"[a-z]+[A-Z][A-Za-z]*", part) and part not in FIELDS | RESULT_FIELDS:
            fail(md, f"`{part}` is not a Buildary input or result field")
    if MODEL_RE.match(head) and re.fullmatch(r"[a-z0-9.-]+\*?", head):
        if head.endswith("*"):
            if not any(m.startswith(head[:-1]) for m in MODELS):
                fail(md, f"`{head}` matches no Buildary model")
        elif head not in MODELS:
            fail(md, f"`{head}` is not a Buildary model name")


def check_json(md: Path, node, key=None) -> None:
    if isinstance(node, dict):
        for name, value in node.items():
            if name not in FIELDS:
                fail(md, f"json example uses unknown field '{name}'")
            check_json(md, value, name)
    elif isinstance(node, list):
        for value in node:
            check_json(md, value, key)
    elif isinstance(node, str) and key in ("model", "format", "role", "resolution", "quality", "kind", "mimeType",
                                           "workflow", "look", "light", "lens", "movement"):
        if not node.startswith("<") and node not in ENUM_BY_KEY.get(key, set()):
            fail(md, f"json example: '{node}' is not a valid {key}")


def main() -> None:
    version = (ROOT / "VERSION").read_text().strip()
    skills = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    for skill in skills:
        if not (skill / "SKILL.md").is_file():
            fail(skill, "SKILL.md missing")
            continue
        check_frontmatter(skill, version)
        check_references(skill)
        check_codex_metadata(skill)
        check_contract(skill)
    if errors:
        print("\n".join(f"::error::{e}" for e in errors))
        sys.exit(1)
    print(f"✓ {len(skills)} skills: frontmatter, {MAX_SKILL_LINES}-line limit, references, self-containment "
          f"and the {len(TOOLS)}-tool contract are valid")


if __name__ == "__main__":
    main()
