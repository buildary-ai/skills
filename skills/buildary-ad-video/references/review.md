# Review and delivery

Adapted from OpenArt-AI/skills `skills/tvc/references/review-and-delivery.md` and
`continuity-and-variants.md` (v0.3.0, commit 7e3e2a6), MIT License, Copyright (c) 2026 OpenArt Inc. See
`THIRD_PARTY_NOTICES.md` in this skill.

## Look at the actual video

In a coding agent, download the output and look at frames spaced across it (for example every 2 seconds with
ffmpeg), and listen if you can. In a chat app you may only have the link. A successful job, a good prompt or a
contact sheet is not proof of a finished ad. Never claim a check you could not do; list it as unchecked.

Record each with a timestamp and accepted / rejected / unchecked:

- **Product:** the right SKU, shape, proportions, cap, materials, logo and label in every shot, including
  inside camera moves.
- **Idea:** the film develops as planned; each shot changes something; the product is recognisable early.
- **Motion:** weight and contact are believable; no melting geometry, extra fingers, duplicated objects.
- **People:** the same face, wardrobe and body throughout; natural skin.
- **Words and sound:** exact approved lines and on-screen text (Turkish letters included); intelligible
  speech; music fits and ends cleanly; planned silence stays silent.
- **Ending:** complete, with the intended end frame and readable space for the end card.
- **Format:** the asked ratio and length.

## Fixing

Name the failed check and change one thing aimed at it (a clearer reference, a guard inside the move, a
simpler action, a slower camera). A redo is a new paid job under the spending rule and inside any approved
retry count. Never resend an unchanged prompt.

## Variants and revisions

- Regenerating a complete ad to change one line can change its body, camera, product and sound. Check the
  whole new output; keep accepted versions.
- For variants, name the variable and the constants; compare the outputs for accidental differences.
- Never claim a variant performs better without data.

## Delivery

When the video (or every video of the set) is ready, call `show_results` once with all their `jobIds` (at most
8 per call) so the owner watches them as a card in Claude and ChatGPT; do not poll `get_job` for the card.
Then, for each video: the link (it expires within an hour; `get_job` gives a fresh one; the file is also in the
owner's library), its label (`hook B: question / 9:16 / 15 s`), the model and resolution, the credits charged
(and the total against any budget), what you assumed, and short QA notes. In a coding agent, save downloads
under names you choose (`spot-v1-9x16.mp4`). End with one plain line on what you can change ("I can change the
opening, the music or make a square version if you like."), with no tool or setting names; start nothing.
