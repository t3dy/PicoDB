function initMap() {
  if (map) { map.invalidateSize(); return; }
  map = L.map('map', { zoomControl: true });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_matter/{z}/{x}/{y}{r}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>'
  }).addTo(map);

  const ICON_MAP = {
    university_city:       { e: '🎓', bg: '#2d5fa8' },
    court_university_city: { e: '🎓', bg: '#2d5fa8' },
    study_city:            { e: '🎓', bg: '#2d5fa8' },
    birthplace_lordship:   { e: '🏰', bg: '#b8920a' },
    patronage_city:        { e: '🌿', bg: '#2d7a4a' },
    villa_milieu:          { e: '🏡', bg: '#3d6e2d' },
    papal_city:            { e: '✝',  bg: '#7a2020' },
    religious_site:        { e: '⛪', bg: '#6e3c1e' },
    power_network:         { e: '⚔', bg: '#4a4a6e' },
    detention_site:        { e: '🔒', bg: '#a82020' },
    encounter_site:        { e: '🤝', bg: '#1e6070' },
    regional_center:       { e: '🏛', bg: '#5a5a4a' },
  };

  const TYPE_LABEL = {
    university_city:       'University',
    court_university_city: 'University & Court',
    study_city:            'Study',
    birthplace_lordship:   'Birthplace & Lordship',
    patronage_city:        'Patronage',
    villa_milieu:          'Villa Milieu',
    papal_city:            'Papal City',
    religious_site:        'Religious Site',
    power_network:         'Political Network',
    detention_site:        'Detention',
    encounter_site:        'Encounter Site',
    regional_center:       'Regional Centre',
  };

  function makeIcon(type) {
    const ic = ICON_MAP[type] || { e: '📍', bg: '#666' };
    return L.divIcon({
      html: '<div style="width:36px;height:36px;border-radius:50%;background:' + ic.bg + ';border:2px solid rgba(255,255,255,0.65);display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 2px 10px rgba(0,0,0,0.6);cursor:pointer">' + ic.e + '</div>',
      className: '',
      iconSize: [36, 36],
      iconAnchor: [18, 18],
      popupAnchor: [0, -20]
    });
  }

  const SKIP = new Set(['aix_en_provence', 'arezzo', 'grenoble', 'la_frata', 'lyon']);
  const byId = Object.fromEntries(locations.map(l => [l.id, l]));
  const visible = locations.filter(l => !SKIP.has(l.id));

  for (const l of visible) {
    const tl = TYPE_LABEL[l.location_type] || l.location_type.replace(/_/g, ' ');
    const marker = L.marker([l.latitude, l.longitude], { icon: makeIcon(l.location_type) })
      .addTo(map)
      .bindPopup(
        '<strong>' + l.name + '</strong><br>' +
        '<span class="map-type">' + tl + '</span>' +
        '<div class="map-role">' + l.pico_role + '</div>'
      );

    marker.bindTooltip(
      '<span class="tt-name">' + l.name + '</span>' +
      '<span class="tt-type">' + tl + '</span>',
      {
        permanent: true,
        direction: 'top',
        offset: [0, -20],
        className: 'map-label'
      }
    );
  }

  for (const r of routes) {
    const seq = JSON.parse(r.sequence_json || '[]')
      .map(id => byId[id]).filter(Boolean).filter(l => !SKIP.has(l.id));
    if (seq.length > 1)
      L.polyline(seq.map(l => [l.latitude, l.longitude]), {
        color: '#8fc7ff', weight: 2, opacity: 0.35, dashArray: '6 5'
      }).addTo(map).bindPopup('<strong>' + r.title + '</strong><br>' + (r.summary || ''));
  }

  // Fit bounds to the actual data — Paris upper-left, Rome lower-right
  const bounds = L.latLngBounds(visible.map(l => [l.latitude, l.longitude]));
  map.fitBounds(bounds, { padding: [48, 48] });
}
