# Mode recipes

Lifestyle and packaging prompt shapes adapted from freepik-company/magnific-plugin `skills/product-imagery`
and `magnific-essentials/references/image-prompt-craft.md` (commit 857f251), MIT License, Copyright (c)
2026 Magnific AI, S.L.U. See `THIRD_PARTY_NOTICES.md` in this skill.

Fill the `[slots]` from the request and the defaults in SKILL.md. Write prompts in English; keep `exactText` in the owner's language.

## Clauses used everywhere

**File manifest** (first line when there are two or more files):
`IMAGE REFERENCES: image 1 = the product; image 2 = brand logo; image 3 = mood reference.`

**PRODUCT LOCK** (every prompt with a `product` file):
`The exact product from the first reference, photographed as the hero product. PRODUCT LOCK: same shape,
proportions, cap and closure, materials, colours, logo and every line of label text; no changes to the
product. Build only the setting, props and light around it; props never cover the product or its label.`

**Physical grounding:** `Contact shadows, true reflections on [material], natural colour bounce; not a flat
paste-in.`

## File roles

| File | Role |
|---|---|
| The owner's product photo (several angles allowed) | `product` |
| The owner's room or shop photo to redecorate (`interior` workflow) | `source` |
| A person to keep (the owner, a hired model) | `character` |
| A logo to place | `logo` |
| A mood or look reference (analysed and followed, not copied) | `style` |

Put the product first. Up to 8 files.

## Workflow modes

`product_shot` → `product`, `lifestyle_scene` → `lifestyle`, `detail` → `macro`, `conceptual_product` →
`conceptual`, `food_photo` → `food`, `interior` → `interior`. The server writes the photography from a short
brief; your prompt says what the owner wants, not how to light it.

```json
{"workflow": "lifestyle",
 "prompt": "My cold-brew bottle on a sunny kitchen counter on a weekday morning, for the Instagram feed. [PRODUCT LOCK]",
 "light": "daylight",
 "files": [{"fileId": "<product photo>", "role": "product"}]}
```

```json
{"workflow": "interior",
 "prompt": "Turn this café corner into a warm Scandinavian look: light oak, linen, plants; keep the windows and the counter where they are.",
 "files": [{"fileId": "<room photo>", "role": "source"}]}
```

- `product`, `lifestyle`, `macro`, `conceptual` need a `product` file; `interior` needs a `source` file;
  `food` needs none (pass a dish photo as `product` when the owner has one).
- `look`, `light`, `lens` take only the ids `list_workflows` lists in `directions`; leave them out to let the
  server choose. `format` left out uses the workflow's own.
- For `conceptual`, tie the idea to a real product trait (citrus scent → citrus slices, not random fruit).
- One coherent scene per call; a different scene or angle is a different call.

## marketplace_main

`E-commerce main image on a pure white background (RGB 255,255,255). [PRODUCT LOCK]. Product centred,
filling about 85% of the frame, front view straight on, soft even light, faint natural contact shadow
directly beneath, no props, no text, no watermark, no border.` Format `1:1`.

For Trendyol, Hepsiburada or Amazon TR, each marketplace's official rules (fill, background, text bans, pixel
limits) are in the `buildary-marketplace-cards` skill; use it for a listing set. This is a generated image of
the product, not a cut-out of their photo: say so when exactness matters.

## closeup_with_person

`Close [two-hand / one-hand] crop: [hands] [hold / pour / apply / open] the exact product from the first
reference, cropped at the wrist or forearm. [PRODUCT LOCK]. Real skin texture, correct anatomy, five fingers
per hand, natural nails. [Light register D or A from photo-direction.md].` If a `character` file is given,
add the person lock from the core skill and keep the face partial unless the owner wants it full.

## virtual_model_tryout

`[Framing] fashion photograph of [model archetype] wearing the exact [garment / accessory] from the first
reference: same cut, fabric, colour, pattern, hardware and logo placement. [Setting]. [Pose with a
specific action]. [Light]. Fabric drapes and folds with the body's weight.` A named real person needs their
own photo as `character`; a photo the owner supplies is taken as theirs to use.

## hero_banner

`Wide 16:9 hero image. The exact product from the first reference on the [left / right] third. [PRODUCT
LOCK]. [Scene or committed colour field]. The opposite two thirds stay calm and uncluttered for the site's
headline and button. No text in the image.` Headlines belong on the website, not in the picture.

## ad_creative

`Paid-social ad image, [4:5 / 9:16]. [PRODUCT LOCK]. [Scene]. Headline text placed [top third /
upper-left], reading exactly as given; offer badge [position]; nothing else written.` Pass the headline and
offer in `exactText` (each string short; at most 12). In `9:16` keep text and product out of the bottom fifth
and the top tenth, where platform buttons and captions sit. Model `sunburst-26`, `quality: "high"`.

## social_carousel

Write the shared system once and paste it into every slide: palette, light register, surface, type position,
logo position. Each slide then adds one line: `Slide [n] of [N]: [what this slide shows]`. Same files on
every slide. Text per slide goes in that slide's `exactText`.

## restyle

The source image is the `product` file (or `character` when it is a person shot). `Keep the product,
its position, scale and camera angle from the first reference exactly. Change only the setting to
[season / mood / aesthetic]: [new surface], [new props], [new light]. [PRODUCT LOCK].` Keep the source's
format. Say plainly that the image is regenerated and small changes are possible.

## Packaging and label mockups

Two references with explicit roles: the real pack first (role `product`: shape, unit count, material), the
flat label artwork second (role `style`). `Keep the exact geometry, proportions, unit count, silhouette and
material of the pack in the first reference. Replace only the printed label with the artwork from the second
reference, applied edge to edge on the correct faces. No other products or text. Contact shadows, true
specular response.` Small dense type will not render reliably; say so before the first paid attempt. After
two failed corrections, stop and ask for a clearer pack photo or switch model.
