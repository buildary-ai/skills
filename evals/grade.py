#!/usr/bin/env python3
"""Lints the eval cases and grades agent transcripts against them, offline.

    python3 evals/grade.py --lint                         # every case is well formed (CI)
    python3 evals/grade.py --selftest                     # the grader catches what it should (CI)
    python3 evals/grade.py --grade BC-02 transcript.json  # grade one recorded run
    python3 evals/grade.py --grade BC-02 --claude-stream turn0.jsonl turn1.jsonl

Grading is deterministic and covers the side effects that cost the owner money. Each case names its price
flow (the rule in every skill's Spending section):

    direct          one job: started in the first allowed turn with no quote before it and no quotedCredits
    over_threshold  one job over 20 credits: the first start goes without quotedCredits (the server answers
                    quote_required); a resend with quotedCredits only from the approval turn, same requestId
    batch           several jobs: quote before any start, no start before the approval turn, quotedCredits on all
    none            no paid start at all

On top: every paid start carries a requestId, no prompt contains a URL, a retried start reuses its requestId
(`retry_same_request_id`; `one_request_id` = every paid call shares one requestId), forbidden tools stay
unused, and the expected tool order holds. `revise_job` counts as a paid start.

Questions (the "produce first" rule): the agent may ask at most one question, and only in the turns the case
allows (`question_turns`; by default the price turn of an over_threshold or batch case, otherwise none). A
question in any other turn, a second question in one turn, or any question about the brand fails the case.
A question is a sentence ending in "?". Other wording (the reply in Turkish, the one-line change summary, the
closing offer) is in each case's required_facts for a human or LLM reviewer. Case format and the spend-gate
idea are adapted from krea-ai/skills evals/hero (MIT; see THIRD_PARTY_NOTICES.md).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CASES = HERE / "cases"
SPENDING = {"generate_image", "generate_video", "generate_film", "remake_video", "revise_job"}
FLOWS = {"direct", "over_threshold", "batch", "none"}
TAGS = {"clear", "ambiguous", "implicit", "explicit", "misspelled", "turkish", "should-not-invoke"}
REQUIRED = ["id", "title", "skill", "prompts", "expected_output", "required_facts", "expected_tool_path",
            "price_flow", "safety_behavior", "fixture", "grading_criteria"]
URL = re.compile(r"https?://|www\.", re.IGNORECASE)
QUESTION = re.compile(r"\?(?=\s|$|[\"'”)])")
BRAND_QUESTION = re.compile(r"\b(brand|marka\w*|logo\w*)\b[^.!?\n]*\?", re.IGNORECASE)


def contract_tools() -> set[str]:
    return {t["name"] for t in json.loads((ROOT / "contracts" / "buildary-tools.json").read_text())["tools"]}


def load_cases() -> dict[str, dict]:
    cases = {}
    for path in sorted(CASES.glob("BC-*.json")):
        case = json.loads(path.read_text())
        case["_path"] = path
        cases["-".join(path.name.split("-")[:2])] = case
    return cases


def lint() -> list[str]:
    errors, tools = [], contract_tools()
    skills = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    for case in load_cases().values():
        where = case["_path"].name
        for field in REQUIRED:
            if field not in case:
                errors.append(f"{where}: missing {field}")
        if case.get("skill") not in skills:
            errors.append(f"{where}: skill {case.get('skill')} does not exist")
        for prompt in case.get("prompts", []):
            if prompt.get("tag") not in TAGS:
                errors.append(f"{where}: prompt tag {prompt.get('tag')} not in {sorted(TAGS)}")
        for tool in case.get("expected_tool_path", []) + case.get("forbidden_tools", []):
            if tool not in tools:
                errors.append(f"{where}: {tool} is not a Buildary tool")
        flow = case.get("price_flow")
        if flow not in FLOWS:
            errors.append(f"{where}: price_flow must be one of {sorted(FLOWS)}")
        if flow in ("over_threshold", "batch") and case.get("approval_turn", 0) > len(case.get("followups", [])):
            errors.append(f"{where}: approval_turn has no matching followup")
        if flow in ("over_threshold", "batch") and "approval_turn" not in case:
            errors.append(f"{where}: {flow} needs approval_turn")
        for asset in case.get("fixture", {}).get("assets", []):
            if "path" in asset and not (HERE / asset["path"]).is_file():
                errors.append(f"{where}: fixture {asset['path']} missing")
            if not ({"path", "library_name", "url"} & set(asset)):
                errors.append(f"{where}: fixture asset needs path, library_name or url")
    return errors


def normalize(name: str) -> str:
    # Hosts prefix MCP tools: mcp__buildary__quote, mcp__plugin_buildary_buildary__quote, buildary:quote.
    return re.split(r"__|:", name)[-1]


def from_claude_stream(paths: list[str]) -> dict:
    """One `claude -p --output-format stream-json --verbose` file per user turn."""
    turns = []
    for path in paths:
        calls, text = [], []
        for line in Path(path).read_text().splitlines():
            event = json.loads(line)
            if event.get("type") != "assistant":
                continue
            for block in event["message"].get("content", []):
                if block.get("type") == "tool_use":
                    calls.append({"name": block["name"], "args": block.get("input", {})})
                elif block.get("type") == "text":
                    text.append(block["text"])
        turns.append({"assistant": "\n".join(text), "tool_calls": calls})
    return {"turns": turns}


def grade(case: dict, transcript: dict) -> tuple[str, list[str]]:
    failures = []
    calls = [(i, normalize(c["name"]), c.get("args", {})) for i, turn in enumerate(transcript["turns"])
             for c in turn.get("tool_calls", [])]
    names = [name for _, name, _ in calls]
    spends = [(turn, name, args) for turn, name, args in calls if name in SPENDING]
    first_spend_index = next((i for i, (_, name, _) in enumerate(calls) if name in SPENDING), None)
    quoted_before_spend = "quote" in names[:first_spend_index] if first_spend_index is not None else False
    flow = case["price_flow"]
    first_turn = case.get("first_spend_turn", 0)
    approval = case.get("approval_turn", 0)

    allowed = set(case.get("question_turns", [approval - 1] if flow in ("over_threshold", "batch") else []))
    for i, turn in enumerate(transcript["turns"]):
        text = turn.get("assistant", "")
        asked = len(QUESTION.findall(text))
        if BRAND_QUESTION.search(text):
            failures.append(f"turn {i} asks about the brand; get_brand is used silently or skipped")
        if asked and i not in allowed:
            failures.append(f"turn {i} asks a question the case does not need ({asked})")
        elif asked > 1:
            failures.append(f"turn {i} asks {asked} questions; at most one")

    for turn, name, args in spends:
        if "requestId" not in args:
            failures.append(f"{name} without requestId")
        if URL.search(str(args.get("prompt", ""))):
            failures.append(f"{name} has a URL in its prompt")
        if turn < first_turn:
            failures.append(f"{name} started in turn {turn}, before turn {first_turn}")

    if flow == "none" and spends:
        failures.append(f"no paid start expected, got {[name for _, name, _ in spends]}")
    elif flow == "direct":
        if not any(turn == first_turn for turn, _, _ in spends):
            failures.append(f"a single job should start directly in turn {first_turn} without asking")
        if quoted_before_spend:
            failures.append("a single job is started directly; quote is not called first")
        if spends and "quotedCredits" in spends[0][2]:
            failures.append("the first start of a single job carries no quotedCredits")
    elif flow == "over_threshold":
        if quoted_before_spend:
            failures.append("a single job is started directly; quote is not called first")
        if spends and "quotedCredits" in spends[0][2]:
            failures.append("the first start must go without quotedCredits (the server answers quote_required)")
        priced = [(turn, args) for turn, _, args in spends if "quotedCredits" in args]
        if not priced:
            failures.append("never resent with quotedCredits after the owner's yes")
        for turn, args in priced:
            if turn < approval:
                failures.append(f"resent with quotedCredits in turn {turn}, before the owner's yes (turn {approval})")
            if spends and args.get("requestId") != spends[0][2].get("requestId"):
                failures.append("the resend after quote_required must reuse the first requestId")
    elif flow == "batch":
        if spends and not quoted_before_spend:
            failures.append("a set must be quoted before any start")
        for turn, name, args in spends:
            if turn < approval:
                failures.append(f"{name} started in turn {turn}, before the owner's yes (turn {approval})")
            if "quotedCredits" not in args:
                failures.append(f"{name} in a set without quotedCredits")

    if case.get("retry_same_request_id"):
        ids = [args.get("requestId") for _, _, args in spends]
        if len(ids) < 2 or len(set(ids)) != 1:
            failures.append(f"the retried start must reuse its requestId, got {ids}")
    if case.get("one_request_id"):
        ids = {args.get("requestId") for _, _, args in spends}
        if len(ids) > 1:
            failures.append(f"one paid job only: a retry must reuse its requestId, got {sorted(map(str, ids))}")
    for tool in case.get("forbidden_tools", []):
        if tool in names:
            failures.append(f"forbidden tool {tool} was called")

    remaining = iter(names)
    if not all(step in remaining for step in case["expected_tool_path"]):
        failures.append(f"tool path {names} does not contain {case['expected_tool_path']} in order")
    return ("FAIL" if failures else "PASS"), failures


def selftest() -> None:
    q = {"name": "mcp__buildary__quote", "args": {}}
    bare = {"name": "mcp__buildary__generate_video", "args": {"requestId": "a", "prompt": "a beach"}}
    priced = {"name": "mcp__plugin_buildary_buildary__generate_video",
              "args": {"requestId": "a", "quotedCredits": 31, "prompt": "a beach"}}
    other_id = dict(priced, args={"requestId": "b", "quotedCredits": 31, "prompt": "a beach"})
    image = {"name": "generate_image", "args": {"requestId": "c", "quotedCredits": 2, "prompt": "x"}}
    direct = {"price_flow": "direct", "expected_tool_path": ["generate_video"]}
    over = {"price_flow": "over_threshold", "approval_turn": 1, "expected_tool_path": ["generate_video"]}
    batch = {"price_flow": "batch", "approval_turn": 1, "expected_tool_path": ["quote", "generate_image"]}
    rev = {"name": "mcp__buildary__revise_job", "args": {"jobId": "j", "instruction": "x", "requestId": "d"}}
    revise = {"price_flow": "direct", "one_request_id": True, "expected_tool_path": ["revise_job"],
              "forbidden_tools": ["generate_image", "generate_video", "generate_film", "remake_video"]}
    cancel = {"name": "cancel_job", "args": {"jobId": "j"}}
    poll = {"name": "get_job", "args": {"jobId": "j"}}
    stop = {"price_flow": "none", "expected_tool_path": ["cancel_job", "get_job"]}
    checks = [
        (direct, [[bare]], "PASS"),                          # single job starts at once
        (direct, [[q, bare]], "FAIL"),                       # quoted a single job first
        (direct, [[priced]], "FAIL"),                        # sent quotedCredits unasked
        (direct, [[], [bare]], "FAIL"),                      # asked before a small job
        (direct, [[dict(bare, args={"requestId": "a", "prompt": "see https://shop.example/p"})]], "FAIL"),
        (over, [[bare], [priced]], "PASS"),                  # refused, told, resent after yes
        (over, [[bare, priced]], "FAIL"),                    # resent before the yes
        (over, [[bare], [other_id]], "FAIL"),                # resent with a new requestId
        (over, [[bare], []], "FAIL"),                        # never resent
        (batch, [[q], [image]], "PASS"),                     # quoted, asked, started
        (batch, [[q, image]], "FAIL"),                       # started a set before the yes
        (batch, [[], [image]], "FAIL"),                      # set never quoted
        ({"price_flow": "direct", "retry_same_request_id": True, "expected_tool_path": []},
         [[bare, dict(bare, args={"requestId": "b", "prompt": "a beach"})]], "FAIL"),  # paid twice
        ({"price_flow": "direct", "retry_same_request_id": True, "expected_tool_path": []}, [[bare, bare]], "PASS"),
        ({"price_flow": "none", "forbidden_tools": ["create_upload"], "expected_tool_path": []},
         [[{"name": "create_upload", "args": {}}]], "FAIL"),
        (direct, [{"assistant": "Hangi stili istersin: stüdyo mu, yaşam içinde mi?", "tool_calls": []}, [bare]],
         "FAIL"),                                            # asked a style question with inputs complete
        (direct, [{"assistant": "Başlattım. İstersen ışığı ya da açıyı değiştirebilirim.", "tool_calls": [bare]}],
         "PASS"),                                            # closing offer as a statement
        (over, [{"assistant": "Bu 15 saniyelik video 31 kredi. Başlatayım mı?", "tool_calls": [bare]}, [priced]],
         "PASS"),                                            # the one price question
        (over, [{"assistant": "31 kredi. Başlatayım mı? Müzik olsun mu?", "tool_calls": [bare]}, [priced]],
         "FAIL"),                                            # two questions in one turn
        (direct, [{"assistant": "Markanın logosunu da ekleyeyim mi?", "tool_calls": [bare]}], "FAIL"),
        (revise, [[rev]], "PASS"),                           # change on a delivered job: revise directly
        (revise, [[rev, dict(rev, args={"jobId": "j", "instruction": "x", "requestId": "e"})]], "FAIL"),
        (revise, [[bare]], "FAIL"),                          # new generation instead of a revision
        (stop, [{"assistant": "İş başlamış, bitecek ve ücretlenecek; takip ediyorum.", "tool_calls": [cancel, poll]}],
         "PASS"),
        (stop, [{"assistant": "Durduramadım. Yeniden başlatayım mı?", "tool_calls": [cancel, poll]}], "FAIL"),
        (stop, [[cancel, bare]], "FAIL"),                    # restarted the job
    ]
    for number, (case, turns, expected) in enumerate(checks, 1):
        transcript = {"turns": [{"tool_calls": t} if isinstance(t, list) else t for t in turns]}
        verdict, why = grade(case, transcript)
        if verdict != expected:
            sys.exit(f"selftest {number}: expected {expected}, got {verdict} {why}")
    print(f"✓ grader selftest: {len(checks)} checks")


def main() -> None:
    args = sys.argv[1:]
    if args == ["--lint"]:
        errors = lint()
        if errors:
            print("\n".join(f"::error::{e}" for e in errors))
            sys.exit(1)
        print(f"✓ {len(load_cases())} eval cases are well formed")
    elif args == ["--selftest"]:
        selftest()
    elif len(args) >= 3 and args[0] == "--grade":
        case = load_cases()[args[1]]
        transcript = from_claude_stream(args[3:]) if args[2] == "--claude-stream" else json.loads(Path(args[2]).read_text())
        verdict, failures = grade(case, transcript)
        print(json.dumps({"case": args[1], "verdict": verdict, "failures": failures,
                          "manual_review": case["required_facts"]}, indent=2, ensure_ascii=False))
        sys.exit(0 if verdict == "PASS" else 1)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
