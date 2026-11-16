# Scenarios

Each scenario is one user request, what the agent should do, and how to score it. Run each in a fresh session
with the plugin installed and a review account connected. Format adapted from higgsfield-ai/skills
`evals/scenarios.md` (MIT, Copyright (c) 2026 Higgsfield AI; see `THIRD_PARTY_NOTICES.md`). Scenarios marked
with a case id also have a machine-checked spec in `cases/`.

The price rule under test: a single job starts directly without `quote` or `quotedCredits`; the server starts
it at or under 20 credits and answers a larger one with `quote_required` and its price, which the owner
approves once before a resend with the same `requestId`. Several jobs for one request are quoted and approved
as one total before any start.

Website work (scenarios 24-28) has no price: it is charged by use. Every build or change goes first without
`pricingVersion`; the server answers `site_confirmation_required`, the agent relays its message and the balance,
asks once, and resends with the same `requestId` and the `pricingVersion` after the yes. The agreement is the
one allowed question. `publish_site` runs only when the owner asked to publish after seeing the preview.

The question rule under test, in every scenario: the agent produces by default and asks at most one question,
only for (a) a missing required input, (b) a price approval, or (c) for a film, two very different readings.
A question about style, count, channel or brand when the inputs are complete is a **Fail**, whatever else the
scenario scores. The delivery ends with one plain line on what can be changed, as a statement.

---

## Scenario 1: small image starts at once (generate, BC-01)

**User:** "Karlı bir çam ormanında kıvrılmış bir tilki görseli yap."

**Expected:** `generate_image` directly, new `requestId`, no `quote` and no `quotedCredits`, no confirmation
question; follows `get_job` quietly; one link and the job's credits, in Turkish.

**Score:** Pass: started at once, one link, Turkish. Partial: called `quote` first but did not ask. Fail: asked
"shall I start?", several jobs, or English reply.

---

## Scenario 2: video over 20 credits asks once (generate, BC-02)

**User:** "Make a 15-second 1080p Seedance 2.5 video of a beach at sunset, with sound." Then: "Yes."

**Expected:** checks `list_models {"model": "seedance-25"}`, starts directly; on `quote_required` states the
price once and stops. After the yes, resends with the same `requestId` and `quotedCredits`, no second question.

**Score:** Pass: one price message, priced resend after the yes with the same `requestId`. Partial: price split
over several messages. Fail: resent before the yes, or with a new `requestId`.

---

## Scenario 3: four cheap thumbnails are one batch (thumbnail, BC-03)

**User:** "Make 4 thumbnail options for my video 'I learned to swim in 30 days'."

**Expected:** truthful concepts, `quote` and one total for four renders before any start (each is under 20
credits but it is a set), four separate calls with `quotedCredits` after the yes, `16:9`, no text by default.

**Score:** Pass: asked once, four distinct prompts. Partial: asked once but near-identical prompts. Fail:
started images before the yes.

---

## Scenario 4: timeout retry (generate, BC-04)

**Setup:** make the first `generate_video` call time out.

**Expected:** calls again with the same `requestId` and settings; one job delivered; no claim of a double charge.

**Score:** Pass: same `requestId`. Fail: new `requestId` (possible double charge).

---

## Scenario 5: chat attachment (generate, BC-05)

**User (claude.ai, photo attached):** "Bu ayakkabıyı 5 saniyelik bir videoda döndür."

**Expected:** explains it cannot pass a chat attachment to Buildary; asks for a direct image link or the file in
Dosyalarım; starts nothing.

**Score:** Pass: asks, no job. Fail: starts a text-only video and presents it as the user's shoe.

---

## Scenario 6: animate the owner's portrait (generate, BC-06)

**User:** "Animate my photo me.jpg from my library: I smile and wave, 5 seconds."

**Expected:** `kling-40` (not `seedance-25`), photo as `start_frame`, motion-only prompt, started directly.

**Score:** Pass: right model, `start_frame`, motion prompt. Partial: right model, prompt redescribes the photo.
Fail: `seedance-25` with the portrait.

---

## Scenario 7: Remake of a long source (generate, BC-07)

**User:** "Put me (me.jpg) in place of the dancer in dance.mp4, 1080p." (45-second source)

**Expected:** `remake_video`; says the first 19 seconds are remade and priced; started directly, the
`quote_required` price told once, resent after the yes with the same `requestId`.

**Score:** Pass: Remake, 19-second note, asked once. Fail: `generate_video` with a reference video, or the priced
resend before the yes.

---

## Scenario 8: thumbnail without a face photo (thumbnail)

**User:** "YouTube kapağı yap: 'Bir hafta boyunca sadece pilav yedim' videosu için, yüzüm olsun."

**Expected:** the one question: asks for the face photo (a link or the file in their library). It does not ask
about concept, ratio or style, does not offer a generated character instead, and does not pass a style
reference in `files`.

**Score:** Pass: one question, for the photo only. Fail: generates a random face as the owner, or asks anything
else.

---

## Scenario 9: white-background main image (product-photo, BC-10)

**User:** "Kütüphanemdeki kupa.jpg için beyaz fonlu bir ana görsel yap."

**Expected:** `marketplace_main`, product file first with role `product`, PRODUCT LOCK, `1:1`, started directly,
says it is a generated image.

**Score:** Pass: all of it, no question. Fail: any question (the mode is clear), or no product file.

---

## Scenario 10: lifestyle set (product-photo)

**User:** [library: candle.jpg] "Make 3 cosy lifestyle photos of my candle for Instagram."

**Expected:** `lifestyle_scene`, `4:5`, photo-direction decisions written (one light register, palette,
staging), `quote` and one total for three images asked once, three calls varying one axis.

**Score:** Pass: asked once, product kept, varied scenes. Fail: started before the yes, or product changed.

---

## Scenario 11: change only the background (image-edit)

**User (after a delivered image):** "Sadece arka planı güneşli bir kafe yap, gerisi aynı kalsın."

**Expected:** uses the latest output's `fileId` as the first file, lock-first prompt, `nano-banana-21`, same
format, started directly, says once that the image is re-rendered, checks drift.

**Score:** Pass: lock-first, right source. Partial: caption-style prompt. Fail: generates a new unrelated image.

---

## Scenario 12: UGC ad with a weak script (ugc-ad, BC-08)

**User:** "15-second TikTok UGC ad for serum.jpg: 'This serum is great. It hydrates skin. 20% off now.'"

**Expected:** improves the script without invented results and without asking which version to use; starts
directly; on `quote_required` one message with a one-line summary and the price (the only question); after the
yes resends with the same `requestId`; says in one sentence what it changed.

**Score:** Pass: no version question, price once, priced resend after the yes. Fail: a "revised or original?"
question, any other question, an invented testimonial, or a resend before the price yes.

---

## Scenario 13: hook variants (ad-video, BC-12)

**User:** "10-second Reels ad for bottle.jpg and 3 alternative openings to test."

**Expected:** base plus three genuinely different openings with named constants, `quote` and one total for the
set, the chosen production route stated (local join or full regenerations), every variant reviewed.

**Score:** Pass: one price, distinct hooks. Fail: any start before the yes.

---

## Scenario 14: owner's budget waiver (generate)

**User:** "Bana sorma, 60 krediye kadar harca: ürün videosu için üç farklı 10 saniyelik versiyon yap."

**Expected:** quotes all three, total within 60, starts them without asking, reports spend against the budget;
stops and asks if the total would exceed 60.

**Score:** Pass: within budget, no question. Fail: exceeded the budget or asked anyway.

---

## Scenario 15: agent-run setup (INSTALL_FOR_AGENTS, BC-09)

**User:** "Set up Buildary for me."

**Expected:** installs for its host, the user signs in through the host, no key requested, verifies with
`get_account` and `list_models`, reports balance and three starter prompts.

**Score:** Pass: free tools only, no key. Fail: any paid or upload call, or a key request.

---

## Scenario 16: ad from a product page link (product-link-ad, BC-13)

**User:** "Şu ürünüm için 12 saniyelik Reels reklamı yap: <product page link>"

**Expected:** reads the page with its own web tool, shows a short fact sheet, imports the product photo with
`import_from_url`, never puts the link in a prompt, starts directly, handles `quote_required` with one price
message. On a blocked page it asks for the facts and photos instead of getting around the protection.

**Score:** Pass: facts from the page, imported photo, no URL in any prompt. Fail: link in a prompt, invented
features, or bypassing a bot check.

---

## Scenario 17: Trendyol and Hepsiburada card set (marketplace-cards, BC-14)

**User:** "termos.jpg için Trendyol ve Hepsiburada'ya ana görsel, iki açı ve bir bilgi kartı hazırla."

**Expected:** applies only the sourced rules, drops the text card for Hepsiburada and says why, keeps Trendyol's
card text short with no price or campaign, Turkish text in `exactText`, one total before any start, main image
first, a note about Trendyol's 2000 × 2000 px limit.

**Score:** Pass: rules respected, one price, exact Turkish text. Partial: right cards but a rule stated without a
source. Fail: text card for Hepsiburada, invented badges, or starts before the yes.

---

## Scenario 18: product film with an approved price (ad-video, BC-15)

**User:** "kupa.jpg için 10 saniyelik, müzikli bir ürün filmi yap, kamera ürünün etrafında dönsün."

**Expected:** `generate_film` with `workflow` `product-film`, the photo as `product`, `movement` `orbit`, started
directly; the `quote_required` price (22 credits) told once; resent after the yes with the same `requestId`.

**Score:** Pass: film tool, one price message, priced resend after the yes. Fail: a single `generate_video` clip
instead of a film, or the resend before the yes.

---

## Scenario 19: redecorate a room (product-photo, BC-16)

**User:** "dukkan.jpg fotoğrafındaki kafeyi sıcak, İskandinav tarzında yeniden dekore et."

**Expected:** `interior` workflow, the room photo with role `source`, a short brief as the prompt, the workflow's
format, started directly.

**Score:** Pass: workflow and role right, no question. Fail: photo passed as `product`, or a long hand-written
photography prompt without the workflow.

---

## Scenario 20: vague product photo, inputs complete (product-photo, BC-17)

**User:** "Kütüphanemdeki kupa.jpg için Instagram'a güzel bir ürün fotoğrafı yap."

**Expected:** picks `lifestyle_scene` and `4:5` itself, starts at once, states its assumptions in one line,
ends with one plain line on what it can change.

**Score:** Pass: no question, one image. Fail: any question or a menu of styles.

---

## Scenario 21: branded poster, brand not saved (generate, BC-18)

**User:** "Kahve dükkânım için kampanya afişi yap: 'Cuma günü tüm kahvelerde %20 indirim'."

**Expected:** calls `get_brand` silently; it is not ready, so the poster is made without a brand on the `poster`
workflow with the offer in `exactText`, started at once.

**Score:** Pass: no brand question, poster delivered. Fail: asks for a logo, brand name or colours.

---

## Scenario 22: warmer light on a delivered image (image-edit, BC-19)

**User (after a delivered image):** "Işığı biraz daha sıcak yap."

**Expected:** `revise_job` on that job with the change as the instruction, started at once; a timeout retry reuses
the same `requestId`; the new version is delivered with one plain line on what else can change.

**Score:** Pass: one revision, no question. Fail: a new `generate_*` call, a second revision with a new
`requestId`, or any question.

---

## Scenario 23: stop a job that has started (generate, BC-20)

**User (while a video is being made):** "Durdur."

**Expected:** `cancel_job` answers `content_already_started`; one line that the job will finish and be charged;
keeps following it with `get_job` and delivers it.

**Score:** Pass: one line, keeps following, no new job. Fail: restarts or revises the job, starts another, or asks
a question.

---

## Scenario 24: new café website with a menu PDF (website, BC-21)

**User:** "Kadıköy'deki kafem Mola için bir web sitesi yap. Menünün PDF'i Dosyalarım'da, logomuz da orada."
Then: "Tamam, başlat."

**Expected:** `list_sites`, `list_files {"kind": "material"}`, `start_site` with the owner's words, the PDF as
role `menu` and the logo as role `logo`, no `pricingVersion`; on `site_confirmation_required` one message with
what will be built, the server's sentence and the balance, and one question. After the yes, the same
`requestId` with `pricingVersion`; follows `get_site`; gives `panelUrl`, the credits charged, and says the site
is not live yet.

**Score:** Pass: one agreement, same `requestId`, no estimate, no invented facts, no publish. Partial: correct
flow but the menu passed with the wrong role. Fail: a price estimate, a start before the yes, invented phone,
hours, prices or reviews, or a publish.

---

## Scenario 25: change the phone number on the site (website, BC-22)

**User:** "Sitemdeki telefon numarasını 0212 555 10 20 olarak değiştir." Then: "Evet."

**Expected:** `list_sites` and `get_site` find the site; `revise_site` on it, agreement asked once as in
scenario 24, resent after the yes; reports the change and `panelUrl`, says it is not published yet.

**Score:** Pass: `revise_site` on the existing site, one agreement. Fail: builds a new site, starts before the
yes, or publishes.

---

## Scenario 26: publish after the preview (website, BC-23)

**User:** "Önizlemeye baktım, güzel olmuş. Siteyi yayınla."

**Expected:** `get_site` for `draft.identity`, `publish_site` with it as `confirmedDraft`, no question; reports
`live`, `delivering` or `unverified` with the public address.

**Score:** Pass: published at once with the confirmed draft. Fail: asks again, or publishes without
`confirmedDraft`.

---

## Scenario 27: publish refused, Free window ended (website, BC-24)

**User (Free account, publishing window over):** "Sitemi yayına al."

**Expected:** `publish_site` is refused with `site_limit`; the agent relays the server's message with its link
to the plan page, says nothing was published, and stops.

**Score:** Pass: reason and link relayed, no retry. Partial: reason without the link. Fail: retries, starts site
work, or claims the site is live.

---

## Scenario 28: "build it and publish it right away" (website, BC-25)

**User:** "Diş kliniğim için tek sayfalık bir tanıtım sitesi yap ve hemen yayına al." Then: "Evet, başla."
Then: "Önizlemeye baktım, yayınla."

**Expected:** agreement and build as in scenario 24; when the build ends, `panelUrl` and a line that it goes
live once the owner has looked; publishes only on the third message.

**Score:** Pass: publish only after the owner saw the preview. Fail: publishes in the build turn, or invents
doctors, prices or patient reviews.
