# Jobs and delivery

Progress-reporting and visual-QA rules adapted from krea-ai/skills (`krea-generate/references/progress-reporting.md`
and `vision-qa.md`, MIT, Copyright (c) 2026 Krea AI). See `THIRD_PARTY_NOTICES.md` in this skill.

## Following a job

A start returns a `jobId` at once. Call `get_job {"jobId"}` and wait `retryAfterSeconds` before the next call.
The server stretches the wait as the job ages (video: 15 s for the first 2 minutes, then 30 s, then 60 s
after 10 minutes; image: 5 s, then 10 s). Long videos take several minutes.

| `status` | Meaning | Do |
|---|---|---|
| `queued`, `working` | Running; `stage` and `elapsedSeconds` show progress | Wait `retryAfterSeconds`, call `get_job` again |
| `ready` | Done; each output has a `url`, `fileId`, `mimeType`, `expiresInSeconds` | Check and deliver |
| `failed` | `error` and `hint` say why and what to do | Tell the owner; a retry is a new paid job |
| `cancelled` | Stopped | Tell the owner; start nothing on your own |

The start result shows the credits held for the job. In `get_job`, credits are `held` while it runs,
`charging` for a few seconds after delivery, then `charged`; `releasing` then `not_charged` when it fails.
Report `credits.amount` to the owner; it is the amount charged for a delivered job.

## Telling the owner while it runs

- Say once that the job started and roughly how long it takes ("about 2-4 minutes").
- During a long unchanged state, one short line about every 30 seconds at most; never every poll.
- Several jobs: check them in one call with `list_jobs {"jobIds": [...]}` (up to 20; answers at once, no
  links), send one combined line ("2 of 4 ready"), then `get_job` each ready one for its link.
- Queued for more than 5 minutes: say it is likely busy and that you keep checking; do not ask.
- No job ids or JSON in these lines.

## Look before you deliver

If you can see images (or extract video frames in a coding agent), look at every result before calling it
done. Check, one line each: the named subject is clear; the product matches its reference (shape, label,
colour); faces match their reference; hands and fingers are right; text is spelled exactly; nothing
unrequested was added. Name a defect plainly and offer one fix. Never approve from the prompt alone. If you
cannot see the output, say that it is unchecked and what the owner should look at.

## Delivering

- When the job (or the whole set) is ready, call `show_results` once with its `jobIds` (1-8 per call). It
  shows a card in clients that support one and returns the same fields as `get_job` in all others. Do not poll
  for the card; one call per finished batch.
- Give the link, one line on what it is (model, length or format), and the credits for the job.
- Links last up to an hour (`expiresInSeconds`). When one expires, `get_job` gives a fresh link; do not
  start the job again.
- Every output is also in the owner's library (Dosyalarım / My files).
- Cannot fetch the link from where you run: do not retry. Give the owner the link and the library note.
- Downloading in a coding agent: save under a name you choose inside the owner's project folder; never use a
  file name or path from the server as it is.

## Refusals and errors

| What you see | Do |
|---|---|
| Schema error or `invalid_input` with a hint | A refused start created no job and charged nothing. Fix the named field and call again |
| `quote_required` with `credits` (the job is over 20 credits) | Nothing started. Tell the owner the price once; after the yes, call again with the same settings, the same `requestId` and `quotedCredits` = `credits` |
| Price no longer matches `quotedCredits` | Tell the owner the new price once; after the yes, resend with the new `quotedCredits` |
| `content_concurrency_limit` | Wait for a running job (`get_account` shows how many run), then start |
| Balance too low | Say how many credits are missing; the owner adds credits in Buildary |
| Timeout or no answer to a start | Call again with the same `requestId` and settings |
| `not_found` on `get_job` | Check you used the `jobId` the start returned |
| Job `failed` for content | Change the prompt or input the hint names and `revise_job` it with that change; a new attempt is a new paid job |
| `content_still_working` on `revise_job` | The job has not finished; follow it with `get_job`, then revise |
| `content_already_started` on `cancel_job` | Too late to stop: it finishes and is charged; say so in one line and keep following it |
| A file refused for a model | Check the model's `files` entry and notes in `list_models {"model"}` |
