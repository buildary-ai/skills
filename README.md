# Buildary skills and plugin

Skills and a plugin that let AI agents make images, videos, ads and websites with
[Buildary](https://buildary.dev) through the Buildary MCP server (`https://buildary.dev/api/agency/mcp`). One
repository installs into Claude Code, Codex, Cursor and any agent that reads [Agent Skills](https://agentskills.io).

The MCP server gives the agent the tools; these skills give it the craft: which model to pick, how to write
the prompt, how to keep a real product exact, how to plan an ad, and how to spend the owner's credits safely.

## Skills

| Skill | What it does |
|---|---|
| [`buildary-generate`](skills/buildary-generate/SKILL.md) | Core: images, videos and Remakes; model choice from the live catalog, prompts, files and uploads, job tracking, the spending rule |
| [`buildary-thumbnail`](skills/buildary-thumbnail/SKILL.md) | Truthful, high-click YouTube thumbnails and vertical covers; face and logo references, variants, text overlay |
| [`buildary-product-photo`](skills/buildary-product-photo/SKILL.md) | Product photos from the owner's real product: studio, marketplace, lifestyle, model, conceptual, banners, ad sets |
| [`buildary-image-edit`](skills/buildary-image-edit/SKILL.md) | Change one thing in an existing image and keep the rest, with lock-first prompts |
| [`buildary-ugc-ad`](skills/buildary-ugc-ad/SKILL.md) | Creator-style UGC ad videos with a real recommendation script and native speech |
| [`buildary-ad-video`](skills/buildary-ad-video/SKILL.md) | Product films, paid-social feed ads and hook variants |
| [`buildary-product-link-ad`](skills/buildary-product-link-ad/SKILL.md) | Ad images or a video from a product page link: the agent reads the page and imports the product photos |
| [`buildary-marketplace-cards`](skills/buildary-marketplace-cards/SKILL.md) | Trendyol, Hepsiburada and Amazon TR listing image sets under each marketplace's official image rules |
| [`buildary-website`](skills/buildary-website/SKILL.md) | Build, change and publish the owner's Buildary websites, with the owner's agreement before every build or change |

## How spending works

Every Buildary job runs on the owner's credits, and the skills follow one rule, enforced by the server:

- **A single job starts directly.** The agent sends it without pricing it first; the server starts it at once
  when it costs 20 credits or less.
- **Over 20 credits,** the server answers `quote_required` with the price. The agent tells the owner that price
  once and, after a yes, sends the same request again with the price attached.
- **Several jobs for one request** (variants, sets, scenes) are priced with the free `quote` tool first; the
  agent tells the owner the total once and starts after a yes.
- When the owner asks what something costs, the agent answers with `quote` and starts nothing.
- A retried request reuses its `requestId`, so a timeout never charges twice.
- The amount reported is the one the start result and `get_job` show for the job.

Hosts such as Claude and ChatGPT may also ask before each paid tool call; that is their own safety prompt.

**Websites are different.** Site work (`start_site`, `revise_site`) has no fixed price: it is charged by use
and stops when the credits run out, keeping and charging what was made. So every build and every change waits
for the owner's agreement: the first call is refused with `site_confirmation_required` and the server's
sentence for the owner; the agent relays it with the balance, asks once, and resends after a yes. The agent
never estimates a site price. Publishing (`publish_site`) costs no credits and happens only when the owner asks
for it after seeing the preview in Buildary.

## Install

Quick start for Claude Code:

```bash
claude plugin marketplace add buildary-ai/skills
claude plugin install buildary@buildary
```

Then run `/mcp` in Claude Code and sign in to Buildary. Other agents (Codex, Cursor, skills.sh, claude.ai)
and manual setups: [INSTALL.md](INSTALL.md). To let your agent do the setup, give it
[INSTALL_FOR_AGENTS.md](INSTALL_FOR_AGENTS.md) or the live page <https://buildary.dev/agent-setup.md>.

Try:

- "Make three lifestyle photos of this product for Instagram."
- "Create a YouTube thumbnail for my video about learning to swim in 30 days."
- "Make a 15-second TikTok UGC ad for this serum."
- "Change only the background of this photo to a sunny café."
- "Build a website for my café; the menu PDF is in my Buildary library."

## Workflows, films, revisions, brand and job history

The skills use Buildary's ready-made jobs as soon as they fit:

- **Image workflows** (`list_workflows`, `workflow` with `look`, `light`, `lens` on `generate_image`):
  `buildary-product-photo` runs product, lifestyle, macro, conceptual, food and interior (the room photo goes
  in with role `source`); `buildary-thumbnail` runs `cover`; `buildary-generate` runs poster, portrait and
  illustration. The server writes the photography; the price does not change.
- **Films** (`generate_film`, workflows `cinema` and `product-film`, with `movement`): a director scripts,
  shoots and edits a 5, 10 or 15 second film with music. Used by `buildary-ad-video` and
  `buildary-product-link-ad`. A 5-second film (17 credits) starts directly; 10 and 15 seconds wait for the
  owner's approval of the price. "Fotoğrafa hareket" stays on `generate_video` with a `start_frame`.
- **Brand** (`get_brand`): name, colours, tone and the logo file for on-brand work.
- **Job history** (`list_jobs`): recent jobs and the status of up to 20 jobs in one call, without waiting.
- **Result cards** (`show_results`): when a job or a whole set is ready, the skills call it once and Claude and
  ChatGPT show the images and videos as a card in the chat; other clients get the same links.
- **Revisions** (`revise_job`): "change X" retouches a finished image in place or remakes a video with the
  change; "again" (`regenerate`) makes a fresh take of the same request. Same 20-credit rule. Used by
  `buildary-generate`, `buildary-image-edit` and `buildary-thumbnail`.
- **Stopping** (`cancel_job`): a job still waiting in the queue stops for free; one already being made finishes
  and is charged.
- **Websites** (`list_sites`, `get_site`, `start_site`, `revise_site`, `publish_site`): `buildary-website` reads
  the owner's sites, builds or changes one after their agreement, follows the build, gives the preview link
  (`panelUrl`) and publishes on request. The site's own files (images, a PDF menu, texts) come from
  `list_files {"kind": "material"}`. A refused publish is relayed with its reason and the Buildary page that
  fixes it.

The "/" commands come from the skills in this package; the server has no MCP prompts or waiting tool. Buildary
is listed in the MCP Registry as `dev.buildary/mcp`.

## What is in this repository

```
.claude-plugin/        Claude Code plugin + marketplace
.codex-plugin/         Codex plugin
.agents/plugins/       Codex marketplace
.cursor-plugin/        Cursor plugin + MCP config
plugin.json, mcp.json  Agent Plugins (portable format)
.mcp.json              MCP config for Claude Code and Codex
skills/                the skills; each folder installs on its own
evals/                 test scenarios and machine-checked eval cases (not shipped to users)
scripts/               validators, version bump, tool-contract snapshot
contracts/             snapshot of the live Buildary tool list the skills are checked against
```

Maintainers: read [.claude/CLAUDE.md](.claude/CLAUDE.md) before changing a skill.

## Licence

MIT, see [LICENSE](LICENSE).

## Türkçe

Bu depo, yapay zekâ ajanlarının Buildary ile görsel, video, reklam ve web sitesi üretmesini sağlayan skill'leri
ve eklentiyi içerir. Claude Code, Codex, Cursor ve Agent Skills okuyan her ajana tek depodan kurulur. MCP sunucusu
araçları verir; skill'ler ise işin ustalığını verir: hangi model, nasıl prompt, ürün nasıl birebir korunur,
reklam nasıl planlanır, kredi nasıl güvenle harcanır.

**Skill'ler:** `buildary-generate` (temel: görsel, video, Remake, model seçimi, dosya yükleme, iş takibi,
harcama kuralı), `buildary-thumbnail` (YouTube kapağı ve dikey kapak), `buildary-product-photo` (gerçek
üründen ürün fotoğrafı: stüdyo, beyaz fon, yaşam içinde, manken, kampanya), `buildary-image-edit` (görselde
tek şeyi değiştir, gerisi aynı kalsın), `buildary-ugc-ad` (içerik üreticisi tarzı UGC reklam videosu),
`buildary-ad-video` (ürün filmi, Reels/TikTok reklamı, farklı açılış varyantları), `buildary-product-link-ad`
(ürün sayfası linkinden reklam görseli ya da videosu; sayfayı ajan okur), `buildary-marketplace-cards`
(Trendyol, Hepsiburada ve Amazon TR için resmî görsel kurallarına uygun ilan görselleri), `buildary-website`
(sahibin Buildary sitelerini kurar, değiştirir ve isteyince yayınlar).

**Harcama kuralı:** Tek iş doğrudan başlatılır, önceden fiyat sorulmaz; sunucu 20 krediye kadar işi hemen
başlatır. 20 krediyi aşan işi sunucu `quote_required` ile reddedip fiyatı verir; ajan bu fiyatı sahibe bir kez
söyler, onay alınca aynı `requestId` ile fiyatı ekleyerek yeniden gönderir. Birden çok iş (varyant, set, sahne)
önce ücretsiz `quote` ile fiyatlanır, toplam bir kez söylenir. Yeniden denemede aynı `requestId` kullanılır,
iki kez ücret alınmaz. Bildirilen tutar, başlatma yanıtının ve `get_job`'ın gösterdiği tutardır.

**Web siteleri:** Site işinin sabit fiyatı yoktur; kullanıldıkça kredi düşer, kredi biterse durur ve o ana kadar
yapılan ücretlenir. Bu yüzden her kurulum ve her değişiklik sahibin onayını bekler: ilk çağrı
`site_confirmation_required` ile reddedilir, ajan sunucunun cümlesini ve bakiyeyi aktarıp bir kez sorar, onay
gelince aynı `requestId` ile yeniden gönderir. Ajan site için fiyat tahmini vermez. Yayın (`publish_site`)
kredi harcamaz ve yalnız sahip önizlemeyi görüp açıkça "yayınla" dediğinde yapılır; yayın reddedilirse
sunucunun söylediği neden ve düzeltme bağlantısı aynen iletilir. Sitenin dosyaları (görsel, PDF menü, metin)
`list_files {"kind": "material"}` ile bulunur.

**Kurulum (Claude Code):** `claude plugin marketplace add buildary-ai/skills`, ardından
`claude plugin install buildary@buildary`, sonra Claude Code içinde `/mcp` ile Buildary hesabına giriş.
Diğer ajanlar için [INSTALL.md](INSTALL.md); kurulumu ajana yaptırmak için
[INSTALL_FOR_AGENTS.md](INSTALL_FOR_AGENTS.md) ya da <https://buildary.dev/agent-setup.md>.

Ajanlar kullanıcıya her zaman kendi dilinde (Türkçe ya da İngilizce) yanıt verir.

**İş akışları ve film:** `buildary-product-photo` ürün, yaşam içinde, detay, yaratıcı, yemek ve mekân iş
akışlarını (mekân fotoğrafı `source` rolüyle), `buildary-thumbnail` `cover` iş akışını, `buildary-generate`
afiş, portre ve illüstrasyonu kullanır. `buildary-ad-video` ve `buildary-product-link-ad` çok sahneli müzikli
film için `generate_film`'i (`cinema`, `product-film`) kullanır; 5 saniyelik film sormadan başlar, 10 ve 15
saniyelik film fiyat onayı bekler. Marka için `get_brand`, iş geçmişi ve toplu durum için `list_jobs`.
Düzeltme istekleri `revise_job` ile yapılır: görsel yerinde rötuşlanır, "yeniden üret" aynı isteğin yeni
denemesidir; 20 kredi kuralı burada da geçerli. `cancel_job` yalnız henüz başlamamış işi ücretsiz durdurur.
