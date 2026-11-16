# Plan, prompt and price

Adapted from OpenArt-AI/skills `skills/ugc/references/sequence-and-prompts.md`, `video-experience.md` and
`generation-approval.md` (v0.3.0, commit 7e3e2a6), MIT License, Copyright (c) 2026 OpenArt Inc. Changes:
Buildary's 20-credit spending rule replaces OpenArt's draft/upgrade flow. See `THIRD_PARTY_NOTICES.md` in
this skill.

## Write the prompt and the Script Plan as one version

Write the full model prompt and derive the readable plan from it, so both are one version. The plan is not
shown for approval; it goes into the price message when one is needed, and the owner can ask to see it.

### The prompt contains

1. The attached files and their roles, named the model's way (`@Image1` on Seedance, `@image1` on Kling
   4.0, in words on models without `promptReferences`): "the creator in @Image2 holds the serum in @Image1".
   Creator, product and wardrobe locks.
2. The everyday setting, the available light and its direction, the phone position, the crop, and who holds
   the camera.
3. Ordered action beats and product states, with which hand does what.
4. Exact dialogue in quotes, in the ad's language, separate from acting notes ("she says, amused: \"…\"").
5. Intention, natural pauses, gaze changes, pace, and a complete ending.
6. Sound: native speech, room tone, product sounds, and light background music unless the format or owner
   wants none.
7. Captions or on-screen text only if the brief asks: exact words, position, rough timing.

Use clear sentences, not fragments. Prompt in English; dialogue and on-screen words in the ad's language.
Default positive direction: no blanket bans on camera motion, cuts or handling unless the owner asked.

Example structure: a phone rests against the kitchen backsplash; the creator in @Image2 picks up the bottle in
@Image1, turns it so the label faces the lens, opens the cap and says "…", sets it down, then reacts.

### The Script Plan shows

A short table or timed beats:

| Time | What we see | What she says | Text on screen |
|---|---|---|---|
| 0-3 s | … | "…" | none |

Plus: concept in one line, creator and setting, sound (music or none), length, format, model and number of
videos; for several videos, the quoted total. Show every word that will be spoken or written; hide technical
syntax only.

## Using your improved script

Use the improved version without asking. Keep the owner's required facts, exact phrases and offer. If the owner
said "exactly my text" (or "aynen benim metnim"), keep every word and the order. After the job starts, say in
one short sentence what you changed, for example:

"I kept the touch-dimming feature and the 299 TL price, and turned the three feature lines into a question, a
demonstration and a reaction."

## Price

- One video: no `quote`. Start directly (new `requestId`, no `quotedCredits`) and say so in one line. If the
  server answers `quote_required`, tell the owner once, with a one-line summary, for example:
  "A 15-second vertical video: a woman at her kitchen counter shows the serum and says why she likes it. It
  costs 31 credits. Shall I start it?"
  After the yes, resend with the same `requestId` and `quotedCredits` = the `credits` it gave.
- Several videos: `quote` each distinct setting and put the total in one message, once.
- A cheap `seedance-mini` 480p preview only when the owner asks for one; say that the final is a new render,
  so preview + final costs more. Preview plus final is two jobs: quote both and state the total.

After a yes, generate exactly the summarised version and settings.

## Settings checklist before the start

Prompt and plan are the same version; model, format, resolution, duration (a listed value), `sound`, files
and their order, number of videos; for several videos, a fresh `quote` if anything changed. New `requestId` per
video; the same one only to retry the same start (after a timeout or a `quote_required`).
