# Install for agents

You are an AI agent. The user asked you to set up Buildary. Follow these steps exactly. They add the skills
in this repository to Buildary's own setup page, <https://buildary.dev/agent-setup.md>, which covers the MCP
connection for more clients; when a client is missing here, follow that page for the connection, then come
back for the skills (step 2).

## Rules for the whole setup

- **Never ask for, read, print, log or store an API key or token.** Sign-in happens in the user's browser
  through the host's MCP login. If the host needs a key, tell the user where to create it (Buildary ›
  Ayarlar › Giriş ve güvenlik › API anahtarları) and to set it themselves as `BUILDARY_API_KEY`; never ask
  them to paste it into the chat.
- **Spend nothing and publish nothing.** Do not call `generate_image`, `generate_video`, `generate_film`,
  `remake_video`, `revise_job`, `start_site`, `revise_site`, `publish_site`, `create_upload` or
  `import_from_url` during setup. Verification uses only the free tools `get_account` and `list_models`.
- Do not edit files outside the agent's own configuration and skills folders.

## Step 1: find the host

| You are | Do |
|---|---|
| Claude Code | Step 2a |
| Codex | Step 2b |
| Cursor | Step 2c |
| Another agent with a shell | Step 2d |
| A chat app (claude.ai, Claude Desktop, ChatGPT) | You cannot install anything. Give the user the steps from `INSTALL.md` for their app and stop |

## Step 2a: Claude Code

```bash
claude plugin marketplace add buildary-ai/skills
claude plugin install buildary@buildary
```

If the plugin commands are unavailable:

```bash
claude mcp add --transport http buildary https://buildary.dev/api/agency/mcp
npx skills add buildary-ai/skills -y
```

Ask the user to restart Claude Code, run `/mcp`, choose `buildary` and sign in, then tell you when done.

## Step 2b: Codex

```bash
codex plugin marketplace add buildary-ai/skills
codex plugin add buildary@buildary
codex mcp login buildary
```

`codex mcp login` opens the browser; wait for the user to finish.

## Step 2c: Cursor

Add the server to `~/.cursor/mcp.json` without removing existing entries:

```json
{ "mcpServers": { "buildary": { "url": "https://buildary.dev/api/agency/mcp" } } }
```

Then `npx skills add buildary-ai/skills -y`. Ask the user to sign in when Cursor prompts.

## Step 2d: other agents

Add an MCP server named `buildary` with transport streamable HTTP and URL
`https://buildary.dev/api/agency/mcp` (OAuth sign-in), then `npx skills add buildary-ai/skills -y`.

## Step 3: verify (free)

1. Call `get_account`. Expect `balanceCredits`, `runningJobs`, `maxRunningJobs`.
2. Call `list_models`. Expect video models, `remake` and `image.models`.

If a call fails:
- 401 or "not connected": the sign-in did not finish; repeat the host's login step.
- The tools are missing: the host has not reloaded; ask the user to restart the agent.
- Network error: the user's connection or a sandbox blocks `buildary.dev`.

## Step 4: report

Tell the user, in their language, in two or three lines: Buildary is connected, their balance, and three
things to try:

- "Make three lifestyle photos of this product for Instagram."
- "Create a YouTube thumbnail for my video."
- "Make a 15-second UGC ad for this product."

Mention once that a job at or under 20 credits starts right away and anything larger is priced for their
approval first, and that a website is built or changed only after they agree. Do not explain skill paths or
file layout.
