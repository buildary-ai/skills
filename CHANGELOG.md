# Changelog

Each release changes `VERSION` and the `version` in every plugin manifest and skill (`scripts/bump_version.py`
writes them all). Claude Code and Codex update an installed plugin only when that number changes.

## 0.2.0

- New skill `buildary-website`: build, change and publish the owner's Buildary websites with `list_sites`,
  `get_site`, `start_site`, `revise_site` and `publish_site`. Site work is charged by use with no price, so
  every build and change is sent first without `pricingVersion`, the server's `site_confirmation_required`
  sentence is relayed once with the balance, and the call is resent with the same `requestId` after the
  owner's yes. Publishing only on the owner's explicit request after the preview, with `confirmedDraft`; a
  refused publish is relayed with its reason and fix link. No invented business facts, prices or reviews.
- `list_files {"kind": "material"}` finds the site's own files (images, a PDF menu, texts) for `files` roles.
- Tool contract refreshed from the live server: 23 tools (was 18), `list_files` kind `material`.
- `buildary-generate` and `buildary-product-photo` route website requests to `buildary-website`; the plugin
  descriptions and the README mention websites; agent setup also stays away from site tools.
- Evals: a `site` price flow and `publish_turn` in `evals/grade.py`, cases BC-21 to BC-25 (build with a menu
  PDF, change, publish on request, publish refused with a link, "build and publish" waits for the preview) and
  scenarios 24-28.

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
