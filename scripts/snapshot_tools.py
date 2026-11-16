#!/usr/bin/env python3
"""Writes contracts/buildary-tools.json: the tool names, annotations and input schemas of the live Buildary MCP.

check_skills.py compares every tool, field, enum value and model name the skills mention with this file, so a
skill can only teach what the server really accepts. Refresh it whenever the server's tools change:

    BUILDARY_API_KEY=... python3 scripts/snapshot_tools.py           # reads tools/list from the live server
    python3 scripts/snapshot_tools.py --from tools-list.json        # or from a saved tools/list response

The key is read from the environment and sent only as the Authorization header; it is never printed or written.
Descriptions are dropped so that wording changes on the server do not churn the snapshot.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

URL = os.environ.get("BUILDARY_MCP_URL", "https://buildary.dev/api/agency/mcp")
OUT = Path(__file__).resolve().parent.parent / "contracts" / "buildary-tools.json"


def live_tools() -> list:
    key = os.environ.get("BUILDARY_API_KEY")
    if not key:
        sys.exit("Set BUILDARY_API_KEY, or pass --from <saved tools/list response>.")
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}).encode()
    request = urllib.request.Request(URL, data=body, method="POST", headers={
        "authorization": f"Bearer {key}",
        "content-type": "application/json",
        "accept": "application/json, text/event-stream",
        "mcp-protocol-version": "2025-06-18",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        text = response.read().decode()
    # Streamable HTTP may answer as an SSE stream; the JSON-RPC message is on the data line.
    if text.lstrip().startswith("event:") or "\ndata:" in text:
        text = next(line[5:] for line in text.splitlines() if line.startswith("data:"))
    return json.loads(text)["result"]["tools"]


def saved_tools(path: str) -> list:
    text = Path(path).read_text()
    # Accept the raw response, or the "<status> <body>" line a test helper prints.
    text = text[text.index("{"):]
    data = json.loads(text)
    return data["result"]["tools"] if "result" in data else data["tools"]


def without_descriptions(node):
    if isinstance(node, dict):
        return {k: without_descriptions(v) for k, v in node.items() if k not in ("description", "$schema")}
    if isinstance(node, list):
        return [without_descriptions(v) for v in node]
    return node


def main() -> None:
    tools = saved_tools(sys.argv[2]) if sys.argv[1:2] == ["--from"] else live_tools()
    snapshot = {
        "source": URL,
        "tools": [
            {"name": t["name"], "annotations": t.get("annotations", {}), "inputSchema": without_descriptions(t["inputSchema"])}
            for t in sorted(tools, key=lambda t: t["name"])
        ],
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {OUT.relative_to(Path.cwd()) if OUT.is_relative_to(Path.cwd()) else OUT}: {len(tools)} tools")


if __name__ == "__main__":
    main()
