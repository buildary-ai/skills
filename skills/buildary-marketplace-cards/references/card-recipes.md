# Card recipes

Card taxonomy adapted from higgsfield-ai/skills `higgsfield-marketplace-cards` (v0.14.0, commit 2700040), MIT
License, Copyright (c) 2026 Higgsfield AI; set workflow and failure terms adapted from krea-ai/skills
`krea-marketing/references/marketplace-cards.md` (commit 9239bb4), MIT License, Copyright (c) 2026 Krea AI.
See `THIRD_PARTY_NOTICES.md` in this skill.

Write prompts in English. Every visible word is Turkish (or the listing's language) and goes in `exactText`,
spelled exactly, including ç, ğ, ı, İ, ö, ş, ü. Check each card against `marketplace-rules.md` before you
start it.

## Clauses

**PRODUCT LOCK:** `The exact product from the first reference: same shape, proportions, cap and closure,
materials, colours, logo and every line of label text; no changes to the product, no extra units.`

**Photo realism:** `A real studio photograph, natural materials and true reflections, no illustration, no
CGI look, no heavy retouching.` Trendyol rejects images that look artificial; Hepsiburada rejects graphic
drawings.

## File roles

The owner's product photos (several angles welcome) → `product`, front view first. The product's own brand
logo → `logo`, only on cards whose marketplace allows a logo (never on Hepsiburada). For cards after the main
image, also pass the approved main image's output `fileId` as a second `product` file so the set stays
consistent.

## Main image (`main_image`)

`Square e-commerce main image of the product on a pure white background (RGB 255, 255, 255). [PRODUCT LOCK]
Front view, straight on, out of its packaging, centred, filling about [85 for Amazon / 80 for Hepsiburada /
most of the frame for Trendyol] percent of the frame, entirely inside it, one unit only. Soft even light, a
faint natural contact shadow. No text, no logo overlay, no props, no frame, no watermark. [Photo realism]`

Model `nano-banana-21`, `format` `1:1`. No `exactText`.

## Multi-angle (`multi_angle`)

One angle per card: `[side / back / top / three-quarter] view of the same product, white background,
[PRODUCT LOCK], filling most of the frame, no text.` Use a real photo of that angle as the first file when the
owner has one; a generated angle the owner has no photo of must be compared with the product before listing.

## Detail (`detail_shot`)

`Close-up of the product's [material / closure / texture / control], filling the frame, white or light
background, sharp focus on [detail], [PRODUCT LOCK].`

## Package contents (`whats_in_box`)

`Flat lay on a white background of exactly these items: [list from the owner]. [PRODUCT LOCK] Items evenly
spaced, nothing else in frame.` Only items the owner confirms are in the box. On Trendyol, anything shown for
clarity but not included must be labelled as not included (`exactText`, for example `Pakete dahil değildir`).

## Size card (`size_card`)

`The product on a white background with thin dimension lines and the measurements written exactly as given.`
Pass the measurements in `exactText` (for example `24 cm`, `12 cm`). Not for Hepsiburada (no text allowed).

## Lifestyle (`lifestyle`)

`The exact product from the first reference in use in [a real, tidy setting matching its buyer], light
[natural / soft window]. [PRODUCT LOCK] No text.` Allowed as an additional image on all three; never as the
main image here.

## Feature card (`infographic`)

`Clean product card: the product on the [left / right] half on a light background; on the other half up to
three short feature lines, each with a simple line icon, written exactly as given. [PRODUCT LOCK]` Model
`sunburst-26`, `quality: "high"`, features in `exactText`, each line short and taken from the owner's facts.
Trendyol: short text only, never price, discount, campaign, shipping or gift lines. Amazon TR: no claims,
ratings or seller information. Hepsiburada: do not make this card.

## Set workflow

1. Before any start, `quote` one card per distinct setting and tell the owner the set and its total once (with
   the facts question, if a requested text card lacks them, in the same message). Wait for the yes.
2. Make the main image first, then the other cards without stopping; each references the product photos and
   the main image so the set stays consistent. Each start has its own `requestId` and `quotedCredits`.

## Reject and retake

- **Recolored logo:** the product collapsed into a tinted, flat, logo-like graphic instead of a photographed
  product.
- **Prompt-text override:** the output follows product words in the prompt instead of the attached photo
  (wrong colour, invented label).
- Invented claims, certifications, ratings, badges or marketplace logos.
- Misspelled or extra text; text on a card whose marketplace forbids it.

Retake with a shorter, scene-only prompt that leans on the reference; change one thing per paid retry.
