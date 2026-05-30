// Chart.js initializers — all lazy, called from app.js onSlideActivate

Chart.defaults.color = '#8BA098';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.font.family = "system-ui, -apple-system, sans-serif";

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
  chartInstances[id] = new Chart(ctx, {
    type: 'line',
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
          beginAtZero: true,
          max: 20
        }
      }
    }
  });
}

// ── 2. Year Bars: elephant deaths per year ────────────────────────────────
function initYearBarsChart(id) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  destroyChart(id);
  const barColors = ['#1B4332','#2d6a4f','#40916c','#F4A261','#E63946'];
  chartInstances[id] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['21-22','22-23','23-24','24-25','25-26*'],
      datasets: [{
        label: 'Elephant Deaths',
        data: DATA.elephantDeaths,
        backgroundColor: barColors,
        borderColor: barColors.map(c => c),
        borderWidth: 0,
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
            label: ctx => ` ${ctx.parsed.y} elephant deaths`
          }
        },
        datalabels: {
          display: false
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098', font: { size: 13 } }
        },
        y: {
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8BA098', stepSize: 2 },
          beginAtZero: true,
          max: 16
        }
      }
    }
  });
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
          max: 12
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
        fill: true
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
          min: 100,
          max: 450
        }
      }
    }
  });
}
