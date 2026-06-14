"""Patch: replace initMap() and add permanent-label CSS."""
import re

with open(r'C:\Dev\PicoDB\site\index.html', encoding='utf-8') as f:
    content = f.read()

with open(r'C:\Dev\PicoDB\scripts\initmap_new.js', encoding='utf-8') as f:
    NEW_INITMAP = f.read().strip()

# 1. Replace initMap()
m = re.search(r'function initMap\(\) \{.*?\n\}', content, re.DOTALL)
if m:
    content = content[:m.start()] + NEW_INITMAP + content[m.end():]
    print("OK: initMap() replaced")
else:
    print("FAIL: initMap not found")

# 2. Add tooltip label CSS after the existing map-label-adjacent rules
LABEL_CSS = (
    "\n.map-label {"
    "\n  background:rgba(17,19,24,0.82) !important;"
    "\n  border:1px solid rgba(216,180,90,0.3) !important;"
    "\n  border-radius:5px !important;"
    "\n  box-shadow:0 2px 8px rgba(0,0,0,0.6) !important;"
    "\n  padding:3px 7px !important;"
    "\n  white-space:nowrap;"
    "\n}"
    "\n.map-label::before { display:none !important; }"
    "\n.tt-name {"
    "\n  display:block;"
    "\n  color:#f2efe7;"
    "\n  font-size:12px;"
    "\n  font-weight:600;"
    "\n  letter-spacing:.01em;"
    "\n}"
    "\n.tt-type {"
    "\n  display:block;"
    "\n  color:#8fc7ff;"
    "\n  font-size:10px;"
    "\n  margin-top:1px;"
    "\n}"
)

ANCHOR = "#mapLegend span { background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:4px 10px; color:var(--muted); }"
if ANCHOR in content:
    content = content.replace(ANCHOR, ANCHOR + LABEL_CSS)
    print("OK: Label CSS added")
else:
    print("FAIL: CSS anchor not found")

with open(r'C:\Dev\PicoDB\site\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Done. {len(content)} bytes")
