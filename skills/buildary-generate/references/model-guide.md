# Model guide

`list_models` is the source of truth. This page maps intent to a starting model and records rules that are
easy to miss. It was written against the catalog of 15 November 2026; when the live list differs, the live
list wins. If a default below is missing from `list_models`, pick the closest listed model and tell the owner
which one you used and why.

These defaults are conventions, not measured results. A model the owner names always wins.

## Video (`generate_video`)

| Job | Start with | Why / watch out |
|---|---|---|
| General video, motion-heavy, multi-shot, up to 30 s | `seedance-25` at 720p | Strong motion, native sound, many references. Refuses images or videos that show a real person's face (its own outputs from the last 30 days excepted) |
| A real person from a photo (the owner, a presenter) | `kling-40` | Takes face references; up to 30 s; own audio. For putting them into an existing video use `remake_video` |
| Animate one photo ("bu fotoğrafı canlandır") | `kling-40` for people, `seedance-25` for products and scenes | Pass the photo as `start_frame`; the prompt describes motion only |
| Spoken lines with native sound | `seedance-25` (sound on) or `veo-31` | `veo-31` only does 4, 6 or 8 s and 9:16 or 16:9 |
| Cheap draft to check an idea | `seedance-mini` at 480p, `h3-lite`, `veo-lite` | A draft is a separate generation; the final is a new render, not an upgrade of the draft |
| Follow the camera or motion of a clip | `kling-40` or `seedance-25` with `reference_video` | The clip guides motion only; reference seconds add to the price on `kling-40` and `h3` |
| Owner leaves the model open, short and cheap | `omni` (server default) | 9:16 or 16:9 only |
| A finished multi-scene film with music, edited by Buildary's director | `generate_film` (not a model) | 5, 10 or 15 s; see `buildary-ad-video` |

Resolution: 720p covers most social use; 1080p costs much more and is for hero or client-final masters.
Default format is 9:16; use 16:9 for YouTube and web, 1:1 for feed squares. No video model makes 4:5.

### Per-model rules (from `list_models` notes)

- `seedance-*`: files are named `@Image1`, `@Video1`, `@Audio1` per kind in `files` order.
- `seedance-25`: the prompt picks the task. "add / remove / replace / change" makes it edit `@Video1`;
  "extend / continue" makes it continue `@Video1`. To take only camera and motion from a video, describe the
  new scene and say what `@Video1` is for.
- `kling-40`: files are `@image1`, `@video1`. A reference video is 3-30 s each, at most 30 s together; price is
  (output seconds + reference seconds) × the row's rate.
- `kling-40-flash`: 720p only, images only, no end frame.
- `kling-30`: leave `resolution` out; sound on changes the price.
- `pixverse`: files are `@ref1`, `@ref2`; put a space after each `@ref` token.
- `wan-30`, `wan-prime`: files are `Image1`, `Video1`, `Audio1` (no `@`).
- `happyhorse`: reference images are `character1`, `character2`.
- Models without `promptReferences` (for example `omni`, `veo-31`, `h3`): describe each file in words, in order.
- `sound` is only accepted by models whose entry lists `sound: true`.

## Images (`generate_image`)

Images cost about 1 to 6 credits each, so a single image almost always starts without asking.

| Job | Start with | Notes |
|---|---|---|
| General image, no special need | leave `model` out (standard image) | Cheapest fixed price |
| Exact words in the image: posters, banners, menus, UI | `sunburst-26` with `exactText` | GPT Image 2.6; no 4K. If it refuses a prompt, `sunburst-25` may accept it |
| Keep a person or a product exact from reference photos; instruction edits | `nano-banana-21` | Alternative `nano-banana-2` |
| 4K | `nano-banana-21` or `nano-banana-2` | The only ones listing `4K` |
| Cheap drafts, many options | `nano-banana-2-lite` or `seedream-55` | `seedream-55` has no 4:5: it renders 3:4 and fits it to 4:5 |

- Formats: `1:1`, `4:5` (default), `9:16`, `16:9`.
- `resolution` and `quality`: send only values the chosen model lists; otherwise the model default is used.
- `exactText`: up to 12 strings, each up to 180 characters, rendered exactly as written. Use it for every
  word that must be spelled right, including Turkish letters (ç, ğ, ı, İ, ö, ş, ü).
- File roles: `product` (the product to show), `character` (a person to keep), `style` (a look to follow),
  `logo` (a logo to place). Up to 8 files.

## Buildary Remake (`remake_video`)

Not a model choice: a separate tool. See `remake.md`.
