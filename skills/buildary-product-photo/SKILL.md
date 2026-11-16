---
name: buildary-product-photo
description: >-
  Brand-quality product images with Buildary from the owner's real product photo, using Buildary's ready-made
  workflows where they fit: studio shots, lifestyle scenes, detail close-ups, conceptual shots, food photos,
  room redecoration ideas, plus white-background main images, model try-ons, hero banners, ad creative sets,
  carousels and restyles, all through generate_image with the product kept exact. Use when: "product photo",
  "studio shot", "lifestyle image", "food photo", "redecorate my shop", "hero banner", "ad creative",
  "ürün fotoğrafı", "ürün çekimi", "beyaz fon", "yemek fotoğrafı", "mekân dekorasyonu",
  "detay çekimi", "mankene giydir", "kampanya görseli". NOT for: images with no product (buildary-generate),
  Trendyol, Hepsiburada or Amazon TR listing sets (buildary-marketplace-cards), ads from a product page link
  (buildary-product-link-ad), video thumbnails (buildary-thumbnail), changing one detail of an existing photo
  (buildary-image-edit), or product videos and ads (buildary-ad-video, buildary-ugc-ad).
license: MIT
metadata:
  version: "0.1.0"
---

# Buildary Product Photo

Product images made with the Buildary MCP `generate_image` tool. Product work is judged first on one thing:
is it the real product? A changed logo, an invented label line or a different cap gets a listing rejected.
Six modes run on Buildary's ready-made workflows (`workflow` field): the server writes the photography
prompt from your short brief. The other modes have no workflow; for them you write the prompt with the
recipes and photo direction in `references/`, so that you never freehand it.

## Bootstrap

- The Buildary MCP tools must be available (`list_models`, `list_workflows`, `generate_image`, `get_job`,
  `list_files`). If not, tell the owner to connect `https://buildary.dev/api/agency/mcp` and stop. Never ask
  for or print an API key.
- Call `list_workflows {"kind": "image"}` once: it gives each workflow's `requiredFile`, suggested `format`
  and the `directions` (look, light, lens ids with Turkish labels). Call `list_models` once for `image.models`.
  Never invent a workflow, direction, model or format.

## UX rules

1. Reply in the owner's language. Mode names, tool fields and model names stay in English.
2. Be concise. The final reply is links plus one-line labels; no JSON, ids or the assembled prompt unless asked.
3. **Produce first.** Choose the mode, workflow, format and directions yourself and start; never offer a menu.
   At most one question, and only when (a) the product photo is missing (food and interior: the dish is
   optional, the room photo is required), or (b) a price must be approved (a set, or a job over 20 credits).
4. **Brand: never ask.** For ads, banners and carousels call `get_brand`: if `ready`, use its colours, tone
   and `logoFileId` (role `logo`) silently; if not, make it without a brand. A brand the owner named wins.
5. Polling is quiet: one line when a set starts, then results.

## Spending

Each image is one paid job of about 1-6 credits. The server starts a job at or under 20 credits at once.

- One image: start it directly with a new `requestId` and no `quotedCredits`. Do not call `quote` first; do
  not ask.
- Several images for one request (3 shots, a carousel, an ad pack, catalog SKUs): before any start, `quote`
  one image per distinct setting (free), multiply, tell the owner once ("5 lifestyle shots, about 10
  credits"), wait for a yes, then start each with its own `requestId` and `quotedCredits` = its quote.
- A start refused with `quote_required` (over 20 credits): tell the owner the price in `credits` once; after the
  yes, resend with the same `requestId` and `quotedCredits` = `credits`.
- Timeout or unsure a start went through: call again with the same `requestId`; never a new one.
- Report the credits the start result and `get_job` show for the job.

## Modes

| Mode | When the owner wants… | `workflow` | Default format |
|---|---|---|---|
| `product_shot` | Product on a clean studio or catalog background | `product` | workflow's (`4:5`) |
| `lifestyle_scene` | Product in a real place, in use, with atmosphere | `lifestyle` | workflow's (`4:5`) |
| `detail` | Material, texture, closure or a small detail up close | `macro` | workflow's (`1:1`) |
| `conceptual_product` | Surreal, CGI-style, levitating, splash, sculptural | `conceptual` | workflow's (`4:5`) |
| `food_photo` | A dish, drink or bakery product (yemek fotoğrafı); photo optional | `food` | workflow's (`4:5`) |
| `interior` | A new decoration idea for the owner's room or shop (mekân dekorasyonu) | `interior` | workflow's (`16:9`) |
| `marketplace_main` | A listing's main image on pure white (Trendyol, Hepsiburada, Amazon, own shop) | none | `1:1` |
| `closeup_with_person` | Tight crop with hands or part of a face: holding, applying, demonstrating | none | `4:5` |
| `virtual_model_tryout` | Product worn or used by a generated model | none | `4:5` |
| `hero_banner` | Wide website, e-mail or campaign header | none | `16:9` |
| `ad_creative` | Static paid-social ads, optionally with exact headline and offer text | none | `4:5` or `9:16` |
| `social_carousel` | 3-10 connected slides with one locked visual system | none | `4:5` |
| `restyle` | An existing product image in a new mood, season or aesthetic | none | source format |

Only `1:1`, `4:5`, `9:16` and `16:9` exist. A Pinterest 2:3 request becomes `9:16` or `4:5`; say which.

## Mode selection

Pick by intent, not surface keyword. When two modes could apply, prefer the more specific one.

- product + neutral, clean, white, studio, catalog, Shopify → `product_shot`
- marketplace listing, main image, pure white → `marketplace_main`; a full Trendyol, Hepsiburada or Amazon TR
  image set with each marketplace's rules → `buildary-marketplace-cards` instead
- product + scene, in use, kitchen, outdoor, café, gym → `lifestyle_scene`
- texture, material, stitching, closure, macro, "detay" → `detail`
- a dish, a plate, a drink, a cake, restaurant menu photo → `food_photo`
- a photo of a room, shop or office + "redecorate / new look / dekorasyon" → `interior`
- hands holding, face with product, beauty application, demonstrating → `closeup_with_person`
- model wearing, try-on, on body, fashion shoot, lookbook → `virtual_model_tryout`
- levitating, floating, splash, frozen motion, surreal, CGI → `conceptual_product`
- hero, banner, website header, landing page, e-mail header, wide → `hero_banner`
- ads, ad set, paid social, Meta, TikTok, Google ads → `ad_creative`
- carousel, slides, swipeable, multi-slide → `social_carousel`
- change the mood, season or look of an EXISTING image, keeping the subject → `restyle`

Tie-breakers: "hero banner showing my product in use" → `hero_banner` (format wins); "carousel of my product
in different scenes" → `social_carousel` (multi-slide wins); "close-up of a person applying my serum" →
`closeup_with_person` (specific genre wins); "white background for Trendyol" → `marketplace_main`.

## Defaults instead of questions

Decide from the request and the photo; say what you assumed in one line after starting.

| Not in the request | Default |
|---|---|
| How many | One image. Several only when the owner asks for a set, options or a carousel |
| Style | The mode's own: `product_shot` studio; vague briefs ("something nice", "cool for my brand") → `lifestyle_scene` in a setting that fits the product |
| Where it will be used | Instagram feed (`4:5`) unless the words name a channel; "banner", "website" → `hero_banner` |
| Look, light, lens | Left to the workflow; on other modes, the photo-direction defaults |
| Restyle aesthetic or season | Taken from the owner's words; otherwise a clean, light, seasonless version |
| Model for a try-on | An adult who fits the product's obvious buyer; framing that shows the whole product |
| Ad copy | Only words the owner gave; without them, an ad image with no text |

**No product photo** is the one question for product modes: ask once for a direct image link or the file in
their Buildary library. If the owner cannot give one and still wants an image, make an invented product from
their description and say it is not their real product.

## Getting the product in

The product photo must be a `fileId`: `list_files`, `import_from_url` for a direct image link (JPEG, PNG,
WebP, at most 20 MB), or `create_upload` → PUT → `complete_upload` in a coding agent. A photo attached to the
chat cannot be passed to the tool: ask for a link or for the file in the library (Dosyalarım). Use the angles
you are given; a set of other angles from one photo is generated, so say so instead of asking for more.

## Building the request

**Workflow modes** (`product_shot`, `lifestyle_scene`, `detail`, `conceptual_product`, `food_photo`,
`interior`):

1. Pass `workflow` and the file its `requiredFile` names: the product photo with role `product`; for
   `interior` the owner's room photo with role `source`; `food` needs no file (a dish photo, if given, goes as
   `product`). A missing required file is refused with `invalid_input`.
2. The prompt is the owner's intent in one or two sentences (setting, mood, use, must-haves) plus the PRODUCT
   LOCK clause when a product file is attached. Do not paste photo-direction paragraphs: the server writes the
   photography.
3. Directions: map the owner's words to `look`, `light` and `lens` ids from `directions` (offer the Turkish
   labels when they ask), or leave them out for the server to choose. Leave `format` out for the workflow's
   own unless the owner names a ratio.

**Other modes:**

1. Read `references/mode-recipes.md` for the chosen mode's skeleton and file roles.
2. For styled modes (hero, ad creative, carousel), read `references/photo-direction.md` and make its four
   decisions in writing first: lighting register, palette, staging, finish.
3. Every prompt with a product file carries the PRODUCT LOCK clause. Words that must appear go in
   `exactText` (headline, offer, price) and nowhere else; never invent label text.

The owner's named colour, mood, setting or reference outranks every default. Never put a URL in a prompt.

## Generation

- Workflow modes: leave `model` out (standard image, 1 credit; the workflow does not change the price). If
  the product drifts, the one retry adds `"model": "nano-banana-21"`.
- Other modes: `nano-banana-21` at `2K` when a product file is attached (strongest at keeping the product and
  its label); `sunburst-26` with `quality: "high"` for `ad_creative` with headline or offer text. Check each
  against `list_models`.
- One `generate_image` call per image. A set is several calls with the same files and settings, varying only
  the planned line (scene, angle, light); vary one axis so the options are easy to compare.
- `social_carousel` and `ad_creative` sets: write the shared visual system once (palette, light, type
  position) and repeat it verbatim in every slide's prompt.
- Follow each job with `get_job`, waiting `retryAfterSeconds`.

## Check, then deliver

If you can see the images, compare each with the product photo before delivering: shape, proportions, cap,
colours, logo and label lines; hands and fingers; spelling of every `exactText`. Name a drift plainly and
offer one fix (tighten the lock, switch model); never repeat the same call unchanged. If you cannot see them,
say they are unchecked and what to look at.

When the image (or the whole set) is ready, call `show_results` once with all their `jobIds` (at most 8 per
call) so the owner sees them as a card in Claude and ChatGPT; do not poll `get_job` for the card. Then deliver
a short list: link, one-line label (`lifestyle / kitchen counter / 4:5`), which images are generated
scenes rather than retouched photos, and the credits charged. For `marketplace_main`, tell the owner to check
the channel's rules (white point, product fill, no extra text) before listing. End with one plain line on what
you can change ("I can change the light, the background or the angle if you like."), with no tool or setting
names.

## What this skill does not do

- Pixel-exact cut-outs, background removal or upscaling: not in the Buildary MCP yet. A white-background
  image here is a new generation of the product; say so when exactness is critical.
- Packaging or label design itself, dense small text (ingredients, legal lines): suggest a design tool.
- Product videos: `buildary-ad-video` or `buildary-ugc-ad`.

## Reference files

- `references/mode-recipes.md`: workflow calls and prompt skeletons for each mode, file roles, marketplace note.
- `references/photo-direction.md`: lighting registers, palettes, staging modes, prompt order, avoid list.

<!-- Mode table and selection rules adapted from higgsfield-ai/skills
higgsfield-product-photoshoot/SKILL.md (v0.14.0, commit 2700040), MIT License, Copyright (c) 2026
Higgsfield AI. Product-lock routing adapted from freepik-company/magnific-plugin skills/product-imagery
(commit 857f251), MIT License, Copyright (c) 2026 Magnific AI, S.L.U. See THIRD_PARTY_NOTICES.md in this
skill. -->
