---
name: buildary-marketplace-cards
description: >-
  Listing image sets for Turkish marketplaces with Buildary: Trendyol, Hepsiburada and Amazon Türkiye. Makes
  the main image, multi-angle, detail, package-contents, size, lifestyle and feature cards through
  generate_image with the owner's product photo, exact Turkish text and each marketplace's official image rules
  (background, product fill, text bans, pixel limits). Use when: "Trendyol images", "Hepsiburada listing
  photos", "Amazon TR main image", "marketplace image set", "Trendyol görseli", "Hepsiburada ürün görselleri",
  "pazaryeri görselleri", "ana görsel ve yardımcı görseller", "ürün kartları", "bilgi kartı". NOT for: social
  ads or banners (buildary-product-photo, buildary-product-link-ad), product videos (buildary-ad-video),
  thumbnails (buildary-thumbnail), or uploading images to the marketplace itself.
license: MIT
metadata:
  version: "0.2.2"
---

# Buildary Marketplace Cards

Image sets for Trendyol, Hepsiburada and Amazon Türkiye listings, made with the Buildary MCP `generate_image`
tool. A listing is judged first on whether it shows the real product and follows the marketplace's rules; a
beautiful card that breaks a rule gets the listing rejected.

## Bootstrap

- The Buildary MCP tools must be available (`list_models`, `list_files`, `import_from_url`, `quote`,
  `generate_image`, `get_job`). If not, tell the owner to connect `https://buildary.dev/api/agency/mcp` and
  stop. Never ask for or print an API key.
- Read `references/marketplace-rules.md` before planning. Use only the rules written there; it lists the
  official source of each. Do not add rules from memory or unofficial blogs.

## UX rules

1. Reply in the owner's language; card text is in the listing's language (Turkish by default).
2. **Produce first.** Decide the marketplace fit, the cards and the settings yourself; never offer a menu.
   - No marketplace named: make the main image fit all three (pure white background, no text, product
     filling about 85% of the square, one unit), and keep other cards inside the strictest rules.
   - No card list: one main image when they ask for "a main image"; for "a set", main image + two angles +
     a detail + a lifestyle card. Text cards only when the owner asks for them.
   - At most one question, and only for (a) a missing product photo or the real facts a requested text card
     needs (features, measurements, package contents), or (b) the set's total price. When both apply, ask in
     the same single message.
3. Brand: never ask. Main images carry no logo. On allowed cards, a `ready` `get_brand` may give the logo;
   otherwise none.
4. No raw JSON or ids in chat. Deliver links with short card labels.
5. Never invent claims, certifications, ratings, badges, prices or marketplace logos.

## Spending

- A set is several jobs: before any start, `quote` one card per distinct setting (free), tell the owner what
  will be made and the total once ("main image + 4 cards, about 10 credits"), wait for a yes, then start each
  with its own new `requestId` and `quotedCredits` = its quote. Ask again only if the total would rise.
- A single card the owner asked for: start it directly with a new `requestId` and no `quotedCredits`; do not
  call `quote` first. If the server answers `quote_required`, tell the owner the price in `credits` once and,
  after the yes, resend with the same `requestId` and `quotedCredits` = `credits`.
- Timeout or unsure a start went through: same `requestId` again, never a new one.
- Report the credits the start result and `get_job` show for each card.

## 1. Plan the set

| Card | Use |
|---|---|
| `main_image` | The listing's first image: product alone on white |
| `multi_angle` | One extra angle per card |
| `detail_shot` | A close-up of material, closure or control |
| `whats_in_box` | Exactly the items in the package |
| `size_card` | Measurements written on the image |
| `lifestyle` | The product in use |
| `infographic` | Up to three short feature lines in Turkish |

Check every planned card against the table at the end of `references/marketplace-rules.md`. Drop or change
cards a marketplace forbids (for example, no text cards for Hepsiburada) and tell the owner why, citing the
marketplace's rule.

## 2. Get the product in

The product photo must be a `fileId`: `list_files`, `import_from_url` for a direct image link (JPEG, PNG or WebP,
at most 20 MB), or `create_upload` → PUT → `complete_upload` in a coding agent. A photo attached to the chat
cannot be passed to the tool; ask for a link or the file in the library (Dosyalarım). Use the angles you are
given; say which cards are generated angles. Never put any URL in a prompt; the server reads it as a
video reference and the job fails after its credits were held.

## 3. Make the cards

Follow `references/card-recipes.md`: PRODUCT LOCK in every prompt, photo realism, words only in `exactText`.

- Model `nano-banana-21` for cards without text; `sunburst-26` with `quality: "high"` for text cards. Check both
  in `list_models`.
- `format` `1:1`. None of the three sources fixes an aspect ratio; square is this skill's default.
- Main image first, then the rest of the approved set without stopping (each later card also references the
  main image). Follow each job with `get_job`.
- The main image is a generated image of the product. Trendyol rejects representative or artificial-looking
  images and Amazon asks for a realistic image: tell the owner that a real studio photo on white is the safest
  main image, and that generated cards suit the additional images best.

## 4. Check before delivering

If you can see the images, check each against its marketplace's rules and the product photo: background,
product fill, one unit, no extra items, no forbidden text, exact spelling, no recoloured logo, no invented
details. Name a failure and retake once with one change.

- **Pixel limits.** Trendyol accepts at most 2000 × 2000 px; Buildary's 2K output can be larger. In a coding
  agent, download the file and check its size; if it is over the limit, scale it down (for example
  `magick in.png -resize 2000x2000 out.jpg`). In a chat app, tell the owner to check the size before uploading.
- **Amazon TR and AI people.** A card with a photorealistic generated person needs the keyword
  `contains-synthetic-performer` in the XMP `dc:subject` field before upload (in a coding agent:
  `exiftool -XMP-dc:Subject+=contains-synthetic-performer file.jpg`). Tell the owner when it applies.

When the set is ready, show every card with one `show_results` call (at most 8 per call). Deliver: a list of links with card labels and the marketplace each suits, the credits for each card, and what
the owner must check before listing. Final approval is the marketplace's review. End with one plain line on
what you can change ("I can change the angle or add a size card if you like."), with no tool names.

## Reference files

- `references/marketplace-rules.md`: Trendyol, Hepsiburada and Amazon TR image rules with official sources.
- `references/card-recipes.md`: prompt skeletons per card, file roles, set workflow, reject reasons.
