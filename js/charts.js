// Chart.js initializers — all lazy, called from app.js onSlideActivate

Chart.defaults.color = '#8BA098';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.font.family = "system-ui, -apple-system, sans-serif";

// Global plugin: draw value labels on all charts
const valueLabelPlugin = {
  id: 'valueLabels',
  afterDatasetsDraw(chart) {
    const { ctx, data } = chart;
    const isHBar = chart.options.indexAxis === 'y';
    data.datasets.forEach((ds, di) => {
      if (ds._noLabels) return;
      const meta = chart.getDatasetMeta(di);
      if (meta.hidden) return;
      meta.data.forEach((el, i) => {
        const val = ds.data[i];
        if (val === null || val === undefined || val === 0) return;
        ctx.save();
        ctx.fillStyle = '#E8F0E8';
        ctx.font = 'bold 11px system-ui,-apple-system,sans-serif';
        if (isHBar) {
          ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
          ctx.fillText(val, el.x + 5, el.y);
        } else if (chart.config.type === 'line') {
          ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
          ctx.fillText(val, el.x, el.y - 8);
        } else {
          ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
          ctx.fillText(val, el.x, el.y - 4);
        }
        ctx.restore();
      });
    });
  }
};
Chart.register(valueLabelPlugin);

const chartInstances = {};

function destroyChart(id) {
  if (chartInstances[id]) {
    chartInstances[id].destroy();
    delete chartInstances[id];
  }
}

// ── 1. Trend Chart: elephant + human deaths by year ───────────────────────
function initTrendChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);

  let drawProgress = 0;

  // Clip plugin: reveals both lines from left to right
  const drawClipPlugin = {
    id: 'trendDrawClip',
    beforeDatasetsDraw(chart) {
      const { ctx: c, chartArea } = chart;
      if (!chartArea) return;
      c.save();
      c.beginPath();
      c.rect(
        chartArea.left,
        chartArea.top - 10,
        (chartArea.right - chartArea.left) * drawProgress,
        chartArea.bottom - chartArea.top + 20
      );
      c.clip();
    },
    afterDatasetsDraw(chart) {
      chart.ctx.restore();
    }
  };

  chartInstances[id] = new Chart(ctx, {
    type: 'line',
    plugins: [drawClipPlugin],
    data: {
      labels: DATA.years,
      datasets: [
        {
          label: 'Elephant Deaths',
          data: DATA.elephantDeaths,
          borderColor: '#52B788',
          backgroundColor: 'rgba(82,183,136,0.12)',
          borderWidth: 3,
          pointBackgroundColor: '#52B788',
          pointRadius: 6,
          pointHoverRadius: 9,
          tension: 0.35,
          fill: true
        },
        {
          label: 'Human Deaths',
          data: DATA.humanDeaths,
          borderColor: '#E63946',
          backgroundColor: 'rgba(230,57,70,0.08)',
          borderWidth: 3,
          pointBackgroundColor: '#E63946',
          pointRadius: 6,
          pointHoverRadius: 9,
          tension: 0.35,
          fill: true
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 400 },
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          position: 'top',
          labels: { color: '#8BA098', padding: 20, usePointStyle: true, pointStyleWidth: 10 }
        },
        tooltip: {
          backgroundColor: 'rgba(17,34,64,0.95)',
          titleColor: '#E8F0E8',
          bodyColor: '#8BA098',
          borderColor: 'rgba(82,183,136,0.3)',
          borderWidth: 1,
          padding: 12
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098' }
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098', stepSize: 4 },
          beginAtZero: true, max: 20
        }
      }
    }
  });

  // Smooth left-to-right draw over 3.5 seconds, starting after initial render
  const chart = chartInstances[id];
  const drawDuration = 3500;
  let drawStart = null;
  function animateDraw(now) {
    if (!drawStart) drawStart = now;
    drawProgress = Math.min((now - drawStart) / drawDuration, 1);
    chart.update('none');
    if (drawProgress < 1) requestAnimationFrame(animateDraw);
  }
  setTimeout(() => requestAnimationFrame(animateDraw), 450);
}

// ── 2. Liquid Fill Bar Chart: elephant deaths per year ────────────────────
function initYearBarsChart(id) {
  const container = document.getElementById(id);
  if (!container) return;

  const vals   = DATA.elephantDeaths;   // [4, 9, 6, 10, 12]
  const labels = ['21-22','22-23','23-24','24-25','25-26'];
  const maxVal = 16;

  container.innerHTML = '';

  const wrap = document.createElement('div');
  wrap.className = 'liq-wrap';

  const barsEl = document.createElement('div');
  barsEl.className = 'liq-bars';

  vals.forEach((val, i) => {
    const pct   = (val / maxVal) * 100;
    const delay = i * 0.7;
    const numDelay = (delay + 5).toFixed(1);

    const group = document.createElement('div');
    group.className = 'liq-group';

    const numEl = document.createElement('div');
    numEl.className = 'liq-num';
    numEl.textContent = val;
    numEl.style.setProperty('--nd', numDelay + 's');

    const box = document.createElement('div');
    box.className = 'liq-box';

    const fill = document.createElement('div');
    fill.className = 'liq-fill';
    fill.style.setProperty('--delay', delay + 's');
    fill.dataset.pct = pct;

    const shimmer = document.createElement('div');
    shimmer.className = 'liq-shimmer';
    shimmer.style.animationDelay = (delay + 5.3) + 's';
    fill.appendChild(shimmer);
    box.appendChild(fill);

    const lbl = document.createElement('div');
    lbl.className = 'liq-lbl';
    lbl.textContent = labels[i];

    group.append(numEl, box, lbl);
    barsEl.appendChild(group);
  });

  const replayBtn = document.createElement('button');
  replayBtn.className = 'liq-replay';
  replayBtn.textContent = '↺  Replay';
  replayBtn.onclick = () => liqReplay(container);

  wrap.append(barsEl, replayBtn);
  container.appendChild(wrap);

  setTimeout(() => liqStart(container), 200);
}

function liqStart(container) {
  const fills = container.querySelectorAll('.liq-fill');
  const nums  = container.querySelectorAll('.liq-num');

  fills.forEach(fill => {
    fill.style.height = fill.dataset.pct + '%';
  });

  nums.forEach((num, i) => {
    const nd = parseFloat(num.style.getPropertyValue('--nd') || (i * 0.7 + 5)) * 1000;
    setTimeout(() => num.classList.add('liq-num-show'), nd);
  });
}

function liqReplay(container) {
  const fills = container.querySelectorAll('.liq-fill');
  const nums  = container.querySelectorAll('.liq-num');

  fills.forEach(fill => {
    fill.style.transition = 'none';
    fill.style.height = '0';
  });
  nums.forEach(n => n.classList.remove('liq-num-show'));

  requestAnimationFrame(() => requestAnimationFrame(() => {
    fills.forEach(fill => { fill.style.transition = ''; fill.style.height = fill.dataset.pct + '%'; });
    nums.forEach((num, i) => {
      const nd = parseFloat(num.style.getPropertyValue('--nd') || (i * 0.7 + 5)) * 1000;
      setTimeout(() => num.classList.add('liq-num-show'), nd);
    });
  }));
}

// ── 3. Cause Chart: horizontal bars, ranked ───────────────────────────────
function initCauseChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);
  const sorted = [...DATA.causeOfDeath].sort((a, b) => b.count - a.count);
  const colors = ['#F4A261', '#52B788', '#40916c', '#2d6a4f', '#1B4332'];
  chartInstances[id] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sorted.map(d => d.cause),
      datasets: [{
        label: 'Deaths',
        data: sorted.map(d => d.count),
        backgroundColor: colors,
        borderRadius: 5,
        borderSkipped: false
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(17,34,64,0.95)',
          titleColor: '#E8F0E8',
          bodyColor: '#8BA098',
          borderColor: 'rgba(82,183,136,0.3)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: ctx => {
              const item = sorted[ctx.dataIndex];
              return ` ${item.count} deaths (${item.pct}%)`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098' },
          beginAtZero: true,
          max: 25
        },
        y: {
          grid: { display: false },
          ticks: { color: '#E8F0E8', font: { size: 13, weight: '600' } }
        }
      }
    }
  });
}

// ── 4. Age Group Chart: vertical bars ────────────────────────────────────
function initAgeChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);
  const colors = ['#2d6a4f','#40916c','#52B788','#74c69d'];
  chartInstances[id] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: DATA.ageProfile.map(d => d.group),
      datasets: [{
        label: 'Count',
        data: DATA.ageProfile.map(d => d.count),
        backgroundColor: colors,
        borderRadius: 6,
        borderSkipped: false
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(17,34,64,0.95)',
          titleColor: '#E8F0E8',
          bodyColor: '#8BA098',
          borderColor: 'rgba(82,183,136,0.3)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: ctx => {
              const item = DATA.ageProfile[ctx.dataIndex];
              return ` ${item.count} deaths (${item.pct}%)`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#8BA098', font: { size: 11 }, maxRotation: 0 }
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098', stepSize: 2 },
          beginAtZero: true,
          min: 0,
          max: 18
        }
      }
    }
  });
}

// ── 5. Sex Donut Chart ─────────────────────────────────────────────────────
function initSexChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);
  const total = DATA.sexProfile.male + DATA.sexProfile.female + (DATA.sexProfile.unknown || 0);
  const malePct   = Math.round(DATA.sexProfile.male   / total * 100);
  const femalePct = Math.round(DATA.sexProfile.female / total * 100);
  const unkPct    = 100 - malePct - femalePct;
  chartInstances[id] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Male', 'Female', 'Unknown'],
      datasets: [{
        data: [DATA.sexProfile.male, DATA.sexProfile.female, DATA.sexProfile.unknown || 0],
        backgroundColor: ['#52B788', '#C9A84C', 'rgba(139,160,152,0.35)'],
        borderColor: ['#0A1628', '#0A1628', '#0A1628'],
        borderWidth: 4,
        hoverOffset: 12
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#8BA098',
            padding: 20,
            usePointStyle: true,
            pointStyleWidth: 10,
            font: { size: 13 }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(17,34,64,0.95)',
          titleColor: '#E8F0E8',
          bodyColor: '#8BA098',
          borderColor: 'rgba(82,183,136,0.3)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: ctx => {
              const pct = Math.round(ctx.parsed / total * 100);
              return ` ${ctx.label}: ${ctx.parsed} (${pct}%) of ${total} records`;
            }
          }
        }
      }
    },
    plugins: [{
      id: 'centerText',
      afterDraw(chart) {
        const { ctx: c, width, height } = chart;
        c.save();
        c.textAlign = 'center';
        c.textBaseline = 'middle';
        const cx = width / 2;
        const cy = (height - 40) / 2;
        c.font = 'bold 1.7rem system-ui';
        c.fillStyle = '#52B788';
        c.fillText(malePct + '%', cx, cy - 16);
        c.font = '0.65rem system-ui';
        c.fillStyle = '#8BA098';
        c.fillText('Male', cx, cy + 4);
        c.font = '0.6rem system-ui';
        c.fillStyle = '#C9A84C';
        c.fillText(femalePct + '% Female', cx, cy + 20);
        c.restore();
      }
    }]
  });
}

// ── Roller bullet helpers ──────────────────────────────────────────────────
function catmullRomPos(pts, t) {
  const n   = pts.length - 1;
  const seg = Math.min(Math.floor(t * n), n - 1);
  const st  = t * n - seg;
  const p0  = pts[Math.max(0, seg - 1)];
  const p1  = pts[seg];
  const p2  = pts[Math.min(n, seg + 1)];
  const p3  = pts[Math.min(n, seg + 2)];
  const t2  = st * st, t3 = t2 * st;
  return {
    x: 0.5*((2*p1.x)+(-p0.x+p2.x)*st+(2*p0.x-5*p1.x+4*p2.x-p3.x)*t2+(-p0.x+3*p1.x-3*p2.x+p3.x)*t3),
    y: 0.5*((2*p1.y)+(-p0.y+p2.y)*st+(2*p0.y-5*p1.y+4*p2.y-p3.y)*t2+(-p0.y+3*p1.y-3*p2.y+p3.y)*t3)
  };
}

function startRollerBullet(chart) {
  const meta = chart.getDatasetMeta(0);
  const pts  = meta.data.map(p => ({ x: p.x, y: p.y }));

  const ov = document.createElement('canvas');
  ov.style.cssText = 'position:absolute;top:0;left:0;pointer-events:none;z-index:2';
  ov.width  = chart.canvas.offsetWidth  * (window.devicePixelRatio || 1);
  ov.height = chart.canvas.offsetHeight * (window.devicePixelRatio || 1);
  ov.style.width  = chart.canvas.offsetWidth  + 'px';
  ov.style.height = chart.canvas.offsetHeight + 'px';
  const ctx = ov.getContext('2d');
  ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
  chart.canvas.parentNode.style.position = 'relative';
  chart.canvas.parentNode.appendChild(ov);

  const cycleDur = 8000;
  const pauseDur = 1500;
  let start = null;

  function tick(now) {
    if (!start) start = now;
    const elapsed = now - start;
    const cycleT  = elapsed % (cycleDur + pauseDur);

    ctx.clearRect(0, 0, ov.width, ov.height);

    if (cycleT < cycleDur) {
      const t   = cycleT / cycleDur;
      const pos = catmullRomPos(pts, t);

      // Trail
      const trailT = Math.max(0, t - 0.04);
      for (let s = 0; s < 8; s++) {
        const tp  = catmullRomPos(pts, trailT + (t - trailT) * (s / 8));
        const r   = (s / 8) * 5;
        const alp = (s / 8) * 0.25;
        ctx.fillStyle = `rgba(212,168,49,${alp})`;
        ctx.beginPath();
        ctx.arc(tp.x, tp.y, r, 0, Math.PI * 2);
        ctx.fill();
      }

      // Glow
      const grd = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, 18);
      grd.addColorStop(0,   'rgba(212,168,49,0.85)');
      grd.addColorStop(0.4, 'rgba(212,168,49,0.25)');
      grd.addColorStop(1,   'rgba(212,168,49,0)');
      ctx.fillStyle = grd;
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 18, 0, Math.PI * 2);
      ctx.fill();

      // Core
      ctx.fillStyle   = '#d4a831';
      ctx.strokeStyle = '#fff';
      ctx.lineWidth   = 2;
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ── 6. Seasonal Line Chart ─────────────────────────────────────────────────
function initSeasonalChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);
  chartInstances[id] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: DATA.seasonal.months,
      datasets: [{
        label: 'Deaths',
        data: DATA.seasonal.counts,
        borderColor: '#52B788',
        backgroundColor: (context) => {
          const chart = context.chart;
          const { ctx: c, chartArea } = chart;
          if (!chartArea) return 'transparent';
          const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
          gradient.addColorStop(0, 'rgba(82,183,136,0.4)');
          gradient.addColorStop(1, 'rgba(82,183,136,0.02)');
          return gradient;
        },
        borderWidth: 3,
        pointBackgroundColor: DATA.seasonal.counts.map((v, i) =>
          v === Math.max(...DATA.seasonal.counts) ? '#F4A261' : '#52B788'
        ),
        pointRadius: DATA.seasonal.counts.map((v) =>
          v === Math.max(...DATA.seasonal.counts) ? 9 : 5
        ),
        pointHoverRadius: 10,
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        onComplete(ctx) {
          if (ctx.initial) startRollerBullet(ctx.chart);
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(17,34,64,0.95)',
          titleColor: '#E8F0E8',
          bodyColor: '#8BA098',
          borderColor: 'rgba(82,183,136,0.3)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: ctx => ` ${ctx.parsed.y} deaths`
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098' }
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098', stepSize: 2 },
          beginAtZero: true,
          max: 10
        }
      }
    }
  });
}

// ── 7. Range-wise Horizontal Bars ─────────────────────────────────────────
function initRangeChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);
  const riskColors = {
    CRITICAL: '#E63946',
    HIGH:     '#F4A261',
    MODERATE: '#C9A84C',
    LOW:      '#52B788'
  };
  const sorted = [...DATA.rangeWise].sort((a, b) => b.count - a.count);
  chartInstances[id] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sorted.map(d => d.beat),
      datasets: [{
        label: 'Elephant Deaths',
        data: sorted.map(d => d.count),
        backgroundColor: sorted.map(d => riskColors[d.risk]),
        borderRadius: 5,
        borderSkipped: false
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(17,34,64,0.95)',
          titleColor: '#E8F0E8',
          bodyColor: '#8BA098',
          borderColor: 'rgba(82,183,136,0.3)',
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: ctx => {
              const item = sorted[ctx.dataIndex];
              return ` ${item.count} deaths · ${item.div} · ${item.risk}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098' },
          beginAtZero: true,
          max: 14
        },
        y: {
          grid: { display: false },
          ticks: { color: '#E8F0E8', font: { size: 12 } }
        }
      }
    }
  });
}

// ── 8. Population Area Chart — vanilla canvas, Catmull-Rom + de Casteljau ──
(function () {
  const RAW = [
    { year: '2001', val: 24  }, { year: '2005', val: 123 },
    { year: '2007', val: 122 }, { year: '2015', val: 247 },
    { year: '2017', val: 247 }, { year: '2021', val: 279 },
    { year: '2026', val: 451 },
  ];
  const Y_TICKS = [50,100,150,200,250,300,350,400,450,500];
  const Y_MIN = 0, Y_MAX = 520, DUR = 10000;
  const LC = '#5fcf97', GC = 'rgba(95,207,151,0.55)';
  let _cv, _cx, _raf, _t0, _running, _pts, _segs, _slen, _tlen, _W, _H, _PAD, _cW, _cH;
  const DPR = window.devicePixelRatio || 1;
  const prefReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function pad() {
    const s = _W/700;
    _PAD = { top:72*s, right:52*s, bottom:50*s, left:62*s };
    _cW = _W-_PAD.left-_PAD.right; _cH = _H-_PAD.top-_PAD.bottom;
  }
  function toY(v) { return _PAD.top+(1-(v-Y_MIN)/(Y_MAX-Y_MIN))*_cH; }

  function setup() {
    const wrap = _cv.parentElement;
    const cssW = wrap.getBoundingClientRect().width;
    const cssH = wrap.getBoundingClientRect().height || Math.round(cssW*0.55);
    _W = cssW; _H = cssH;
    _cv.style.width=_W+'px'; _cv.style.height=_H+'px';
    _cv.width=Math.round(_W*DPR); _cv.height=Math.round(_H*DPR);
    _cx.setTransform(1,0,0,1,0,0); _cx.scale(DPR,DPR);
    pad();
    const n=RAW.length;
    _pts = RAW.map((d,i)=>({ x:_PAD.left+(i/(n-1))*_cW, y:toY(d.val), val:d.val, year:d.year }));
    _segs=[];
    for(let i=0;i<n-1;i++){
      const p0=_pts[Math.max(0,i-1)],p1=_pts[i],p2=_pts[i+1],p3=_pts[Math.min(n-1,i+2)];
      _segs.push({ p0:p1, cp1:{x:p1.x+(p2.x-p0.x)/6,y:p1.y+(p2.y-p0.y)/6},
                          cp2:{x:p2.x-(p3.x-p1.x)/6,y:p2.y-(p3.y-p1.y)/6}, p3:p2 });
    }
    _slen = _segs.map(s=>{ let l=0,p=bpt(s,0);
      for(let i=1;i<=80;i++){const q=bpt(s,i/80),dx=q.x-p.x,dy=q.y-p.y;l+=Math.sqrt(dx*dx+dy*dy);p=q;}
      return l; });
    _tlen = _slen.reduce((a,b)=>a+b,0);
  }

  function bpt(s,t){ const m=1-t; return {
    x:m*m*m*s.p0.x+3*m*m*t*s.cp1.x+3*m*t*t*s.cp2.x+t*t*t*s.p3.x,
    y:m*m*m*s.p0.y+3*m*m*t*s.cp1.y+3*m*t*t*s.cp2.y+t*t*t*s.p3.y }; }

  function lp(a,b,t){ return {x:a.x+(b.x-a.x)*t, y:a.y+(b.y-a.y)*t}; }

  function splitL(s,t){
    const p01=lp(s.p0,s.cp1,t),p12=lp(s.cp1,s.cp2,t),p23=lp(s.cp2,s.p3,t);
    const p012=lp(p01,p12,t),p123=lp(p12,p23,t),mid=lp(p012,p123,t);
    return {p0:s.p0,cp1:p01,cp2:p012,p3:mid};
  }

  function tip(prog){
    if(prog<=0) return {si:0,t:0,..._pts[0]};
    if(prog>=1) return {si:_segs.length-1,t:1,..._pts[_pts.length-1]};
    const tgt=prog*_tlen; let acc=0;
    for(let i=0;i<_slen.length;i++){
      if(acc+_slen[i]>=tgt){ const t=(tgt-acc)/_slen[i]; return {si:i,t,...bpt(_segs[i],t)}; }
      acc+=_slen[i];
    }
    return {si:_segs.length-1,t:1,..._pts[_pts.length-1]};
  }

  function ease(t){ return t<0.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2; }

  function draw(prog){
    _cx.clearRect(0,0,_W,_H);
    // Grid
    const s=_W/700;
    _cx.save();
    _cx.font=`${Math.round(11*s)}px system-ui,sans-serif`;
    _cx.textAlign='right'; _cx.textBaseline='middle';
    Y_TICKS.forEach(v=>{ const y=toY(v);
      _cx.beginPath(); _cx.moveTo(_PAD.left,y); _cx.lineTo(_PAD.left+_cW,y);
      _cx.strokeStyle='rgba(255,255,255,0.05)'; _cx.lineWidth=1; _cx.stroke();
      _cx.fillStyle='rgba(148,175,200,0.55)'; _cx.fillText(v,_PAD.left-8*s,y);
    });
    _cx.textAlign='center'; _cx.textBaseline='top';
    _pts.forEach(p=>{ _cx.fillStyle='rgba(148,175,200,0.55)'; _cx.fillText(p.year,p.x,_PAD.top+_cH+10*s); });
    _cx.beginPath();
    _cx.moveTo(_PAD.left,_PAD.top); _cx.lineTo(_PAD.left,_PAD.top+_cH+4);
    _cx.moveTo(_PAD.left-4,_PAD.top+_cH); _cx.lineTo(_PAD.left+_cW,_PAD.top+_cH);
    _cx.strokeStyle='rgba(255,255,255,0.1)'; _cx.lineWidth=1; _cx.stroke();
    _cx.restore();

    if(prog<=0) return;
    const tp=tip(prog);

    // Area fill
    _cx.save();
    _cx.beginPath(); _cx.rect(_PAD.left-1,_PAD.top-20,tp.x-_PAD.left+2,_cH+30); _cx.clip();
    const ag=_cx.createLinearGradient(0,_PAD.top,0,_PAD.top+_cH);
    ag.addColorStop(0,'rgba(95,207,151,0.38)'); ag.addColorStop(0.55,'rgba(95,207,151,0.12)'); ag.addColorStop(1,'rgba(95,207,151,0.02)');
    _cx.beginPath(); _cx.moveTo(_pts[0].x,_PAD.top+_cH); _cx.lineTo(_pts[0].x,_pts[0].y);
    _segs.forEach(sg=>_cx.bezierCurveTo(sg.cp1.x,sg.cp1.y,sg.cp2.x,sg.cp2.y,sg.p3.x,sg.p3.y));
    _cx.lineTo(_pts[_pts.length-1].x,_PAD.top+_cH); _cx.closePath();
    _cx.fillStyle=ag; _cx.fill(); _cx.restore();

    // Line
    _cx.save();
    _cx.shadowColor=GC; _cx.shadowBlur=14;
    _cx.strokeStyle=LC; _cx.lineWidth=3; _cx.lineJoin='round'; _cx.lineCap='round';
    _cx.beginPath(); _cx.moveTo(_pts[0].x,_pts[0].y);
    for(let i=0;i<tp.si;i++){ const sg=_segs[i]; _cx.bezierCurveTo(sg.cp1.x,sg.cp1.y,sg.cp2.x,sg.cp2.y,sg.p3.x,sg.p3.y); }
    if(tp.t>1e-6){ const pl=splitL(_segs[tp.si],tp.t); _cx.bezierCurveTo(pl.cp1.x,pl.cp1.y,pl.cp2.x,pl.cp2.y,pl.p3.x,pl.p3.y); }
    _cx.stroke(); _cx.restore();

    // Markers
    const n=_pts.length;
    _pts.forEach((p,i)=>{
      const mp=i/(n-1); if(prog<mp-0.004) return;
      const alpha=Math.min(1,(prog-mp)/0.04); const r=6.5*s;
      _cx.save(); _cx.globalAlpha=alpha;
      const halo=_cx.createRadialGradient(p.x,p.y,0,p.x,p.y,r*2.8);
      halo.addColorStop(0,'rgba(95,207,151,0.2)'); halo.addColorStop(1,'rgba(95,207,151,0)');
      _cx.beginPath(); _cx.arc(p.x,p.y,r*2.8,0,Math.PI*2); _cx.fillStyle=halo; _cx.fill();
      _cx.beginPath(); _cx.arc(p.x,p.y,r,0,Math.PI*2);
      _cx.strokeStyle=LC; _cx.lineWidth=2.2*s; _cx.shadowColor=GC; _cx.shadowBlur=10; _cx.stroke();
      _cx.beginPath(); _cx.arc(p.x,p.y,r-2.2*s,0,Math.PI*2); _cx.fillStyle='#fff'; _cx.shadowBlur=0; _cx.fill();
      _cx.font=`700 ${Math.round(12*s)}px system-ui,sans-serif`;
      _cx.textAlign='center'; _cx.textBaseline='bottom'; _cx.fillStyle='#fff';
      _cx.shadowColor='rgba(0,0,0,0.9)'; _cx.shadowBlur=5;
      _cx.fillText(p.val,p.x,p.y-r-5*s); _cx.restore();
    });

    // Tip glow dot
    if(prog<1){ _cx.save(); _cx.beginPath(); _cx.arc(tp.x,tp.y,5*s,0,Math.PI*2);
      _cx.fillStyle='#fff'; _cx.shadowColor=LC; _cx.shadowBlur=18; _cx.fill(); _cx.restore(); }
  }

  function loop(ts){
    if(!_t0) _t0=ts;
    const raw=Math.min((ts-_t0)/DUR,1);
    draw(ease(raw));
    if(raw<1) _raf=requestAnimationFrame(loop); else _running=false;
  }

  function start(){
    if(_raf) cancelAnimationFrame(_raf);
    _t0=null; _running=true; _raf=requestAnimationFrame(loop);
  }

  window.initPopChart = function(id){
    _cv = document.getElementById(id);
    if(!_cv) return;
    if(chartInstances[id] && chartInstances[id].destroy) { chartInstances[id].destroy(); delete chartInstances[id]; }
    _cx = _cv.getContext('2d');
    setup();
    _cv.onclick = ()=>{ if(!prefReduced) start(); };
    if(prefReduced) draw(1); else start();
  };
})();
