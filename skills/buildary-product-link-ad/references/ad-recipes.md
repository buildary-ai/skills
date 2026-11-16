# Ad recipes

Fill the `[slots]` from the fact sheet. Write prompts in English; ad copy goes in `exactText` (images) or in
quoted lines (video), in the market's language. No URL ever goes into a prompt.

## Clauses

**PRODUCT LOCK:** `The exact product from the first reference: same shape, proportions, cap and closure,
materials, colours, logo and every line of label text; no changes to the product. Props never cover the
product or its label.`

**Copy rule:** only words from the fact sheet or approved by the owner. Short: a headline of 2-6 words, at
most one supporting line, optionally a price the owner confirmed. Every string the image must show goes in
`exactText`.

## Feed or story image (`generate_image`)

```json
{"prompt": "Paid-social ad image. [PRODUCT LOCK] [Scene that shows the main feature in use]. Headline placed in the top third, reading exactly as given; one supporting line under it; nothing else written. [Light], [palette from the product's own colours].",
 "format": "4:5", "model": "sunburst-26", "quality": "high",
 "exactText": ["<headline>", "<supporting line>"],
 "files": [{"fileId": "<imported product photo>", "role": "product"}]}
```

- Story or Reels cover: `"format": "9:16"`; keep text and product out of the bottom fifth and the top tenth,
  where platform buttons sit.
- Website banner: `"format": "16:9"`, product on one third, no text in the image (the site sets it).
- Without copy, use `"model": "nano-banana-21"` and drop `exactText`: it keeps the product closest.

## Ad film (`generate_film`)

```json
{"workflow": "product-film", "durationSeconds": 10, "format": "9:16",
 "prompt": "A launch film for [product name, variant]: [2-3 key features from the fact sheet, in plain words]. For [audience], [mood]. Show it in use, end on the product with space for the brand name.",
 "exactText": ["<headline from the fact sheet>"],
 "files": [{"fileId": "<imported product photo>", "role": "product"}]}
```

- The prompt is a brief, not a shot list: the director writes the scenes. Never the page link; the film
  prompt refuses any link that is not a supported social or `.mp4` video link.
- `look`, `light`, `lens`, `movement` only from `list_workflows` `directions`, or left out.
- The owner's logo: `get_brand` gives `logoFileId`; add it with role `logo`.

## Video ad (`generate_video`)

```json
{"model": "seedance-25", "durationSeconds": 12, "format": "9:16", "resolution": "720p", "sound": true,
 "prompt": "Vertical 12-second product ad, bright natural light. The product in @Image1 is the hero; keep its shape, label and colours exactly as in @Image1 in every shot. 0-3s: [hook: the product already in use, showing the key feature]. 3-8s: [the second feature, a close detail]. 8-12s: [the product on a surface, slow push in, clean space in the upper third]. Light upbeat music, product sounds.",
 "files": [{"fileId": "<imported product photo>", "role": "reference_image"}]}
```

- Product shown by a real person from a photo: use `kling-40` (its files are `@image1`, `@image2`).
- Spoken lines: quote them, name the speaker, about 2.5 words per second.
- Most control: first make a still with the feed-image recipe (no text), then animate it with its output
  `fileId` as `start_frame` and a motion-only prompt. That is two jobs: quote both and ask once.

## Checks before the start

No URL in any prompt; files point at imported photos; the copy is on the fact sheet; the format is one the
model lists; the duration is one the model lists.
