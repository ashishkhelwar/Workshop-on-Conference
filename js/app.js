// ============================================================
//  PRESENTATION NAVIGATION & ANIMATION CONTROLLER
// ============================================================

const slides = [];
let current = 0;
const chartsInitialized = new Set();
// mapsInitialized is declared in maps.js as window.mapsInitialized

// Spotlight state for Resource Persons slide
let spotlightInterval = null;
let spotlightIndex = 0;
let spotlightStopped = false;

// ── Collect slides after DOM ready ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.slide').forEach(s => slides.push(s));
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

// ── Spotlight / zoom-to-centre for Resource Persons (slide index 2) ─────
const s3backdrop  = () => document.getElementById('s3-backdrop');
const s3stage     = () => document.getElementById('s3-zoom-stage');
const s3CardWraps = () => Array.from(document.querySelectorAll(
  '#pFeatured, #pCard1, #pCard2, #pCard3, #pCard4'));

let s3pinned      = false;
let s3returnTimer = null;

function s3ZoomIn(idx) {
  const wraps = s3CardWraps();
  const wrap  = wraps[idx];
  if (!wrap) return;
  const card  = wrap.querySelector('.person-card');
  if (!card)  return;
  const rect  = card.getBoundingClientRect();

  // Populate zoom stage
  const stage = s3stage();
  stage.innerHTML = card.outerHTML;
  stage.style.cssText =
    `left:${rect.left}px;top:${rect.top}px;` +
    `width:${rect.width}px;height:${rect.height}px;` +
    `transform:scale(1);transition:none;`;
  stage.offsetHeight; // reflow

  // Dim others, mark active
  wraps.forEach((w, i) => {
    w.classList.toggle('dim',     i !== idx);
    w.classList.toggle('spotlit', i === idx);
  });

  s3backdrop().classList.add('visible');
  stage.classList.add('visible');

  // Compute translate to viewport centre + scale
  const cx    = rect.left + rect.width  / 2;
  const cy    = rect.top  + rect.height / 2;
  const dx    = window.innerWidth  / 2 - cx;
  const dy    = window.innerHeight / 2 - cy;
  const scale = Math.min((window.innerHeight * 0.6) / rect.height, 2.4);

  requestAnimationFrame(() => {
    stage.style.transition = 'transform .55s cubic-bezier(.22,1,.36,1)';
    stage.style.transform  = `translate(${dx}px,${dy}px) scale(${scale})`;
  });

  spotlightIndex = idx;
}

function s3ZoomOut(onDone) {
  const stage = s3stage();
  stage.style.transition = 'transform .45s cubic-bezier(.55,0,1,.45), opacity .3s ease';
  stage.style.transform  = 'scale(1)';
  s3backdrop().classList.remove('visible');
  setTimeout(() => {
    stage.classList.remove('visible');
    stage.innerHTML = '';
    s3CardWraps().forEach(w => w.classList.remove('dim', 'spotlit'));
    if (onDone) onDone();
  }, 460);
}

function startSpotlight() {
  spotlightStopped = false;
  s3pinned         = false;
  spotlightIndex   = -1;

  // Click-to-pin on card wraps
  s3CardWraps().forEach((wrap, i) => {
    wrap._s3Click = () => {
      if (s3pinned && spotlightIndex === i) return;
      s3pinned = true;
      clearInterval(spotlightInterval);
      if (s3returnTimer) { clearTimeout(s3returnTimer); s3returnTimer = null; }
      s3ZoomOut(() => s3ZoomIn(i));
    };
    wrap.addEventListener('click', wrap._s3Click);
  });

  // Click backdrop to release pin and resume
  s3backdrop()._s3Release = () => {
    if (!s3pinned) return;
    s3pinned = false;
    if (s3returnTimer) { clearTimeout(s3returnTimer); s3returnTimer = null; }
    s3ZoomOut(() => scheduleS3Next());
  };
  s3backdrop().addEventListener('click', s3backdrop()._s3Release);

  scheduleS3Advance();
}

function scheduleS3Advance() {
  clearInterval(spotlightInterval);
  spotlightInterval = null;
  s3Advance();
}

function scheduleS3Next() {
  spotlightInterval = setTimeout(s3Advance, 600);
}

function s3Advance() {
  const next = (spotlightIndex + 1) % 5;
  s3ZoomIn(next);
  if (s3returnTimer) clearTimeout(s3returnTimer);
  s3returnTimer = setTimeout(() => {
    s3ZoomOut(() => { if (!s3pinned) scheduleS3Next(); });
  }, 5000);
}

function stopSpotlight() {
  spotlightStopped = true;
  clearInterval(spotlightInterval);
  if (s3returnTimer) { clearTimeout(s3returnTimer); s3returnTimer = null; }

  // Remove listeners
  s3CardWraps().forEach(w => {
    if (w._s3Click) { w.removeEventListener('click', w._s3Click); delete w._s3Click; }
  });
  const bd = s3backdrop();
  if (bd && bd._s3Release) { bd.removeEventListener('click', bd._s3Release); delete bd._s3Release; }

  s3ZoomOut(null);
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

  // Stop spotlight if leaving slide 3
  if (index !== 2) stopSpotlight();

  switch (index) {

    // Slide 1 — Title (no special init)
    case 0: break;

    // Slide 2 — Workshop Context
    case 1: {
      const kpis = slides[1].querySelectorAll('.kpi-value[data-count]');
      kpis.forEach(el => countUp(el, parseInt(el.dataset.count, 10)));
      break;
    }

    // Slide 3 — Resource Persons
    case 2:
      setTimeout(startSpotlight, 600);
      break;

    // Slide 4 — Schedule (timeline, no special anim)
    case 3: break;

    // Slide 5 — Participants
    case 4: {
      const el = slides[4].querySelector('.hero-count');
      if (el) countUp(el, 48, 1800);
      break;
    }

    // Slide 6a — Population
    case 5:
      if (!chartsInitialized.has('popCanvas')) {
        chartsInitialized.add('popCanvas');
        setTimeout(() => initPopChart('popCanvas'), 300);
      }
      break;

    // Slide 6b — Distribution Map
    case 6:
      setTimeout(() => initDistributionMap('distMap'), 300);
      break;

    // Slide 7 — Elephant Casualty Total
    case 7: {
      const el = slides[7].querySelector('.hero-count');
      if (el) countUp(el, 41, 1800);
      if (!chartsInitialized.has('yearBarsCanvas')) {
        chartsInitialized.add('yearBarsCanvas');
        setTimeout(() => initYearBarsChart('yearBarsCanvas'), 400);
      }
      break;
    }

    // Slide 8 — Cause of Death
    case 8:
      if (!chartsInitialized.has('causeCanvas')) {
        chartsInitialized.add('causeCanvas');
        setTimeout(() => initCauseChart('causeCanvas'), 300);
      }
      break;

    // Slide 9a — Age Group
    case 9:
      if (!chartsInitialized.has('ageCanvas')) {
        chartsInitialized.add('ageCanvas');
        setTimeout(() => initAgeChart('ageCanvas'), 300);
      }
      break;

    // Slide 9b — Sex Group
    case 10:
      if (!chartsInitialized.has('sexCanvas')) {
        chartsInitialized.add('sexCanvas');
        setTimeout(() => initSexChart('sexCanvas'), 300);
      }
      break;

    // Slide 9c — Seasonal
    case 11:
      if (!chartsInitialized.has('seasonCanvas')) {
        chartsInitialized.add('seasonCanvas');
        setTimeout(() => initSeasonalChart('seasonCanvas'), 300);
      }
      break;

    // Slide 9d — Range-wise
    case 12:
      if (!chartsInitialized.has('rangeCanvas')) {
        chartsInitialized.add('rangeCanvas');
        setTimeout(() => initRangeChart('rangeCanvas'), 300);
      }
      break;

    // Slide 10 — Geo Casualty Map
    case 13:
      setTimeout(() => initCasualtyMap('casualtyMap'), 300);
      break;

    // Slide 11 — PM Report Summary (no special init)
    case 14: break;

    // Slide 12 — PM Analysis
    case 15:
      if (!chartsInitialized.has('trendCanvas')) {
        chartsInitialized.add('trendCanvas');
        setTimeout(() => initTrendChart('trendCanvas'), 300);
      }
      break;

    // Slide 13 — Lab Report (no special init)
    case 16: break;

    // Slide 14 — Conclusion (no special init)
    case 17: break;

    // Slide 15 — Human Casualty
    case 18: {
      const el = slides[18].querySelector('.hero-count');
      if (el) countUp(el, 45, 1800);
      setTimeout(animateHumanBars, 400);
      break;
    }

    // Slide 16 — Overlay Map
    case 19:
      setTimeout(() => initOverlayMap('overlayMap'), 300);
      break;

    // Slide 17 — Thank You
    case 20: break;

    default: break;
  }
}
