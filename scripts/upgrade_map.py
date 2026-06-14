"""Upgrade PicoDB map: dark tiles, focused zoom, custom emoji icons, legend, styled popups."""
import re

with open(r'C:\Dev\PicoDB\site\index.html', encoding='utf-8') as f:
    content = f.read()

with open(r'C:\Dev\PicoDB\scripts\initmap_new.js', encoding='utf-8') as f:
    NEW_INITMAP = f.read().strip()

# ============================================================
# 1. ADD MAP CSS (after input:focus rule)
# ============================================================
OLD_FOCUS = "input:focus { outline:none; border-color:var(--gold); }"
MAP_CSS = (
    "\n.leaflet-popup-content-wrapper {\n"
    "  background:#181c24 !important; color:#f2efe7 !important;\n"
    "  border:1px solid #343b4a !important; border-radius:8px !important;\n"
    "  box-shadow:0 4px 20px rgba(0,0,0,0.7) !important;\n"
    "}\n"
    ".leaflet-popup-tip { background:#181c24 !important; }\n"
    ".leaflet-popup-content strong { color:#d8b45a; }\n"
    ".leaflet-popup-content .map-type { color:#8fc7ff; font-size:12px; text-transform:uppercase; letter-spacing:.04em; }\n"
    ".leaflet-popup-content .map-role { color:#b9b0a0; font-size:13px; margin-top:6px; line-height:1.4; }\n"
    ".leaflet-container a.leaflet-popup-close-button { color:#b9b0a0 !important; }\n"
    "#mapLegend { display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 14px; font-size:12px; }\n"
    "#mapLegend span { background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:4px 10px; color:var(--muted); }"
)

if OLD_FOCUS in content:
    content = content.replace(OLD_FOCUS, OLD_FOCUS + MAP_CSS)
    print("OK: Map CSS added")
else:
    print("FAIL: CSS anchor not found")

# ============================================================
# 2. UPDATE MAPSEC HTML
# ============================================================
OLD_H2 = '<h2>Italy-France Pico Map</h2>'
OLD_P   = ('<p>Locations include birth, study, patronage, papal trouble, French detention, '
           'late Florence, and provisional route nodes. Provisional nodes are labeled in their popups.</p>')
OLD_MAP_DIV = '<div id="map"></div>'

MAPSEC_BLOCK = OLD_H2 + '\n' + OLD_P + '\n' + OLD_MAP_DIV

NEW_MAPSEC_BLOCK = (
    '<h2>Pico’s Geography</h2>\n'
    '<p class="section-intro">Fifteen locations spanning Pico’s birth, university years, '
    'Medici patronage, papal dispute, French detention at Vincennes, and final years in Florence. '
    'Click any marker for details.</p>\n'
    '<div id="mapLegend">\n'
    '  <span>\U0001F393 Study / University</span>\n'
    '  <span>\U0001F3F0 Birthplace &amp; Lordship</span>\n'
    '  <span>\U0001F33F Medici Patronage</span>\n'
    '  <span>\U0001F3E1 Villa &amp; Retreat</span>\n'
    '  <span>✝ Papal Rome</span>\n'
    '  <span>⛪ Religious Site</span>\n'
    '  <span>⚔ Political Network</span>\n'
    '  <span>\U0001F512 Detention</span>\n'
    '  <span>\U0001F91D Encounter</span>\n'
    '</div>\n'
    '<div id="map"></div>'
)

if MAPSEC_BLOCK in content:
    content = content.replace(MAPSEC_BLOCK, NEW_MAPSEC_BLOCK)
    print("OK: Mapsec HTML updated")
else:
    print("WARN: exact mapsec block not matched, trying partial replacements")
    if OLD_H2 in content:
        content = content.replace(OLD_H2, '<h2>Pico’s Geography</h2>')
        print("  OK: h2 replaced")
    if OLD_P in content:
        content = content.replace(
            OLD_P,
            '<p class="section-intro">Fifteen locations spanning Pico’s birth, university years, '
            'Medici patronage, papal dispute, French detention at Vincennes, and final years in Florence. '
            'Click any marker for details.</p>\n'
            '<div id="mapLegend">\n'
            '  <span>\U0001F393 Study / University</span>\n'
            '  <span>\U0001F3F0 Birthplace &amp; Lordship</span>\n'
            '  <span>\U0001F33F Medici Patronage</span>\n'
            '  <span>\U0001F3E1 Villa &amp; Retreat</span>\n'
            '  <span>✝ Papal Rome</span>\n'
            '  <span>⛪ Religious Site</span>\n'
            '  <span>⚔ Political Network</span>\n'
            '  <span>\U0001F512 Detention</span>\n'
            '  <span>\U0001F91D Encounter</span>\n'
            '</div>'
        )
        print("  OK: description + legend inserted")

# ============================================================
# 3. REPLACE initMap() using regex
# ============================================================
m = re.search(r'function initMap\(\) \{.*?\n\}', content, re.DOTALL)
if m:
    content = content[:m.start()] + NEW_INITMAP + content[m.end():]
    print("OK: initMap() replaced")
else:
    print("FAIL: initMap() not found")

# ============================================================
# WRITE BACK
# ============================================================
with open(r'C:\Dev\PicoDB\site\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Done. File: {len(content)} bytes")
