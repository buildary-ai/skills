# Performance ads and hook variants

Adapted from OpenArt-AI/skills `skills/performance-ads/SKILL.md`, `skills/hook-variants/SKILL.md` and
`references/opening-hooks.md` (v0.3.0, commit 7e3e2a6), MIT License, Copyright (c) 2026 OpenArt Inc. See
`THIRD_PARTY_NOTICES.md` in this skill.

## Performance ads

A feed ad gives the intended audience a reason to stop, to understand the product, and to take the requested
next step. These are three decisions; do not optimise only the opening. Presenters, stickers, big text, fast
cuts and a call to action are not universal requirements; the brief decides.

- Connect attention to one main communication goal. Choose action, demonstration, situation, comparison,
  humour, sensory detail or graphics to serve it.
- Give every shot, word and sound a role. Remove what has none.
- Normally include product-appropriate background music with energy that fits; drop it when the format or
  owner calls for silence.
- Product and claims: only what the owner supplied or the photos show. An offer appears only when given.
- A creative hypothesis is not a verified conversion improvement; never promise results.

## The first 3-5 seconds

Decide why this viewer keeps watching. Start with a recognisable situation, a pointed question, real
curiosity, a supported contrast, a visible demonstration or a consequential detail. Avoid greetings, generic
hype, unrelated shock and feature or discount lists that delay the reason to care. Make the product
recognisable from the first image (in hand, in use, clearly present). The hook creates an expectation the body
must pay off; curiosity never licenses invented results, scarcity or testimonials.

## Hook variants

Default delivery is a set of complete videos sharing one body: one base ad plus alternative openings (about
four, or the count the owner asks for). The opening is the variable; body, message, offer, call to action and
product are held constant and named as constants in every prompt.

1. Develop the complete base ad first and get it approved and accepted.
2. Write genuinely different opening ideas (not synonyms): situation, question, demonstration, contrast,
   sensory detail. Each pays off in the same body.
3. Choose how the variants are made, and price the whole set in one message:
   - **Coding agent with ffmpeg:** generate only the new openings (short clips matching the base's look,
     ratio and resolution) and join each to the accepted base body locally. Check every seam: matching
     colour, framing, sound level, no repeated or missing beat. Say that you joined them locally.
   - **Chat app or no ffmpeg:** each variant is a full regenerated video with the new opening and the same
     body prompt. The body will differ slightly between versions; say so.
4. Review every complete variant, not only the openings. Report the hook-to-file mapping.

Keep the sound policy the same across all versions (if the base has no music, no variant adds music). A new
concept or body is a separately reviewed change, not a hook variant.
