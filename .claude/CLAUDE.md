# CLAUDE.md: Buildary skills

Maintainer contract for this repository. Adapted from higgsfield-ai/skills `CLAUDE.md` (v0.14.0, MIT,
Copyright (c) 2026 Higgsfield AI; see `THIRD_PARTY_NOTICES.md`). It lives in `.claude/` because a `CLAUDE.md` at
the plugin root fails `claude plugin validate --strict` (hosts never load it as context); Claude Code still reads it
here when you work in this repository.

## What this is

Skills that drive the Buildary MCP server (`https://buildary.dev/api/agency/mcp`), packaged as one plugin for
Claude Code, Codex, Cursor and Agent Plugins hosts, and installable one by one with `npx skills add`.

```
buildary-generate          core: models, prompts, files, start → get_job, workflows, get_brand, list_jobs, spending
buildary-thumbnail         self-contained; generate_image on the cover workflow at 4K, revise_job tweaks
buildary-product-photo     self-contained; image workflows (product, lifestyle, macro, conceptual, food, interior)
buildary-image-edit        self-contained; revise_job retouch, lock-first generate_image for own photos
buildary-ugc-ad            self-contained; one complete generate_video with native speech
buildary-ad-video          self-contained; generate_film (cinema, product-film) or directed generate_video clips
buildary-product-link-ad   self-contained; the agent reads the page, import_from_url, then image, film or video
buildary-marketplace-cards self-contained; listing sets under sourced Trendyol, Hepsiburada, Amazon TR rules
```

## The server is the contract

- Use only tools, input fields, enum values and model names the live server lists. `contracts/buildary-tools.json`
  is the snapshot; `scripts/check_skills.py` fails on anything a skill mentions that the snapshot lacks.
- After a server change, refresh the snapshot (`python3 scripts/snapshot_tools.py`, key from the environment)
  and fix the skills in the same change.
- The server never renames or removes a tool, field or enum value (clients cache tool lists). A name missing from
  the snapshot is a skill bug.
- Never write a skill against a tool that does not exist yet. Planned tools go in the README's "Coming" section.
- Model choices in `model-guide.md` are a starting map; `list_models` is the source of truth at run time, and
  every skill tells the agent to check it.

## Money rules every skill carries

Each skill states them itself (skills install alone), in its own words but with the same meaning:

1. A single job starts directly: new `requestId`, no `quotedCredits`, no `quote` first, no question. The server
   starts it at or under 20 credits.
2. Over 20 credits the server answers `quote_required` with `credits`: tell the owner that price once; after a
   yes, resend with the same settings, the same `requestId` and `quotedCredits` = `credits`.
3. Several jobs for one request: `quote` each first, tell the owner the total once, start after a yes with each
   job's `quotedCredits`; ask again only if the total would rise. `quote` is also the answer when the owner asks a price.
4. A timeout is retried with the same `requestId`; a new `requestId` only for a deliberate new paid attempt.
5. Report the credits the start result and `get_job` show for the job.
6. Never put a URL in a prompt: the server reads it as a video reference and the job fails after its credits
   were held.
7. The host's per-call permission prompt for a spending tool is its own safety net, not the price approval.

Changing any of these needs the founder's decision and a matching server change. Marketplace rules in
`buildary-marketplace-cards` come only from the marketplaces' own seller documentation, each with its source.

## Produce first: rules every skill carries

1. Make it by default: the agent chooses model, format, workflow, length and directions and starts. No menus.
2. At most one question, only for (a) a missing required input, (b) a price approval (`quote_required` or a
   set's total, in one message), or (c) for a film, two very different readings with a costly wrong guess.
3. Brand: never asked. `get_brand` is used silently when `ready`, skipped otherwise; the owner's own brand wins.
4. Improved prompts and scripts are used without approval; "exactly my text" keeps it untouched; one sentence
   after the start says what changed.
5. After delivery, one plain line naming 2-3 possible changes, as a statement, without tool or setting names.

`evals/grade.py` fails an unneeded question or any brand question.

## Line limit

Each `SKILL.md` stays under **300 lines** (CI enforces it). Skill files load into the agent's context whenever
the skill triggers; every line costs latency and tokens.

The test: if removing a section from `SKILL.md` would NOT break the agent's ability to decide what to do next,
it belongs in `references/`.

- **Stays in SKILL.md:** frontmatter, the stage flow, decision tables (model, mode, form), the money rules, UX
  rules that apply on every turn, short pointers to `references/`.
- **Moves to references/:** prompt galleries, long checklists, per-model notes, error tables, anything needed once
  after the path is chosen.

## Frontmatter

Agent Skills spec keys only: `name` (= folder name), `description`, `license`, `metadata.version`. The
description is at most 1024 characters and contains:

- what the skill does, in one or two sentences;
- `Use when:` with English **and Turkish** trigger phrases (agents reply in the owner's language);
- `NOT for:` with the neighbouring skills to use instead.

Each skill also has `agents/openai.yaml` (Codex display name, short description, `$skill-name` starter prompt).

## Self-contained skills

Each skill folder is independent: no `../` paths, every `references/*.md` file is linked from its `SKILL.md`,
and shared rules are copied, not linked. Drift between copies is acceptable as long as each skill is internally
consistent. Skills chain only through return values the owner can see: an output `fileId` or link from one
skill becomes an input of the next.

## Attribution

Material copied or adapted from another project keeps its notice:

- the adapted file names the source repository, version or commit, licence and copyright in a note at its top
  (references) or in an HTML comment at its bottom (`SKILL.md`);
- the skill's own `THIRD_PARTY_NOTICES.md` lists those sources with the full licence text;
- the root `THIRD_PARTY_NOTICES.md` lists every source with what was adapted and where.

Only MIT or Apache-2.0 material may be copied. Kling, Luma and eachlabs/skills are learn-only (no licence).
CI checks that every adapted file carries a copyright line and that both notices list its source.

## Versions

`VERSION` is the source of truth. It must match every plugin manifest, the Claude marketplace entry and each
skill's `metadata.version`. Bump with `python3 scripts/bump_version.py <patch|minor|major> "<changelog line>"`;
never by hand. Hosts update an installed plugin only when the version changes.

## Checks

Run before every commit; CI runs the same:

```bash
uv run scripts/check_skills.py        # or: pip install pyyaml && python3 scripts/check_skills.py
for s in skills/*/; do uvx --from skills-ref==0.1.1 agentskills validate "$s"; done
python3 scripts/check_manifests.py
python3 evals/grade.py --lint && python3 evals/grade.py --selftest
claude plugin validate --strict .
npx skills add . --list
```

## Adding a skill

New folder `skills/buildary-<name>/` with `SKILL.md`, `agents/openai.yaml`, `references/` as needed and
`THIRD_PARTY_NOTICES.md` if anything is adapted. Add it to the README tables (English and Turkish), add at least
one eval case, run the checks.

## Eval discipline

> **Key Decisions (Do Not Revisit Without Data)**
>
> None yet. Each entry must be a defended choice: "X over Y because Z% on metric M across N runs".

Until then, every default (model choice, mode choice, question count) is conventional, not measured.
