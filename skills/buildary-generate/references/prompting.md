# Prompting

## General

- Concrete and sensory beats adjectives: subject, setting, light, camera, style. One precise detail beats
  three vague words; replace "premium", "aesthetic", "high-end" with the physical fact that produces it.
- Write the prompt in English; keep spoken lines and `exactText` in the language the owner wants.
- Phrase positively: "tack sharp" instead of "no blur", "empty street" instead of "no people". Name a
  negative only for a real, likely failure ("no extra text, no watermark").
- Keep one visual register per image: never photoreal and flat vector together.
- Avoid real public figures, sexual content, and brands or characters the owner does not own.
- Never put a URL in a prompt, not even a product page or image link. The server reads a link in the prompt
  as a video reference and the job fails after its credits were held. Bring images in as files and describe
  everything else in words.

## New image

Order, densest first: subject (count, attributes) → action or pose → setting → composition (shot size,
angle, lens feel) → light (source, direction, quality, time of day) → style or medium → colour and detail.

- Words that must appear go in `exactText`, not only in the prompt. Short strings render best; small dense
  text (ingredients, legal lines) is unreliable: say so before the first paid attempt.
- Lens by job: a wide view for places, about 50 mm for full body, about 85 mm for faces. Never a wide lens on
  a face.
- Depth: name one focus target and which layers go soft; otherwise everything renders sharp.

## Image with reference files

Say what each file is for, in order: "The first image is the product: keep its shape, cap, colours and every
line of its label exactly. The second image sets the light and mood."

- Product lock: "same shape, proportions, materials, colours, logo and label text; no changes to the
  product". Props never cover the product or its label.
- Person lock: "same face, bone structure, eye shape, skin tone, hairline and hair; do not beautify or
  restyle the face".
- To change an existing image, describe what changes, not the whole image again (see `buildary-image-edit`).

## New video

Order: style and mood → subject and setting → one physically plausible action → camera (shot size, angle,
one movement with a start and an end) → light and atmosphere with one environmental force (wind, water,
moving light) → sound, when the model has sound.

- One action and one camera move per beat. Never "static camera" and "orbit" in the same beat.
- Over about 8 seconds, write timed beats: `0-3s: … / 3-7s: … / 7-10s: …`, and end on a small continuing
  action, not a frozen hold.
- Camera words that work: locked frame, slow push in, pull back, pan, tilt, tracking at human height, orbit
  with a set arc, handheld micro-drift, whip pan; low, high, overhead, POV.
- Guard what matters inside a move: "during the arc, the bottle's label and cap stay exactly as in @Image1".
- Weight and contact beat emotion labels: breath, a held beat, a hand that grips.
- Dialogue: quote each line, name who says it and how ("she says quietly: \"…\""), one speaker per beat,
  about 2.5 words per second. Put the line in the language the owner wants.

## Image-to-video (`start_frame`)

The start frame already shows the scene. The prompt describes only what moves and how the camera moves.

- Bad: "a man with brown hair in a leather jacket holding coffee, cinematic".
- Good: "he lifts the cup and blows on it; steam drifts left; slow push in to a close-up".
- With an `end_frame`, describe the motion that gets from the first frame to the last.

## Fixing a bad result

Change one thing per paid retry, aimed at the visible failure, and say what you changed:

| Failure | Change |
|---|---|
| Floating, weightless bodies | Describe weight transfer and contact |
| Product or face drifts | Repeat the lock, add a guard inside the move, use a clearer reference |
| Camera flies around | Slow it and give the move an end point |
| Stiff cloth, hair, water | Name one force acting on them |
| Overacting | Breath, small actions, a held beat |

Never regenerate a result nobody has looked at, and never retry automatically.
