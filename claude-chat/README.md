# My Claude — your personal Claude chat website

A small website where **you** chat with Claude and customize how it behaves:

- 💬 **Chat** with streaming answers (text appears live, like claude.ai)
- 🎭 **Customize Claude** — system prompt / persona (with one-click presets)
- 🧠 **Extended thinking** — deeper reasoning with a visible "Thinking" summary
- 🎚 **Model picker** — Opus 4.8 (default), Fable 5, Sonnet 4.6, Haiku 4.5
- ⚡ **Effort control** — low / medium / high / max (depth vs. speed & cost)
- 🌡 **Temperature** — on models that support it (Sonnet / Haiku)
- 🗂 **Multiple conversations**, saved in your browser (localStorage)

The Node server keeps your API key **server-side** and proxies requests to the
Anthropic API — the key is never exposed to the browser.

## 1. Get an API key

1. Go to <https://console.anthropic.com/> and sign in / sign up
2. Open **API Keys** → **Create Key**, and copy the `sk-ant-...` value
3. Note: API usage is paid per token (separate from a claude.ai subscription)

## 2. Run it

```bash
cd claude-chat
npm install

# Option A — key inline
ANTHROPIC_API_KEY=sk-ant-your-key npm start

# Option B — key in a .env file (recommended)
cp .env.example .env     # then edit .env and paste your key
npm run dev
```

Open **http://localhost:3000** — that's your website.

## 3. Customize Claude

Click **⚙ Customize** (top right):

| Setting | What it does |
|---|---|
| **Model** | Which Claude answers. Opus 4.8 = most capable default; Sonnet = faster/cheaper; Haiku = fastest; Fable 5 = Anthropic's most capable (premium pricing, always thinks). |
| **System prompt** | Claude's persona and rules — applies to the whole conversation. Use a preset chip or write your own. |
| **Extended thinking** | Lets Claude reason before answering; you see a collapsible summary. Always on for Fable 5; not available on Haiku. |
| **Effort** | How hard Claude works: `low` → fast & cheap, `max` → most thorough. |
| **Temperature** | Creativity (Sonnet/Haiku only — newer Opus models don't accept it). Ignored while thinking is on. |
| **Max response tokens** | Upper limit on answer length. |

Settings and conversations are saved in your browser automatically.

## Notes & troubleshooting

- **"API key not set" warning** — start the server with `ANTHROPIC_API_KEY` set (see step 2).
- **Fable 5 returns an error on every request** — Fable 5 requires the
  organization to have 30-day data retention enabled; it's also premium-priced.
  Use Opus 4.8 otherwise.
- **"Claude declined this request"** — the API's safety system refused
  (`stop_reason: refusal`); rephrase and try again.
- **Costs** — every message sends the whole conversation history (the API is
  stateless), so very long chats cost more. Start a new chat for new topics.

## Put it on the internet (optional)

This needs a Node host (GitHub Pages won't work — it's static-only):

- **Render / Railway / Fly.io** — create a web service from this folder,
  set the `ANTHROPIC_API_KEY` environment variable, done.
- If you expose it publicly, add authentication first — otherwise anyone who
  finds the URL can chat on your API bill.

## Files

```
claude-chat/
├── server.js          # Node + Express server, streams Claude replies (SSE)
├── public/
│   ├── index.html     # chat + settings UI
│   ├── app.js         # frontend logic (conversations, streaming, settings)
│   └── style.css      # theme
├── package.json
└── .env.example       # template for your API key
```
