// ============================================================
//  PRESENTATION CONFIGURATION
//  All editable content lives here. Use the GUI editor (✎ Edit button)
//  to modify, then Export JSON. Share that file with the AI to import.
// ============================================================

const CONFIG = {

  meta: {
    eventName : "Bilaspur Forest Department Workshop",
    eventDate : "30 May 2026",
    venue     : "Forest Rest House, Bilaspur",
    title     : "Elephant & Human Casualty",
    subtitle  : "Dharamjaigarh & Raigarh Forest Divisions | Bilaspur, Chhattisgarh",
    metaLine  : "Financial Years 2021–22 to 2025–26 · 86 Geo-referenced Incidents",
    s2Heading : "Human-Elephant Conflict: Data, Science & Solutions",
    s2Para    : "A technical workshop bringing together field officers, scientists, and GIS analysts to review five years of casualty data, identify spatial hotspots, and formulate an evidence-based intervention framework for Bilaspur District."
  },

  stats: {
    years          : 5,
    geoPoints      : 86,
    elephantTotal  : 41,
    humanTotal     : 45,
    dhElephant     : 23,
    dhHuman        : 36,
    rgElephant     : 18,
    rgHuman        : 9,
    participants   : 48
  },

  resourcePersons: [
    {
      initials : "PN",
      name     : "Dr. Parag Nigam",
      title    : "Scientist G & Head, Dept. of Wildlife Health Management\nICAR-IVRI, Izatnagar",
      badge    : "Session Chair",
      color    : "green"
    },
    {
      initials : "TS",
      name     : "Dr. Tapendra Saini",
      title    : "Scientist-C\nDept. of Wildlife Health Management",
      badge    : "Resource Person",
      color    : "green"
    },
    {
      initials : "CS",
      name     : "Dr. C.P. Sharma",
      title    : "Principal Technical Officer\nForensic Cell",
      badge    : "Resource Person",
      color    : "green"
    },
    {
      initials : "MK",
      name     : "Dr. M. Karikalan",
      title    : "Senior Scientist\nCentre for Wildlife",
      badge    : "Resource Person",
      color    : "green"
    },
    {
      initials : "AS",
      name     : "Dr. A.B. Shrivastav",
      title    : "Former Director\nCentre for Wildlife & Forensic Health",
      badge    : "Resource Person",
      color    : "green"
    }
  ],

  schedule: [
    { time: "09:30", title: "Registration & Welcome",                  sub: "Participant registration, distribution of materials",          special: "" },
    { time: "10:00", title: "Inaugural Session & Workshop Objectives",  sub: "Opening remarks, scope and expected outcomes",                special: "" },
    { time: "10:30", title: "Elephant Population & Range Dynamics",     sub: "Dr. Parag Nigam — ICAR-IVRI, Izatnagar",                     special: "" },
    { time: "11:00", title: "Five-Year Casualty Data Presentation",     sub: "Dr. Tapendra Saini — Scientist-C",                           special: "" },
    { time: "11:30", title: "Tea Break",                                sub: "15 minutes",                                                  special: "tea" },
    { time: "11:45", title: "GIS Hotspot Analysis & Mapping",           sub: "Dr. A.B. Shrivastav — Forensic Cell",                        special: "" },
    { time: "12:15", title: "PM & Lab Report Findings",                 sub: "Dr. M. Karikalan — ICAR-IVRI Izatnagar",                     special: "" },
    { time: "12:45", title: "Recommendations & Action Plan",            sub: "Panel discussion — all resource persons",                    special: "" },
    { time: "13:15", title: "Lunch & Field Discussion",                 sub: "Informal networking and field-level deliberations",           special: "lunch" }
  ]

};


// ============================================================
//  applyConfig — pushes CONFIG values into the live DOM
// ============================================================
function applyConfig() {

  function escH(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  // ── Slide 1 — Title ──────────────────────────────────────────────────────
  const s1 = document.getElementById('s1');
  if (s1) {
    const tag = s1.querySelector('.section-tag');
    if (tag) tag.textContent = `${CONFIG.meta.eventName}  ·  ${CONFIG.meta.eventDate}`;

    const h1 = s1.querySelector('h1');
    if (h1) {
      const parts = CONFIG.meta.title.split('&');
      h1.innerHTML = parts.length > 1
        ? `${escH(parts[0].trim())} <span>&amp;</span> ${escH(parts[1].trim())}`
        : escH(CONFIG.meta.title);
    }

    const sub = s1.querySelector('.subtitle');
    if (sub) sub.textContent = CONFIG.meta.subtitle;

    const meta = s1.querySelector('.meta');
    if (meta) meta.textContent = CONFIG.meta.metaLine;
  }

  // ── Slide 2 — Workshop Context ───────────────────────────────────────────
  const s2 = document.getElementById('s2');
  if (s2) {
    const h2 = s2.querySelector('h2');
    if (h2) {
      const parts = CONFIG.meta.s2Heading.split(':');
      h2.innerHTML = parts.length > 1
        ? `${escH(parts[0])}:<br>${escH(parts.slice(1).join(':').trim())}`
        : escH(CONFIG.meta.s2Heading);
    }
    const para = s2.querySelector('p.muted');
    if (para) para.textContent = CONFIG.meta.s2Para;

    // KPI values: years, geoPoints
    const kpiEls = s2.querySelectorAll('.kpi-value[data-count]');
    const kpiKeys = ['years', 'geoPoints'];
    kpiEls.forEach((el, i) => {
      if (kpiKeys[i] && CONFIG.stats[kpiKeys[i]] !== undefined) {
        el.dataset.count = CONFIG.stats[kpiKeys[i]];
        el.textContent   = CONFIG.stats[kpiKeys[i]];
      }
    });
  }

  // ── Slide 3 — Resource Persons ───────────────────────────────────────────
  CONFIG.resourcePersons.forEach((p, i) => {
    const wrap = document.getElementById('rp' + i);
    if (!wrap) return;

    const av = wrap.querySelector('.s3-av');
    if (av) { av.textContent = p.initials; av.className = `s3-av s3-av-${p.color}`; }

    const nm = wrap.querySelector('.s3-name');
    if (nm) nm.textContent = p.name;

    const tt = wrap.querySelector('.s3-title');
    if (tt) tt.innerHTML = escH(p.title).replace(/\n/g, '<br>');

    const bd = wrap.querySelector('.person-badge');
    if (bd) bd.textContent = p.badge;
  });

  // ── Slide 4 — Schedule ───────────────────────────────────────────────────
  const s4 = document.getElementById('s4');
  if (s4) {
    const dateLine = s4.querySelector('p.muted');
    if (dateLine) dateLine.innerHTML =
      `${escH(CONFIG.meta.eventDate)} &nbsp;·&nbsp; ${escH(CONFIG.meta.venue)}`;

    const tl = s4.querySelector('.timeline');
    if (tl) {
      tl.innerHTML = CONFIG.schedule.map(item => {
        const dotStyle   = item.special === 'tea'   ? 'style="background:#C9A84C;border-color:#0A1628"'
                         : item.special === 'lunch' ? 'style="background:#F4A261;border-color:#0A1628"'
                         : '';
        const titleStyle = item.special === 'tea'   ? ' style="color:#C9A84C"'
                         : item.special === 'lunch' ? ' style="color:#F4A261"'
                         : '';
        return `<div class="timeline-item">
          <div class="timeline-time">${escH(item.time)}</div>
          <div class="timeline-dot" ${dotStyle}></div>
          <div class="timeline-text">
            <h4${titleStyle}>${escH(item.title)}</h4>
            <p>${escH(item.sub)}</p>
          </div>
        </div>`;
      }).join('');
    }
  }

  // ── Slide 5 — Participants ───────────────────────────────────────────────
  const s5Hero = document.querySelector('#s5 .hero-count');
  if (s5Hero) {
    s5Hero.textContent = CONFIG.stats.participants;
    s5Hero.dataset.target = CONFIG.stats.participants;
  }

  // ── Slide 7 — Elephant Casualty Hero ────────────────────────────────────
  const s7Hero = document.querySelector('#s7 .hero-count');
  if (s7Hero) {
    s7Hero.textContent = 0;
    s7Hero.dataset.count = CONFIG.stats.elephantTotal;
  }

  // ── Slide 15 — Human Casualty Hero ──────────────────────────────────────
  const s15Hero = document.querySelector('#s15 .hero-count');
  if (s15Hero) {
    s15Hero.textContent = 0;
    s15Hero.dataset.count = CONFIG.stats.humanTotal;
  }
}

// ============================================================
//  STYLE CONFIGURATION
// ============================================================
const STYLE = {
  primary     : '#52B788',
  primaryDark : '#1B4332',
  gold        : '#C9A84C',
  amber       : '#F4A261',
  red         : '#E63946',
  bg          : '#0A1628',
  card        : '#112240',
  textPrimary : '#E8F0E8',
  textMuted   : '#8BA098',
  fontScale   : 1.2,
  cardRadius  : 12,
  slideGap    : 20,
  h1Size      : 3.2,
  h2Size      : 2.0,
  h3Size      : 1.35,
  bodySize    : 1.1,
  captionSize : 1.2,
};

function hexToRgb(hex) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `${r},${g},${b}`;
}

function applyStyle() {
  // Font scale: change root font-size so all rem values scale uniformly
  document.documentElement.style.fontSize = `${STYLE.fontScale * 16}px`;

  let el = document.getElementById('cfg-dyn');
  if (!el) {
    el = document.createElement('style');
    el.id = 'cfg-dyn';
    document.head.appendChild(el);
  }

  const g  = STYLE.primary;
  const gd = STYLE.primaryDark;
  const go = STYLE.gold;
  const am = STYLE.amber;
  const rd = STYLE.red;
  const bg = STYLE.bg;
  const cd = STYLE.card;
  const tx = STYLE.textPrimary;
  const mt = STYLE.textMuted;
  const rr = STYLE.cardRadius + 'px';

  el.textContent = `
    :root {
      --cfg-green:      ${g};
      --cfg-green-rgb:  ${hexToRgb(g)};
      --cfg-green-dark: ${gd};
      --cfg-gold:       ${go};
      --cfg-gold-rgb:   ${hexToRgb(go)};
      --cfg-amber:      ${am};
      --cfg-red:        ${rd};
      --cfg-red-rgb:    ${hexToRgb(rd)};
      --cfg-bg:         ${bg};
      --cfg-card:       ${cd};
      --cfg-text:       ${tx};
      --cfg-muted:      ${mt};
      --cfg-radius:     ${rr};
      --cfg-gap:        ${STYLE.slideGap}px;
    }
    /* Primary green */
    .section-tag:not(.red):not(.amber) {
      color: var(--cfg-green) !important;
      background: rgba(var(--cfg-green-rgb),.15) !important;
      border-color: rgba(var(--cfg-green-rgb),.3) !important;
    }
    .green, .kpi-value.green, .slide-title h1 span,
    .slide-thanks h1, .conclusion-line span:not(.red) { color: var(--cfg-green) !important; }
    .timeline-dot:not([style]) { background: var(--cfg-green) !important; }
    .timeline-dot:not([style])::after { background: rgba(var(--cfg-green-rgb),.25) !important; }
    .timeline-time { color: var(--cfg-green) !important; }
    .person-badge {
      color: var(--cfg-green) !important;
      background: rgba(var(--cfg-green-rgb),.15) !important;
      border-color: rgba(var(--cfg-green-rgb),.3) !important;
    }
    .s3-av-green {
      background: var(--cfg-green-dark) !important;
      border-color: var(--cfg-green) !important;
      box-shadow: 0 3px 10px rgba(0,0,0,.55),0 0 0 2px rgba(var(--cfg-green-rgb),.3) !important;
    }
    .s3-card { border-color: rgba(var(--cfg-green-rgb),.22) !important; }
    .s3-cw:not(.s3-hidden):not(.s3-zooming) .s3-card:hover {
      border-color: rgba(var(--cfg-green-rgb),.5) !important;
    }
    .stat-badge:not(.red) {
      background: rgba(var(--cfg-green-rgb),.12) !important;
      border-color: rgba(var(--cfg-green-rgb),.25) !important;
      color: var(--cfg-green) !important;
    }
    /* Gold */
    .gold, .kpi-value.amber { color: var(--cfg-gold) !important; }
    /* Red */
    .red, .kpi-value.red, .hero-number.red { color: var(--cfg-red) !important; }
    .section-tag.red {
      color: var(--cfg-red) !important;
      background: rgba(var(--cfg-red-rgb),.15) !important;
      border-color: rgba(var(--cfg-red-rgb),.35) !important;
    }
    /* Backgrounds */
    .bg-dark { background: var(--cfg-bg) !important; }
    .bg-forest { background: linear-gradient(135deg, var(--cfg-bg) 0%,
      color-mix(in srgb, var(--cfg-green) 15%, var(--cfg-bg)) 100%) !important; }
    /* Card backgrounds + radius */
    .kpi-card, .s3-card, .report-section, .action-card, .dept-logo {
      background: var(--cfg-card) !important;
      border-radius: var(--cfg-radius) !important;
    }
    .kpi-card { border-color: rgba(var(--cfg-green-rgb),.2) !important; }
    /* Typography colors */
    .s3-name { color: var(--cfg-text) !important; }
    .s3-title, .muted { color: var(--cfg-muted) !important; }
    /* Slide padding gap */
    .s3-grid4 { gap: var(--cfg-gap) !important; }
    .s3-wrapper { gap: var(--cfg-gap) !important; }
    /* Text sizes — scoped to .slide to avoid affecting editor UI */
    .slide h1 { font-size: ${STYLE.h1Size}rem !important; }
    .slide h2 { font-size: ${STYLE.h2Size}rem !important; }
    .slide h3, .slide h4 { font-size: ${STYLE.h3Size}rem !important; }
    .slide p, .slide .muted, .slide .s3-title, .slide .timeline-item p,
    .slide .kpi-label, .slide .report-body, .slide .action-desc { font-size: ${STYLE.bodySize}rem !important; }
    .slide .section-tag, .slide .person-badge, .slide .stat-badge,
    .slide .timeline-time, .slide .kpi-card .kpi-label { font-size: ${STYLE.captionSize}rem !important; }
    .slide .s2-card-title { font-size: ${(STYLE.bodySize * 1.2).toFixed(2)}rem !important; }
  `;
}

document.addEventListener('DOMContentLoaded', function () {
  applyConfig();
  applyStyle();
});
