# Elephant & Human Casualty Workshop Presentation — Complete Rebuild Specification

> **Purpose of this document:** A self-contained blueprint to recreate this entire
> interactive HTML presentation from scratch in a new session. Hand this file to
> the assistant and say *"Build this presentation exactly as specified."*
>
> **Live reference:** https://ashishkhelwar.github.io/Workshop-on-Conference/
> **Full source (exact copy):** https://github.com/ashishkhelwar/Workshop-on-Conference/archive/refs/heads/main.zip

---

## 1. What This Is

A **single-page, keyboard-driven HTML5 slide deck** (28 slides) built for a Bilaspur
Forest Department workshop on elephant & human casualties in Chhattisgarh (Raigarh &
Dharamjaigarh divisions). It is **vanilla JS + Chart.js + Leaflet** — no build step,
no framework. Slides are absolutely-positioned `<section>` elements that cross-fade by
toggling an `.active` class. Charts and maps lazy-initialize when their slide opens.

**Tech stack**
- Pure HTML/CSS/JS (ES5/ES6, no bundler)
- **Chart.js 4.4.0** (CDN) — bar/line/doughnut charts
- **Leaflet 1.9.4** (CDN + local `node_modules`) — interactive maps w/ OpenStreetMap tiles
- **Google Fonts:** Bebas Neue, Fraunces, Hanken Grotesk
- Custom **vanilla-canvas** animated area chart (population trend) — no library
- Served via **GitHub Pages from `main` branch** (important: Pages serves `main`, not feature branches)

---

## 2. File Structure

```
/
├── index.html              # All 28 slides, ~1725 lines
├── css/
│   ├── theme.css           # Master stylesheet (~1358 lines) — all slide styling
│   ├── rp-slides.css        # Scoped styles for 5 Resource-Person intro slides
│   ├── editor.css           # (optional) live-edit toolbar styling
│   └── inline-editor.css    # (optional) inline contenteditable styling
├── js/
│   ├── config.js            # Editor/config flags (optional feature)
│   ├── data.js              # ALL presentation data (single source of truth)
│   ├── maps.js              # 6 Leaflet map initializers
│   ├── charts.js            # Chart.js initializers + custom canvas population chart
│   ├── app.js               # Slide navigation controller + onSlideActivate switch
│   ├── editor.js            # (optional) live editing
│   └── inline-editor.js     # (optional) inline editing
├── assets/
│   ├── raigarh_boundary.geojson        # 555 polygons, gold overlay (~181KB)
│   └── dharamjaigarh_boundary.geojson  # 751 polygons, green overlay (~354KB)
├── img/                     # logos (CG, WII), cover & resource-person photos
└── node_modules/leaflet/    # local Leaflet copy (CDN also used)
```

**Script load order (bottom of `index.html`, critical):**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="js/config.js"></script>
<script src="js/data.js"></script>
<script src="js/maps.js"></script>
<script src="js/charts.js"></script>
<script src="js/app.js"></script>
<script src="js/editor.js"></script>
<script src="js/inline-editor.js"></script>
```

**Head includes:**
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<link rel="stylesheet" href="css/theme.css">
<link rel="stylesheet" href="css/editor.css">
<link rel="stylesheet" href="css/inline-editor.css">
<link rel="stylesheet" href="css/rp-slides.css">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 3. Design System / Theme Tokens

**Color palette** (forest-green + dark navy, with red/amber accents):

| Token | Hex | Use |
|-------|-----|-----|
| Primary green | `#52B788` | brand, elephant data, highlights |
| Light green (line) | `#5fcf97` | population chart line |
| Deep forest | `#1B4332` / `#0f2d1e` | dark green gradients |
| Dark navy (bg) | `#0A1628` | primary background |
| Navy panel | `#112240` / `#0d1f3c` | secondary panels |
| Red | `#E63946` (bright `#ff2d3a`) | human deaths, critical/danger |
| Amber/orange | `#F4A261` | warnings, 2026 highlight, peaks |
| Gold | `#C9A84C` / `#d4a831` | Raigarh division, moderate risk |
| Text light | `#E8F0E8` | headings |
| Text muted | `#8BA098` | body/secondary text |
| Text soft | `#C8D8C8` | emphasis subtext |

**Background variants (CSS classes):**
```css
.bg-dark   { background: #0A1628; }
.bg-forest { background: linear-gradient(135deg, #0A1628 0%, #0f2d1e 100%); }
.bg-somber { background: linear-gradient(160deg, #0e0a0a 0%, #1a0f0f 100%); }
```

**Fonts:** Bebas Neue (display numerals), Fraunces (serif headings on RP slides),
Hanken Grotesk (RP body), system-ui sans (default body & charts).

**Slide base mechanic:**
```css
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:100%; height:100%; overflow:hidden; background:#0A1628; }
.slide {
  position:absolute; inset:0;
  opacity:0; pointer-events:none;
  transition: opacity 0.6s ease;
}
.slide.active { opacity:1; pointer-events:all; }
.slide.prev   { opacity:0; }
```
Slides are stacked; only `.active` is visible. `16:9` implied (full-viewport).

---

## 4. Navigation Controller (`js/app.js`)

**Core behavior:**
- On `DOMContentLoaded`: collect all `.slide` elements into `slides[]`, activate slide 0,
  set `#slideNum` counter to `1 / N`, call `onSlideActivate(0)`.
- `goTo(n)`: clamp index, remove `.active` from current (add temporary `.prev` for
  650ms), add `.active` to next, update counter, call `onSlideActivate(next)`.
- **Keyboard:** `→/↓` next, `←/↑` prev, `Home` first, `End` last, `f/F` toggle fullscreen.

**`countUp(el, target, duration=1500)`** — ease-out-cubic number animation
(`1 - (1-p)³`), writes integer to `el.textContent` each frame via `requestAnimationFrame`.

**`animateHumanBars()`** — sets `.year-bar-fill` widths from `data-val` (max 16 → %) after 200ms.

**`onSlideActivate(index)`** — a `switch(index)` that lazy-inits the chart/map for each
slide. Each chart/map call is wrapped in `setTimeout(..., 300–400)` so the slide
fade finishes before canvas sizing. **Full mapping in §6 (slide inventory).**

---

## 5. Data Model (`js/data.js`)

Everything is one global `const DATA = { ... }`. Reproduce verbatim:

```javascript
const DATA = {
  years: ['2021-22','2022-23','2023-24','2024-25','2025-26','2026-27*'],

  elephantDeaths: [4, 12, 6, 10, 12, 4],
  humanDeaths:    [13, 1, 7, 8, 16, 0],

  divisionTotals: {
    dh: { human: 36, elephant: 27 },   // Dharamjaigarh
    rg: { human: 9,  elephant: 21 }    // Raigarh
  },

  causeOfDeath: [
    { cause: 'Electrocution',     count: 23, pct: 48 },
    { cause: 'Drowning',          count: 12, pct: 25 },
    { cause: 'Natural / Old Age', count: 4,  pct: 8  },
    { cause: 'Fall / Trauma',     count: 4,  pct: 8  },
    { cause: 'Other',             count: 5,  pct: 10 }
  ],

  ageProfile: [   // totals 40 (8 of 48 cases have no age record)
    { group: 'Calves (<1 yr)',   count: 10, pct: 26 },
    { group: 'Young (1–15 yr)',  count: 14, pct: 36 },
    { group: 'Adults (16–50 yr)',count: 8,  pct: 21 },
    { group: 'Old (50+ yr)',     count: 8,  pct: 21 }
  ],

  sexProfile: { male: 24, female: 18, unknown: 3 },  // 45 confirmed

  seasonal: {
    months: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    counts: [6, 4, 3, 2, 5, 4, 1, 1, 3, 8, 6, 5]      // peak Oct = 8
  },

  rangeWise: [
    { beat: 'Ghargoda (RG)',    count: 15, div: 'Raigarh',       risk: 'CRITICAL' },
    { beat: 'Chhal (DH)',       count: 10, div: 'Dharamjaigarh', risk: 'CRITICAL' },
    { beat: 'Dharamjaigarh HQ', count: 7,  div: 'Dharamjaigarh', risk: 'HIGH' },
    { beat: 'Tamanar (RG)',     count: 5,  div: 'Raigarh',       risk: 'MODERATE' },
    { beat: 'Borojh (DH)',      count: 4,  div: 'Dharamjaigarh', risk: 'HIGH' },
    { beat: 'Lailungaan (DH)',  count: 2,  div: 'Dharamjaigarh', risk: 'HIGH' },
    { beat: 'Baakaaruma (DH)',  count: 1,  div: 'Dharamjaigarh', risk: 'MODERATE' },
    { beat: 'Raigarh HQ',       count: 1,  div: 'Raigarh',       risk: 'LOW' }
  ],

  // geoPoints: [lat, lon, cause-or-village, year] — full lists in source file.
  // Four arrays: dhHuman (36), dhElephant (27), rgHuman (9), rgElephant (21).
  geoPoints: { dhHuman: [...], dhElephant: [...], rgHuman: [...], rgElephant: [...] },

  populationTrend: {
    years: ['2001','2005','2007','2015','2017','2021','2026'],
    cg:   [24, 123, 122, 247, 247, 279, 451]
  }
};
```
> Copy the full `geoPoints` arrays from the repo's `js/data.js` (they hold ~93 exact
> lat/lon points). They drive the casualty & overlay maps.

---

## 6. Slide Inventory (28 slides, 0-indexed `onSlideActivate` cases)

| # | id | Title / Content | Init on activate |
|---|-----|-----------------|------------------|
| 0 | `s1` | **Title** — animated SVG elephant-corridor network, diagonal navy panel | — |
| 1 | `s2` | **Workshop Context / Objectives** — KPI count-up cards | `countUp` KPIs |
| 2 | `rp1` | **Resource Person 1** intro (scoped `.rp-section`) | — |
| 3 | `rp2` | **Resource Person 2** | — |
| 4 | `rp3` | **Resource Person 3** (Dr. Karikalan — pathology) | — |
| 5 | `rp4` | **Resource Person 4** (Dr. Sharma — forensics) | — |
| 6 | `rp5` | **Resource Person 5** (Prof. Shrivastav — NDVSU) | — |
| 7 | `s4` | **Schedule** — Day-1/Day-2 session timeline | — |
| 8 | `s5` | **Participants** — hero count-up (48) | `countUp(48)` |
| 9 | `s6a` | **Population & Current Status** — animated canvas area chart + 2021→2026 comparison widget | `initPopChart('popCanvas')` |
| 10 | `s6b` | **Distribution Map** — Leaflet + KMZ/KML division boundaries | `initDistributionMap('distMap')` |
| 11 | `s7` | **Live Elephant GPS Tracking** — 16 herd locations, sized bubbles | `initCurrentElephantsMap('s7-live-map')` |
| 12 | `s7b` | **Elephant Casualties** — hero count (48) + liquid-fill year bars | `countUp(48)` + `initYearBarsChart` |
| 13 | `s8` | **Cause of Death** — horizontal ranked bars | `initCauseChart('causeCanvas')` |
| 14 | `s9a` | **Age Group** (dashboard, tabbed) | `initAgeChart('ageCanvas')` |
| 15 | `s9b` | **Sex Group** — doughnut w/ center text | `initSexChart('sexCanvas')` |
| 16 | `s9drown` | **Drowning Cases** map (13 cases, color-coded by div/year) | `initDrownMap('drownMap')` |
| 17 | `s9drown-pm` | **Drowning PM & Lab Report** findings | — |
| 18 | `s9c` | **Seasonal Variation of Casualty of Elephant** — line + roller-bullet | `initSeasonalChart('seasonCanvas')` |
| 19 | `s9d` | **Range Wise Casualty of Elephant** — horizontal risk-colored bars | `initRangeChart('rangeCanvas')` |
| 20 | `s10` | **Geo Casualty Map** — all points, green=elephant red=human | `initCasualtyMap('casualtyMap')` |
| 21 | `s11` | **PM Report Summary** | — |
| 22 | `s12` | **PM Report Analysis** — dual trend line (elephant+human) | `initTrendChart('trendCanvas')` |
| 23 | `s13` | **Lab Report Analysis** — ICAR-IVRI + NDVSU Jabalpur sections | — |
| 24 | `s14` | **Conclusion** — verdict + 3 action cards | — |
| 25 | `s15` | **Human Casualty** — hero count (45) + year bars | `countUp(45)` + `animateHumanBars` |
| 26 | `s16` | **GIS Overlay (climax)** — phased markers + pulsing hotspots | `initOverlayMap('overlayMap')` |
| 27 | `s17` | **Thank You** | — |

> ⚠️ User-facing slide numbers = case index + 1 (e.g. "slide 11" = `s7` = case 11
> in some references; confirm against the live deck). The distribution map the user
> calls "slide 11" is `initDistributionMap`.

---

## 7. Charts (`js/charts.js`)

Global setup:
```javascript
Chart.defaults.color = '#8BA098';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.font.family = "system-ui, -apple-system, sans-serif";
```
A global **`valueLabelPlugin`** draws value labels above bars/points.
`chartInstances{}` + `destroyChart(id)` prevent double-init.

**Chart.js charts:**
1. **`initTrendChart`** — dual line (elephant green / human red), custom left-to-right
   *clip-reveal* plugin animating `drawProgress` 0→1 over 3.5s (starts after 450ms).
2. **`initYearBarsChart`** — *liquid-fill* vertical bars built from DOM divs (not Chart.js):
   `.liq-fill` heights animate via CSS, staggered `--delay`, wave & shimmer keyframes,
   count-up numbers, `↺ Replay` button. Max value 16.
3. **`initCauseChart`** — horizontal bars, sorted desc, 5-color forest ramp.
4. **`initAgeChart`** — vertical bars, 4 green shades, y-max 18.
5. **`initSexChart`** — doughnut (68% cutout) + custom `centerText` plugin showing male %.
6. **`initSeasonalChart`** — area line, gradient fill, peak month highlighted amber/larger,
   on animation complete spawns **`startRollerBullet`**: an overlay `<canvas>` with a glowing
   gold dot that rides the Catmull-Rom path (8s cycle, 1.5s pause, trail + radial glow).
7. **`initRangeChart`** — horizontal bars colored by risk (CRITICAL red, HIGH amber,
   MODERATE gold, LOW green).

**Custom canvas population chart (the showpiece) — `initPopChart`:**
Self-invoking IIFE, **no Chart.js**. Renders `populationTrend` as an animated area+line.
- **Data:** `2001:24, 2005:123, 2007:122, 2015:247, 2017:247, 2021:279, 2026:451`
- **Scale:** `Y_MIN=0, Y_MAX=520`, `Y_TICKS=[50..500]`; padding `{top:72, right:52, bottom:50, left:62}` × scale `s=W/700`
- **Curve:** Catmull-Rom → cubic-Bézier control points (`(p2-p0)/6` tangents) for smooth natural overshoot
- **Animation:** 10s (`DUR=10000`), `easeInOutCubic`, arc-length-parameterized so the line
  tip advances at uniform speed; mid-segment tip drawn exactly via **de Casteljau split** (`splitL`)
- **Render order each frame:** grid + axis labels → orange 451 reference line (fades in last
  12%) → clipped area gradient fill → glowing green line → point markers (fade in per-point) → tip glow dot
- **2026 highlight:** larger amber marker (`9s` vs `6.5s`), pulsing outer ring (`sin(_now/700)`),
  `"2026 est."` label; the **orange dashed reference line at y=451** splits around a large
  centered `"451"` label (font `20s`, amber, dark outline via `strokeText`)
- **Interaction:** click canvas to replay; respects `prefers-reduced-motion` (draws static final frame)
- Loop keeps running after completion to sustain the pulse.

> ⚠️ **Browser-compat lesson learned:** avoid `ctx.roundRect()` (not universal) — use
> `strokeText`+`fillText` for labels. And the last marker's fade-in alpha must use
> `(prog - mp + 0.04)/0.04` (not `(prog-mp)/0.04`) or it stays invisible at prog=1.

---

## 8. Maps (`js/maps.js`)

All use Leaflet + OSM tiles, `scrollWheelZoom:false`, `setTimeout(map.invalidateSize,500)`.
`window.mapsInitialized{}` guards against re-init.

| Fn | Center / Zoom | Notes |
|----|---------------|-------|
| `initDistributionMap` | `[22.3,83.4]` z **9.2** (`zoomSnap:0.1`) | range rectangle, division markers, forest polygon, **fetches both GeoJSON boundary overlays** (Raigarh gold `#C9A84C`, Dharamjaigarh green `#52B788`, fillOpacity 0.12; popups join `range_name › beat_name › fdc_name`) |
| `initCasualtyMap` | `[22.3,83.4]` z9 | green elephant dots + red human dots from `DATA.geoPoints`, popups w/ cause/village + year |
| `initOverlayMap` | `[22.3,83.4]` z9 | **phased:** elephants → (2s) humans → (3s) pulsing CSS hotspots at Chhal & Ghargoda |
| `initCurrentElephantsMap` | `[22.25,83.22]` z9 | 16 herd locations; bubble size `√count×7` (16–46px); pulse rings on herds ≥30 |
| `initDrownMap` | `[22.2,83.28]` z10 | 13 drowning cases; icons colored DH=green, RG=gold, 2026-27=red; popups w/ date/age/water |
| `addPulsingHotspot` | — | helper: 8km dashed circle + `.pulse-ring` divIcon |

**Boundary GeoJSON** was generated by converting the user's KMZ (Raigarh) and KML
(Dharamjaigarh UTM) with Python + Douglas-Peucker simplification (epsilon≈0.001) to
shrink 3–9MB sources to 181KB/354KB. Keep these in `assets/`.

---

## 9. Resource-Person Slides (`css/rp-slides.css`)

5 slides (`rp1`–`rp5`), scoped under `.rp-section` to avoid colliding with theme.css.
- Paper-tone background, Fraunces serif + Hanken Grotesk fonts
- CSS vars: `--rp-navy, --rp-amber, --rp-paper`
- Entry: `.rp-section { transform: translateX(52px) }` → `.rp-section.active { translateX(0) }`,
  staggered `.reveal` children fade/slide via `--d` delay vars
- Each: photo (or initials placeholder), name, role/qualification, expertise row, bio paragraph
> Build these as clean hand-written CSS — an earlier auto-generated version broke
> with comments-mid-selector and an unterminated `@keyframes`. Keep selectors clean.

---

## 10. Key CSS Keyframes (theme.css)

`drawLine`, `dashFlow` (SVG network on title), `s1Pulse` (title travel pulse),
`pulseRing`/`pulseDot` (map hotspots), `fadeUp`, `fadeIn`, `zoomSlow`, `slideInLeft`,
`liqWave1`/`liqWave2`/`liqShimmer` (liquid-fill bars).

```css
@keyframes pulseRing { 0%{transform:scale(0.8);opacity:1} 100%{transform:scale(2.4);opacity:0} }
@keyframes fadeUp    { from{opacity:0;transform:translateY(30px)} to{opacity:1;transform:none} }
```

---

## 11. Slide 23 Lab Report — Current Content (post-edits)

Two reference laboratories. Sections (callout color in brackets):
- **[amber] ARSENIC DETECTED** — 2 specimens, Dec 2025, Tamnar Range (Raigarh Div),
  hepatocyte degeneration on histopathology.
- **[green] TOXICOLOGY — NEGATIVE** — 5 batches negative for nitrate/nitrite, heavy metals
  (Pb/Hg/Cd), organochlorine & organophosphate, HCN.
- **[green] EEHV — NEGATIVE** — EEHV-I PCR (ter gene, Baurer et al. 2018) negative in all
  samples. Independently confirmed by **NDVSU Jabalpur** for **Dharamjaigarh Division**:
  Report No. 251 (MD-1424/1425/1426) and No. 252 (MD-1496–1500), both 15.05.2026,
  signed Dr. Kajal K. Jadav. ICAR-IVRI signing authority: Dr. M. Karikalan.
- Header badge: `ICAR-IVRI · NDVSU`.
> The old "Lab Coverage (8 reports)" and "Critical Gap — Missing Report 5008/2025"
> blocks were **removed** per latest direction.

---

## 12. Deployment & Gotchas

- **GitHub Pages serves the `main` branch.** Any change must land on `main` to appear live.
  (A whole debugging episode was caused by editing a feature branch.)
- No build step — just open `index.html` or `python3 -m http.server`.
- Charts/maps size to their container; they need the slide visible → hence the
  `setTimeout` + `invalidateSize` pattern.
- Leaflet is loaded both from CDN and bundled in `node_modules/` (CDN wins at runtime).
- Keep `geoPoints` and the two GeoJSON files intact — they carry the real coordinates.

---

## 13. Rebuild Order (suggested)

1. Scaffold `index.html` head + 28 empty `<section class="slide">` shells with correct ids.
2. Add `theme.css` tokens, `.slide` mechanic, background variants, keyframes.
3. Build `app.js` navigation + `onSlideActivate` switch (table in §6).
4. Drop in `data.js` verbatim (copy full geoPoints from repo).
5. Implement `charts.js` (Chart.js charts first, then the custom canvas population chart).
6. Implement `maps.js` (6 initializers) + place both GeoJSON files in `assets/`.
7. Build the 5 RP slides + `rp-slides.css`.
8. Flesh out each slide's HTML content per §6 & live reference.
9. Wire fonts + Leaflet/Chart.js CDN tags in correct order.
10. Verify on a local server, then deploy to `main` for GitHub Pages.
