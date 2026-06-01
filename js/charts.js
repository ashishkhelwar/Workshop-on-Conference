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
  chartInstances[id] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Male', 'Female'],
      datasets: [{
        data: [DATA.sexProfile.male, DATA.sexProfile.female],
        backgroundColor: ['#52B788', '#C9A84C'],
        borderColor: ['#0A1628', '#0A1628'],
        borderWidth: 4,
        hoverOffset: 12,
        _noLabels: true
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
            label: ctx => ` ${ctx.label}: ${ctx.parsed} of 32 PM records`
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
        const cy = (height - 40) / 2; // account for legend
        c.font = 'bold 2rem system-ui';
        c.fillStyle = '#E8F0E8';
        c.fillText('16 / 16', cx, cy - 8);
        c.font = '0.72rem system-ui';
        c.fillStyle = '#8BA098';
        c.fillText('M / F', cx, cy + 20);
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

// ── 8. Population Area Chart ──────────────────────────────────────────────
function initPopChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);
  chartInstances[id] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: DATA.populationTrend.years,
      datasets: [{
        label: 'CG Elephant Population',
        data: DATA.populationTrend.cg,
        borderColor: '#52B788',
        backgroundColor: (context) => {
          const chart = context.chart;
          const { ctx: c, chartArea } = chart;
          if (!chartArea) return 'transparent';
          const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
          gradient.addColorStop(0, 'rgba(82,183,136,0.5)');
          gradient.addColorStop(1, 'rgba(82,183,136,0.02)');
          return gradient;
        },
        borderWidth: 3,
        pointBackgroundColor: '#52B788',
        pointRadius: 5,
        pointHoverRadius: 8,
        tension: 0.3,
        fill: true,
        clip: false
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
            label: ctx => ` ${ctx.parsed.y} elephants (est.)`
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
          ticks: { color: '#8BA098', stepSize: 50 },
          beginAtZero: false,
          min: 24,
          max: 480
        }
      }
    }
  });
}
