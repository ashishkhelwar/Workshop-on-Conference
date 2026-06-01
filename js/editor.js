// ============================================================
//  PRESENTATION EDITOR
//  Right-side drawer with tabbed form, live preview,
//  and JSON export / import.
// ============================================================

(function () {

  // ── Build the panel HTML once ────────────────────────────────────────────
  function buildPanel() {
    // Overlay (click to close)
    const ov = document.createElement('div');
    ov.id = 'cfg-overlay';
    ov.onclick = closeEditor;
    document.body.appendChild(ov);

    // Panel
    const p = document.createElement('div');
    p.id = 'cfg-panel';
    p.innerHTML = `
      <div class="cfg-header">
        <div class="cfg-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
               stroke="#52B788" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
          Customize Presentation
        </div>
        <button class="cfg-close" onclick="closeEditor()" title="Close">✕</button>
      </div>

      <div class="cfg-io">
        <button class="cfg-btn-io cfg-import" onclick="importConfig()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          Import JSON
        </button>
        <button class="cfg-btn-io cfg-export" onclick="exportConfig()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"
               stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          Export JSON
        </button>
      </div>

      <div class="cfg-tabs" role="tablist">
        <button class="cfg-tab active" data-tab="info"     onclick="cfgTab(this,'info')">Info</button>
        <button class="cfg-tab"        data-tab="persons"  onclick="cfgTab(this,'persons')">Persons</button>
        <button class="cfg-tab"        data-tab="stats"    onclick="cfgTab(this,'stats')">Stats</button>
        <button class="cfg-tab"        data-tab="schedule" onclick="cfgTab(this,'schedule')">Schedule</button>
        <button class="cfg-tab"        data-tab="style"    onclick="cfgTab(this,'style')">Style</button>
      </div>

      <div class="cfg-body" id="cfg-body"></div>

      <div class="cfg-footer">
        <button class="cfg-apply" onclick="cfgApplyAll()">
          Apply Changes to Presentation
        </button>
      </div>`;
    document.body.appendChild(p);

    cfgRenderTab('info');
  }

  // ── Tab switch ────────────────────────────────────────────────────────────
  window.cfgTab = function (btn, tab) {
    document.querySelectorAll('.cfg-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    cfgRenderTab(tab);
  };

  // ── Render active tab ─────────────────────────────────────────────────────
  function cfgRenderTab(tab) {
    const body = document.getElementById('cfg-body');
    if (!body) return;

    if (tab === 'info') {
      body.innerHTML =
        section('Event Details', [
          fld('meta.eventName', 'Workshop / Event Name',  CONFIG.meta.eventName),
          fld('meta.eventDate', 'Date',                   CONFIG.meta.eventDate),
          fld('meta.venue',     'Venue',                  CONFIG.meta.venue)
        ]) +
        section('Title Slide (Slide 1)', [
          fld('meta.title',    'Main Title  (use & for ampersand)', CONFIG.meta.title),
          fld('meta.subtitle', 'Subtitle',                          CONFIG.meta.subtitle),
          fld('meta.metaLine', 'Meta / Caption Line',               CONFIG.meta.metaLine)
        ]) +
        section('Workshop Context Slide (Slide 2)', [
          fld('meta.s2Heading', 'Section Heading',  CONFIG.meta.s2Heading),
          txa('meta.s2Para',    'Description Para', CONFIG.meta.s2Para)
        ]);
    }

    else if (tab === 'persons') {
      const labels = [
        'Person 1 — Session Chair (top card)',
        'Person 2', 'Person 3', 'Person 4', 'Person 5'
      ];
      body.innerHTML = CONFIG.resourcePersons.map((p, i) =>
        section(labels[i], [
          fld(`rp.${i}.initials`, 'Initials  (2 chars shown in circle)', p.initials),
          fld(`rp.${i}.name`,     'Full Name',                           p.name),
          txa(`rp.${i}.title`,    'Designation  (new line = line break)', p.title),
          fld(`rp.${i}.badge`,    'Badge Label',                          p.badge),
          sel(`rp.${i}.color`,    'Avatar Color', p.color, [
            { v: 'green', l: '● Green  (Session Chair / Scientist)' },
            { v: 'red',   l: '● Red    (Resource Person / Officer)' }
          ])
        ])
      ).join('');
    }

    else if (tab === 'stats') {
      body.innerHTML =
        section('Study Period', [
          num('stats.years',        'Financial Years Covered',        CONFIG.stats.years),
          num('stats.geoPoints',    'Total Geo-referenced Incidents', CONFIG.stats.geoPoints),
          num('stats.participants', 'Workshop Participants',          CONFIG.stats.participants)
        ]) +
        section('Elephant Casualties', [
          num('stats.elephantTotal', 'Total Elephant Deaths',           CONFIG.stats.elephantTotal),
          num('stats.dhElephant',    'Dharamjaigarh Division Deaths',   CONFIG.stats.dhElephant),
          num('stats.rgElephant',    'Raigarh Division Deaths',         CONFIG.stats.rgElephant)
        ]) +
        section('Human Casualties', [
          num('stats.humanTotal', 'Total Human Deaths',           CONFIG.stats.humanTotal),
          num('stats.dhHuman',    'Dharamjaigarh Division Deaths', CONFIG.stats.dhHuman),
          num('stats.rgHuman',    'Raigarh Division Deaths',       CONFIG.stats.rgHuman)
        ]);
    }

    else if (tab === 'schedule') {
      body.innerHTML =
        `<div class="cfg-section">
          <div class="cfg-section-title">Timeline Items  <span class="cfg-hint">(drag to reorder — not yet)</span></div>
          <div id="cfg-sched-list">${CONFIG.schedule.map(schedRow).join('')}</div>
          <button class="cfg-add-row" onclick="cfgAddSchedRow()">+ Add Item</button>
        </div>`;
    }

    else if (tab === 'style') {
      body.innerHTML =
        section('Theme Colors', [
          clr('style.primary',     'Primary Accent',         STYLE.primary),
          clr('style.primaryDark', 'Dark Accent / Avatar',   STYLE.primaryDark),
          clr('style.gold',        'Gold / Secondary',       STYLE.gold),
          clr('style.amber',       'Amber / Warning',        STYLE.amber),
          clr('style.red',         'Alert / Red',            STYLE.red),
        ]) +
        section('Slide Backgrounds', [
          clr('style.bg',   'Slide Background', STYLE.bg),
          clr('style.card', 'Card Background',  STYLE.card),
        ]) +
        section('Text Colors', [
          clr('style.textPrimary', 'Primary Text Color',  STYLE.textPrimary),
          clr('style.textMuted',   'Muted / Sub Text Color', STYLE.textMuted),
        ]) +
        section('Text Sizes', [
          rng('style.h1Size',      'Header (H1)',         STYLE.h1Size,      1.5, 5.0,  0.1,  'rem'),
          rng('style.h2Size',      'Sub-Header (H2)',     STYLE.h2Size,      1.0, 3.5,  0.1,  'rem'),
          rng('style.h3Size',      'Section Heading (H3/H4)', STYLE.h3Size,  0.8, 2.5,  0.05, 'rem'),
          rng('style.bodySize',    'Body Text',           STYLE.bodySize,    0.5, 1.5,  0.05, 'rem'),
          rng('style.captionSize', 'Caption / Label / Badge', STYLE.captionSize, 0.4, 1.2, 0.05, 'rem'),
          rng('style.fontScale',   'Global Scale (all rem)', STYLE.fontScale, 0.7, 1.35, 0.05, 'pct'),
        ]) +
        section('Layout', [
          rng('style.cardRadius', 'Card Corner Radius', STYLE.cardRadius, 0, 24, 1, 'px'),
          rng('style.slideGap',   'Card / Row Gap',     STYLE.slideGap,   8, 40, 2, 'px'),
        ]) +
        `<div class="cfg-section">
          <button class="cfg-reset-style" onclick="cfgResetStyle()">Reset to Defaults</button>
        </div>`;
    }
  }

  // ── HTML helpers ──────────────────────────────────────────────────────────
  function section(title, fields) {
    return `<div class="cfg-section">
      <div class="cfg-section-title">${esc(title)}</div>
      ${fields.join('')}
    </div>`;
  }

  function fld(key, label, val) {
    return `<div class="cfg-field">
      <label class="cfg-label">${esc(label)}</label>
      <input class="cfg-input" data-key="${key}" value="${escAttr(val)}"
             oninput="cfgLive(this)">
    </div>`;
  }

  function txa(key, label, val) {
    return `<div class="cfg-field">
      <label class="cfg-label">${esc(label)}</label>
      <textarea class="cfg-textarea" data-key="${key}" rows="3"
                oninput="cfgLive(this)">${esc(val)}</textarea>
    </div>`;
  }

  function num(key, label, val) {
    return `<div class="cfg-field cfg-field-num">
      <label class="cfg-label">${esc(label)}</label>
      <input class="cfg-input cfg-num" type="number" min="0" data-key="${key}"
             value="${Number(val)}" oninput="cfgLive(this)">
    </div>`;
  }

  function sel(key, label, current, opts) {
    const options = opts.map(o =>
      `<option value="${escAttr(o.v)}" ${o.v === current ? 'selected' : ''}>${esc(o.l)}</option>`
    ).join('');
    return `<div class="cfg-field">
      <label class="cfg-label">${esc(label)}</label>
      <select class="cfg-select" data-key="${key}" onchange="cfgLive(this)">${options}</select>
    </div>`;
  }

  function clr(key, label, val) {
    return `<div class="cfg-field cfg-clr-field">
      <label class="cfg-label">${esc(label)}</label>
      <div class="cfg-clr-row">
        <input class="cfg-clr-swatch" type="color" data-key="${key}"
               value="${escAttr(val)}" oninput="cfgLive(this)">
        <input class="cfg-input cfg-clr-hex" data-key="${key}"
               value="${escAttr(val)}" maxlength="7" placeholder="#rrggbb"
               oninput="cfgSyncHex(this)">
        <div class="cfg-clr-preview" style="background:${escAttr(val)}"></div>
      </div>
    </div>`;
  }

  function rng(key, label, val, min, max, step, unit) {
    const disp = unit === 'pct' ? Math.round(val * 100) + '%' : val + unit;
    return `<div class="cfg-field">
      <div class="cfg-label-row">
        <label class="cfg-label">${esc(label)}</label>
        <span class="cfg-rng-val" id="rv_${key.replace(/\./g,'_')}">${disp}</span>
      </div>
      <input class="cfg-range" type="range" data-key="${key}"
             min="${min}" max="${max}" step="${step}" value="${val}"
             data-unit="${unit}"
             oninput="cfgLive(this)">
    </div>`;
  }

  function schedRow(item, i) {
    const specOpts = [
      { v: '',      l: 'Normal session' },
      { v: 'tea',   l: '☕ Tea Break'   },
      { v: 'lunch', l: '🍽 Lunch Break' }
    ];
    const specSel = specOpts.map(o =>
      `<option value="${o.v}" ${(item.special||'')=== o.v?'selected':''}>${o.l}</option>`
    ).join('');
    return `<div class="cfg-sr" data-idx="${i}">
      <div class="cfg-sr-row1">
        <input class="cfg-input cfg-sr-time" placeholder="HH:MM"
               value="${escAttr(item.time)}" data-si="${i}" data-sf="time">
        <select class="cfg-select cfg-sr-type" data-si="${i}" data-sf="special">${specSel}</select>
        <button class="cfg-del-row" onclick="cfgDelSchedRow(${i})" title="Remove">✕</button>
      </div>
      <input class="cfg-input cfg-sr-title" placeholder="Session title"
             value="${escAttr(item.title)}" data-si="${i}" data-sf="title">
      <input class="cfg-input cfg-sr-sub" placeholder="Presenter / sub-text"
             value="${escAttr(item.sub||'')}" data-si="${i}" data-sf="sub">
    </div>`;
  }

  function esc(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }
  function escAttr(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');
  }

  // ── Live-write one field to CONFIG or STYLE ──────────────────────────────
  window.cfgLive = function (el) {
    const key = el.dataset.key;
    if (!key) return;

    if (key.startsWith('style.')) {
      const prop = key.slice(6);
      const rawVal = el.type === 'range' ? parseFloat(el.value) : el.value;
      STYLE[prop] = rawVal;
      // Update range display
      const unit = el.dataset.unit;
      if (unit) {
        const dispEl = document.getElementById('rv_' + key.replace(/\./g,'_'));
        if (dispEl) dispEl.textContent = unit === 'pct' ? Math.round(rawVal*100)+'%' : rawVal+unit;
      }
      // Sync color preview
      if (el.type === 'color') {
        const row = el.closest('.cfg-clr-row');
        if (row) {
          const hex = row.querySelector('.cfg-clr-hex');
          const prev = row.querySelector('.cfg-clr-preview');
          if (hex)  hex.value = rawVal;
          if (prev) prev.style.background = rawVal;
        }
      }
      applyStyle();
      return;
    }

    const val = el.tagName === 'SELECT' ? el.value
              : el.type === 'number'    ? Number(el.value)
              : el.value;
    const parts = key.split('.');
    if (parts[0] === 'rp') {
      CONFIG.resourcePersons[+parts[1]][parts[2]] = val;
    } else if (CONFIG[parts[0]]) {
      CONFIG[parts[0]][parts[1]] = val;
    }
  };

  // ── Sync hex text input → color picker ───────────────────────────────────
  window.cfgSyncHex = function (hexEl) {
    const val = hexEl.value.trim();
    if (!/^#[0-9a-fA-F]{6}$/.test(val)) return;
    const row = hexEl.closest('.cfg-clr-row');
    if (row) {
      const picker = row.querySelector('input[type="color"]');
      const prev   = row.querySelector('.cfg-clr-preview');
      if (picker) picker.value = val;
      if (prev)   prev.style.background = val;
    }
    cfgLive(hexEl);
  };

  // ── Reset style to defaults ───────────────────────────────────────────────
  window.cfgResetStyle = function () {
    Object.assign(STYLE, {
      primary:'#52B788', primaryDark:'#1B4332', gold:'#C9A84C', amber:'#F4A261',
      red:'#E63946', bg:'#0A1628', card:'#112240', textPrimary:'#E8F0E8',
      textMuted:'#8BA098', fontScale:1.2, cardRadius:12, slideGap:20,
      h1Size:3.2, h2Size:2.0, h3Size:1.35, bodySize:1.1, captionSize:1.2,
    });
    applyStyle();
    cfgRenderTab('style');
    cfgToast('Style reset to defaults');
  };

  // ── Schedule: flush all rows to CONFIG ───────────────────────────────────
  function flushSchedule() {
    document.querySelectorAll('.cfg-sr').forEach(row => {
      const i = +row.dataset.idx;
      if (!CONFIG.schedule[i]) return;
      row.querySelectorAll('[data-si][data-sf]').forEach(el => {
        CONFIG.schedule[i][el.dataset.sf] = el.value;
      });
    });
  }

  window.cfgAddSchedRow = function () {
    flushSchedule();
    CONFIG.schedule.push({ time: '', title: 'New Session', sub: '', special: '' });
    cfgRenderTab('schedule');
  };

  window.cfgDelSchedRow = function (i) {
    flushSchedule();
    CONFIG.schedule.splice(i, 1);
    cfgRenderTab('schedule');
  };

  // ── Apply all changes ─────────────────────────────────────────────────────
  window.cfgApplyAll = function () {
    flushSchedule();
    applyConfig();
    applyStyle();
    cfgToast('Changes applied to presentation ✓');
  };

  // ── Open / Close ──────────────────────────────────────────────────────────
  window.openEditor = function () {
    const activeTab = document.querySelector('.cfg-tab.active');
    cfgRenderTab(activeTab ? activeTab.dataset.tab : 'info');
    document.getElementById('cfg-panel').classList.add('open');
    document.getElementById('cfg-overlay').classList.add('open');
  };

  window.closeEditor = function () {
    document.getElementById('cfg-panel').classList.remove('open');
    document.getElementById('cfg-overlay').classList.remove('open');
  };

  // ── Export ────────────────────────────────────────────────────────────────
  window.exportConfig = function () {
    flushSchedule();
    const json = JSON.stringify({ ...CONFIG, style: STYLE }, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url  = URL.createObjectURL(blob);
    const a    = Object.assign(document.createElement('a'), { href: url, download: 'workshop-config.json' });
    a.click();
    URL.revokeObjectURL(url);
    cfgToast('Exported as workshop-config.json');
  };

  // ── Import ────────────────────────────────────────────────────────────────
  window.importConfig = function () {
    const inp = Object.assign(document.createElement('input'),
      { type: 'file', accept: '.json,application/json' });
    inp.onchange = e => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = ev => {
        try {
          const src = JSON.parse(ev.target.result);
          if (src.meta)            Object.assign(CONFIG.meta,  src.meta);
          if (src.stats)           Object.assign(CONFIG.stats, src.stats);
          if (src.resourcePersons) CONFIG.resourcePersons = src.resourcePersons;
          if (src.schedule)        CONFIG.schedule         = src.schedule;
          if (src.style)           Object.assign(STYLE, src.style);
          applyConfig();
          applyStyle();
          const activeTab = document.querySelector('.cfg-tab.active');
          cfgRenderTab(activeTab ? activeTab.dataset.tab : 'info');
          cfgToast('Configuration imported ✓');
        } catch {
          cfgToast('⚠ Invalid JSON file — check the format', true);
        }
      };
      reader.readAsText(file);
    };
    inp.click();
  };

  // ── Toast ─────────────────────────────────────────────────────────────────
  function cfgToast(msg, isErr) {
    let t = document.getElementById('cfg-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'cfg-toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.className   = 'cfg-toast' + (isErr ? ' cfg-toast-err' : '');
    t.classList.add('show');
    clearTimeout(t._tmr);
    t._tmr = setTimeout(() => t.classList.remove('show'), 3200);
  }

  // ── Init ──────────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildPanel);
  } else {
    buildPanel();
  }

})();
