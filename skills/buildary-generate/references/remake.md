# Buildary Remake

`remake_video` re-creates an existing video with the people or products in 1 to 8 photos. It keeps the
source's camera, timing and action and swaps who or what is in it: "put me into this trend video", "show my
bottle instead of theirs", "bu videoyu benim ürünümle yap".

## When to use which tool

| The owner wants… | Tool |
|---|---|
| The same video, with their person or product in it | `remake_video` |
| A new video that only borrows camera, motion or pacing from a clip | `generate_video` with a `reference_video` |
| To edit, trim or caption their own footage | Not available in the MCP yet; say so |

## Inputs

- `sourceVideoFileId`: an MP4 from the library. A video link cannot be imported; the owner adds the file to
  Dosyalarım, or a coding agent uploads it (`files-and-uploads.md`). Only the first 19 seconds of a longer
  source are remade and priced; say so when the source is longer.
- `photoFileIds`: 1 to 8 images, in the order they should be used. Clear, well-lit, front-facing photos of
  each person; clean product photos showing the label.
- `resolution`: `480p` (default), `720p` or `1080p`.
- `prompt`: optional direction, up to 10000 characters: who replaces whom ("the person in the first photo
  replaces the woman on the left"), what to keep, what to change. Leave it empty when the photos are
  self-explanatory.

## Price

Priced per source second (up to 19 s) at the chosen resolution; `list_models` shows the rates under
`remake`. Start directly without `quotedCredits`: at 480p a 19-second remake is usually under 20 credits and
starts at once; at 1080p it usually crosses 20 credits, so the server answers `quote_required` with the price.
Tell the owner that price once, and after the yes resend with the same `requestId` and `quotedCredits`.

## Rights

A source video and photos the owner supplies are taken as theirs to use; do not ask. If the source is plainly
someone else's video (a known creator's trend clip), add one line in the delivery that publishing it may need
the creator's permission.

## Delivery

Follow the job with `get_job` like any video. Look at a few frames if you can: is every replaced face or
product right, does the motion still match the source?
