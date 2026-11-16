# Evals

Test material for the skills. **Dev-only**: not shipped to users (the plugin and `npx skills add` install
only `skills/`).

Skill behaviour is defined in plain Markdown, and plain Markdown drifts. These evals catch regressions after a
`SKILL.md` edit, after a Buildary server change, and before a "Key Decision" goes into `.claude/CLAUDE.md`.

Two layers, adapted from higgsfield-ai/skills (`evals/scenarios.md`, hand-scored) and krea-ai/skills
(`evals/hero`, machine-checked cases), both MIT; see `THIRD_PARTY_NOTICES.md`:

| File | What | Run by |
|---|---|---|
| [`scenarios.md`](scenarios.md) | 23 user requests with expected behaviour and a pass / partial / fail rubric | A person (or an agent playing the user) in a fresh session |
| `cases/BC-*.json` | The money-relevant scenarios as specs: prompts in English, Turkish and misspelled forms, follow-ups, the expected tool order and a price flow | `grade.py` |
| [`grade.py`](grade.py) | Lints the cases and grades a recorded transcript deterministically | You and CI |

## Offline (CI, no account, no spend)

```bash
python3 evals/grade.py --lint       # every case is well formed and names real tools and skills
python3 evals/grade.py --selftest   # the grader fails what it should fail
```

## Grading a real run

Real runs spend real Buildary credits. Use a review account with a small balance, never a customer account.

1. Install the plugin in a fresh agent and connect the review account (`INSTALL.md`).
2. Put the case's fixture files in that account's library.
3. Send the case's prompt; send each follow-up as the next turn.
4. Grade. From Claude Code, save each turn with
   `claude -p "<prompt>" --output-format stream-json --verbose > turn0.jsonl` (and `--resume` for follow-ups):

   ```bash
   python3 evals/grade.py --grade BC-02 --claude-stream turn0.jsonl turn1.jsonl
   ```

   Any other agent: write the transcript as
   `{"turns": [{"user": "…", "assistant": "…", "tool_calls": [{"name": "quote", "args": {…}}]}]}` and run
   `python3 evals/grade.py --grade BC-02 transcript.json`.

`grade.py` checks the side effects that cost money for each case's `price_flow`: a single job started directly
without a `quote` or `quotedCredits` (`direct`); a job over 20 credits resent with `quotedCredits` only after the
owner's yes and with its first `requestId` (`over_threshold`); a set quoted before any start and started only
after the yes (`batch`); no paid start at all (`none`). It also checks a `requestId` on every start, no URL in any
prompt, the same `requestId` on a retry, forbidden tools and the expected tool order. It prints the case's
`required_facts` (language, wording, honesty) for a person or an LLM judge. Questions are graded too: a
sentence ending in "?" outside the turns the case allows (`question_turns`; by default only the price turn),
two questions in one turn, or any question about the brand fails the case.

## Recording a round

For each round record: the commit, the date, the server's tool snapshot (`contracts/buildary-tools.json`),
verdict per case and scenario, the failure mode, and time to result. A regression of more than 15% in score or
2× in time means revert and investigate. After 3+ stable rounds, codify findings in `.claude/CLAUDE.md` → Key Decisions.

## When to add a case

- A bug was caught only by hand → codify it.
- A new skill or a new Buildary tool ships → write the case before the merge.
- A user reports surprising behaviour → write the case during triage.

Test what the owner sees and pays for, not internals.
