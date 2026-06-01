/* ============================================================
   INLINE ELEMENT EDITOR — click any element to inspect & edit
   ============================================================ */
(function () {
  'use strict';

  let active = false;       // selection mode on/off
  let hoveredEl = null;
  let selectedEl = null;
  let inlineEditing = false;
  let origStyles = {};      // stored per-element overrides for reset
  const IGNORE = new Set(['HTML','BODY','SCRIPT','STYLE','LINK','META','HEAD']);

  // ── Helpers ───────────────────────────────────────────────
  function rgbToHex(rgb) {
    if (!rgb || rgb === 'transparent') return '#000000';
    const m = rgb.match(/\d+/g);
    if (!m || m.length < 3) return '#000000';
    return '#' + [m[0], m[1], m[2]].map(n => (+n).toString(16).padStart(2,'0')).join('');
  }

  function px(v) { return Math.round(parseFloat(v) || 0); }

  function getKey(el) {
    // unique-ish key for storing overrides
    return el.id || (el.className ? el.className.toString().trim().split(/\s+/)[0] : '') + '_' + el.tagName;
  }

  // ── Find best target: skip wrappers that are too large ──
  function findTarget(el) {
    if (!el) return null;
    let cur = el;
    while (cur && cur !== document.body) {
      if (IGNORE.has(cur.tagName)) return null;
      // skip the nav bar, the panel itself, and overlay
      if (cur.id === 'ie-panel' || cur.id === 'cfg-panel' || cur.id === 'cfg-overlay') return null;
      if (cur.classList.contains('nav')) return null;
      // accept .slide children but not the .slide itself
      if (cur.classList.contains('slide')) return null;
      // good target
      return cur;
    }
    return null;
  }

  // ── Selection ─────────────────────────────────────────────
  function clearHover() {
    if (hoveredEl) { hoveredEl.classList.remove('ie-hover'); hoveredEl = null; }
  }

  function deselect() {
    stopInline();
    if (selectedEl) {
      selectedEl.classList.remove('ie-selected');
      selectedEl = null;
    }
    panel.classList.remove('open');
  }

  function ieSelect(el) {
    if (!active) return;
    if (selectedEl === el) return;
    deselect();
    selectedEl = el;
    selectedEl.classList.add('ie-selected');
    buildPanel(el);
    panel.classList.add('open');
  }

  // ── Inline contenteditable ────────────────────────────────
  function startInline() {
    if (!selectedEl) return;
    stopInline();
    inlineEditing = true;
    selectedEl.contentEditable = 'true';
    selectedEl.classList.remove('ie-selected');
    selectedEl.classList.add('ie-editing');
    selectedEl.focus();
    inlineBtn.classList.add('active');
    inlineBtn.textContent = '✓ Done Editing';
  }

  function stopInline() {
    if (!inlineEditing || !selectedEl) return;
    inlineEditing = false;
    selectedEl.contentEditable = 'false';
    selectedEl.classList.remove('ie-editing');
    selectedEl.classList.add('ie-selected');
    inlineBtn.classList.remove('active');
    inlineBtn.textContent = '✎ Edit Text Inline';
    // sync textarea
    const ta = document.getElementById('ie-text-area');
    if (ta) ta.value = selectedEl.innerText;
  }

  // ── Apply style helpers ───────────────────────────────────
  function applyProp(el, prop, value) {
    if (!el) return;
    el.style[prop] = value;
  }

  function readComputed(prop) {
    if (!selectedEl) return '';
    return getComputedStyle(selectedEl)[prop] || '';
  }

  // ── Build inspector panel ─────────────────────────────────
  function buildPanel(el) {
    const cs = getComputedStyle(el);
    const tag = el.tagName.toLowerCase() + (el.id ? '#'+el.id : '') +
                (el.className && typeof el.className === 'string' ? '.'+el.className.trim().split(/\s+/)[0] : '');

    panelTag.textContent = tag;

    const textContent = el.innerText || '';
    const fontSize    = px(cs.fontSize);
    const fontWeight  = cs.fontWeight;
    const textAlign   = cs.textAlign;
    const color       = rgbToHex(cs.color);
    const bg          = rgbToHex(cs.backgroundColor);
    const radius      = px(cs.borderRadius);
    const padT        = px(cs.paddingTop);
    const padR        = px(cs.paddingRight);
    const padB        = px(cs.paddingBottom);
    const padL        = px(cs.paddingLeft);
    const letterSp    = parseFloat(cs.letterSpacing).toFixed(1);
    const lineH       = parseFloat(cs.lineHeight).toFixed(1);

    panelBody.innerHTML = `
      <!-- TEXT CONTENT -->
      <div class="ie-section">
        <div class="ie-section-title">Text Content</div>
        <textarea id="ie-text-area" rows="3" placeholder="Element text…">${escH(textContent)}</textarea>
        <button id="ie-inline-btn">✎ Edit Text Inline</button>
      </div>

      <!-- TYPOGRAPHY -->
      <div class="ie-section">
        <div class="ie-section-title">Typography</div>
        <div class="ie-row" style="margin-bottom:8px">
          <span class="ie-lbl">Font Size</span>
          <div class="ie-stepper">
            <button class="ie-step-btn" onclick="ieStep(-1)">−</button>
            <span class="ie-step-val" id="ie-fs-val">${fontSize}px</span>
            <button class="ie-step-btn" onclick="ieStep(1)">+</button>
          </div>
        </div>
        <div style="margin-bottom:7px">
          <span class="ie-lbl">Font Weight</span>
          <div class="ie-toggle-row" style="margin-top:5px">
            <button class="ie-tog ${fontWeight<500?'on':''}" onclick="ieFwt(this,'400')">Regular</button>
            <button class="ie-tog ${fontWeight>=500&&fontWeight<700?'on':''}" onclick="ieFwt(this,'600')">Semi</button>
            <button class="ie-tog ${fontWeight>=700?'on':''}" onclick="ieFwt(this,'700')">Bold</button>
          </div>
        </div>
        <div style="margin-bottom:7px">
          <span class="ie-lbl">Align</span>
          <div class="ie-toggle-row" style="margin-top:5px">
            <button class="ie-tog ${textAlign==='left'?'on':''}" onclick="ieAlign(this,'left')">Left</button>
            <button class="ie-tog ${textAlign==='center'?'on':''}" onclick="ieAlign(this,'center')">Ctr</button>
            <button class="ie-tog ${textAlign==='right'?'on':''}" onclick="ieAlign(this,'right')">Right</button>
          </div>
        </div>
        <div class="ie-range-row">
          <span class="ie-rng-lbl">Letter Spacing</span>
          <span class="ie-rng-val" id="ie-ls-val">${letterSp}px</span>
        </div>
        <input class="ie-rng" type="range" id="ie-ls-rng" min="-2" max="10" step="0.5" value="${letterSp}"
          oninput="ieLs(this)">
        <div class="ie-range-row">
          <span class="ie-rng-lbl">Line Height</span>
          <span class="ie-rng-val" id="ie-lh-val">${lineH}px</span>
        </div>
        <input class="ie-rng" type="range" id="ie-lh-rng" min="8" max="80" step="1" value="${lineH}"
          oninput="ieLh(this)">
      </div>

      <!-- COLORS -->
      <div class="ie-section">
        <div class="ie-section-title">Colors</div>
        <div class="ie-row" style="margin-bottom:8px">
          <span class="ie-lbl">Text Color</span>
          <div class="ie-clr-row">
            <input type="color" class="ie-clr-sw" id="ie-clr-text-sw" value="${color}"
              oninput="ieColor(this,'color')">
            <input type="text" class="ie-inp ie-clr-hex" id="ie-clr-text-hex" maxlength="7" value="${color}"
              oninput="ieSyncClr(this,'ie-clr-text-sw','color')">
          </div>
        </div>
        <div class="ie-row">
          <span class="ie-lbl">Background</span>
          <div class="ie-clr-row">
            <input type="color" class="ie-clr-sw" id="ie-clr-bg-sw" value="${bg}"
              oninput="ieColor(this,'backgroundColor')">
            <input type="text" class="ie-inp ie-clr-hex" id="ie-clr-bg-hex" maxlength="7" value="${bg}"
              oninput="ieSyncClr(this,'ie-clr-bg-sw','backgroundColor')">
          </div>
        </div>
      </div>

      <!-- SPACING & SHAPE -->
      <div class="ie-section">
        <div class="ie-section-title">Spacing & Shape</div>
        <div class="ie-range-row">
          <span class="ie-rng-lbl">Border Radius</span>
          <span class="ie-rng-val" id="ie-r-val">${radius}px</span>
        </div>
        <input class="ie-rng" type="range" id="ie-r-rng" min="0" max="60" step="1" value="${radius}"
          oninput="ieRadius(this)">
        <div style="margin-top:6px">
          <span class="ie-lbl" style="display:block;margin-bottom:6px">Padding (T / R / B / L)</span>
          <div class="ie-row-3" style="grid-template-columns:1fr 1fr 1fr 1fr;gap:5px">
            <input type="number" class="ie-inp ie-inp-num" id="ie-pad-t" value="${padT}" min="0"
              oninput="iePad()">
            <input type="number" class="ie-inp ie-inp-num" id="ie-pad-r" value="${padR}" min="0"
              oninput="iePad()">
            <input type="number" class="ie-inp ie-inp-num" id="ie-pad-b" value="${padB}" min="0"
              oninput="iePad()">
            <input type="number" class="ie-inp ie-inp-num" id="ie-pad-l" value="${padL}" min="0"
              oninput="iePad()">
          </div>
        </div>
      </div>

      <!-- RESET -->
      <div class="ie-actions">
        <button class="ie-reset-btn" onclick="ieResetEl()">↺ Reset Element</button>
      </div>
    `;

    // wire up text area
    document.getElementById('ie-text-area').addEventListener('input', function () {
      if (selectedEl) selectedEl.innerText = this.value;
    });

    // wire up inline-edit button
    inlineBtn = document.getElementById('ie-inline-btn');
    inlineBtn.addEventListener('click', function () {
      if (inlineEditing) stopInline(); else startInline();
    });
  }

  function escH(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  // ── Global inspector action functions ─────────────────────
  window.ieStep = function (dir) {
    if (!selectedEl) return;
    const cs  = getComputedStyle(selectedEl);
    const cur = px(cs.fontSize);
    const nv  = Math.max(8, cur + dir);
    applyProp(selectedEl, 'fontSize', nv + 'px');
    const v = document.getElementById('ie-fs-val');
    if (v) v.textContent = nv + 'px';
  };

  window.ieFwt = function (btn, val) {
    if (!selectedEl) return;
    applyProp(selectedEl, 'fontWeight', val);
    btn.closest('.ie-toggle-row').querySelectorAll('.ie-tog').forEach(b => b.classList.remove('on'));
    btn.classList.add('on');
  };

  window.ieAlign = function (btn, val) {
    if (!selectedEl) return;
    applyProp(selectedEl, 'textAlign', val);
    btn.closest('.ie-toggle-row').querySelectorAll('.ie-tog').forEach(b => b.classList.remove('on'));
    btn.classList.add('on');
  };

  window.ieLs = function (rng) {
    if (!selectedEl) return;
    applyProp(selectedEl, 'letterSpacing', rng.value + 'px');
    const v = document.getElementById('ie-ls-val');
    if (v) v.textContent = rng.value + 'px';
  };

  window.ieLh = function (rng) {
    if (!selectedEl) return;
    applyProp(selectedEl, 'lineHeight', rng.value + 'px');
    const v = document.getElementById('ie-lh-val');
    if (v) v.textContent = rng.value + 'px';
  };

  window.ieColor = function (sw, prop) {
    if (!selectedEl) return;
    applyProp(selectedEl, prop, sw.value);
    const hexId = sw.id.replace('-sw', '-hex');
    const hexEl = document.getElementById(hexId);
    if (hexEl) hexEl.value = sw.value;
  };

  window.ieSyncClr = function (hexEl, swId, prop) {
    const v = hexEl.value.trim();
    if (!/^#[0-9a-fA-F]{6}$/.test(v)) return;
    const sw = document.getElementById(swId);
    if (sw) sw.value = v;
    if (selectedEl) applyProp(selectedEl, prop, v);
  };

  window.ieRadius = function (rng) {
    if (!selectedEl) return;
    applyProp(selectedEl, 'borderRadius', rng.value + 'px');
    const v = document.getElementById('ie-r-val');
    if (v) v.textContent = rng.value + 'px';
  };

  window.iePad = function () {
    if (!selectedEl) return;
    const t = document.getElementById('ie-pad-t').value || 0;
    const r = document.getElementById('ie-pad-r').value || 0;
    const b = document.getElementById('ie-pad-b').value || 0;
    const l = document.getElementById('ie-pad-l').value || 0;
    applyProp(selectedEl, 'padding', `${t}px ${r}px ${b}px ${l}px`);
  };

  window.ieResetEl = function () {
    if (!selectedEl) return;
    selectedEl.removeAttribute('style');
    buildPanel(selectedEl);
  };

  // ── Toggle selection mode ─────────────────────────────────
  window.ieToggle = function () {
    active = !active;
    toggleBtn.classList.toggle('on', active);
    bar.classList.toggle('on', active);
    document.body.style.cursor = active ? 'crosshair' : '';
    if (!active) deselect();
  };

  // ── Event handlers ────────────────────────────────────────
  function onMove(e) {
    if (!active) return;
    const el = findTarget(e.target);
    if (el === hoveredEl) return;
    clearHover();
    if (el && el !== selectedEl) {
      el.classList.add('ie-hover');
      hoveredEl = el;
    }
  }

  function onClick(e) {
    if (!active) return;
    const el = findTarget(e.target);
    if (!el) return;
    e.stopPropagation();
    e.preventDefault();
    clearHover();
    if (el === selectedEl) {
      // second click on same element → enter inline edit
      startInline();
    } else {
      stopInline();
      ieSelect(el);
    }
  }

  function onKeyDown(e) {
    if (e.key === 'Escape') {
      if (inlineEditing) { stopInline(); return; }
      if (selectedEl) { deselect(); return; }
      if (active) ieToggle();
    }
  }

  // ── DOM creation ──────────────────────────────────────────
  let bar, panel, panelTag, panelBody, inlineBtn, toggleBtn;

  function init() {
    // mode bar
    bar = document.createElement('div');
    bar.id = 'ie-bar';
    document.body.appendChild(bar);

    // panel
    panel = document.createElement('div');
    panel.id = 'ie-panel';
    panel.innerHTML = `
      <div id="ie-panel-hdr">
        <span id="ie-panel-tag">—</span>
        <button id="ie-panel-close" title="Close">✕</button>
      </div>
      <div id="ie-panel-body"></div>
    `;
    document.body.appendChild(panel);

    panelTag  = document.getElementById('ie-panel-tag');
    panelBody = document.getElementById('ie-panel-body');
    document.getElementById('ie-panel-close').addEventListener('click', deselect);

    // toggle button in nav
    const nav = document.querySelector('.nav-controls') || document.querySelector('nav') || document.querySelector('.nav');
    if (nav) {
      toggleBtn = document.createElement('button');
      toggleBtn.id = 'ie-toggle-btn';
      toggleBtn.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> Select`;
      toggleBtn.title = 'Select element to edit (S)';
      toggleBtn.addEventListener('click', ieToggle);
      // insert before the Edit button if it exists, else append
      const editBtn = document.getElementById('cfg-open-btn');
      if (editBtn) nav.insertBefore(toggleBtn, editBtn);
      else nav.appendChild(toggleBtn);
    }

    // global listeners
    document.addEventListener('mouseover', onMove, true);
    document.addEventListener('click', onClick, true);
    document.addEventListener('keydown', onKeyDown);

    // keyboard shortcut S
    document.addEventListener('keydown', function (e) {
      if (e.target.isContentEditable) return;
      const tag = e.target.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
      if (e.key === 's' || e.key === 'S') {
        if (!e.ctrlKey && !e.metaKey) ieToggle();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
