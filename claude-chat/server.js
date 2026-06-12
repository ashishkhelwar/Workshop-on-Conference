/**
 * My Claude — personal chat server.
 *
 * Serves the static UI from ./public and proxies chat requests to the
 * Anthropic API with streaming (SSE). The API key stays server-side:
 * set ANTHROPIC_API_KEY in the environment — it is never sent to the browser.
 *
 * Run:  ANTHROPIC_API_KEY=sk-ant-... npm start
 *  or:  node --env-file=.env server.js   (put the key in a .env file)
 */
import path from "node:path";
import { fileURLToPath } from "node:url";
import express from "express";
import Anthropic from "@anthropic-ai/sdk";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3000;
const DEFAULT_MODEL = "claude-opus-4-8";

/**
 * Capability map — which knobs each model accepts.
 *  - temperature was removed on Fable 5 / Opus 4.8: the API returns 400 if sent
 *  - the effort parameter errors on Haiku 4.5
 *  - Fable 5 always thinks (adaptive); thinking cannot be disabled there
 */
const MODELS = {
  "claude-opus-4-8": {
    label: "Claude Opus 4.8",
    note: "Most capable Opus — recommended default",
    thinking: "optional",
    effort: true,
    temperature: false,
    maxOutput: 128000,
  },
  "claude-fable-5": {
    label: "Claude Fable 5",
    note: "Anthropic's most capable model — always thinks; premium pricing",
    thinking: "always",
    effort: true,
    temperature: false,
    maxOutput: 128000,
  },
  "claude-sonnet-4-6": {
    label: "Claude Sonnet 4.6",
    note: "Best speed / intelligence balance",
    thinking: "optional",
    effort: true,
    temperature: true,
    maxOutput: 64000,
  },
  "claude-haiku-4-5": {
    label: "Claude Haiku 4.5",
    note: "Fastest and cheapest for simple tasks",
    thinking: "none",
    effort: false,
    temperature: true,
    maxOutput: 64000,
  },
};

const app = express();
app.use(express.json({ limit: "2mb" }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/api/health", (_req, res) => {
  res.json({ ok: true, hasKey: Boolean(process.env.ANTHROPIC_API_KEY) });
});

app.get("/api/models", (_req, res) => {
  res.json({
    default: DEFAULT_MODEL,
    models: Object.entries(MODELS).map(([id, m]) => ({ id, ...m })),
  });
});

const clamp = (n, lo, hi) => Math.min(Math.max(n, lo), hi);

/** Build a Messages API request from the browser payload, applying per-model rules. */
function buildParams(body) {
  const model = MODELS[body.model] ? body.model : DEFAULT_MODEL;
  const caps = MODELS[model];

  const messages = (Array.isArray(body.messages) ? body.messages : [])
    .filter(
      (m) =>
        (m.role === "user" || m.role === "assistant") &&
        typeof m.content === "string" &&
        m.content.trim().length > 0,
    )
    .map((m) => ({ role: m.role, content: m.content }));
  if (messages.length === 0) throw new Error("No messages to send.");

  const requested = Number.parseInt(body.maxTokens, 10);
  const maxTokens = clamp(
    Number.isFinite(requested) ? requested : 64000,
    256,
    caps.maxOutput,
  );

  const params = { model, max_tokens: maxTokens, messages };

  const system = typeof body.system === "string" ? body.system.trim() : "";
  if (system) params.system = system;

  // Thinking: adaptive only (budget_tokens is removed on these models).
  // display:"summarized" opts back into readable reasoning summaries.
  const wantThinking = caps.thinking === "always" || (caps.thinking === "optional" && body.thinking);
  if (wantThinking) params.thinking = { type: "adaptive", display: "summarized" };

  if (caps.effort && ["low", "medium", "high", "max"].includes(body.effort)) {
    params.output_config = { effort: body.effort };
  }

  // Temperature only where the model accepts it, and never alongside thinking.
  if (
    caps.temperature &&
    !wantThinking &&
    typeof body.temperature === "number" &&
    body.temperature >= 0 &&
    body.temperature <= 1
  ) {
    params.temperature = body.temperature;
  }

  return params;
}

function friendlyError(err) {
  if (err instanceof Anthropic.AuthenticationError)
    return "Invalid API key. Check ANTHROPIC_API_KEY on the server.";
  if (err instanceof Anthropic.PermissionDeniedError)
    return "Your API key doesn't have access to this model.";
  if (err instanceof Anthropic.NotFoundError)
    return "Model not found — it may not be available to your account.";
  if (err instanceof Anthropic.RateLimitError)
    return "Rate limited by the API. Wait a moment and try again.";
  if (err instanceof Anthropic.BadRequestError)
    return `The API rejected the request: ${err.message}`;
  if (err instanceof Anthropic.APIError)
    return `API error ${err.status ?? ""}: ${err.message}`;
  return err?.message || "Unexpected server error.";
}

app.post("/api/chat", async (req, res) => {
  if (!process.env.ANTHROPIC_API_KEY) {
    res.status(500).json({
      error:
        "ANTHROPIC_API_KEY is not set on the server. Start it with: ANTHROPIC_API_KEY=sk-ant-... npm start",
    });
    return;
  }

  let params;
  try {
    params = buildParams(req.body ?? {});
  } catch (err) {
    res.status(400).json({ error: err.message });
    return;
  }

  // Stream the answer to the browser as Server-Sent Events.
  res.setHeader("Content-Type", "text/event-stream; charset=utf-8");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.setHeader("X-Accel-Buffering", "no");
  res.flushHeaders();
  const send = (obj) => res.write(`data: ${JSON.stringify(obj)}\n\n`);

  const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env
  const stream = client.messages.stream(params);

  // If the browser disconnects (or hits Stop), cancel the upstream request.
  // Note: watch res, not req — req's "close" fires once the request body is
  // fully received (Node 16+), which would abort the stream immediately.
  res.on("close", () => {
    if (res.writableEnded) return; // response finished normally
    try {
      stream.controller.abort();
    } catch {
      /* already finished */
    }
  });

  try {
    for await (const event of stream) {
      if (event.type === "content_block_delta") {
        if (event.delta.type === "text_delta") {
          send({ type: "text", text: event.delta.text });
        } else if (event.delta.type === "thinking_delta" && event.delta.thinking) {
          send({ type: "thinking", text: event.delta.thinking });
        }
      }
    }
    const final = await stream.finalMessage();
    send({
      type: "done",
      model: final.model,
      stop_reason: final.stop_reason,
      stop_details: final.stop_details ?? null,
      usage: {
        input: final.usage?.input_tokens ?? null,
        output: final.usage?.output_tokens ?? null,
      },
    });
  } catch (err) {
    if (err instanceof Anthropic.APIUserAbortError || err?.name === "AbortError") {
      // Client hit Stop — nothing more to send.
    } else {
      console.error("[chat]", err);
      send({ type: "error", message: friendlyError(err) });
    }
  } finally {
    res.end();
  }
});

app.listen(PORT, () => {
  console.log(`My Claude is running →  http://localhost:${PORT}`);
  if (!process.env.ANTHROPIC_API_KEY) {
    console.warn(
      "⚠  ANTHROPIC_API_KEY is not set — the UI will load, but chat requests will fail.\n" +
        "   Get a key at https://console.anthropic.com/ and restart with:\n" +
        "   ANTHROPIC_API_KEY=sk-ant-... npm start",
    );
  }
});
