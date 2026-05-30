// Maps module — Leaflet-based map initializers
// All maps are initialized lazily; subsequent calls are no-ops.

const mapsInitialized = {};

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
    .bindPopup('<b>Raigarh Van Mandal</b><br>18 elephant casualties<br>9 human casualties');

  // Forest patches (rough polygons)
  L.polygon([
    [22.0, 82.9], [22.5, 83.0], [22.8, 83.2], [22.9, 83.5],
    [22.6, 83.8], [22.2, 83.9], [21.9, 83.6], [21.8, 83.2]
  ], {
    color: '#1B4332', weight: 1, fill: true,
    fillOpacity: 0.2, fillColor: '#52B788'
  }).addTo(map).bindPopup('Core Forest Area');

  setTimeout(() => map.invalidateSize(), 200);
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

  setTimeout(() => map.invalidateSize(), 200);
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

  setTimeout(() => map.invalidateSize(), 200);
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
