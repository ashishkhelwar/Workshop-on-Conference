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
      badge    : "Lab Reports",
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
