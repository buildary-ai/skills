# Plan, prompt and approval

## Prompt and plan are one version

Write the full model prompt for every planned video and derive the readable plan from it, so both are one
version. The plan is not shown for approval: it goes into the price message when one is needed, and the
owner can ask to see it.

### Each prompt contains

1. Format, length and style as a short cinematography note.
2. The files and their roles, named the model's way (`@Image1` on Seedance, `@image1` on Kling 4.0, in words
   elsewhere), with the product lock.
3. Timed beats (`0-4s: … / 4-9s: … / 9-15s: …`): framing, one camera move with a start and an end, one
   physically plausible action, the product moment.
4. Light by source, direction and quality, motivated by something in frame.
5. Exact spoken lines in quotes with who says them and how; on-screen words exactly, with position.
6. Sound: music texture and arc or none, product and room sounds, voice balance.
7. The ending: a small continuing action under the last beat, not a frozen hold; space for the end card.
8. Negatives aimed at real failures only: no extra text or logos, no product deformation, no duplicate faces.

Prompt in English; dialogue and on-screen words in the ad's language. Seedance 2.5 accepts long prompts; keep
other models' prompts tight.

### The readable plan shows

| # | Time | What we see | Camera | Sound / words |
|---|---|---|---|---|

Plus: the idea in one line, format, length, model and resolution, number of videos and generation steps
(stills + videos), for several steps the quoted total, and what you assumed. Every spoken and written word is
visible; technical syntax stays hidden.

## Your improved script, and the price message

- **Improved script:** use your improved version without asking. If the owner said "exactly my text" (or
  "aynen benim metnim"), keep every word. After the job starts, say in one short sentence what you changed.
- **One video:** start directly. If the server answers `quote_required`, one message with a one-line summary
  and the price: "A 15-second vertical spot: the mug on a cold morning commute, ending on the desk. It costs
  31 credits. Shall I start it?" After the yes, resend with the same `requestId` and `quotedCredits`.
- **Several steps** (a still plus a video, several videos): `quote` each and state the total once: "One
  product still for the opening frame plus one 15-second vertical spot: 33 credits in total. Shall I start?"
- **Hook set:** "Base ad plus 4 openings, joined locally: 5 generations, 58 credits in total. Shall I start?"
- A cheap preview only when the owner asks for one; the final is a new render, so preview plus final costs more.

A yes covers exactly the summarised plan. Silence is not approval.

## Before each start

Prompt and plan versions match; model, format, resolution, a listed duration, `sound`, files in order; for a
set, the quote for those exact settings. New `requestId` per video; the same one only to retry the same start
(after a timeout or a `quote_required`).
