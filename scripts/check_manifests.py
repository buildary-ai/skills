#!/usr/bin/env python3
"""Fails when the plugin manifests disagree with each other or with VERSION. Run: python3 scripts/check_manifests.py

Claude Code, Codex, Cursor and Agent Plugins hosts install the same files, and each updates an installed plugin
only when its own manifest's version changes, so name, version and description must match everywhere, and every
MCP config must point at the same server.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = "buildary"
MCP_URL = "https://buildary.dev/api/agency/mcp"
PLUGINS = [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json", "plugin.json"]
MCP_CONFIGS = [".mcp.json", "mcp.json", ".cursor-plugin/mcp.json"]
errors: list[str] = []


def read(path: str) -> dict:
    return json.loads((ROOT / path).read_text())


def expect(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def exists(manifest: str, relative: str, field: str) -> None:
    # Every manifest path is relative to the plugin root (this repository's root), not to the manifest's folder.
    expect((ROOT / relative).exists(), f"{manifest}: {field} points at {relative}, which does not exist")


def main() -> None:
    version = (ROOT / "VERSION").read_text().strip()
    claude = read(PLUGINS[0])
    for path in PLUGINS:
        manifest = read(path)
        expect(manifest.get("version") == version, f"{path}: version {manifest.get('version')} != VERSION {version}")
        for key in ("name", "description"):
            expect(manifest.get(key) == claude.get(key), f"{path}: {key} differs from {PLUGINS[0]}")
        expect(manifest.get("license") == "MIT", f"{path}: license must be MIT")

    market = read(".claude-plugin/marketplace.json")
    entry = next((p for p in market["plugins"] if p["name"] == claude["name"]), None)
    expect(entry is not None, ".claude-plugin/marketplace.json: does not list the plugin")
    if entry:
        expect(entry.get("version") == version, ".claude-plugin/marketplace.json: plugin version != VERSION")
        expect(entry.get("description") == claude["description"], ".claude-plugin/marketplace.json: description differs")
        expect(entry.get("source") == "./", ".claude-plugin/marketplace.json: source must be ./")
    codex_market = read(".agents/plugins/marketplace.json")
    expect(any(p["name"] == claude["name"] for p in codex_market["plugins"]),
           ".agents/plugins/marketplace.json: does not list the plugin")

    for path in MCP_CONFIGS:
        server = read(path).get("mcpServers", {}).get(SERVER, {})
        expect(server.get("url") == MCP_URL, f"{path}: mcpServers.{SERVER}.url must be {MCP_URL}")

    codex = read(".codex-plugin/plugin.json")
    face = codex.get("interface", {})
    # Limits from the OpenAI plugin submission guide: the directory truncates or rejects longer values.
    expect(len(face.get("displayName", "")) <= 30, ".codex-plugin/plugin.json: interface.displayName over 30 characters")
    expect(len(face.get("shortDescription", "")) <= 30, ".codex-plugin/plugin.json: interface.shortDescription over 30 characters")
    expect(1 <= len(face.get("defaultPrompt", [])) <= 3, ".codex-plugin/plugin.json: interface.defaultPrompt needs 1-3 prompts")
    for field in ("skills", "mcpServers"):
        exists(".codex-plugin/plugin.json", codex[field], field)
    for field in ("logo", "composerIcon"):
        exists(".codex-plugin/plugin.json", face[field], f"interface.{field}")
    cursor = read(".cursor-plugin/plugin.json")
    for field in ("skills", "mcpServers", "logo"):
        exists(".cursor-plugin/plugin.json", cursor[field], field)
    exists(".claude-plugin/plugin.json", claude["icon"], "icon")

    # claude.ai refuses a plugin whose repository root has a bin/ directory.
    expect(not (ROOT / "bin").exists(), "bin/ at the repository root makes claude.ai refuse the plugin")

    if errors:
        print("\n".join(f"::error::{e}" for e in errors))
        sys.exit(1)
    print(f"✓ {len(PLUGINS)} plugin manifests and 2 marketplaces agree on version {version}; "
          f"{len(MCP_CONFIGS)} MCP configs point at {MCP_URL}")


if __name__ == "__main__":
    main()
