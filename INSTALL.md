# Install

Two parts: the **Buildary MCP connection** (the tools; you sign in with your Buildary account) and the
**skills** (the know-how). The plugin installs both. Pick your agent below.

MCP address: `https://buildary.dev/api/agency/mcp`

## Claude Code

Plugin (MCP + skills, updates with the plugin version):

```bash
claude plugin marketplace add buildary-ai/skills
claude plugin install buildary@buildary
```

Restart Claude Code, run `/mcp`, choose `buildary` and sign in. Skills are then available as
`/buildary:buildary-generate`, `/buildary:buildary-thumbnail` and so on, and load on their own when a request
matches.

Without the plugin:

```bash
claude mcp add --transport http buildary https://buildary.dev/api/agency/mcp
npx skills add buildary-ai/skills
```

## Codex

```bash
codex plugin marketplace add buildary-ai/skills
codex plugin add buildary@buildary
codex mcp login buildary
```

## Cursor

From the Cursor marketplace once Buildary is listed, or by hand: add to `~/.cursor/mcp.json`

```json
{ "mcpServers": { "buildary": { "url": "https://buildary.dev/api/agency/mcp" } } }
```

then `npx skills add buildary-ai/skills` and sign in when Cursor asks.

## Any agent that reads Agent Skills (skills.sh)

```bash
npx skills add buildary-ai/skills                         # all skills
npx skills add buildary-ai/skills --skill buildary-thumbnail   # one skill
```

The skills need the Buildary MCP connected in the same agent.

## claude.ai, Claude Desktop

Settings › Connectors › Add custom connector: name `Buildary`, URL `https://buildary.dev/api/agency/mcp`,
then sign in. To add the skills, add this repository as a plugin marketplace where your plan offers it
(`buildary-ai/skills`). In chat apps a file attached to the conversation cannot be passed to Buildary: share
a direct image link, or put the file in your Buildary library (Dosyalarım) first.

## ChatGPT

Add a custom app or connector with the MCP address (developer mode) and sign in. The skills are not loaded in
ChatGPT; the Buildary server's own instructions apply.

## Headless or CI agents (API key)

Where a browser sign-in is impossible, create a key in Buildary under **Ayarlar › Giriş ve güvenlik › API
anahtarları** (shown once) and send it as a header:

```bash
claude mcp add --transport http buildary https://buildary.dev/api/agency/mcp \
  --header "Authorization: Bearer $BUILDARY_API_KEY"
```

Whoever holds the key can spend your credits. Keep it in an environment variable or a secret store, never in
a repository or a chat.

## Check the connection (free)

Ask your agent: "What is my Buildary balance, and which video models can I use?" It should call
`get_account` and `list_models`; neither charges anything.

## Update

Claude Code and Codex update an installed plugin when its `version` changes. `npx skills add` again
refreshes copied skills.
