// Presentation navigation & animation controller

const slides = [];
let current = 0;
const chartsInitialized = new Set();
const mapsInitializedSlides = new Set();

// Spotlight state
let spotlightTimer = null;
let spotlightIdx = 0;
const SPOTLIGHT_DURATION = 5000;

function buildSlideList() {
  document.querySelectorAll('.slide').forEach(s => slides.push(s));
}

function goTo(n) {
  if (slides.length === 0) return;
  const prev = current;
  current = Math.max(0, Math.min(n, slides.length - 1));
  if (prev === current) return;

  slides[prev].classList.remove('active');
  slides[prev].classList.add('leaving');
  setTimeout(() => slides[prev].classList.remove('leaving'), 700);

  slides[current].classList.add('active');
  document.getElementById('slideNum').textContent = `${current + 1} / ${slides.length}`;
  onSlideActivate(current);
}

function onSlideActivate(idx) {
  const slide = slides[idx];
  const id = slide.id;

  // Trigger count-up for KPI numbers
  slide.querySelectorAll('[data-countup]').forEach(el => {
    const target = parseInt(el.dataset.countup, 10);
    countUp(el, target, 1600);
  });

  // Lazy chart init
  if (!chartsInitialized.has(id)) {
    chartsInitialized.add(id);
    switch (id) {
      case 's6a': initPopChart('popCanvas'); break;
      case 's7':  initYearBarsChart('yearBarsCanvas'); initTrendChart('trendMiniCanvas'); break;
      case 's8':  initCauseChart('causeCanvas'); break;
      case 's9a': initAgeChart('ageCanvas'); break;
      case 's9b': initSexChart('sexCanvas'); break;
      case 's9c': initSeasonalChart('seasonCanvas'); break;
      case 's9d': initRangeChart('rangeCanvas'); break;
      case 's12': initTrendChart('trendCanvas'); break;
      case 's15': initHumanBarsChart('humanBarsCanvas'); break;
    }
  }

  // Lazy map init
  if (!mapsInitializedSlides.has(id)) {
    mapsInitializedSlides.add(id);
    if (id === 's6b')  setTimeout(() => initDistributionMap('distMap'), 100);
    if (id === 's10')  setTimeout(() => initCasualtyMap('casualtyMap'), 100);
    if (id === 's16')  setTimeout(() => initOverlayMap('overlayMap'), 100);
  }

  // Spotlight for Resource Persons slide
  if (id === 's3') {
    startSpotlight();
  } else {
    stopSpotlight();
  }

  // Animate list items in report slides
  slide.querySelectorAll('.reveal-item').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, 200 + i * 150);
  });
}

// ── Count-up animation ──────────────────────────────────────────────────────

function countUp(el, target, duration) {
  const start = performance.now();
  const from = 0;
  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(from + (target - from) * eased);
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ── Spotlight animation ─────────────────────────────────────────────────────

function startSpotlight() {
  const cards = document.querySelectorAll('#s3 .person-card');
  if (!cards.length) return;
  spotlightIdx = 0;
  applySpotlight(cards, spotlightIdx);
  spotlightTimer = setInterval(() => {
    spotlightIdx = (spotlightIdx + 1) % cards.length;
    applySpotlight(cards, spotlightIdx);
  }, SPOTLIGHT_DURATION);

  cards.forEach((card, i) => {
    card.addEventListener('click', () => {
      stopSpotlight();
      applySpotlight(cards, i);
    });
  });
}

function applySpotlight(cards, activeIdx) {
  cards.forEach((card, i) => {
    card.classList.remove('spotlight', 'dim');
    if (i === activeIdx) card.classList.add('spotlight');
    else card.classList.add('dim');
  });
}

function stopSpotlight() {
  if (spotlightTimer) {
    clearInterval(spotlightTimer);
    spotlightTimer = null;
  }
}

// ── Dashboard tabs (slides 9a-9d) ───────────────────────────────────────────

function switchDashTab(tabId, slideId) {
  // Navigate to correct slide
  const targetIdx = slides.findIndex(s => s.id === slideId);
  if (targetIdx >= 0) goTo(targetIdx);
}

// ── Keyboard & init ─────────────────────────────────────────────────────────

document.addEventListener('keydown', e => {
  switch (e.key) {
    case 'ArrowRight':
    case 'ArrowDown':
    case ' ':
      e.preventDefault();
      goTo(current + 1);
      break;
    case 'ArrowLeft':
    case 'ArrowUp':
      e.preventDefault();
      goTo(current - 1);
      break;
    case 'f':
    case 'F':
      document.documentElement.requestFullscreen?.();
      break;
    case 'Home':
      goTo(0);
      break;
    case 'End':
      goTo(slides.length - 1);
      break;
  }
});

window.addEventListener('DOMContentLoaded', () => {
  buildSlideList();
  document.getElementById('slideNum').textContent = `1 / ${slides.length}`;
  onSlideActivate(0);

  // Touch/swipe support
  let touchStartX = 0;
  document.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
  document.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) goTo(current + (dx < 0 ? 1 : -1));
  });
});
