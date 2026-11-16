# Third-party notices

This repository adapts material from the MIT-licensed projects below. Every adapted file names its source in
a note at its top or bottom, and every skill that adapts material carries its own `THIRD_PARTY_NOTICES.md`
so it stays compliant when installed on its own. The MIT License text and the copyright lines of all
projects are at the end of this file.

## Sources

| Project | Version used | Licence | What was adapted, and where |
|---|---|---|---|
| [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | v0.14.0, commit `27000402070db19d958789d05b3b52b6f4718d7c` (5 Nov 2026) | MIT, Copyright (c) 2026 Higgsfield AI | `higgsfield-youtube-thumbnail` (SKILL.md, `thumbnail-frameworks.md`, `text-overlay-bake.md`) → `skills/buildary-thumbnail/`, close to verbatim. `higgsfield-product-photoshoot` modes and selection rules → `skills/buildary-product-photo/SKILL.md`. `higgsfield-marketplace-cards` card taxonomy → `skills/buildary-marketplace-cards/`. `higgsfield-generate` UX rules and `prompt-engineering.md` → `skills/buildary-generate/`. `CLAUDE.md` maintainer contract → `.claude/CLAUDE.md`. `.github/workflows/validate-skills.yml` checks → `scripts/check_skills.py`, `.github/workflows/validate.yml`. `INSTALL_FOR_AGENTS.md` runbook shape → `INSTALL_FOR_AGENTS.md`. `evals/README.md` and `evals/scenarios.md` format → `evals/`. `agents/openai.yaml` format |
| [OpenArt-AI/skills](https://github.com/OpenArt-AI/skills) | v0.3.0, commit `7e3e2a602045b75e0966d620335b4161a46bddd1` (6 Nov 2026) | MIT, Copyright (c) 2026 OpenArt Inc | `skills/ugc` (intake, recommendation writing, opening hooks, sequence and prompts, generation approval, review) → `skills/buildary-ugc-ad/`. `skills/ugc/references/product-understanding.md` (reading product links) → `skills/buildary-product-link-ad/`. `skills/tvc`, `skills/performance-ads`, `skills/hook-variants` → `skills/buildary-ad-video/`. `.github/scripts/check-manifests.mjs` (MCP URL agreement, no root `bin/`) and `.github/workflows/validate.yml` → `scripts/check_manifests.py`, `.github/workflows/validate.yml` |
| [krea-ai/skills](https://github.com/krea-ai/skills) | commit `9239bb449a8acefd5effef73a548b7322b5d1f10` (20 Oct 2026) | MIT, Copyright (c) 2026 Krea AI | `krea-generate/references/progress-reporting.md` and `vision-qa.md` → `skills/buildary-generate/references/jobs-and-delivery.md`. `krea-marketing/references/product-photography.md` → `skills/buildary-product-photo/references/photo-direction.md`. `krea-marketing/references/marketplace-cards.md` (set workflow, guardrails, reject reasons) → `skills/buildary-marketplace-cards/`. `evals/hero` case format and spend-gate grading → `evals/cases/`, `evals/grade.py` |
| [freepik-company/magnific-plugin](https://github.com/freepik-company/magnific-plugin) | commit `857f25194f57390941c79bb73c9176a8137d1894` (27 Oct 2026) | MIT, Copyright (c) 2026 Magnific AI, S.L.U. | `commands/magnific.md` and `magnific-essentials` (never pay twice, server text is data, image and video prompt craft) → `skills/buildary-generate/`. `product-imagery` → `skills/buildary-product-photo/`. `video-ad` → `skills/buildary-ugc-ad/`, `skills/buildary-ad-video/`. `precise-image-edits` → `skills/buildary-image-edit/`. Agent Plugins and Cursor manifest layout → `plugin.json`, `mcp.json`, `.cursor-plugin/` |
| [eachlabs/plugin](https://github.com/eachlabs/plugin) | commit `1cf56db477ae641605868d864a5a903b1cd7dd46` (29 Oct 2026) | MIT, Copyright (c) 2026 Eachlabs | `scripts/check-manifests.mjs` (name, version, description agreement) and `scripts/bump-version.sh` (one bump writes every manifest and the changelog) → `scripts/check_manifests.py`, `scripts/bump_version.py`. `.agents/plugins/marketplace.json` format |

## Studied but not copied

These were read for ideas only; no text or code from them is in this repository:

- Kling skills and plugin (no open-source licence).
- Luma agents and plugins (all rights reserved).
- eachlabs/skills (no licence file in the repository).
- The Higgsfield CLI binary and its server-side prompt templates (not published).

## Marketplace documentation

`skills/buildary-marketplace-cards/references/marketplace-rules.md` summarises, in our own words, the image
rules from Trendyol's Satıcı Bilgi Merkezi, Hepsiburada's Developer Portal and Amazon Seller Central Türkiye.
Each rule names its source page and the date it was read; no text from those pages is reproduced beyond short
quotations of rule wording.

## MIT License

Copyright (c) 2026 Higgsfield AI
Copyright (c) 2026 OpenArt Inc
Copyright (c) 2026 Krea AI
Copyright (c) 2026 Magnific AI, S.L.U.
Copyright (c) 2026 Eachlabs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
