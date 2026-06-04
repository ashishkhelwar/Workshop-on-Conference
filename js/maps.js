// Maps module — Leaflet-based map initializers
// Lazily initialized; mapsInitialized object is declared in app.js
// and available globally since scripts are loaded in order.
// This ensures the same object is shared between maps.js and app.js.
window.mapsInitialized = window.mapsInitialized || {};

function initDistributionMap(id) {
  if (mapsInitialized[id]) return;
  mapsInitialized[id] = true;

  const map = L.map(id, { zoomControl: true, scrollWheelZoom: false, zoomSnap: 0.1 })
    .setView([22.3, 83.4], 9.2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 13
  }).addTo(map);

  // Approximate elephant range rectangle
  L.rectangle([[21.8, 82.8], [22.9, 84.1]], {
    color: '#52B788', weight: 2, fill: true,
    fillOpacity: 0.1, dashArray: '6 4'
  }).addTo(map)
    .bindPopup('<b style="color:#52B788">Estimated Elephant Range</b><br>Bilaspur District, Chhattisgarh');

  // Division markers
  L.marker([22.55, 83.18]).addTo(map)
    .bindPopup('<b>Dharamjaigarh Van Mandal</b><br>27 elephant casualties');

  L.marker([22.25, 83.58]).addTo(map)
    .bindPopup('<b>Raigarh Van Mandal</b><br>21 elephant casualties');

  // Forest patches (rough polygons)
  L.polygon([
    [22.0, 82.9], [22.5, 83.0], [22.8, 83.2], [22.9, 83.5],
    [22.6, 83.8], [22.2, 83.9], [21.9, 83.6], [21.8, 83.2]
  ], {
    color: '#1B4332', weight: 1, fill: true,
    fillOpacity: 0.2, fillColor: '#52B788'
  }).addTo(map).bindPopup('Core Forest Area');

  // Raigarh division boundary overlay
  fetch('assets/raigarh_boundary.geojson')
    .then(r => r.json())
    .then(data => {
      L.geoJSON(data, {
        style: { color: '#C9A84C', weight: 1.2, fill: true, fillColor: '#C9A84C', fillOpacity: 0.12 },
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          const label = [p.range_name, p.beat_name, p.fdc_name].filter(Boolean).join(' › ') || p.name || '';
          layer.bindPopup(`<b style="color:#C9A84C">Raigarh Division</b>${label ? '<br>' + label : ''}`);
        }
      }).addTo(map);
    })
    .catch(e => console.warn('Raigarh boundary load failed:', e));

  // Dharamjaigarh division boundary overlay
  fetch('assets/dharamjaigarh_boundary.geojson')
    .then(r => r.json())
    .then(data => {
      L.geoJSON(data, {
        style: { color: '#52B788', weight: 1.2, fill: true, fillColor: '#52B788', fillOpacity: 0.12 },
        onEachFeature: (feature, layer) => {
          const p = feature.properties || {};
          const label = [p.range_name, p.beat_name, p.fdc_name].filter(Boolean).join(' › ') || p.name || '';
          layer.bindPopup(`<b style="color:#52B788">Dharamjaigarh Division</b>${label ? '<br>' + label : ''}`);
        }
      }).addTo(map);
    })
    .catch(e => console.warn('Dharamjaigarh boundary load failed:', e));

  setTimeout(() => map.invalidateSize(), 500);
}

function initCasualtyMap(id) {
  if (mapsInitialized[id]) return;
  mapsInitialized[id] = true;

  const map = L.map(id, { zoomControl: true, scrollWheelZoom: false, zoomSnap: 0.5 })
    .setView([22.3, 83.4], 10);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 14
  }).addTo(map);

  const elephantIcon = L.divIcon({
    className: '',
    html: '<div style="width:11px;height:11px;border-radius:50%;background:#52B788;border:2px solid #fff;box-shadow:0 0 4px rgba(82,183,136,0.8);"></div>',
    iconSize: [11, 11],
    iconAnchor: [5, 5]
  });

  const humanIcon = L.divIcon({
    className: '',
    html: '<div style="width:11px;height:11px;border-radius:50%;background:#E63946;border:2px solid #fff;box-shadow:0 0 4px rgba(230,57,70,0.8);"></div>',
    iconSize: [11, 11],
    iconAnchor: [5, 5]
  });

  DATA.geoPoints.dhElephant.forEach(([lat, lon, cause, yr]) => {
    L.marker([lat, lon], { icon: elephantIcon }).addTo(map)
      .bindPopup(`<b style="color:#52B788">Elephant Death</b><br><span style="color:#999">Dharamjaigarh · ${yr}</span><br>${cause}`);
  });

  DATA.geoPoints.rgElephant.forEach(([lat, lon, cause, yr]) => {
    L.marker([lat, lon], { icon: elephantIcon }).addTo(map)
      .bindPopup(`<b style="color:#52B788">Elephant Death</b><br><span style="color:#999">Raigarh · ${yr}</span><br>${cause}`);
  });

  setTimeout(() => map.invalidateSize(), 500);
}

function initOverlayMap(id) {
  if (mapsInitialized[id]) return;
  mapsInitialized[id] = true;

  const map = L.map(id, { zoomControl: true, scrollWheelZoom: false })
    .setView([22.3, 83.4], 9);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 14
  }).addTo(map);

  const elephantIcon = L.divIcon({
    className: '',
    html: `<div style="
  width:16px;height:16px;border-radius:50%;
  background:#52B788;border:3px solid #fff;
  box-shadow:0 0 10px rgba(82,183,136,0.9),0 2px 5px rgba(0,0,0,0.5);
"></div>`,
    iconSize: [16, 16], iconAnchor: [8, 8]
  });

  const humanIcon = L.divIcon({
    className: '',
    html: `<div style="
  width:16px;height:16px;border-radius:50%;
  background:#E63946;border:3px solid #fff;
  box-shadow:0 0 10px rgba(230,57,70,0.9),0 2px 5px rgba(0,0,0,0.5);
"></div>`,
    iconSize: [16, 16], iconAnchor: [8, 8]
  });

  // Phase 1: elephant markers immediately
  DATA.geoPoints.dhElephant.forEach(([lat, lon, cause, yr]) => {
    L.marker([lat, lon], { icon: elephantIcon }).addTo(map)
      .bindPopup(`<b style="color:#52B788">Elephant Death</b><br><span style="color:#999">Dharamjaigarh · ${yr}</span><br>${cause}`);
  });

  DATA.geoPoints.rgElephant.forEach(([lat, lon, cause, yr]) => {
    L.marker([lat, lon], { icon: elephantIcon }).addTo(map)
      .bindPopup(`<b style="color:#52B788">Elephant Death</b><br><span style="color:#999">Raigarh · ${yr}</span><br>${cause}`);
  });

  // Phase 2: human markers after 2 seconds
  setTimeout(() => {
    DATA.geoPoints.dhHuman.forEach(([lat, lon, village, yr]) => {
      L.marker([lat, lon], { icon: humanIcon }).addTo(map)
        .bindPopup(`<b style="color:#E63946">Human Death</b><br><span style="color:#999">Dharamjaigarh · ${yr}</span><br>${village}`);
    });

    DATA.geoPoints.rgHuman.forEach(([lat, lon, village, yr]) => {
      L.marker([lat, lon], { icon: humanIcon }).addTo(map)
        .bindPopup(`<b style="color:#E63946">Human Death</b><br><span style="color:#999">Raigarh · ${yr}</span><br>${village}`);
    });

    // Phase 3: pulsing circles on hotspots after 3s
    setTimeout(() => {
      addPulsingHotspot(map, 22.19, 83.16, 'CRITICAL HOTSPOT: Chhal Area', '#E63946');
      addPulsingHotspot(map, 22.20, 83.45, 'CRITICAL HOTSPOT: Ghargoda Area', '#E63946');
    }, 1000);
  }, 2000);

  setTimeout(() => map.invalidateSize(), 500);
}

function initCurrentElephantsMap(id) {
  if (mapsInitialized[id]) return;
  mapsInitialized[id] = true;

  const map = L.map(id, { zoomControl: true, scrollWheelZoom: false })
    .setView([22.5, 83.0], 8);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 14
  }).addTo(map);

  const herdPts = [
    [23.6971, 82.998],
    [23.7437, 83.0037],
    [23.7169, 82.9018],
    [23.6971, 82.998],
    [23.301667, 83.219444],
    [23.7058, 82.8924],
    [23.5177, 82.2369],
    [22.153611, 82.852778],
    [22.4188, 83.1999],
    [22.694, 83.1795],
    [22.4188, 83.1999],
    [23.829167, 83.373333],
    [22.43694, 83.3794],
    [20.3575, 82.370833],
    [21.45163, 82.4737],
    [22.453, 81.8194],
    [22.675, 82.3311]
  ];

  const tuskerPts = [
    [22.6904, 83.7842],
    [22.700278, 83.973889],
    [23.0071, 83.4983],
    [23.7133, 83.0827],
    [23.7486, 83.0372],
    [21.51211, 83.0448],
    [22.4412, 83.3316],
    [22.687778, 83.265],
    [22.546667, 83.620278],
    [22.686389, 83.298611],
    [22.7702, 83.1688],
    [22.686389, 83.298611],
    [22.335, 83.167222],
    [22.160556, 82.862222],
    [22.1255, 82.7833],
    [20.5061, 82.3451],
    [20.29, 82.391111],
    [23.2142, 83.1917],
    [23.2142, 83.1917],
    [23.2142, 83.1917],
    [23.2142, 83.1917],
    [22.7214, 82.4428],
    [22.9304, 82.3832],
    [23.8879, 83.576],
    [23.8322, 83.5939],
    [23.7801, 83.1465],
    [23.51309, 83.3775],
    [22.793333, 83.134167],
    [22.793333, 83.134167]
  ];

  const herdIcon = L.divIcon({
    className: '',
    html: `<div style="
      width:14px;height:14px;border-radius:50%;
      background:#E63946;
      border:2.5px solid #fff;
      box-shadow:0 0 7px rgba(230,57,70,0.85),0 1px 4px rgba(0,0,0,0.4);
    "></div>`,
    iconSize: [14, 14], iconAnchor: [7, 7], popupAnchor: [0, -9]
  });

  const tuskerIcon = L.divIcon({
    className: '',
    html: `<div style="
      width:13px;height:13px;
      background:#F4A261;
      border:2.5px solid #fff;
      box-shadow:0 0 7px rgba(244,162,97,0.85),0 1px 4px rgba(0,0,0,0.4);
      transform:rotate(45deg);
      margin:1px;
      animation:tuskerBlink 1.2s ease-in-out infinite;
    "></div>`,
    iconSize: [15, 15], iconAnchor: [7, 7], popupAnchor: [0, -9]
  });

  herdPts.forEach(([lat, lng]) => {
    L.marker([lat, lng], { icon: herdIcon }).addTo(map)
      .bindPopup(`<b style="color:#52B788">Herd Elephant</b><br><small style="color:#888">${lat.toFixed(5)}, ${lng.toFixed(5)}</small>`);
  });

  tuskerPts.forEach(([lat, lng]) => {
    L.marker([lat, lng], { icon: tuskerIcon }).addTo(map)
      .bindPopup(`<b style="color:#F4A261">Tusker Elephant</b><br><small style="color:#888">${lat.toFixed(5)}, ${lng.toFixed(5)}</small>`);
  });

  // District boundaries — Chhattisgarh
  fetch('https://raw.githubusercontent.com/datameet/maps/master/Districts/chhattisgarh.geojson')
    .then(r => r.json())
    .then(data => {
      L.geoJSON(data, {
        style: {
          color: '#52B788',
          weight: 1.5,
          opacity: 0.6,
          fillOpacity: 0.04,
          fillColor: '#52B788',
          dashArray: '4 3'
        },
        onEachFeature(feature, layer) {
          const name = feature.properties.DISTRICT || feature.properties.district || feature.properties.NAME_2 || '';
          if (name) layer.bindTooltip(name, { permanent: false, direction: 'center', className: 'dist-label' });
        }
      }).addTo(map);
    })
    .catch(() => {});

  const bounds = L.latLngBounds([...herdPts, ...tuskerPts]);
  map.fitBounds(bounds, { padding: [28, 28] });

  setTimeout(() => map.invalidateSize(), 500);
}

function addPulsingHotspot(map, lat, lon, label, color) {
  // Static circle
  L.circle([lat, lon], {
    radius: 8000,
    color: color,
    weight: 2,
    fill: true,
    fillOpacity: 0.15,
    dashArray: '6 4'
  }).addTo(map).bindPopup(`<b style="color:${color}">${label}</b>`);

  // CSS pulsing marker
  const pulseIcon = L.divIcon({
    className: '',
    html: `<div class="pulse-ring" style="--pulse-color:${color}"></div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15]
  });

  L.marker([lat, lon], { icon: pulseIcon }).addTo(map)
    .bindPopup(`<b style="color:${color}">${label}</b>`);
}

// ── Drowning Cases Map ────────────────────────────────────────────────────────
function initDrownMap(id) {
  if (mapsInitialized[id]) return;
  mapsInitialized[id] = true;

  const map = L.map(id, { zoomControl: true, scrollWheelZoom: false })
    .setView([22.2, 83.28], 10);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 15
  }).addTo(map);

  function mkIcon(color, ring) {
    return L.divIcon({
      className: '',
      html: `<div style="width:14px;height:14px;border-radius:50%;background:${color};border:2px solid #fff;box-shadow:0 0 0 3px ${ring},0 2px 6px rgba(0,0,0,0.5);"></div>`,
      iconSize: [14, 14],
      iconAnchor: [7, 7],
      popupAnchor: [0, -9]
    });
  }

  const dhIcon  = mkIcon('#52B788', 'rgba(82,183,136,0.4)');
  const rgIcon  = mkIcon('#C9A84C', 'rgba(201,168,76,0.4)');
  const newIcon = mkIcon('#E63946', 'rgba(230,57,70,0.4)');

  const cases = [
    // DH — 2024-25 / 2025-26
    { lat:22.3217, lon:83.0956, label:'DH1', div:'Dharamjaigarh', loc:'Chal / Hati',      date:'21/11/24', age:'~15–20 days', water:'Pond',           icon: dhIcon  },
    { lat:22.2838, lon:83.1371, label:'DH2', div:'Dharamjaigarh', loc:'Chal / Kida',      date:'18/03/25', age:'~1 yr',       water:'Pond',           icon: dhIcon  },
    { lat:22.1662, lon:83.1731, label:'DH3', div:'Dharamjaigarh', loc:'Chal / Auranara',  date:'29/10/25', age:'~9–11 months',water:'Pond',           icon: dhIcon  },
    // DH — 2026-27 (red)
    { lat:22.1461, lon:83.2119, label:'DH4', div:'Dharamjaigarh', loc:'Chal / Singhijhap',date:'08/05/26', age:'~6 months',   water:'Pond',           icon: newIcon },
    { lat:22.1655, lon:83.1155, label:'DH5', div:'Dharamjaigarh', loc:'Chal / Chal',      date:'11/05/26', age:'~5–6 months', water:'Asphyxiation',   icon: newIcon },
    { lat:22.1000, lon:83.1556, label:'DH6', div:'Dharamjaigarh', loc:'Chal / Edu',       date:'24/05/26', age:'~1.5–2 yrs',  water:'Pond',           icon: newIcon },
    // RG — 2024-25 / 2025-26
    { lat:22.1060, lon:83.2434, label:'RG1', div:'Raigarh',       loc:'Gharghoda / Dehridih',date:'31/12/24',age:'~2 yrs',    water:'Panikhet dam',   icon: rgIcon  },
    { lat:22.1983, lon:83.4681, label:'RG2', div:'Raigarh',       loc:'Gharghoda / Charmar', date:'14/01/25',age:'~2–3 months',water:'Rabo dam',      icon: rgIcon  },
    { lat:22.1017, lon:83.2411, label:'RG3', div:'Raigarh',       loc:'Gharghoda / Dehridih',date:'22/01/25',age:'~2 yrs',    water:'Panikhet dam',   icon: rgIcon  },
    { lat:22.1522, lon:83.4939, label:'RG4', div:'Raigarh',       loc:'Gharghoda / Charmar', date:'25/05/25',age:'~5 months', water:'Pond',           icon: rgIcon  },
    { lat:22.0214, lon:83.3322, label:'RG5', div:'Raigarh',       loc:'Tamnar / Saraipali',  date:'25/11/25',age:'~7 months', water:'Drowned',        icon: rgIcon  },
    { lat:21.9850, lon:83.4617, label:'RG6', div:'Raigarh',       loc:'Raigarh / Bangursiya',date:'20/12/25',age:'~6 months', water:'Drowned',        icon: rgIcon  },
    { lat:22.5550, lon:83.6153, label:'RG7', div:'Raigarh',       loc:'Gharghoda / Kya',     date:'28/01/26',age:'~1 yr',     water:'Sakra stream',   icon: rgIcon  },
  ];

  cases.forEach(c => {
    L.marker([c.lat, c.lon], { icon: c.icon }).addTo(map)
      .bindPopup(
        `<b style="color:${c.label.startsWith('DH') ? '#52B788' : '#C9A84C'}">${c.label} — ${c.div}</b><br>` +
        `<span style="color:#aaa">${c.loc}</span><br>` +
        `Date: ${c.date}<br>Age: ${c.age}<br>Water: ${c.water}`
      );
  });
}
