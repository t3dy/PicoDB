"""Upgrade PicoDB site/index.html: CSS polish, Scholars tab, improved nav and section intros."""
import sys

with open(r'C:\Dev\PicoDB\site\index.html', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# ============================================================
# 1. REPLACE CSS
# ============================================================
OLD_CSS = """<style>
:root { --bg:#111318; --panel:#181c24; --panel2:#202633; --text:#f2efe7; --muted:#b9b0a0; --gold:#d8b45a; --blue:#8fc7ff; --green:#6fb18a; --line:#343b4a; font-family: Inter, Segoe UI, Arial, sans-serif; }
body { margin:0; background:var(--bg); color:var(--text); line-height:1.55; }
header { padding:28px 36px 18px; border-bottom:1px solid var(--line); background:#151922; }
h1 { margin:0 0 8px; font-size:30px; letter-spacing:0; }
p { color:var(--muted); }
main { padding:24px 36px 44px; }
nav { display:flex; flex-wrap:wrap; gap:8px; margin-top:16px; }
button { background:var(--panel2); color:var(--text); border:1px solid var(--line); border-radius:6px; padding:8px 12px; cursor:pointer; }
button.active { border-color:var(--gold); color:var(--gold); }
.section { display:none; }
.section.active { display:block; }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:18px 0 26px; }
.stat,.card { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; }
.num { font-size:26px; color:var(--gold); font-weight:700; }
.label,.small { color:var(--muted); font-size:13px; }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }
h2 { margin-top:30px; color:var(--gold); font-size:20px; }
h3 { margin:0 0 6px; }
.pill { display:inline-block; margin:3px 5px 3px 0; padding:3px 8px; border-radius:999px; background:var(--panel2); color:var(--text); font-size:13px; border:1px solid var(--line); }
input { width:100%; max-width:720px; box-sizing:border-box; background:#0d1016; color:var(--text); border:1px solid var(--line); border-radius:6px; padding:10px 12px; font-size:15px; }
table { width:100%; border-collapse:collapse; margin-top:14px; font-size:14px; }
th,td { border-bottom:1px solid var(--line); padding:9px; text-align:left; vertical-align:top; }
th { color:var(--gold); background:#151922; position:sticky; top:0; }
a { color:var(--blue); }
#map { height:620px; border:1px solid var(--line); border-radius:8px; background:#0d1016; }
.timeline { border-left:2px solid var(--line); margin-left:12px; padding-left:18px; }
.event { margin:0 0 14px; padding:12px; background:var(--panel); border:1px solid var(--line); border-radius:8px; }
.event strong { color:var(--gold); }
.draft { color:var(--gold); }
</style>"""

NEW_CSS = """<style>
:root {
  --bg:#111318; --panel:#181c24; --panel2:#202633;
  --text:#f2efe7; --muted:#b9b0a0;
  --gold:#d8b45a; --blue:#8fc7ff; --green:#6fb18a; --terracotta:#c4785c;
  --line:#343b4a;
  font-family: Inter, Segoe UI, Arial, sans-serif;
}
body { margin:0; background:var(--bg); color:var(--text); line-height:1.55; }
header {
  padding:28px 36px 18px;
  border-bottom:2px solid var(--gold);
  background:#151922;
}
h1 {
  margin:0 0 4px; font-size:32px;
  font-family: Georgia, 'Times New Roman', serif;
  color:var(--gold); letter-spacing:-0.5px;
}
header p { color:var(--muted); margin:0 0 14px; font-size:15px; }
p { color:var(--muted); }
main { padding:24px 36px 44px; }
nav { display:flex; flex-wrap:wrap; gap:8px; margin-top:16px; }
button {
  background:var(--panel2); color:var(--muted);
  border:1px solid var(--line); border-radius:6px;
  padding:8px 14px; cursor:pointer; font-size:13px;
  transition: border-color 0.18s, color 0.18s, background 0.18s;
}
button:hover { border-color:var(--gold); color:var(--gold); background:rgba(216,180,90,0.06); }
button.active { border-color:var(--gold); color:var(--gold); background:rgba(216,180,90,0.1); font-weight:600; }
.section { display:none; }
.section.active { display:block; }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:18px 0 26px; }
.stat { background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; }
.card {
  background:var(--panel); border:1px solid var(--line); border-radius:8px;
  padding:14px; transition:transform 0.15s ease, box-shadow 0.15s ease;
}
.card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,0.4); border-color:#454e60; }
.scholar-card {
  background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--blue);
  border-radius:8px; padding:14px;
  transition:transform 0.15s ease, box-shadow 0.15s ease;
}
.scholar-card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,0.4); }
.num { font-size:26px; color:var(--gold); font-weight:700; }
.label,.small { color:var(--muted); font-size:13px; }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }
h2 {
  margin-top:30px; font-size:20px;
  font-family: Georgia, 'Times New Roman', serif;
  color:var(--gold);
}
h3 { margin:0 0 6px; font-size:15px; }
.pill {
  display:inline-block; margin:3px 5px 3px 0; padding:3px 8px;
  border-radius:999px; background:var(--panel2); color:var(--muted);
  font-size:12px; border:1px solid var(--line);
}
input {
  width:100%; max-width:720px; box-sizing:border-box;
  background:#0d1016; color:var(--text);
  border:1px solid var(--line); border-radius:6px;
  padding:10px 14px; font-size:15px; margin-bottom:16px;
  transition:border-color 0.18s;
}
input:focus { outline:none; border-color:var(--gold); }
table { width:100%; border-collapse:collapse; margin-top:14px; font-size:14px; }
th,td { border-bottom:1px solid var(--line); padding:9px; text-align:left; vertical-align:top; }
th { color:var(--gold); font-family:Georgia,serif; background:#151922; position:sticky; top:0; }
a { color:var(--blue); text-decoration:none; transition:color 0.15s; }
a:hover { color:var(--gold); }
#map { height:620px; border:1px solid var(--line); border-radius:8px; background:#0d1016; }
.timeline { border-left:2px solid var(--gold); margin-left:12px; padding-left:18px; }
.event {
  margin:0 0 14px; padding:12px;
  background:var(--panel); border:1px solid var(--line); border-radius:8px;
  transition:transform 0.12s ease, box-shadow 0.12s ease;
}
.event:hover { transform:translateY(-1px); box-shadow:0 4px 14px rgba(0,0,0,0.35); }
.event strong { color:var(--gold); }
.draft { color:var(--gold); }
.section-intro { color:var(--muted); margin:0 0 18px; max-width:720px; font-size:14px; }
</style>"""

if OLD_CSS in content:
    content = content.replace(OLD_CSS, NEW_CSS)
    print("OK: CSS replaced")
else:
    print("FAIL: CSS block not found")
    sys.exit(1)

# ============================================================
# 2. UPDATE NAV — add Scholars button
# ============================================================
OLD_NAV = """<nav>
<button class="active" onclick="showSection('overview', this)">Overview</button>
<button onclick="showSection('concepts', this)">Concepts</button>
<button onclick="showSection('research', this)">Research Artifacts</button>
<button onclick="showSection('timeline', this)">Timeline</button>
<button onclick="showSection('mapsec', this)">Map</button>
<button onclick="showSection('catalog', this)">Catalog</button>
</nav>"""

NEW_NAV = """<nav>
<button class="active" onclick="showSection('overview', this)">Overview</button>
<button onclick="showSection('concepts', this)">Concepts</button>
<button onclick="showSection('scholars', this)">Scholars</button>
<button onclick="showSection('research', this)">Artifacts</button>
<button onclick="showSection('timeline', this)">Timeline</button>
<button onclick="showSection('mapsec', this)">Map</button>
<button onclick="showSection('catalog', this)">Catalog</button>
</nav>"""

count = content.count(OLD_NAV)
print(f"  Nav occurrences: {count}")
if count > 0:
    content = content.replace(OLD_NAV, NEW_NAV)
    print("OK: Nav updated")
else:
    print("FAIL: Nav not matched")
    sys.exit(1)

# ============================================================
# 3. ADD SEARCH INPUT to Research Artifacts section
# ============================================================
OLD_RESEARCH_OPEN = (
    '<section id="research" class="section">\n'
    '<h2>Artifact System</h2>\n'
    '<p>The portal now tracks source packets, section summaries, claims, scholar profiles, '
    'Pico work dossiers, concept dossiers, historiography nodes, timeline events, map locations, '
    'and promoted website cards/pages.</p>\n'
    '<div class="grid">'
)

NEW_RESEARCH_OPEN = (
    '<section id="research" class="section">\n'
    '<h2>Artifact System</h2>\n'
    '<p class="section-intro">Concept dossiers, source packets, section summaries, scholar profiles, '
    'Pico work dossiers, and historiography nodes. Filter by title or artifact type.</p>\n'
    '<input id="artifactSearch" placeholder="Filter artifacts..." oninput="filterArtifacts()">\n'
    '<div class="grid" id="artifactGrid">'
)

if OLD_RESEARCH_OPEN in content:
    content = content.replace(OLD_RESEARCH_OPEN, NEW_RESEARCH_OPEN)
    print("OK: Research section updated")
else:
    print("WARN: Research open tag not matched exactly — skipping search input")

# ============================================================
# 4. INSERT SCHOLARS SECTION before timeline
# ============================================================
SCHOLARS_SECTION = """<section id="scholars" class="section">
<h2>Scholar Profiles</h2>
<p class="section-intro">Profiles of 13 scholars whose work is central to the PicoDB corpus, mapping interpretive values, theoretical commitments, and relationships to Pico's primary texts. Blue left-border indicates a dedicated values profile derived from close reading.</p>
<input id="scholarSearch" placeholder="Search scholars..." oninput="filterScholars()">
<div class="grid" id="scholarGrid">
<div class="scholar-card"><h3>Amos Edelheit</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/edelheit_values_profile.md">Edelheit Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Brian P. Copenhaver</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/copenhaver_values_profile.md">Copenhaver Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Chaim Wirszubski</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/wirszubski_values_profile.md">Wirszubski Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Crofton Black</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/crofton_black_values_profile.md">Crofton Black Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Giulio Busi</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/busi_values_profile.md">Busi Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>M. V. Dougherty</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/dougherty_values_profile.md">Dougherty Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Michael J. B. Allen</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/allen_values_profile.md">Allen Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Olga Zorzi Pugliese</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED_DRAFT</div><p><a href="../artifacts/scholar_profiles/olga_zorzi_pugliese_profile_pass018.md">Pugliese Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Sears Jayne</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED_DRAFT</div><p><a href="../artifacts/scholar_profiles/sears_jayne_profile_pass019.md">Jayne Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Sophia Howlett</h3><div class="small">scholar_profile &middot; SOURCE_ANCHORED</div><p><a href="../artifacts/scholar_profiles/howlett_values_profile.md">Howlett Values Profile &rarr;</a></p></div>
<div class="scholar-card"><h3>Brian Copenhaver (Seed)</h3><div class="small">scholar_profile &middot; DRAFT</div><p><a href="../artifacts/website_notes/scholars/copenhaver_profile_seed.md">Copenhaver Seed &rarr;</a></p></div>
<div class="scholar-card"><h3>Sophia Howlett (Seed)</h3><div class="small">scholar_profile &middot; DRAFT</div><p><a href="../artifacts/website_notes/scholars/howlett_profile_seed.md">Howlett Seed &rarr;</a></p></div>
<div class="scholar-card"><h3>Walden / Savonarola (Seed)</h3><div class="small">scholar_profile &middot; DRAFT</div><p><a href="../artifacts/website_notes/scholars/walden_savonarola_profile_seed.md">Walden Savonarola Seed &rarr;</a></p></div>
</div>
</section>
"""

TIMELINE_MARKER = '<section id="timeline" class="section">'
if TIMELINE_MARKER in content:
    content = content.replace(TIMELINE_MARKER, SCHOLARS_SECTION + TIMELINE_MARKER)
    print("OK: Scholars section inserted")
else:
    print("FAIL: timeline section marker not found")
    sys.exit(1)

# ============================================================
# 5. ADD JS FILTER FUNCTIONS
# ============================================================
OLD_JS = "function filterRows() {"
NEW_JS = """function filterArtifacts() {
  const q = document.getElementById('artifactSearch').value.toLowerCase();
  for (const el of document.querySelectorAll('#artifactGrid .card')) el.style.display = el.innerText.toLowerCase().includes(q) ? '' : 'none';
}
function filterScholars() {
  const q = document.getElementById('scholarSearch').value.toLowerCase();
  for (const el of document.querySelectorAll('#scholarGrid .scholar-card')) el.style.display = el.innerText.toLowerCase().includes(q) ? '' : 'none';
}
function filterRows() {"""

if OLD_JS in content:
    content = content.replace(OLD_JS, NEW_JS, 1)
    print("OK: JS filter functions added")
else:
    print("FAIL: filterRows() anchor not found")
    sys.exit(1)

# ============================================================
# WRITE BACK
# ============================================================
with open(r'C:\Dev\PicoDB\site\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDone. Original: {original_len} bytes -> Final: {len(content)} bytes (+{len(content)-original_len})")
