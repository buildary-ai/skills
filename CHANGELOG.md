# Changelog

Each release changes `VERSION` and the `version` in every plugin manifest and skill (`scripts/bump_version.py`
writes them all). Claude Code and Codex update an installed plugin only when that number changes.

## 0.1.0

- First release: the Buildary plugin for Claude Code, Codex and Cursor, Agent Plugins manifests, and eight
  skills: `buildary-generate`, `buildary-thumbnail`, `buildary-product-photo`, `buildary-image-edit`,
  `buildary-ugc-ad`, `buildary-ad-video`, `buildary-product-link-ad`, `buildary-marketplace-cards`.
- Spending rule in every skill: a single job starts directly; the server starts it at or under 20 credits
  and answers a larger one with `quote_required`, whose price the owner approves once before a resend with
  the same `requestId`; several jobs for one request are quoted and approved as one total first.
- Buildary's ready-made image workflows (`list_workflows`, `workflow`, `look`, `light`, `lens`, role `source`),
  multi-scene films (`generate_film`), the owner's brand (`get_brand`) and job history (`list_jobs`), result cards (`show_results`), revisions (`revise_job`) and stopping a queued job (`cancel_job`).
- CI: frontmatter, line limit, version sync, references, self-containment, attribution, the live tool
  contract, manifests and eval cases.
