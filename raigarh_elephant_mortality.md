---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  :root {
    --forest:  #0F3D26;
    --blue:    #1A6EA8;
    --red:     #B02020;
    --gold:    #B8841E;
    --green:   #1E7E3E;
    --orange:  #B85A00;
    --grey:    #6B7A8D;
    --purple:  #6A2A8A;
    --cream:   #F6F7F9;
  }

  section {
    background: var(--cream);
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 18px;
    color: #1a1a1a;
    padding: 40px 56px;
  }

  /* ── Cover ── */
  section.cover {
    background: linear-gradient(145deg, #062014 0%, #0F3D26 60%, #0d2840 100%);
    color: #fff;
    justify-content: flex-end;
    padding-bottom: 60px;
  }
  section.cover h1 {
    font-size: 52px;
    font-weight: 900;
    color: #fff;
    border: none;
    margin-bottom: 12px;
    line-height: 1.1;
  }
  section.cover h1 span { color: #52B788; }
  section.cover p { color: rgba(255,255,255,0.65); font-size: 16px; }
  section.cover .stats {
    display: flex; gap: 24px; margin-top: 28px; flex-wrap: wrap;
  }
  section.cover .stat-box {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 10px;
    padding: 12px 20px;
    text-align: center;
    min-width: 110px;
  }
  section.cover .stat-box .val {
    font-size: 30px; font-weight: 900; display: block;
  }
  section.cover .stat-box .lbl {
    font-size: 10px; opacity: 0.6; text-transform: uppercase; letter-spacing: 0.6px;
  }
  section.cover footer { color: rgba(255,255,255,0.3); font-size: 12px; margin-top: 32px; }

  /* ── Section divider ── */
  section.divider {
    background: var(--forest);
    color: white;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.divider h2 { color: #52B788; border: none; font-size: 44px; }
  section.divider p  { color: rgba(255,255,255,0.55); font-size: 18px; }

  /* ── End ── */
  section.end {
    background: linear-gradient(145deg, #062014, #0F3D26);
    color: white;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.end h1 { color: #52B788; border: none; font-size: 54px; }
  section.end p  { color: rgba(255,255,255,0.6); font-size: 18px; }

  /* ── Headings ── */
  h1 { color: var(--forest); font-size: 34px; font-weight: 900; border-bottom: 3px solid #52B788; padding-bottom: 8px; margin-bottom: 20px; }
  h2 { color: var(--forest); font-size: 26px; font-weight: 800; margin-top: 0; }
  h3 { color: #333; font-size: 18px; font-weight: 700; margin: 10px 0 6px; }

  /* ── Tables ── */
  table { border-collapse: collapse; width: 100%; font-size: 14px; margin-top: 10px; }
  th    { background: var(--forest); color: white; padding: 8px 12px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 0.6px; }
  td    { padding: 6px 12px; border-bottom: 1px solid #ddd; }
  tr:nth-child(even) td { background: rgba(15,61,38,0.04); }

  /* ── Cause colours ── */
  .blue   { color: var(--blue);   font-weight: 700; }
  .red    { color: var(--red);    font-weight: 700; }
  .gold   { color: var(--gold);   font-weight: 700; }
  .green  { color: var(--green);  font-weight: 700; }
  .orange { color: var(--orange); font-weight: 700; }
  .grey   { color: var(--grey);   font-weight: 700; }
  .purple { color: var(--purple); font-weight: 700; }

  /* ── Alert boxes ── */
  .alert {
    border-radius: 8px; padding: 10px 16px;
    margin: 10px 0; font-size: 15px; font-weight: 600;
    display: flex; gap: 10px; align-items: flex-start;
  }
  .alert.red    { background: #fdecea; border-left: 4px solid var(--red);    color: #7a0000; }
  .alert.green  { background: #e8f5e9; border-left: 4px solid var(--green);  color: #0d3a13; }
  .alert.gold   { background: #fff8e1; border-left: 4px solid var(--gold);   color: #5a3c00; }
  .alert.blue   { background: #e3f2fd; border-left: 4px solid var(--blue);   color: #0a3460; }
  .alert.purple { background: #f3e5f5; border-left: 4px solid var(--purple); color: #3a0060; }

  /* ── Info cards ── */
  .card {
    background: white; border-radius: 10px;
    border: 1px solid #dde; padding: 12px 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }

  /* ── Grid helpers ── */
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }

  /* ── Progress-bar style for charts ── */
  .bar-row { display: flex; align-items: center; gap: 10px; margin: 6px 0; }
  .bar-label { width: 160px; font-size: 14px; font-weight: 600; flex-shrink: 0; }
  .bar-track { flex: 1; height: 16px; background: #e5e5e5; border-radius: 8px; overflow: hidden; }
  .bar-fill  { height: 100%; border-radius: 8px; }
  .bar-pct   { font-size: 13px; font-weight: 700; min-width: 80px; }

  /* ── Badge ── */
  .badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
  .badge.critical { background: #B02020; color: white; }
  .badge.high     { background: #E65100; color: white; }
  .badge.elevated { background: #F57F17; color: white; }
  .badge.neg      { background: #1E7E3E; color: white; }
  .badge.pos      { background: #B02020; color: white; }

  /* ── Priority items ── */
  .pri { display: flex; gap: 12px; align-items: flex-start; padding: 9px 12px; background: white; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 8px; }
  .pri-tag { min-width: 36px; height: 36px; border-radius: 7px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; color: white; flex-shrink: 0; }

  /* ── Paginator ── */
  section::after { color: rgba(15,61,38,0.4); font-size: 13px; }

  /* ── Footnote ── */
  .fn { font-size: 11px; color: #888; margin-top: 10px; font-style: italic; }
---

<!-- _class: cover -->

# Wild Elephant Mortality —<br><span style="color:#52B788">Complete Forensic Analysis</span>

**Raigarh + Dharamjaigarh Forest Divisions · Bilaspur Circle · Chhattisgarh**

Integrated analysis of 16 Post-Mortem reports · 12 forensic laboratory findings (ICAR-IVRI Izatnagar + NDVSU SWFH Jabalpur) · 558-compartment GIS overlay

<div class="stats">
<div class="stat-box"><span class="val" style="color:#52B788">18</span><span class="lbl">Elephant Deaths</span></div>
<div class="stat-box"><span class="val" style="color:#e07b54">9</span><span class="lbl">Human Deaths</span></div>
<div class="stat-box"><span class="val" style="color:#5bb3e8">20 mo</span><span class="lbl">Study Period</span></div>
<div class="stat-box"><span class="val" style="color:#f1c40f">₹48.25L</span><span class="lbl">Compensation</span></div>
<div class="stat-box"><span class="val" style="color:#ce9ef8">558</span><span class="lbl">Compartments</span></div>
</div>

<footer>CONFIDENTIAL · Raigarh Forest Division · Compiled 27 May 2026</footer>

---

# Executive Summary

<div class="grid2" style="margin-top:10px">

<div class="alert red">⚠️ <strong>83% of deaths</strong> from human-modified hazards — unsafe water bodies, unprotected power lines, one suspected snare.</div>

<div class="alert gold">☠️ <strong>Arsenic confirmed</strong> in Tamnar–Bangursiya water bodies — multi-organ damage discovered only via histopathology (Dec 2025).</div>

<div class="alert green">🔬 <strong>Zero viral/bacterial cause</strong> — EEHV-1, EMCV, all toxicology <strong>negative</strong> across 12 lab reports and 29+ samples.</div>

<div class="alert blue">🐘 <strong>61% calf mortality</strong> (11/18 calves ≤24 months) — every drowning victim was under 3 years old.</div>

<div class="alert purple">🚫 <strong>Electrocution preventable</strong> — electricity dept was notified the day before the Oct 2024 incident. PIL 89/2024 filed.</div>

<div class="alert green">✅ <strong>Intervention works</strong> — Dehardih pond clearance (10,620 m²) stopped all deaths at that site. Proven by DFO administrative record.</div>

</div>

---

# Complete Mortality Record — 18 Deaths (2021–2026)

| # | Date | Range | Location | Sex / Age | Cause | Lab |
|---|------|-------|----------|-----------|-------|-----|
| 1 | 20/11/2022 | Gharghoda | Amlidih | F · 10–12 yr | ⚡ Electrocution | Tox Neg |
| 2 | 09/12/2022 | Gharghoda | Pusalda | F · 1 yr | ⚡ Electrocution | Tox Neg |
| 3–5 | 26/10/2024 | Tamnar | Kachkoba | M+F · 65+55+2.5 yr | ⚡ Electrocution ×3 | Tox Neg |
| 6 | 31/12/2024 | Gharghoda | Deharidih | M · 2 yr calf | 💧 Drowning | Tox Neg |
| 7 | 14/01/2025 | Gharghoda | Karkatta Dam | F · 2–3 mo | 💧 Drowning | Tox Neg |
| 8 | 22/01/2025 | Gharghoda | Pankhatadam | F · 2 yr calf | 💧 Drowning | Tox Neg |
| 9 | 12/05/2025 | Gharghoda | Karkatta Nadi | F · 2–4 mo | 🦴 Head Trauma | Tox+HCN Neg |
| 10 | 25/05/2025 | Gharghoda | Karkatta Nadi | M · 5 mo | 💧 Drowning | Tox+HCN Neg |
| 11 | 20/10/2025 | Tamnar | Kerakhol East | M · 20 yr | ⚡ Electrocution | Pending |
| 12 | 25/11/2025 | Tamnar | Saraipali | M · 7 mo | 💧 Drowning | ⚠ **As+** |
| 13 | 20/12/2025 | Raigarh | Bangursiya | M · 4–6 mo | 💧 Drowning | ⚠ **As+ Pneumonia** |
| 14 | 28/01/2026 | Gharghoda | Kaya/Sakra Nala | M · 1 yr | 🪨 Fall/Injury | Pending |
| 15 | 21/02/2026 | Tamnar | Jhingol | F · calf | 🌿 Malnutrition | Pending |
| 16–17 | 11/03/2026 | Gharghoda | Kurkut Nadi | M+F · 2.5–3 yr | ❓ Under Inv. | Decomposed |
| 18 | 08/05/2026 | Chhal (DHJ) | Ghoghra Dam | M · 6 mo | 💧 Drowning | EEHV Neg |
| 19 | 11/05/2026 | Chhal (DHJ) | 511 RF Kerajharia | M · 5–6 mo | 💧 Drowning | EEHV Neg |
| 20 | 24/05/2026 | Chhal (DHJ) | Amamuda Talab | M · 1.5–2 yr | 💧 Drowning | Pending |

<p class="fn">💧 Drowning · ⚡ Electrocution · 🦴 Trauma · 🌿 Disease · ❓ Under Investigation · ⚠ As+ = Arsenic Positive</p>

---

# Cause of Death — Distribution

<div class="bar-row" style="margin-top:20px">
  <div class="bar-label">💧 Drowning</div>
  <div class="bar-track"><div class="bar-fill" style="width:55.6%;background:#1A6EA8"></div></div>
  <div class="bar-pct" style="color:#1A6EA8">10 deaths · 55.6%</div>
</div>
<p style="font-size:13px;margin:0 0 12px 172px;color:#555">All victims ≤3 yr · 8 water bodies · No toxin/virus found</p>

<div class="bar-row">
  <div class="bar-label">⚡ Electrocution</div>
  <div class="bar-track"><div class="bar-fill" style="width:38.9%;background:#B02020"></div></div>
  <div class="bar-pct" style="color:#B02020">7 deaths · 38.9%</div>
</div>
<p style="font-size:13px;margin:0 0 12px 172px;color:#555">4 incidents · Tamnar Range × 2 · Gharghoda × 2 · PIL 89/2024 filed</p>

<div class="bar-row">
  <div class="bar-label">❓ Under Inv.</div>
  <div class="bar-track"><div class="bar-fill" style="width:11.1%;background:#6B7A8D"></div></div>
  <div class="bar-pct" style="color:#6B7A8D">2 deaths · 11.1%</div>
</div>
<p style="font-size:13px;margin:0 0 12px 172px;color:#555">Kurkut Nadi · 106 cm circumferential neck ring · possible snare</p>

<div class="bar-row">
  <div class="bar-label">🦴 Head Trauma</div>
  <div class="bar-track"><div class="bar-fill" style="width:5.6%;background:#6A2A8A"></div></div>
  <div class="bar-pct" style="color:#6A2A8A">1 death · 5.6%</div>
</div>

<div class="bar-row">
  <div class="bar-label">🌿 Malnutrition</div>
  <div class="bar-track"><div class="bar-fill" style="width:5.6%;background:#1E7E3E"></div></div>
  <div class="bar-pct" style="color:#1E7E3E">1 death · 5.6%</div>
</div>

<div class="alert red" style="margin-top:18px">⚠️ <strong>83% of all deaths (15/18)</strong> are attributable to human-modified hazards. ZERO viral or conventional poisoning cause found in any lab.</div>

---

# Age Distribution — The Calf Catastrophe

<div class="bar-row" style="margin-top:20px">
  <div class="bar-label">Infant 0–6 mo</div>
  <div class="bar-track"><div class="bar-fill" style="width:38.9%;background:#B02020"></div></div>
  <div class="bar-pct" style="color:#B02020">7 deaths · 38.9%</div>
</div>
<div class="bar-row">
  <div class="bar-label">Calf 7–24 mo</div>
  <div class="bar-track"><div class="bar-fill" style="width:22.2%;background:#E65100"></div></div>
  <div class="bar-pct" style="color:#E65100">4 deaths · 22.2%</div>
</div>
<div class="bar-row">
  <div class="bar-label">Sub-adult 2–5 yr</div>
  <div class="bar-track"><div class="bar-fill" style="width:22.2%;background:#F57F17"></div></div>
  <div class="bar-pct" style="color:#F57F17">4 deaths · 22.2%</div>
</div>
<div class="bar-row">
  <div class="bar-label">Adult 5–30 yr</div>
  <div class="bar-track"><div class="bar-fill" style="width:5.6%;background:#1A6EA8"></div></div>
  <div class="bar-pct" style="color:#1A6EA8">1 death · 5.6%</div>
</div>
<div class="bar-row">
  <div class="bar-label">Senior 30+ yr</div>
  <div class="bar-track"><div class="bar-fill" style="width:11.1%;background:#6B7A8D"></div></div>
  <div class="bar-pct" style="color:#6B7A8D">2 deaths · 11.1%</div>
</div>

<div class="grid2" style="margin-top:18px">
<div class="alert red">🐘 <strong>61% of deaths (11/18)</strong> are calves ≤24 months. Median drowning age: <strong>6 months</strong>. Not one drowning victim was over 3 years old.</div>
<div class="alert blue">♂ Sex skew: <strong>70% of drowning victims are male calves</strong> — exploratory behaviour increases exposure to water hazards.</div>
</div>

---

# Seasonal Pattern — May Pulse &amp; Monsoon Silence

| Month | Deaths | Key Driver |
|-------|--------|-----------|
| January | 2 | ❄️ Winter drowning — water scarcity |
| February | 1 | ❄️ Winter drowning |
| March | 3 | Includes 2 under investigation |
| **May** | **5** | ☀️ **DEADLIEST — 27.8% of all deaths** |
| Jun–Sep | **0** | 🌧️ **Monsoon silence — zero deaths** |
| **October** | **4** | ⚡ **Electrocution peak (22.2%)** |
| November | 1 | Early dry season |
| December | 2 | Winter drowning begins |

<div class="grid2" style="margin-top:16px">
<div class="alert gold">☀️ <strong>May:</strong> Pre-monsoon pools shrink into steep muddy traps. Summer calving adds newborns. 5 deaths in 1 month.</div>
<div class="alert blue">⚡ <strong>October:</strong> Post-monsoon vegetation flush draws herds into power corridors. 4 electrocution deaths.</div>
</div>

<div class="alert green" style="margin-top:8px">💡 <strong>Zero deaths June–September (monsoon).</strong> Abundant dispersed water eliminates crowding at hazardous sites — proves the structural hazard theory.</div>

---

# The Evidence Chain: PM → Laboratory → Verdict

<div style="display:flex;gap:6px;align-items:stretch;margin:20px 0">
  <div class="card" style="flex:1;border-top:4px solid #1E7E3E;text-align:center">
    <div style="font-size:26px">📍</div>
    <h3 style="color:#1E7E3E;font-size:14px">① Death Found</h3>
    <p style="font-size:13px">Field staff report carcass location</p>
  </div>
  <div style="display:flex;align-items:center;color:#aaa;font-size:20px">→</div>
  <div class="card" style="flex:1;border-top:4px solid #1A6EA8;text-align:center">
    <div style="font-size:26px">🔍</div>
    <h3 style="color:#1A6EA8;font-size:14px">② Post-Mortem</h3>
    <p style="font-size:13px">Vet within hours · frothy fluid, burns, trauma</p>
  </div>
  <div style="display:flex;align-items:center;color:#aaa;font-size:20px">→</div>
  <div class="card" style="flex:1;border-top:4px solid #F57F17;text-align:center">
    <div style="font-size:26px">🧪</div>
    <h3 style="color:#F57F17;font-size:14px">③ Sample Collection</h3>
    <p style="font-size:13px">Formalin / salt / ice preservation</p>
  </div>
  <div style="display:flex;align-items:center;color:#aaa;font-size:20px">→</div>
  <div class="card" style="flex:1;border-top:4px solid #6A2A8A;text-align:center">
    <div style="font-size:26px">🏛️</div>
    <h3 style="color:#6A2A8A;font-size:14px">④ Lab Testing</h3>
    <p style="font-size:13px">ICAR-IVRI Izatnagar or NDVSU Jabalpur</p>
  </div>
  <div style="display:flex;align-items:center;color:#aaa;font-size:20px">→</div>
  <div class="card" style="flex:1;border-top:4px solid #B02020;text-align:center">
    <div style="font-size:26px">✅</div>
    <h3 style="color:#B02020;font-size:14px">⑤ Final Verdict</h3>
    <p style="font-size:13px">PM + Lab together = definitive cause</p>
  </div>
</div>

| PM Finding | Lab Adds | Combined Verdict |
|-----------|----------|-----------------|
| Frothy muddy airways | No toxin, no virus | **Drowning confirmed** |
| Burns on trunk/back | All tox negative | **Electrocution confirmed** |
| "Drowning" — Saraipali | **Arsenic POSITIVE** | Drowning + arsenic weakening |
| "Drowning" — Bangursiya | **Arsenic + Pneumonia** | Lab **changed** PM diagnosis |
| 5-6 day decomposed | Advanced autolysis | Diagnosis not possible → re-examine neck ring |

---

# Geographic Distribution — 558 Compartments

<div class="grid2" style="margin-top:10px">

<div>

| Range | Comps | 🐘 Deaths | Key Hazard |
|-------|-------|-----------|-----------|
| Gharghoda | 166 | **7** | Drowning zone — Karkatta, Pankhatadam |
| Tamnar | 159 | **6** | Electrocution corridor + Arsenic |
| Raigarh | 162 | **2** | Bangursiya — Arsenic + Pneumonia |
| Kharsiya | 71 | 0 | 2 human deaths only |
| Chhal (DHJ) | — | **3** | New cluster May 2026 |

</div>

<div>

**Water Body Risk Index**

| Rank | Water Body | Deaths | Arsenic | Tier |
|------|-----------|--------|---------|------|
| 1 | Bangursiya Pond | 2 | ✅ YES | <span class="badge critical">Critical</span> |
| 2 | Karkatta Nadi | 3 | — | <span class="badge critical">Critical</span> |
| 3 | Saraipali | 1 | ✅ YES | <span class="badge high">High</span> |
| 4 | Kurkut Nadi | 2 | — | <span class="badge high">High</span> |
| 5 | Pankhatadam | 2 | — | <span class="badge high">High</span> |
| 6–8 | Chhal DHJ × 3 | 1 each | — | <span class="badge elevated">Elevated</span> |

</div>

</div>

<div class="alert green" style="margin-top:12px">✅ <strong>Proven:</strong> Dehardih clearance (10,620 m² aquatic vegetation) → zero further calf deaths at that site. Documented in DFO Raigarh administrative letter.</div>

---

# Drowning — Root Cause Analysis

<div class="grid3" style="margin-top:16px">

<div class="card" style="border-top:4px solid #1A6EA8">
  <h3 style="color:#1A6EA8">💧 Proximate Mechanism</h3>
  <ul style="font-size:14px">
    <li>Muddy water → bronchi/alveoli</li>
    <li>Asphyxia → cardiac arrest</li>
    <li>PM: frothy fluid, sand in airways, stomach full of mud</li>
    <li>Bladder voiding at death</li>
    <li>Confirmed in all 10 drowning cases</li>
  </ul>
</div>

<div class="card" style="border-top:4px solid #E65100">
  <h3 style="color:#E65100">🏗️ Structural Hazard</h3>
  <ul style="font-size:14px">
    <li>Steep / vertical pond banks</li>
    <li>Deep muddy bottoms trap calf limbs</li>
    <li>Pre-monsoon shrinkage removes egress</li>
    <li>No escape ledges or ramps</li>
    <li>Calves physically too short to self-extract</li>
  </ul>
</div>

<div class="card" style="border-top:4px solid #B02020">
  <h3 style="color:#B02020">⚙️ Why Calves — Not Adults</h3>
  <ul style="font-size:14px">
    <li>📏 Height: calf 0.8–1.2 m vs adult 2.5 m</li>
    <li>💪 Mud traps calf; adult mass frees itself</li>
    <li>🧭 Male calves explore further (70% victims)</li>
    <li>☠️ Calves absorb more arsenic per kg</li>
    <li>⚠️ Ramps must be calf-scaled ≤1:4 slope</li>
  </ul>
</div>

</div>

<div class="alert red" style="margin-top:16px">🚫 <strong>Systemic failure:</strong> Water bodies not designed for wildlife egress · No early monitoring at ranked sites · Reactive (post-mortem) not preventive · Dehardih model not replicated elsewhere.</div>

---

# Electrocution — Negligence-Linked Pattern

<div class="grid2" style="margin-top:12px">

<div class="card" style="border-left:5px solid #B02020">
  <h3 style="color:#B02020">⚡ Incident 1 — 26 Oct 2024 · Kachkoba, Tamnar</h3>
  <span class="badge critical">3 DEATHS</span>
  <ul style="font-size:14px;margin-top:8px">
    <li>Makna ♂ 65 yr · Female ♀ 55 yr · Calf ♀ 2.5 yr</li>
    <li>PM: Trunk burn 25×10×1.5 cm · Unclotted tarry blood</li>
    <li>11 kV wire broken on ground — below standard 3.45 m</li>
    <li><strong style="color:#B02020">Electricity dept notified the day before — failed to act</strong></li>
    <li>2 field staff suspended · PIL 89/2024 filed</li>
  </ul>
</div>

<div class="card" style="border-left:5px solid #B02020">
  <h3 style="color:#B02020">⚡ Incident 2 — 20 Oct 2025 · Kerakhol East, Tamnar</h3>
  <span class="badge critical">1 DEATH</span>
  <ul style="font-size:14px;margin-top:8px">
    <li>Male ♂ 25 yr · 3,200 kg</li>
    <li>PM: 110 cm burn mark on back/arm — longest documented</li>
    <li>Empty heart chambers · Multi-organ haemorrhage</li>
    <li><strong style="color:#B02020">Recurred in same range — 12 months after PIL + suspension</strong></li>
    <li>No permanent infrastructure fix made</li>
  </ul>
</div>

</div>

<div class="alert red" style="margin-top:16px">🔺 <strong>Critical pattern:</strong> PIL 89/2024, staff suspension and formal notification did NOT prevent recurrence. Total: <strong>7 electrocution deaths across 4 incidents</strong> in Raigarh Van Mandal. Permanent power-line rectification is the only solution.</div>

---

# Arsenic Contamination — The Hidden Threat

<div class="grid2" style="margin-top:10px">

<div class="card" style="border-top:4px solid #B8841E">
  <h3 style="color:#B8841E">Case 10 — Saraipali, Tamnar · 25/11/2025</h3>
  <p style="font-size:13px">♂ Male calf · 7 months · ICAR-IVRI CAD-1274/25-26</p>
  <ul style="font-size:13px">
    <li><strong>Histopathology:</strong> Liver — mild hepatocyte degeneration</li>
    <li><strong class="pos">Toxicology: ARSENIC POSITIVE</strong> (qualitative)</li>
    <li>Lab note: "Indicative of arsenic contaminant water/feed"</li>
    <li>PM diagnosis: drowning → <em>lab added arsenic exposure</em></li>
  </ul>
</div>

<div class="card" style="border-top:4px solid #B02020">
  <h3 style="color:#B02020">Case 11 — Bangursiya Pond, Raigarh · 20/12/2025</h3>
  <p style="font-size:13px">♂ Male calf · 4–6 months · ICAR-IVRI</p>
  <ul style="font-size:13px">
    <li>Liver — engorged sinusoids + haemorrhages</li>
    <li>Kidney — engorged glomeruli + haemorrhages</li>
    <li>Brain — <strong>neuronal degeneration + neuronophagia</strong> (arsenic encephalopathy)</li>
    <li><strong class="pos">Arsenic POSITIVE</strong> · EEHV Neg · No pathogens</li>
    <li><strong style="color:#B02020">Diagnosis: ACUTE PNEUMONIA — Lab changed PM diagnosis</strong></li>
  </ul>
</div>

</div>

<div class="alert gold" style="margin-top:12px">⛏️ <strong>Likely source — Raigarh coal belt:</strong> Fly-ash pond leachate · Geogenic arsenic in groundwater · Legacy arsenical pesticide runoff at forest edges. Same water bodies used by cattle and villages — public health risk.</div>
<div class="alert red" style="margin-top:6px">🚨 <strong>URGENT:</strong> Arsenic + heavy-metal water survey of ALL elephant water bodies in Tamnar–Bangursiya corridor. Escalate to State PCB + District Health immediately.</div>

---

# Complete Forensic Laboratory Register — 12 Reports

<div class="grid3" style="margin-top:10px">

<div class="card" style="border-left:4px solid #1E7E3E">
  <h3 style="color:#1E7E3E">☠️ Toxicology</h3>
  <p style="font-size:13px">13 cases tested (nitrate, metals, insecticides)</p>
  <p><span class="badge neg">ALL NEGATIVE</span></p>
  <p style="font-size:13px">No poisoning in any case</p>
</div>

<div class="card" style="border-left:4px solid #1E7E3E">
  <h3 style="color:#1E7E3E">🌿 HCN / Cyanide</h3>
  <p style="font-size:13px">4 cases · From May 2025</p>
  <p><span class="badge neg">ALL NEGATIVE</span></p>
  <p style="font-size:13px">Bamboo cyanide ruled out</p>
</div>

<div class="card" style="border-left:4px solid #1E7E3E">
  <h3 style="color:#1E7E3E">🦠 EEHV-1 PCR</h3>
  <p style="font-size:13px">7 cases — ICAR-IVRI + NDVSU</p>
  <p><span class="badge neg">ALL NEGATIVE</span></p>
  <p style="font-size:13px">No herpesvirus epidemic</p>
</div>

<div class="card" style="border-left:4px solid #1E7E3E">
  <h3 style="color:#1E7E3E">❤️ EMCV RT-PCR</h3>
  <p style="font-size:13px">2 cases · From Mar 2026</p>
  <p><span class="badge neg">ALL NEGATIVE</span></p>
  <p style="font-size:13px">Cardiac virus ruled out</p>
</div>

<div class="card" style="border-left:4px solid #B02020">
  <h3 style="color:#B02020">🔬 Histopathology</h3>
  <p style="font-size:13px">4 cases · From Dec 2025</p>
  <p><span class="badge pos">ARSENIC + PNEUMONIA</span></p>
  <p style="font-size:13px;color:#B02020;font-weight:600">Lab changed PM diagnosis</p>
</div>

<div class="card" style="border-left:4px solid #1E7E3E">
  <h3 style="color:#1E7E3E">🧫 Bacteriology</h3>
  <p style="font-size:13px">2 cases · Heart blood culture</p>
  <p><span class="badge neg">NO PATHOGENS</span></p>
  <p style="font-size:13px">No bacterial sepsis</p>
</div>

</div>

**Panel evolution:** Feb 2025: Tox only → Jul 2025: +HCN → **Dec 2025: +Histopath+EEHV+Bacteriology (arsenic discovered)** → Mar 2026: +EMCV → May 2026: NDVSU PCR

---

# Dharamjaigarh Cluster — 3 Deaths in 16 Days (May 2026)

<div class="grid3" style="margin-top:12px">

<div class="card" style="border-top:4px solid #E65100">
  <h3 style="color:#E65100">Case 16 · 08 May 2026</h3>
  <p style="font-size:13px">📍 Ghoghra Dam · 502 RF · <code>N 22°08'46" E 83°12'43"</code></p>
  <ul style="font-size:13px">
    <li>♂ Male calf · ~6 months · ~350 kg</li>
    <li>Brownish muddy fluid + sand in trachea</li>
    <li>Frothy muddy water in bronchi/alveoli</li>
    <li>Stomach full of muddy water + sand</li>
    <li><span class="badge neg">EEHV-1 NEGATIVE</span> · NDVSU (7-day turnaround)</li>
  </ul>
  <p style="color:#1A6EA8;font-weight:700;font-size:14px">VERDICT: DROWNING</p>
</div>

<div class="card" style="border-top:4px solid #E65100">
  <h3 style="color:#E65100">Case 17 · 11 May 2026</h3>
  <p style="font-size:13px">📍 511 RF Kerajharia · <code>N 22°09'56" E 83°06'58"</code></p>
  <ul style="font-size:13px">
    <li>♂ Male calf · 5–6 months · ~250 kg</li>
    <li>Tongue protruded · Blood+fluid from mouth</li>
    <li>Mud in both eyes · Muddy fluid in trachea</li>
    <li>Fluid + sand in lungs</li>
    <li><span class="badge neg">EEHV-1 NEGATIVE</span> · NDVSU</li>
  </ul>
  <p style="color:#1A6EA8;font-weight:700;font-size:14px">VERDICT: DROWNING</p>
</div>

<div class="card" style="border-top:4px solid #B02020">
  <h3 style="color:#B02020">Case 18 · 24 May 2026 ⚠️</h3>
  <p style="font-size:13px">📍 Amamuda Talab · <code>N 22°06'00" E 83°09'31"</code></p>
  <ul style="font-size:13px">
    <li>♂ Male calf · 1.5–2 yr · ~475 kg</li>
    <li>Heart <strong>completely empty</strong></li>
    <li>Intestinal haemorrhages · Liver inflamed</li>
    <li>Kidney haemorrhages · Vocal cord inflammation</li>
    <li><strong style="color:#B02020">Lab pending — arsenic testing recommended</strong></li>
  </ul>
  <p style="color:#1A6EA8;font-weight:700;font-size:14px">VERDICT: DROWNING</p>
</div>

</div>

<div class="alert red" style="margin-top:14px">🗺️ <strong>3 GPS-confirmed distinct water bodies · 3 male calves · 16 days · EEHV-1 negative ×2.</strong> Confirmed range-wide structural water hazard in Chhal Range.</div>

---

# Human Deaths — 5-Year Official Record

<div class="grid2" style="margin-top:10px">

<div>

| Year | Range | Beat | Notes |
|------|-------|------|-------|
| 2021-22 | Tamnar | Samaruma | — |
| 2022-23 | Gharghoda | Porha | — |
| 2022-23 | Gharghoda | Baturakchhar | Property dmg ₹25K |
| 2022-23 | Kharsiya | Kafarmar | — |
| 2023-24 | Raigarh | Kantajhariya | — |
| 2024-25 | Tamnar | Jhingol | — |
| 2024-25 | Kharsiya | Tendumuri | — |
| 2024-25 | Gharghoda | Baroud | — |
| 2025-26 | Gharghoda | Deharidih | — |
| **TOTAL** | **9 deaths** | ₹48.25L | ₹6L/death std. |

</div>

<div style="display:flex;flex-direction:column;gap:12px">

<div class="card" style="border-left:4px solid #B85A00">
  <h3 style="color:#B85A00;font-size:16px">Key Observations</h3>
  <ul style="font-size:14px">
    <li>All deaths GPS-tagged in official record</li>
    <li>Deaths at elephant-human interface zones</li>
    <li>Kharsiya: 2 human deaths, 0 elephant deaths</li>
    <li>Compensation: ₹6 Lakh per death (standard)</li>
    <li>₹48.25L vs expected ₹54L — one entry is property damage</li>
  </ul>
</div>

<div class="alert orange">👤 Human-elephant conflict extends beyond core elephant mortality zones. Kharsiya Range has no elephant deaths but 2 human fatalities.</div>

</div>

</div>

---

# GIS Compartment Map — 558 Forest Compartments

<div class="grid2" style="margin-top:10px">

<div>

**Range breakdown — 558 total compartments**

| Range | Compartments | 🐘 Deaths | 👤 Human |
|-------|-------------|-----------|---------|
| Gharghoda | 166 | 7 | 3 |
| Raigarh | 162 | 2 | 1 |
| Tamnar | 159 | 6 | 2 |
| Kharsiya | 71 | 0 | 2 |
| **Total** | **558** | **15** | **8** |

*Chhal (DHJ): 3 additional deaths, not in above count*

</div>

<div>

**Key beats highlighted by death cause**

| Beat | Cause | Deaths |
|------|-------|--------|
| Kachkoba | ⚡ Electrocution | 3 |
| Kerakhol East | ⚡ Electrocution | 1 |
| Chhartatangar | ⚡ / ❓ Investigation | 2 |
| Deharidih/Charmar | 💧 Drowning | 3+ |
| Saraipali | 💧 + ⚠️ Arsenic | 1 |
| Bangursiya E+W | 💧 + ⚠️ Arsenic | 2 |
| Kaya/Sakra Nala | 🪨 Trauma/Fall | 1 |
| Jhingol | 🌿 Malnutrition | 1 |

</div>

</div>

---

# Forensic Quality Audit

<div class="grid2" style="margin-top:12px">

<div>

## ✅ Strengths

- **Dual-lab corroboration** — ICAR-IVRI Izatnagar + NDVSU SWFH Jabalpur (two independent national reference labs)
- **Panel expanded over 15 months** — Tox → HCN → Histopath+EEHV → EMCV
- **7-day turnaround** — Chhal EEHV-1 results (PM 08/05 → Result 15/05/2026)
- **Chain of custody** — Sealed samples, GPS in 2026 cases, multiple officer signatures
- **Physical intervention documented** — Dehardih clearance stopped deaths at site

</div>

<div>

## ⚠️ Gaps to Fix

- **Histopathology only from Dec 2025** — arsenic missed for a full year (Cases 1–9)
- **No retrospective arsenic screening** — archived formalin blocks from Cases 1–9 exist but untested
- **Decomposition defeated diagnosis** — Kurkut cases (5–6 days old) too advanced for histopathology
- **106 cm neck ring unresolved** — Case 13 needs physical forensic re-examination
- **No water/soil sampling** — arsenic source unconfirmed; no environmental samples collected

</div>

</div>

**Target KPIs:** 0 calf drownings at intervened sites · 100% PMs with histopathology + arsenic · <48hr carcass-to-PM · ≥6 m power line clearance in corridors

---

# Why This Is NOT a Disease Problem

<div class="alert green" style="font-size:16px;margin-bottom:16px">🔬 <strong>ZERO</strong> viral disease · <strong>ZERO</strong> bacterial pathogen · <strong>ZERO</strong> conventional poison · <strong>ZERO</strong> HCN · <strong>ZERO</strong> EEHV · <strong>ZERO</strong> EMCV — across <strong>12 lab reports and 29+ samples (Feb 2025 – May 2026)</strong></div>

<div class="grid3">

<div class="card" style="border-top:4px solid #B02020">
  <h3 style="color:#B02020">Would disease explain it?</h3>
  <ul style="font-size:13px">
    <li>EEHV-1 (deadliest elephant virus): <span class="badge neg">NEGATIVE</span></li>
    <li>EMCV (cardiac virus): <span class="badge neg">NEGATIVE</span></li>
    <li>No bacteria in heart blood</li>
    <li>Uniform PM pathology across 2 divisions</li>
  </ul>
</div>

<div class="card" style="border-top:4px solid #E65100">
  <h3 style="color:#E65100">Would poisoning explain it?</h3>
  <ul style="font-size:13px">
    <li>HCN (bamboo cyanide): <span class="badge neg">NEGATIVE</span></li>
    <li>Pesticides/insecticides: <span class="badge neg">NEGATIVE</span></li>
    <li>Nitrate-nitrite: <span class="badge neg">NEGATIVE</span></li>
    <li>Heavy metals (excl. arsenic): <span class="badge neg">NEGATIVE</span></li>
  </ul>
</div>

<div class="card" style="border-top:4px solid #1E7E3E">
  <h3 style="color:#1E7E3E">What DOES explain it?</h3>
  <ul style="font-size:13px">
    <li>PM frothy muddy water = <strong>drowning</strong></li>
    <li>Burns + dark unclotted blood = <strong>electrocution</strong></li>
    <li>Structural water hazards = <strong>calf traps</strong></li>
    <li>Unprotected 11 kV wires = <strong>electrocution risk</strong></li>
  </ul>
</div>

</div>

<div class="alert green" style="margin-top:14px">✅ <strong>Dehardih dam — forest dept cleared 10,620 m² → NO FURTHER CALF DEATHS at that site.</strong> The same approach, at scale, stops the deaths.</div>

---

# Prioritised Action Matrix — P1 to P4

<div class="pri" style="margin-top:16px">
  <div class="pri-tag" style="background:#B02020">P1</div>
  <div><strong style="color:#B02020">Arsenic water survey</strong> &nbsp;<span class="badge critical">IMMEDIATE</span> &nbsp; Forest + PCB + Health<br><span style="font-size:14px">Sample all elephant-use water bodies. Repeat Feb–May dry-down. Escalate to State PCB + District Health — livestock + public health risk.</span></div>
</div>

<div class="pri">
  <div class="pri-tag" style="background:#E65100">P2</div>
  <div><strong style="color:#E65100">Calf-scaled egress ramps at top-4 water bodies</strong> &nbsp;<span class="badge high">Pre-monsoon 2026</span> &nbsp; Forest Division<br><span style="font-size:14px">≤1:4 gradient ramps + firm substrate at Bangursiya, Karkatta, Saraipali, Kurkut. Must be calf-scaled (0.8 m height). Replicate Dehardih model.</span></div>
</div>

<div class="pri">
  <div class="pri-tag" style="background:#F57F17">P3</div>
  <div><strong style="color:#B8841E">Power-line audit &amp; rectification — Tamnar corridor</strong> &nbsp;<span class="badge high">Before Oct 2026</span> &nbsp; Forest + CSPDCL<br><span style="font-size:14px">Audit all 11 kV lines through elephant corridors. Enforce ≥6 m clearance or underground/insulation. Bind electricity dept under PIL 89/2024.</span></div>
</div>

<div class="pri">
  <div class="pri-tag" style="background:#1E7E3E">P4</div>
  <div><strong style="color:#1E7E3E">May–October intensive patrol protocol</strong> &nbsp;<span class="badge elevated">Annual Seasonal</span> &nbsp; Range Offices<br><span style="font-size:14px">Daily monitoring at ranked water bodies and power corridors in peak-death windows. Calf-rescue rapid-response teams on standby.</span></div>
</div>

---

# Prioritised Action Matrix — P5 to P8

<div class="pri" style="margin-top:16px">
  <div class="pri-tag" style="background:#1A6EA8">P5</div>
  <div><strong style="color:#1A6EA8">Mandatory histopathology + arsenic for every PM</strong> &nbsp;<span class="badge critical">IMMEDIATE</span> &nbsp; Vet Services<br><span style="font-size:14px">Standardise Dec 2025 expanded panel for ALL future cases. Retrospectively test archived formalin blocks from Cases 1–9 and 16–18.</span></div>
</div>

<div class="pri">
  <div class="pri-tag" style="background:#6A2A8A">P6</div>
  <div><strong style="color:#6A2A8A">Criminal re-investigation — Kurkut Nadi 106 cm neck ring</strong> &nbsp;<span class="badge critical">IMMEDIATE</span> &nbsp; Forest + WCCB<br><span style="font-size:14px">Physical forensic re-examination of Case 13 neck mark photographs. Sweep Comp 1273 RF for wire snares. Treat as potential wildlife crime until excluded.</span></div>
</div>

<div class="pri">
  <div class="pri-tag" style="background:#00796B">P7</div>
  <div><strong>Carcass rapid-detection &amp; cold-transport</strong> &nbsp;<span class="badge elevated">6 Months</span> &nbsp; Forest Division<br><span style="font-size:14px">Camera-trap + informer network at ranked sites. Portable refrigeration for samples. Target &lt;48 hr detection-to-PM to prevent decomposition blocking diagnosis.</span></div>
</div>

<div class="pri">
  <div class="pri-tag" style="background:#2c3e50">P8</div>
  <div><strong>Herd-level census &amp; calf survivorship study</strong> &nbsp;<span style="background:#607D8B;color:white;padding:2px 9px;border-radius:20px;font-size:11px;font-weight:700">12 Months</span> &nbsp; Forest + Research<br><span style="font-size:14px">Establish baseline herd structure. Quantify population impact of 11 lost calves. Track calving sites. Identify herds with calves for targeted water protection.</span></div>
</div>

<p style="font-size:14px;margin-top:10px;font-weight:600">Priority: <span style="color:#B02020">P1–P3 = before Oct 2026 (critical)</span> · <span style="color:#E65100">P4–P6 = immediate</span> · <span style="color:#1A6EA8">P7–P8 = within 12 months</span></p>

---

# Concluding Assessment

> *"18 wild elephants died in 20 months — an annualised rate of 11.4 deaths/year. Every dominant cause is preventable. The Dehardih pond clearance proved it: when the Forest Dept acts on a specific hazard, deaths at that site stop."*

<div style="display:flex;flex-direction:column;gap:8px;margin-top:16px">

<div class="alert red">⚠️ <strong>83% of deaths</strong> from human-modified hazards — unsafe water bodies, unprotected power lines, one suspected snare.</div>

<div class="alert green">🔬 <strong>Zero viral / bacterial / chemical cause</strong> — 12 lab reports, 29+ samples. No epidemic. EEHV negative. The herd is safe from infectious disease.</div>

<div class="alert gold">☠️ <strong>Arsenic contamination confirmed</strong> — urgent water-quality and public-health escalation needed beyond the Forest Dept alone.</div>

<div class="alert red">🐘 <strong>61% calf mortality</strong> — 11 lost calves in 20 months will echo through herd demographics for decades. A generational reproductive crisis.</div>

<div class="alert green">✅ <strong>Drowning IS preventable.</strong> Calf-scaled egress ramps + aquatic vegetation clearance + pre-monsoon patrol = the solution. It has already been proven at Dehardih.</div>

</div>

<p style="font-size:12px;color:#888;margin-top:12px">Sources: PM Reports POR 4950/01 et al. · ICAR-IVRI CAD-1309/24-25, CAD-474/24-25, CAD-1274/25-26, CAD-1671/2025-26 · NDVSU No.251 &amp; 252/SWFH · DFO Raigarh administrative letter · PIL No.89/2024</p>

---

<!-- _class: end -->

# Thank You

## Questions &amp; Discussion

---

**Raigarh Forest Division + Dharamjaigarh Forest Division**
Bilaspur Circle · Chhattisgarh

*ICAR-IVRI Centre for Wildlife, Izatnagar*
*NDVSU School of Wildlife Forensic &amp; Health, Jabalpur*

Compiled: 27 May 2026 · CONFIDENTIAL
