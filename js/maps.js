// Maps module — Leaflet-based map initializers
// Lazily initialized; mapsInitialized object is declared in app.js
// and available globally since scripts are loaded in order.
// This ensures the same object is shared between maps.js and app.js.
window.mapsInitialized = window.mapsInitialized || {};

function initDistributionMap(id) {
  if (mapsInitialized[id]) return;
  mapsInitialized[id] = true;

  const map = L.map(id, { zoomControl: true, scrollWheelZoom: false })
    .setView([22.3, 83.4], 8);

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
    .bindPopup('<b>Dharamjaigarh Van Mandal</b><br>23 elephant casualties<br>36 human casualties');

  L.marker([22.25, 83.58]).addTo(map)
    .bindPopup('<b>Raigarh Van Mandal</b><br>21 elephant casualties<br>9 human casualties');

  // Forest patches (rough polygons)
  L.polygon([
    [22.0, 82.9], [22.5, 83.0], [22.8, 83.2], [22.9, 83.5],
    [22.6, 83.8], [22.2, 83.9], [21.9, 83.6], [21.8, 83.2]
  ], {
    color: '#1B4332', weight: 1, fill: true,
    fillOpacity: 0.2, fillColor: '#52B788'
  }).addTo(map).bindPopup('Core Forest Area');

  setTimeout(() => map.invalidateSize(), 500);
}

function initCasualtyMap(id) {
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

  DATA.geoPoints.dhHuman.forEach(([lat, lon, village, yr]) => {
    L.marker([lat, lon], { icon: humanIcon }).addTo(map)
      .bindPopup(`<b style="color:#E63946">Human Death</b><br><span style="color:#999">Dharamjaigarh · ${yr}</span><br>${village}`);
  });

  DATA.geoPoints.rgHuman.forEach(([lat, lon, village, yr]) => {
    L.marker([lat, lon], { icon: humanIcon }).addTo(map)
      .bindPopup(`<b style="color:#E63946">Human Death</b><br><span style="color:#999">Raigarh · ${yr}</span><br>${village}`);
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
    .setView([22.25, 83.22], 9);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 14
  }).addTo(map);

  const locations = [
    { lat: 22.1700, lng: 83.3878, loc: 'Dehri-Dih, Ghargoda',         count: 2,  herd: 'DH-HE07, RG-HE2',           div: 'Raigarh' },
    { lat: 22.0430, lng: 83.4546, loc: 'Kantajharian East, Raigarh',  count: 2,  herd: 'DJHE07, KBHE4',             div: 'Raigarh' },
    { lat: 22.3101, lng: 83.3649, loc: 'Barod, Ghargoda',              count: 2,  herd: 'JPHE02',                    div: 'Raigarh' },
    { lat: 22.0667, lng: 83.1447, loc: 'Gurda, Kharsiya',              count: 35, herd: 'RaigarhHE1',                div: 'Raigarh' },
    { lat: 22.1953, lng: 83.0958, loc: 'Chainpur, Dharamjaigarh',      count: 30, herd: 'DH-HE7, JPHE2, KorbaHE15', div: 'Dharamjaigarh' },
    { lat: 22.4076, lng: 83.1385, loc: 'Koylar, Dharamjaigarh',        count: 8,  herd: 'JPHE2',                    div: 'Dharamjaigarh' },
    { lat: 22.4469, lng: 83.0998, loc: 'Rupunga, Dharamjaigarh',       count: 15, herd: 'JPHE2',                    div: 'Dharamjaigarh' },
    { lat: 22.4148, lng: 83.2677, loc: 'Ongna, Dharamjaigarh',         count: 1,  herd: 'JPHE2',                    div: 'Dharamjaigarh' },
    { lat: 22.0788, lng: 83.1433, loc: 'Edu, Chhala Range',            count: 52, herd: 'RaigarhHE1',               div: 'Dharamjaigarh' },
    { lat: 22.2917, lng: 83.1437, loc: 'Purunga, Chhala Range',        count: 1,  herd: '—',                        div: 'Dharamjaigarh' },
    { lat: 22.2030, lng: 83.1861, loc: 'Banhar, Chhala Range',         count: 1,  herd: 'DH-HE7',                   div: 'Dharamjaigarh' },
    { lat: 22.1561, lng: 83.1169, loc: 'Chhala',                       count: 1,  herd: '—',                        div: 'Dharamjaigarh' },
    { lat: 22.1952, lng: 83.1461, loc: 'Banhar-Narangi, Chhala',       count: 1,  herd: 'RaigarhHE2',               div: 'Dharamjaigarh' },
    { lat: 22.1766, lng: 83.1723, loc: 'Auranara, Chhala',             count: 1,  herd: 'DJME7',                    div: 'Dharamjaigarh' },
    { lat: 22.1327, lng: 83.1461, loc: 'Boziya, Chhala',               count: 1,  herd: 'RaigarhHE1',               div: 'Dharamjaigarh' },
    { lat: 22.2709, lng: 83.1172, loc: 'Behramar, Chhala',             count: 1,  herd: 'DJME13',                   div: 'Dharamjaigarh' },
  ];

  locations.forEach(p => {
    const size = Math.max(16, Math.min(46, Math.round(Math.sqrt(p.count) * 7)));
    const half = Math.round(size / 2);
    const icon = L.divIcon({
      className: '',
      html: `<div style="
        width:${size}px;height:${size}px;border-radius:50%;
        background:rgba(230,57,70,0.88);
        border:2px solid #fff;
        box-shadow:0 0 8px rgba(230,57,70,0.7),0 2px 5px rgba(0,0,0,0.45);
        display:flex;align-items:center;justify-content:center;
      "><div style="width:4px;height:4px;border-radius:50%;background:#fff;opacity:0.9"></div></div>`,
      iconSize: [size, size],
      iconAnchor: [half, half]
    });
    L.marker([p.lat, p.lng], { icon }).addTo(map).bindPopup(
      `<b style="color:#E63946">${p.loc}</b><br>` +
      `<span style="color:#555">${p.div} &nbsp;·&nbsp; ${p.count} elephant${p.count > 1 ? 's' : ''}</span><br>` +
      `<small style="color:#777">Herd: ${p.herd}</small>`
    );
  });

  // Pulsing red rings on large herds (≥30 elephants)
  locations.filter(p => p.count >= 30).forEach(p => {
    const pulseIcon = L.divIcon({
      className: '',
      html: `<div class="pulse-ring" style="--pulse-color:#E63946;width:30px;height:30px"></div>`,
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });
    L.marker([p.lat, p.lng], { icon: pulseIcon, interactive: false }).addTo(map);
  });

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
