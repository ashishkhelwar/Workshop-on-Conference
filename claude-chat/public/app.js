/* My Claude — chat frontend.
 * Conversations + settings persist in localStorage. Each request sends the
 * full message history to /api/chat, which streams the reply back as SSE. */

"use strict";

/* ───────────── State ───────────── */

const STORAGE_KEY = "my-claude-v1";

const DEFAULT_SETTINGS = {
  model: "claude-opus-4-8",
  system: "",
  thinking: true,
  effort: "high",
  tempOn: false,
  temperature: 0.7,
  maxTokens: 64000,
};

const PRESETS = {
  "Friendly tutor":
    "You are a friendly, patient tutor. Explain ideas step by step in simple language, and give one concrete example for every concept. End each answer with a short question to check understanding.",
  "Code expert":
    "You are an expert software engineer. Give working, well-commented code with a brief explanation of the approach. Point out edge cases and pitfalls. Prefer simple, readable solutions over clever ones.",
  "Concise analyst":
    "You are a sharp analyst. Lead with the answer in one or two sentences, then give only the key supporting points as a short bullet list. No filler, no preamble.",
  "Hindi assistant":
    "You are a helpful assistant. Always reply in Hindi (Devanagari script), in a warm and respectful tone. Keep technical terms in English where that is clearer.",
};

const STARTERS = [
  "Explain how the Claude API works, like I'm new to programming.",
  "Help me draft a professional email to reschedule a meeting.",
  "Write a Python script that renames all files in a folder.",
  "Give me a 7-day plan to learn the basics of web development.",
];

let state = loadState();
let modelCaps = {}; // filled from /api/models
let streaming = false;
let abortController = null;

function loadState() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (raw && Array.isArray(raw.conversations)) {
      return {
        conversations: raw.conversations,
        activeId: raw.activeId ?? null,
        settings: { ...DEFAULT_SETTINGS, ...(raw.settings || {}) },
      };
    }
  } catch {
    /* corrupted storage — start fresh */
  }
  return { conversations: [], activeId: null, settings: { ...DEFAULT_SETTINGS } };
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function activeConvo() {
  return state.conversations.find((c) => c.id === state.activeId) ?? null;
}

function newConvo() {
  const convo = {
    id: `c${Date.now().toString(36)}${Math.random().toString(36).slice(2, 7)}`,
    title: "New chat",
    createdAt: Date.now(),
    messages: [], // {role, content, thinking?, meta?}
  };
  state.conversations.unshift(convo);
  state.activeId = convo.id;
  saveState();
  return convo;
}

/* ───────────── DOM handles ───────────── */

const $ = (id) => document.getElementById(id);
const els = {
  sidebar: $("sidebar"),
  convoList: $("convo-list"),
  newChat: $("new-chat"),
  clearAll: $("clear-all"),
  sidebarToggle: $("sidebar-toggle"),
  messages: $("messages"),
  input: $("input"),
  send: $("send"),
  stop: $("stop"),
  modelChip: $("model-chip"),
  modelChipLabel: $("model-chip-label"),
  keyWarning: $("key-warning"),
  openSettings: $("open-settings"),
  closeSettings: $("close-settings"),
  settings: $("settings"),
  setModel: $("set-model"),
  modelNote: $("model-note"),
  presetRow: $("preset-row"),
  setSystem: $("set-system"),
  rowThinking: $("row-thinking"),
  setThinking: $("set-thinking"),
  thinkingNote: $("thinking-note"),
  rowEffort: $("row-effort"),
  setEffort: $("set-effort"),
  rowTemp: $("row-temp"),
  setTempOn: $("set-temp-on"),
  setTemp: $("set-temp"),
  tempValue: $("temp-value"),
  tempNote: $("temp-note"),
  setMaxTokens: $("set-maxtokens"),
  resetSettings: $("reset-settings"),
};

/* ───────────── Rendering helpers ───────────── */

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderMarkdown(text) {
  if (window.marked && window.DOMPurify) {
    return DOMPurify.sanitize(marked.parse(text, { breaks: true }));
  }
  return escapeHtml(text).replace(/\n/g, "<br>");
}

function scrollToBottom() {
  els.messages.scrollTop = els.messages.scrollHeight;
}

function renderConvoList() {
  els.convoList.innerHTML = "";
  for (const convo of state.conversations) {
    const item = document.createElement("div");
    item.className = "convo-item" + (convo.id === state.activeId ? " active" : "");
    const title = document.createElement("span");
    title.className = "convo-title";
    title.textContent = convo.title;
    const del = document.createElement("button");
    del.className = "convo-del";
    del.title = "Delete this chat";
    del.textContent = "✕";
    del.addEventListener("click", (e) => {
      e.stopPropagation();
      if (streaming && convo.id === state.activeId) return;
      state.conversations = state.conversations.filter((c) => c.id !== convo.id);
      if (state.activeId === convo.id) state.activeId = state.conversations[0]?.id ?? null;
      saveState();
      renderConvoList();
      renderMessages();
    });
    item.append(title, del);
    item.addEventListener("click", () => {
      if (streaming) return;
      state.activeId = convo.id;
      saveState();
      renderConvoList();
      renderMessages();
    });
    els.convoList.appendChild(item);
  }
}

function messageRow(role) {
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;
  const label = document.createElement("div");
  label.className = "msg-label";
  label.textContent = role === "user" ? "You" : "Claude";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  row.append(label, bubble);
  return { row, bubble };
}

function thinkingBlock(text, open) {
  const details = document.createElement("details");
  details.className = "thinking";
  if (open) details.open = true;
  const summary = document.createElement("summary");
  summary.textContent = "💭 Thinking";
  const body = document.createElement("div");
  body.className = "thinking-body";
  body.textContent = text;
  details.append(summary, body);
  return details;
}

function metaLine(meta) {
  if (!meta) return null;
  const div = document.createElement("div");
  div.className = "msg-meta";
  const bits = [];
  if (meta.model) bits.push(meta.model);
  if (meta.usage?.input != null) bits.push(`in ${meta.usage.input} tok`);
  if (meta.usage?.output != null) bits.push(`out ${meta.usage.output} tok`);
  if (meta.stop_reason === "max_tokens") bits.push("⚠ cut off at max tokens");
  div.textContent = bits.join(" · ");
  return div;
}

function noticeEl(text) {
  const wrap = document.createElement("div");
  wrap.className = "notice";
  const inner = document.createElement("div");
  inner.className = "notice-inner";
  inner.textContent = text;
  wrap.appendChild(inner);
  return wrap;
}

function renderEmptyState() {
  const wrap = document.createElement("div");
  wrap.id = "empty-state";
  wrap.innerHTML = `
    <h1>Welcome to <em>My Claude</em></h1>
    <p>Your personal Claude — pick a model, give it a persona in <strong>⚙ Customize</strong>, and start chatting.</p>
    <div class="starter-grid"></div>`;
  const grid = wrap.querySelector(".starter-grid");
  for (const text of STARTERS) {
    const btn = document.createElement("button");
    btn.className = "starter";
    btn.textContent = text;
    btn.addEventListener("click", () => {
      els.input.value = text;
      els.input.focus();
      autosize();
    });
    grid.appendChild(btn);
  }
  els.messages.appendChild(wrap);
}

function renderMessages() {
  els.messages.innerHTML = "";
  const convo = activeConvo();
  if (!convo || convo.messages.length === 0) {
    renderEmptyState();
    return;
  }
  for (const msg of convo.messages) {
    const { row, bubble } = messageRow(msg.role);
    if (msg.role === "assistant") {
      if (msg.thinking) row.insertBefore(thinkingBlock(msg.thinking, false), bubble);
      bubble.innerHTML = renderMarkdown(msg.content);
      const meta = metaLine(msg.meta);
      if (meta) row.appendChild(meta);
      if (msg.meta?.stop_reason === "refusal") {
        els.messages.appendChild(row);
        els.messages.appendChild(
          noticeEl("Claude declined this request for safety reasons. Try rephrasing it."),
        );
        continue;
      }
    } else {
      bubble.textContent = msg.content;
    }
    els.messages.appendChild(row);
  }
  scrollToBottom();
}

/* ───────────── Settings panel ───────────── */

function capsFor(modelId) {
  return modelCaps[modelId] ?? { thinking: "optional", effort: true, temperature: true, label: modelId };
}

function applySettingsToUI() {
  const s = state.settings;
  els.setModel.value = s.model;
  els.setSystem.value = s.system;
  els.setThinking.checked = s.thinking;
  els.setEffort.value = s.effort;
  els.setTempOn.checked = s.tempOn;
  els.setTemp.value = String(s.temperature);
  els.setTemp.disabled = !s.tempOn;
  els.tempValue.textContent = Number(s.temperature).toFixed(2);
  els.setMaxTokens.value = String(s.maxTokens);

  const caps = capsFor(s.model);
  els.modelChipLabel.textContent = caps.label || s.model;
  els.modelNote.textContent = caps.note || "";

  // Thinking row
  if (caps.thinking === "none") {
    els.rowThinking.classList.remove("hidden");
    els.setThinking.checked = false;
    els.setThinking.disabled = true;
    els.thinkingNote.textContent = "Not available on this model.";
  } else if (caps.thinking === "always") {
    els.setThinking.checked = true;
    els.setThinking.disabled = true;
    els.thinkingNote.textContent = "Always on for this model — it cannot be switched off.";
  } else {
    els.setThinking.disabled = false;
    els.thinkingNote.textContent = "";
  }

  // Effort row
  els.rowEffort.classList.toggle("hidden", !caps.effort);

  // Temperature row
  if (!caps.temperature) {
    els.rowTemp.classList.add("hidden");
  } else {
    els.rowTemp.classList.remove("hidden");
    const blocked = caps.thinking !== "none" && thinkingEnabledFor(s);
    els.setTempOn.disabled = blocked;
    els.setTemp.disabled = blocked || !s.tempOn;
    els.tempNote.textContent = blocked
      ? "Ignored while extended thinking is on — turn thinking off to use it."
      : "Lower = focused & repeatable, higher = varied & creative.";
  }
}

function thinkingEnabledFor(s) {
  const caps = capsFor(s.model);
  if (caps.thinking === "always") return true;
  if (caps.thinking === "none") return false;
  return Boolean(s.thinking);
}

function bindSettings() {
  els.setModel.addEventListener("change", () => {
    state.settings.model = els.setModel.value;
    saveState();
    applySettingsToUI();
  });
  els.setSystem.addEventListener("input", () => {
    state.settings.system = els.setSystem.value;
    saveState();
  });
  els.setThinking.addEventListener("change", () => {
    state.settings.thinking = els.setThinking.checked;
    saveState();
    applySettingsToUI();
  });
  els.setEffort.addEventListener("change", () => {
    state.settings.effort = els.setEffort.value;
    saveState();
  });
  els.setTempOn.addEventListener("change", () => {
    state.settings.tempOn = els.setTempOn.checked;
    saveState();
    applySettingsToUI();
  });
  els.setTemp.addEventListener("input", () => {
    state.settings.temperature = Number(els.setTemp.value);
    els.tempValue.textContent = Number(els.setTemp.value).toFixed(2);
    saveState();
  });
  els.setMaxTokens.addEventListener("change", () => {
    const v = Number.parseInt(els.setMaxTokens.value, 10);
    state.settings.maxTokens = Number.isFinite(v) ? v : DEFAULT_SETTINGS.maxTokens;
    saveState();
  });
  els.resetSettings.addEventListener("click", () => {
    state.settings = { ...DEFAULT_SETTINGS };
    saveState();
    applySettingsToUI();
  });

  // Persona preset chips
  for (const [name, prompt] of Object.entries(PRESETS)) {
    const chip = document.createElement("button");
    chip.className = "preset-chip";
    chip.textContent = name;
    chip.title = "Fill the system prompt with this persona";
    chip.addEventListener("click", () => {
      els.setSystem.value = prompt;
      state.settings.system = prompt;
      saveState();
    });
    els.presetRow.appendChild(chip);
  }
}

async function loadModels() {
  try {
    const resp = await fetch("/api/models");
    const data = await resp.json();
    els.setModel.innerHTML = "";
    for (const m of data.models) {
      modelCaps[m.id] = m;
      const opt = document.createElement("option");
      opt.value = m.id;
      opt.textContent = `${m.label} — ${m.note}`;
      els.setModel.appendChild(opt);
    }
    if (!modelCaps[state.settings.model]) state.settings.model = data.default;
  } catch {
    /* server not reachable yet — chip will show the raw id */
  }
  applySettingsToUI();
}

async function checkKey() {
  try {
    const resp = await fetch("/api/health");
    const data = await resp.json();
    els.keyWarning.classList.toggle("hidden", Boolean(data.hasKey));
  } catch {
    /* ignore */
  }
}

/* ───────────── Chat streaming ───────────── */

async function readSSE(resp, onEvent) {
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx;
    while ((idx = buf.indexOf("\n\n")) !== -1) {
      const chunk = buf.slice(0, idx);
      buf = buf.slice(idx + 2);
      for (const line of chunk.split("\n")) {
        if (line.startsWith("data: ")) {
          try {
            onEvent(JSON.parse(line.slice(6)));
          } catch {
            /* skip malformed frame */
          }
        }
      }
    }
  }
}

function setStreaming(on) {
  streaming = on;
  els.send.classList.toggle("hidden", on);
  els.stop.classList.toggle("hidden", !on);
  els.input.disabled = on;
}

async function sendMessage() {
  const text = els.input.value.trim();
  if (!text || streaming) return;

  let convo = activeConvo();
  if (!convo) convo = newConvo();

  // First message titles the conversation
  if (convo.messages.length === 0) {
    convo.title = text.length > 42 ? `${text.slice(0, 42)}…` : text;
  }
  convo.messages.push({ role: "user", content: text });
  saveState();
  els.input.value = "";
  autosize();
  renderConvoList();
  renderMessages();

  // Live assistant bubble
  const { row, bubble } = messageRow("assistant");
  bubble.classList.add("streaming");
  els.messages.appendChild(row);
  scrollToBottom();

  let answer = "";
  let thinking = "";
  let thinkingEl = null;
  let doneInfo = null;
  let errorMsg = null;

  const s = state.settings;
  const payload = {
    model: s.model,
    system: s.system,
    thinking: thinkingEnabledFor(s),
    effort: s.effort,
    maxTokens: s.maxTokens,
    messages: convo.messages.map((m) => ({ role: m.role, content: m.content })),
  };
  if (s.tempOn && capsFor(s.model).temperature && !thinkingEnabledFor(s)) {
    payload.temperature = s.temperature;
  }

  abortController = new AbortController();
  setStreaming(true);

  try {
    const resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: abortController.signal,
    });

    const ctype = resp.headers.get("content-type") || "";
    if (!resp.ok || !ctype.includes("text/event-stream")) {
      let msg = `Request failed (${resp.status})`;
      try {
        msg = (await resp.json()).error || msg;
      } catch {
        /* not JSON */
      }
      throw new Error(msg);
    }

    await readSSE(resp, (ev) => {
      if (ev.type === "text") {
        answer += ev.text;
        bubble.innerHTML = renderMarkdown(answer);
        scrollToBottom();
      } else if (ev.type === "thinking") {
        thinking += ev.text;
        if (!thinkingEl) {
          thinkingEl = thinkingBlock("", true);
          row.insertBefore(thinkingEl, bubble);
        }
        thinkingEl.querySelector(".thinking-body").textContent = thinking;
        scrollToBottom();
      } else if (ev.type === "done") {
        doneInfo = ev;
      } else if (ev.type === "error") {
        errorMsg = ev.message;
      }
    });
  } catch (err) {
    if (err.name === "AbortError") {
      if (answer) answer += "\n\n*(stopped)*";
      else errorMsg = "Stopped before any reply arrived.";
    } else {
      errorMsg = err.message || "Could not reach the server. Is it running?";
    }
  } finally {
    abortController = null;
    setStreaming(false);
  }

  bubble.classList.remove("streaming");
  if (thinkingEl) thinkingEl.open = false;

  if (errorMsg && !answer) {
    row.remove();
    els.messages.appendChild(noticeEl(`⚠ ${errorMsg}`));
    scrollToBottom();
    return;
  }

  bubble.innerHTML = renderMarkdown(answer || "*(no text in reply)*");
  const meta = doneInfo
    ? { model: doneInfo.model, usage: doneInfo.usage, stop_reason: doneInfo.stop_reason }
    : null;
  const metaEl = metaLine(meta);
  if (metaEl) row.appendChild(metaEl);

  if (doneInfo?.stop_reason === "refusal") {
    els.messages.appendChild(
      noticeEl("Claude declined this request for safety reasons. Try rephrasing it."),
    );
  }
  if (errorMsg && answer) {
    els.messages.appendChild(noticeEl(`⚠ ${errorMsg}`));
  }

  convo.messages.push({
    role: "assistant",
    content: answer || "(no text in reply)",
    thinking: thinking || undefined,
    meta: meta || undefined,
  });
  saveState();
  scrollToBottom();
  els.input.focus();
}

/* ───────────── Composer & layout ───────────── */

function autosize() {
  els.input.style.height = "auto";
  els.input.style.height = `${Math.min(els.input.scrollHeight, 220)}px`;
}

function bindUI() {
  els.send.addEventListener("click", sendMessage);
  els.stop.addEventListener("click", () => abortController?.abort());
  els.input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  els.input.addEventListener("input", autosize);

  els.newChat.addEventListener("click", () => {
    if (streaming) return;
    newConvo();
    renderConvoList();
    renderMessages();
    els.input.focus();
  });

  els.clearAll.addEventListener("click", () => {
    if (streaming) return;
    if (!confirm("Delete all conversations? This cannot be undone.")) return;
    state.conversations = [];
    state.activeId = null;
    saveState();
    renderConvoList();
    renderMessages();
  });

  els.sidebarToggle.addEventListener("click", () =>
    els.sidebar.classList.toggle("collapsed"),
  );
  els.openSettings.addEventListener("click", () =>
    els.settings.classList.toggle("hidden"),
  );
  els.modelChip.addEventListener("click", () =>
    els.settings.classList.remove("hidden"),
  );
  els.closeSettings.addEventListener("click", () =>
    els.settings.classList.add("hidden"),
  );
}

/* ───────────── Boot ───────────── */

bindUI();
bindSettings();
renderConvoList();
renderMessages();
applySettingsToUI();
loadModels();
checkKey();
els.input.focus();
