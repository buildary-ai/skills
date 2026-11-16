# Intake for everyday creator videos

Adapted from OpenArt-AI/skills `skills/ugc/references/intake.md`, `product-and-claims.md` and
`creative-preflight.md` (v0.3.0, commit 7e3e2a6), MIT License, Copyright (c) 2026 OpenArt Inc. See
`THIRD_PARTY_NOTICES.md` in this skill.

Read existing material and decisions; decide instead of asking. Identify: new creation, approved-script execution,
reference adaptation, correction of a result, variations, or a prompt-only/analysis request.

Record: audience, one intended message, product or SKU, creator identity or fictional role, everyday
situation, spoken language, length, format, exact copy, visual, text and sound requirements, and how many
videos are wanted. Default to one fictional adult creator when identity is unspecified; do not demand
identity uploads.

A supplied script or timed plan is a draft unless the owner says to use it exactly, or it was already
approved and is requested unchanged. Develop its intent; keep required facts, exact keywords and explicit
locks.

## What each input supports

| Material | Use it for | Do not assume |
|---|---|---|
| Identity photos | Appearance and visible wardrobe | Voice or lived experience |
| A speaking recording | Appearance, manner, voice guidance (on models that take audio) | Exact voice cloning |
| A creative reference video | Delivery, framing, rhythm, situation | Identity to copy or true product claims |
| Product photos and specifications | Appearance and documented operations | Unseen construction or performance |
| An approved script | Exact words and pronunciation | Permission to shorten locked wording |
| Real customer evidence | The documented experience, with its attribution | A testimonial for a different, generated creator |

A link to a social video (TikTok, Instagram, YouTube) cannot be analysed or imported. Ask the owner to add
the video file to their Buildary library if it matters; never claim to have watched it from its title or
thumbnail. A product page link can supply facts if you can read web pages; product images from it can be
brought in with `import_from_url` when they are direct image links.

## Camera arrangement

Choose a plausible phone setup: arm's-length selfie, phone propped nearby, or another person holding it.
If both hands must work the product, use a propped phone or a helper. Never describe the creator holding the
phone, opening a package and handling accessories at once. In a selfie one hand holds the phone.

## UGC or presenter-led

A phone on a stand can still be UGC; a deliberate home studio with structured presentation is presenter-led
(PGC). UGC stresses an everyday situation and a personal, conversational relationship. For mixed briefs,
name the combination instead of forcing a stereotype.

## Product truth

Keep a small evidence ledger: statement or demonstration, source, confirmed fact or visual inference,
approved wording, open gap. Lock silhouette, proportions, colour, material, structure, hardware, logo, SKU
and accessory count from the photos.

- Photos support visible design observations, not waterproofing, battery life, skin results, taste or
  durability. A lifestyle scene must not imply an unverified result either.
- Never invent purchases, long-term use, tests, results, reviews, credentials or endorsements. A present-tense
  observation tied to a visible action ("here is the side pocket") is fine; "I've carried this for six
  months" is not.
- Prices, offers and guarantees appear only when the owner supplied them.
- For an unknown mechanism, pick an action the evidence supports (holding, showing the label, a visible
  feature). Do not remove all interaction, and do not ask.

## Real people

A photo of a person the owner supplies for the ad is taken as theirs to use; do not ask about it. Never use a
photo of a public figure. `seedance-25` refuses images showing a real person's face; use `kling-40` for them.

Output of intake: a keep/change map (words, creator, voice, wardrobe, location, handling, camera) and the
planned video count, ready for the script.
