"""
Patch site/index.html to:
1. Embed CONCEPTS JS variable with full data including summaries
2. Replace static conceptGrid HTML with JS-rendered cards
3. Add concept modal overlay (HTML, CSS, JS)
"""
import json, html as htmllib, re

# Load concept card data
with open(r'C:\Dev\PicoDB\data\website_cards.json', encoding='utf-8') as f:
    all_cards = json.load(f)

# Load generated summaries
with open(r'C:\Dev\PicoDB\data\concept_summaries.json', encoding='utf-8') as f:
    summaries = json.load(f)

# Load scholars from concepts_for_summary.json
with open(r'C:\Dev\PicoDB\data\concepts_for_summary.json', encoding='utf-8') as f:
    concepts_meta = json.load(f)
scholars_map = {c['id']: c.get('guide_scholars', '') for c in concepts_meta}

# Filter to concept cards only
concept_cards = [c for c in all_cards if c.get('entity_type') == 'concept']

# Build merged CONCEPTS list
concepts_data = []
for c in concept_cards:
    cid = c['id']
    summary = summaries.get(cid, c.get('summary', ''))
    scholars = scholars_map.get(cid, '')
    # Build artifact path for "Read more" link
    src = c.get('source_artifact_id', '')
    if src.startswith('encyclopedia_concept_'):
        slug = src.replace('encyclopedia_concept_', '')
        md_path = f'../artifacts/concepts/encyclopedia/{slug}.md'
    else:
        slug = src.replace('concept_pico_', '').replace('concept_', '').replace('concept-', '').replace('-', '_')
        md_path = f'../artifacts/concepts/encyclopedia/{slug}.md'

    concepts_data.append({
        'id': cid,
        'title': c.get('title', ''),
        'loci': c.get('subtitle', ''),
        'scholars': scholars,
        'summary': summary,
        'status': c.get('status', ''),
        'md_path': md_path
    })

# Sort alphabetically by title
concepts_data.sort(key=lambda x: x['title'].lower())

with open(r'C:\Dev\PicoDB\site\index.html', encoding='utf-8') as f:
    content = f.read()

# ── 1. Inject CONCEPTS JS variable ──────────────────────────────────────────────
CONCEPTS_JS = 'const CONCEPTS = ' + json.dumps(concepts_data, ensure_ascii=False, indent=None) + ';\n'

# Insert after the existing JS variables (find 'let map;')
MAP_ANCHOR = 'let map;'
if MAP_ANCHOR in content:
    content = content.replace(MAP_ANCHOR, CONCEPTS_JS + MAP_ANCHOR)
    print('OK: CONCEPTS JS variable injected')
else:
    print('FAIL: map anchor not found')

# ── 2. Add Concept Modal HTML (before </body>) ────────────────────────────────
MODAL_HTML = '''
<div id="conceptModal" class="concept-modal-overlay" onclick="if(event.target===this)closeConcept()">
  <div class="concept-modal-box" role="dialog" aria-modal="true">
    <button class="concept-modal-close" onclick="closeConcept()" aria-label="Close">&times;</button>
    <div id="conceptModalBody"></div>
  </div>
</div>
'''

if '</body>' in content:
    content = content.replace('</body>', MODAL_HTML + '</body>')
    print('OK: Modal HTML injected')
else:
    print('FAIL: </body> not found')

# ── 3. Add Concept Modal CSS ──────────────────────────────────────────────────
MODAL_CSS = '''
/* ── Concept Cards ─────────────────────────────────── */
#conceptGrid .card {
  cursor: pointer;
  border-left: 3px solid var(--gold);
  padding-left: 14px;
  transition: transform .15s, box-shadow .15s;
}
#conceptGrid .card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 24px rgba(0,0,0,.5);
}
#conceptGrid .card h3 { color: var(--gold); margin-bottom: 4px; }
#conceptGrid .card .card-loci { color: var(--blue); font-size: 12px; margin-bottom: 8px; letter-spacing: .02em; }
#conceptGrid .card .card-summary { color: var(--text); font-size: 13px; line-height: 1.5; margin-bottom: 10px; }
#conceptGrid .card .card-more { color: var(--gold); font-size: 12px; font-style: italic; }

/* ── Concept Modal ─────────────────────────────────── */
.concept-modal-overlay {
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,.75);
  z-index: 1000;
  align-items: center; justify-content: center;
  padding: 24px;
}
.concept-modal-overlay.open { display: flex; }
.concept-modal-box {
  background: var(--panel);
  border: 1px solid var(--line);
  border-top: 3px solid var(--gold);
  border-radius: 10px;
  max-width: 680px; width: 100%;
  max-height: 80vh; overflow-y: auto;
  padding: 32px 36px;
  position: relative;
  box-shadow: 0 16px 64px rgba(0,0,0,.8);
}
.concept-modal-close {
  position: absolute; top: 14px; right: 18px;
  background: none; border: none;
  color: var(--muted); font-size: 22px; cursor: pointer;
  line-height: 1;
}
.concept-modal-close:hover { color: var(--text); }
.concept-modal-title {
  font-family: Georgia, serif;
  font-size: 22px; color: var(--gold);
  margin: 0 0 6px; font-weight: normal;
}
.concept-modal-loci {
  color: var(--blue); font-size: 12px;
  text-transform: uppercase; letter-spacing: .06em;
  margin-bottom: 18px;
}
.concept-modal-summary {
  color: var(--text); font-size: 15px; line-height: 1.7;
  margin-bottom: 20px;
}
.concept-modal-scholars {
  display: flex; flex-wrap: wrap; gap: 8px;
  margin-bottom: 20px;
}
.concept-modal-scholar-label {
  font-size: 11px; color: var(--muted); text-transform: uppercase;
  letter-spacing: .06em; align-self: center;
}
.concept-modal-scholars span {
  background: var(--panel2);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 12px; color: var(--text);
}
.concept-modal-link {
  display: inline-block;
  color: var(--gold); font-size: 13px;
  border: 1px solid var(--gold);
  border-radius: 5px; padding: 6px 16px;
  text-decoration: none;
  transition: background .15s;
}
.concept-modal-link:hover { background: rgba(216,180,90,.1); }
.concept-modal-status {
  font-size: 11px; color: var(--muted);
  margin-top: 16px; padding-top: 12px;
  border-top: 1px solid var(--line);
}
'''

# Insert before </style>
STYLE_CLOSE = '</style>'
if STYLE_CLOSE in content:
    content = content.replace(STYLE_CLOSE, MODAL_CSS + STYLE_CLOSE, 1)
    print('OK: Modal CSS injected')
else:
    print('FAIL: </style> not found')

# ── 4. Add Modal JS functions ──────────────────────────────────────────────────
MODAL_JS = '''
function openConcept(id) {
  const c = CONCEPTS.find(x => x.id === id);
  if (!c) return;
  const scholars = (c.scholars || '').split(/[,;]/).map(s => s.trim()).filter(Boolean);
  const scholarHtml = scholars.length
    ? '<div class="concept-modal-scholars"><span class="concept-modal-scholar-label">Key scholars:</span>' + scholars.map(s => '<span>' + s + '</span>').join('') + '</div>'
    : '';
  const statusNote = c.status && c.status !== 'ENCYCLOPEDIA_SEED'
    ? '<div class="concept-modal-status">Status: ' + c.status.replace(/_/g,' ') + '</div>'
    : '';
  document.getElementById('conceptModalBody').innerHTML =
    '<h2 class="concept-modal-title">' + c.title + '</h2>' +
    (c.loci ? '<div class="concept-modal-loci">In: ' + c.loci + '</div>' : '') +
    '<p class="concept-modal-summary">' + (c.summary || '') + '</p>' +
    scholarHtml +
    '<a class="concept-modal-link" href="' + c.md_path + '" target="_blank">Full research entry →</a>' +
    statusNote;
  document.getElementById('conceptModal').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeConcept() {
  document.getElementById('conceptModal').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeConcept(); });

function renderConcepts(list) {
  const grid = document.getElementById('conceptGrid');
  if (!grid) return;
  grid.innerHTML = list.map(c => {
    const teaser = c.summary ? c.summary.split('. ').slice(0,2).join('. ') + (c.summary.split('. ').length > 2 ? '.' : '') : '';
    return '<div class="card" onclick="openConcept(\\''+c.id+'\\')">'+
      '<h3>'+c.title+'</h3>'+
      (c.loci ? '<div class="card-loci">'+c.loci+'</div>' : '')+
      (teaser ? '<div class="card-summary">'+teaser+'</div>' : '')+
      '<div class="card-more">Explore →</div>'+
      '</div>';
  }).join('');
}

function filterConcepts() {
  const q = document.getElementById('conceptSearch').value.toLowerCase();
  const filtered = q ? CONCEPTS.filter(c =>
    c.title.toLowerCase().includes(q) ||
    (c.summary || '').toLowerCase().includes(q) ||
    (c.loci || '').toLowerCase().includes(q)
  ) : CONCEPTS;
  renderConcepts(filtered);
}
'''

# Insert modal JS before the closing script tag (just before </script>)
# Find the filterConcepts function and replace it
OLD_FILTER = '''function filterConcepts() {
  const q = document.getElementById('conceptSearch').value.toLowerCase();
  for (const el of document.querySelectorAll('#conceptGrid .card')) el.style.display = el.innerText.toLowerCase().includes(q) ? '' : 'none';
}'''

if OLD_FILTER in content:
    content = content.replace(OLD_FILTER, MODAL_JS)
    print('OK: Modal JS injected (replaced filterConcepts)')
else:
    print('WARN: filterConcepts not found exactly; appending before </script>')
    content = content.replace('</script>', MODAL_JS + '\n</script>', 1)

# ── 5. Replace static conceptGrid HTML with JS render call ────────────────────
# Find the static grid and replace with empty div + onload init
GRID_OPEN = '<div class="grid" id="conceptGrid">'
grid_start = content.find(GRID_OPEN)
grid_end   = content.find('</div>', grid_start) + 6

if grid_start > 0:
    old_grid = content[grid_start:grid_end]
    new_grid = '<div class="grid" id="conceptGrid"></div>'
    content = content[:grid_start] + new_grid + content[grid_end:]
    print('OK: Static conceptGrid replaced with empty div')
else:
    print('FAIL: conceptGrid not found')

# ── 6. Add renderConcepts() call on tab activation ───────────────────────────
# Find the showSection function and add concept init
OLD_SHOW = "function showSection(id) {"
NEW_SHOW = """function showSection(id) {
  if (id === 'concepts') { renderConcepts(CONCEPTS); }"""
if OLD_SHOW in content:
    content = content.replace(OLD_SHOW, NEW_SHOW, 1)
    print('OK: renderConcepts hooked into showSection')
else:
    # Try alternate hook via init
    print('WARN: showSection not found; adding DOMContentLoaded init')
    INIT_JS = '''
document.addEventListener('DOMContentLoaded', function() {
  const activeSection = document.querySelector('.section.active');
  if (activeSection && activeSection.id === 'concepts') renderConcepts(CONCEPTS);
});
'''
    content = content.replace('</script>', INIT_JS + '</script>', 1)

# Write back
with open(r'C:\Dev\PicoDB\site\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Done. File: {len(content)} bytes')
