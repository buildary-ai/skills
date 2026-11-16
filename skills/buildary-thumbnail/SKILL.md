---
name: buildary-thumbnail
description: >-
  Create high-click-through YouTube thumbnails and vertical video covers with Buildary. Builds a truthful
  information-gap concept, keeps up to three referenced faces, supports logos and controlled variants,
  renders with a 4K-capable image model through generate_image, and retouches it in place with revise_job. Use
  when: "make a YouTube thumbnail", "thumbnail for this video", "MrBeast-style cover", "Shorts cover",
  "Reels cover", "Instagram video cover", "kapak görseli", "YouTube kapağı yap", "video kapağı", "küçük
  resim", "Shorts kapağı". Chain after any video work once its truthful topic and look are known. NOT for:
  making the video itself (buildary-generate or buildary-ad-video), product catalog photos
  (buildary-product-photo), or editing an unrelated existing photo (buildary-image-edit).
license: MIT
metadata:
  version: "0.2.0"
---

# Buildary Thumbnail

Create a clean thumbnail concept, generate each variant with the Buildary MCP `generate_image` tool,
inspect it, and make only requested focused edits.

## Bootstrap

1. The Buildary MCP tools must be available (`list_models`, `list_workflows`, `generate_image`, `revise_job`, `get_job`).
   If they are not, tell the owner to connect `https://buildary.dev/api/agency/mcp` and stop. Never ask for
   or print an API key.
2. Call `list_workflows {"kind": "image"}` once: confirm the `cover` workflow (Video kapağı) and read the
   `directions` ids for look, light and lens. Call `list_models` once and read `image.models`: confirm which
   models list `4K` (today `nano-banana-21` and `nano-banana-2`). Never invent a workflow, direction or model.
3. Brand, without asking: when the owner mentions their logo or brand, `get_brand` gives `logoFileId` (pass
   it with role `logo`) if `ready`; if not ready, leave the logo out.

## UX rules

1. Match the owner's language. Keep tool and model mechanics out of normal chat.
2. **Produce first.** Pick the concept, ratio, model and directions yourself and start; never offer a menu.
   At most one question, only when (a) the owner wants themselves or a named person on the cover and no face
   photo was given, or (b) a price must be approved (a variant set or a job over 20 credits). Say what you
   assumed in one line after starting.
3. Never invent claims, outcomes, products, people, screenshots or statistics that are not true of the video.
4. No raw JSON, job ids or file ids in chat. Deliver the image link and a short variant label.
5. A style-reference thumbnail is for visual analysis only. Never pass it in `files`; copying its identity
   or exact composition is forbidden.
6. Every concept, emotion or camera take gets its own prompt and its own `generate_image` call.

## Spending

Each render is one paid job of about 1-2 credits. The server starts a job at or under 20 credits at once.

- One render: start it directly with a new `requestId` and no `quotedCredits`. Do not call `quote` first; do
  not ask.
- A variant set: before any start, `quote` one render (free), multiply by the planned count, tell the owner once
  ("4 variants, about 8 credits"), and wait for a yes. Then start each with its own `requestId` and
  `quotedCredits` = the quote, without asking again. Hard cap: 16 generations per thumbnail, retries included.
- A start refused with `quote_required` (over 20 credits): tell the owner the price in `credits` once; after the
  yes, resend with the same `requestId` and `quotedCredits` = `credits`.
- Timeout or unsure a start went through: call again with the same `requestId`; never a new one.
- Report the credits the start result and `get_job` show for the job.

## Intake gates

Collect only what the brief does not answer:

- The video's topic or title and the truthful promise the thumbnail may imply.
- Exact scene requirements, if any.
- Who appears: 0-3 people. The owner wants themselves or a given person but sent no face photo → the one
  question: ask for the photo (a link or the file in their library). Otherwise, when the concept needs a person,
  use a generic generated character and say so; never present it as the owner.
- Optional style-reference thumbnail. Analyze it with vision for energy, framing, split layout, palette and
  emotion; do not send it to Buildary.
- Optional logo: only when the owner sends one or mentions it; it stays flat unless they ask for 3D. Never ask
  about the brand. If `get_brand` is `ready`, its main colour may set the rim accent; otherwise ignore brand.
- Optional headline, 2-4 words. Default delivery is a clean image with no text. Use a deterministic overlay
  when an overlay is requested; bake text into the image only when explicitly asked.
- Ratio: `16:9` for YouTube by default, `9:16` for Shorts and Reels, or `4:5` for Instagram.
- One final thumbnail by default. A variant set only when the owner asks for options.

If the owner gives an emotion count without names, use this ladder: shock, hype, rage, awe, laugh, fear,
smug, charisma, confusion, determination, disgust.

## Getting the files in

Faces and logos must be `fileId`s from the owner's Buildary library: `list_files`, `import_from_url` for a
direct image link, or `create_upload` → PUT → `complete_upload` in a coding agent. A photo attached to the
chat cannot be passed to the tool; ask for a link or for the file in the library (Dosyalarım).

## Concept gate

Read `references/thumbnail-frameworks.md`. Brainstorm at least five truthful concepts internally, across
several frameworks, then pick the strongest information gap with one focal subject and minimal clutter.
Combine frameworks only when the result still reads in under one second at about 120 px wide.

When a reference thumbnail exists, extract this structure before prompting:

```text
brief, generic subject pose/action, elements, location, composition, background,
split (true/false), split_count, person_count, emotion, emotion_detail
```

The reference supplies art direction, never a specific identity. Owner instructions override it field by field.

## Reference order

Put face photos first in character order with role `character`, then the logo with role `logo`. When two or
more files are attached, the prompt's first line is a manifest:

```text
IMAGE REFERENCES: image 1 = CHARACTER 1 face reference; image 2 = brand logo.
```

## Prompt contract

Assemble every main-render prompt in this order:

1. **Frame:** `Bold, punchy YouTube-thumbnail composite — poster-grade, photoreal and high-impact, NOT a muted cinematic movie still, <ratio>, single unified frame — no split-screen, no diagonal divide, everything blends smoothly and organically across the same continuous shot.` For `9:16`, add `faces in the upper two-thirds`. A requested graphical representation replaces photoreal language with a clean diagram or graphic brief.
2. **Scene brief:** depict the owner's exact content.
3. **Text:** default `No text, no readable UI labels, no watermark.` For an explicit baked headline: `TEXT: bold thumbnail headline text baked into the image, reading exactly "<TEXT>" — massive, ultra-legible sans-serif with a clean outline/glow treatment, placed where it never covers the subject's face. No other text, no watermark.` and pass the same string in `exactText`.
4. **Subjects:** large, foreground-dominant, chest-up or medium-close, filling about 40-60% of the frame. End with `All faces crisply sharp as the anchors of the shot.`
5. **Key elements:** only signature props or effects that explain the information gap.
6. **Logo:** keep exact shapes, colours, proportions and letterforms; keep it away from faces.
7. **Location:** place, time, weather and atmosphere when relevant.
8. **Composition:** one power-third hero, clear scale hierarchy, depth, strong subject/background separation.
9. **Background:** vivid high-contrast colour field or environment, soft vignette and edge falloff; do not divide it unless a split layout was requested.
10. **Lighting on people:** `signature YouTube thumbnail lighting rig — strong key light sculpting the face, soft dreamy fill lifting shadows, and defined back light plus hair light tracing a clean bright rim around hair, shoulders and silhouette.` Only the rim may use a coloured accent.
11. **Grade:** vivid, bright, glossy, poster-punchy, deep blacks, crisp highlights, rich saturated colours, cohesive as one image. Restrain it only for an explicit calm, premium or muted brief.

For each photo-referenced person, include:

```text
CHARACTER N: the person from attached face reference #K — IDENTITY LOCK: reproduce
this exact person with a photographic identity match — same bone structure, eye shape,
nose, lips, jawline, skin tone, hairline and hair texture. Do not beautify, average,
or restyle the face. Expression: <emotion phrase>.
```

### Split layouts

Use a split only when the owner asks for `split`, `before/after`, `versus`, `side by side`, or the analyzed
reference is split. A topical phrase such as `X vs Y` does not itself require a split. Replace the normal
frame block with a clear halves or panels contract and keep labels out unless short, truthful baked UI was
explicitly requested.

## Optional 3D logo

First make a 1:1 logo render, then use its output `fileId` (from `get_job`) as the `logo` file on every
thumbnail call:

```json
{"prompt": "Transform the attached 2D logo into a premium 3D logo render: extrude the exact logo shapes into glossy dimensional volumes; preserve every letterform, proportion and brand colour; soft studio reflections, subtle bevels, crisp edges, clean dark neutral background, soft contact shadow, centered, generous margins, no extra text, no watermark.",
 "format": "1:1", "model": "sunburst-26", "quality": "high",
 "files": [{"fileId": "<logo fileId>", "role": "logo"}]}
```

## Main render

Run every main render on the `cover` workflow (Buildary's video-cover job), on a 4K-capable model at explicit
4K (`nano-banana-21`; `nano-banana-2` if it is missing). The prompt contract above stays the prompt: it
carries the concept, identities and text policy the workflow cannot know.

```json
{"workflow": "cover", "prompt": "<assembled prompt>", "format": "16:9", "model": "nano-banana-21", "resolution": "4K",
 "files": [{"fileId": "<face 1>", "role": "character"}, {"fileId": "<logo>", "role": "logo"}]}
```

- `format`: `16:9` for YouTube (the workflow's own), `9:16` for Shorts and Reels, `4:5` for Instagram.
- `light`, `look`, `lens`: leave them out; the prompt's lighting rig and grade decide. Pass one only when the
  owner asks for a specific look, using an id from `directions` (for example `"look": "bold"`).
- A poster or event announcement (afiş, duyuru) is not a thumbnail: that is the `poster` workflow in
  `buildary-generate`.

Leave `files` out when there are no references. For a variant set, one call per distinct prompt; keep the
same files and settings and vary only the concept, expression or camera-take line. Follow each job with
`get_job`; keep each ready output's link and `fileId` privately: the link is delivered, the `fileId` is the
source for later edits.

## Post-render gate

Inspect every result with vision when available:

- Referenced identities visibly match.
- No stray text or watermark unless baked text was ordered.
- Baked text matches character for character, Turkish letters included.
- The face, emotion and hero element stay readable at about 120 px wide.
- The concept truthfully matches the video's promise.

On a hard failure, make one new take with `revise_job` and `"regenerate": true` on that job (instruction
"Yeniden üret"), at most twice, inside the approved count. If you cannot see the image, do not claim it passed;
deliver it for the owner's review. When several variants pass, deliver them all; the owner picks.

## Focused tweaks

A tweak retouches the picked thumbnail in place with `revise_job` on its job: the server changes that one thing
and keeps the rest. Start it without asking; it is a 1-4 credit job (over 20 credits the price rule applies).

```json
{"jobId": "<picked thumbnail's job>", "requestId": "<new UUID>",
 "instruction": "Change ONLY the person's facial expression to: <phrase>. Keep identity, face, hair, pose, clothing, logo, background, lighting and composition exactly as they are."}
```

- Allowed tweak scopes: expression only, background replacement only, background recolour only, or rim-light
  recolour only. One scope per revision; chain them, each building on the version before.
- "Another version" of the same concept: `revise_job` with `"regenerate": true` (instruction "Yeniden üret").
- The job must have finished; `content_still_working` means follow it with `get_job` first. The `jobId` stays
  the same and the earlier version stays in the library.
- Never silently regenerate the full composition for a focused request.

## Text overlay

Keep the generated image text-free by default. When a headline overlay is requested, read
`references/text-overlay-bake.md` and use one of its five presets: Beast, Fire, Neon Lime, Clean Glass or
Marker. The overlay needs an environment that can render HTML canvas (a coding agent with a browser); if
unavailable, deliver the clean image and say a baked-text version can be made. Never
present an HTML preview as a flattened PNG.

## Delivery

When the thumbnail (or every variant of the set) is ready, call `show_results` once with all their `jobIds`
(at most 8 per call) so the owner sees them as a card in Claude and ChatGPT; do not poll `get_job` for the card.
Return the passing links with short labels such as `shock / close-up` or `product / size contrast`. Mention
the ratio, whether each deliverable is clean, overlay-ready or text-baked, and the credits charged. Links
expire within an hour; `get_job` gives a fresh one, and every output is in the owner's library. End with one
plain line on what you can change ("I can change the expression, the background colour or add a headline if
you like."), with no tool or setting names.

## Reference files

- `references/thumbnail-frameworks.md`: 16 concept frameworks, the information-gap rule, the truthfulness law.
- `references/text-overlay-bake.md`: five deterministic text-overlay styles and the 4K canvas-bake recipe.

<!-- Adapted from higgsfield-ai/skills higgsfield-youtube-thumbnail/SKILL.md (v0.14.0, commit 2700040),
MIT License, Copyright (c) 2026 Higgsfield AI. Changes: Buildary MCP tools and models instead of the
higgsfield CLI, the 20-credit spending rule, library file inputs, revise_job tweaks.
See THIRD_PARTY_NOTICES.md in this skill. -->
