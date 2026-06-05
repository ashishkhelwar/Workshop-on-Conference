// ============================================================
//  PRESENTATION NAVIGATION & ANIMATION CONTROLLER
// ============================================================

const slides = [];
let current = 0;
// mapsInitialized is declared in maps.js as window.mapsInitialized


// ── Collect slides after DOM ready ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.slide:not(.slide--hidden)').forEach(s => slides.push(s));
  // Set first slide active
  if (slides.length > 0) {
    slides[0].classList.add('active');
    document.getElementById('slideNum').textContent = `1 / ${slides.length}`;
    onSlideActivate(0);
  }
});

// ── Navigation ───────────────────────────────────────────────────────────
function goTo(n) {
  if (slides.length === 0) return;
  const prev = current;
  const next = Math.max(0, Math.min(n, slides.length - 1));
  if (next === prev) return;

  slides[prev].classList.remove('active');
  slides[prev].classList.add('prev');
  setTimeout(() => slides[prev].classList.remove('prev'), 650);

  current = next;
  slides[current].classList.add('active');
  document.getElementById('slideNum').textContent = `${current + 1} / ${slides.length}`;
  onSlideActivate(current);
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') goTo(current + 1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   goTo(current - 1);
  if (e.key === 'f' || e.key === 'F') {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  }
  if (e.key === 'Home') goTo(0);
  if (e.key === 'End')  goTo(slides.length - 1);
});

// ── Count-up animation ───────────────────────────────────────────────────
function countUp(el, target, duration) {
  if (!el) return;
  duration = duration || 1500;
  const start = performance.now();
  const startVal = 0;

  function step(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const value = Math.round(startVal + (target - startVal) * eased);
    el.textContent = value;
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  }
  requestAnimationFrame(step);
}

// ── Human casualty inline bars animation ─────────────────────────────────
function animateHumanBars() {
  const maxVal = 16;
  document.querySelectorAll('.year-bar-fill').forEach(fill => {
    const val = parseInt(fill.dataset.val || 0, 10);
    const pct = (val / maxVal) * 100;
    fill.style.width = '0%';
    setTimeout(() => {
      fill.style.width = pct + '%';
    }, 200);
  });
}

// ── Slide activation handler ─────────────────────────────────────────────
function onSlideActivate(index) {
  const slideId = slides[index] ? slides[index].id : null;

  switch (index) {

    // Slide 1 — Title (no special init)
    case 0: break;

    // Slide 2 — Workshop Context
    case 1: {
      const kpis = slides[1].querySelectorAll('.kpi-value[data-count]');
      kpis.forEach(el => countUp(el, parseInt(el.dataset.count, 10)));
      break;
    }

    // Slides 3a–3e — Resource Persons Introduction (5 slides)
    case 2: case 3: case 4: case 5: case 6: break;

    // Slide 4 — Schedule (timeline, no special anim)
    case 7: break;

    // Slide 5 — Participants
    case 8: {
      const el = slides[8].querySelector('.hero-count');
      if (el) countUp(el, 48, 1800);
      break;
    }

    // Section Cover — Elephant Status & HEI
    case 9: break;

    // Slide 6a — Population
    case 10:
      setTimeout(() => initPopChart('popCanvas'), 300);
      break;

    // Slide 6b — Distribution Map
    case 11:
      setTimeout(() => initDistributionMap('distMap'), 300);
      break;

    // Slide 7 — Live Elephant GPS Tracking
    case 12:
      setTimeout(() => initCurrentElephantsMap('s7-live-map'), 300);
      break;

    // Slide 7b — Elephant Casualties
    case 13: {
      const el = slides[13].querySelector('.hero-count');
      if (el) countUp(el, 49, 1800);
      setTimeout(() => initYearBarsChart('yearBarsCanvas'), 400);
      break;
    }

    // Slide 8 — Cause of Death
    case 14:
      setTimeout(() => initCauseChart('causeCanvas'), 300);
      break;

    // Slide 9a — Age Group
    case 15:
      setTimeout(() => initAgeChart('ageCanvas'), 300);
      break;

    // Slide 9b — Sex Group
    case 16:
      setTimeout(() => initSexChart('sexCanvas'), 300);
      break;

    // Slide 9b-Drown — Drowning Cases map
    case 17:
      setTimeout(() => initDrownMap('drownMap'), 300);
      break;

    // Slide 9drown-PM — Drowning PM & Lab Report Analysis
    case 18: break;

    // Slide 9c — Seasonal
    case 19:
      setTimeout(() => initSeasonalChart('seasonCanvas'), 300);
      break;

    // Slide 9c-cause — Season-wise Cause of Death
    case 20:
      setTimeout(() => {
        initSeasonDrownChart('seasonDrownCanvas');
        initSeasonElecChart('seasonElecCanvas');
      }, 300);
      break;

    // Slide 9d — Range-wise
    case 21:
      setTimeout(() => initRangeChart('rangeCanvas'), 300);
      break;

    // Slide 10 — Geo Casualty Map
    case 22:
      setTimeout(() => initCasualtyMap('casualtyMap'), 300);
      break;

    // Slide 11 — PM Report Summary (no special init)
    case 23: break;

    // Slide 13 — Lab Report (no special init)
    case 24: break;

    // Slide 14 — Gurda Case Photos & PM Report (no special init)
    case 25: break;

    // Slide 17 — Thank You
    case 26: break;

    default: break;
  }
}
