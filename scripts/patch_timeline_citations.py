"""Regenerate timelineList HTML from JSON, adding source_note as a visible citation."""
import json, html as htmllib

with open(r'C:\Dev\PicoDB\data\pico_life_timeline.json', encoding='utf-8') as f:
    events = json.load(f)

with open(r'C:\Dev\PicoDB\site\index.html', encoding='utf-8') as f:
    content = f.read()

# ── Build new timelineList HTML ──────────────────────────────────────────────
def build_timeline_html(events):
    parts = ['<div class="timeline" id="timelineList">\n']
    for e in events:
        date    = htmllib.escape(e.get('date_label', ''))
        title   = htmllib.escape(e.get('title', ''))
        summary = htmllib.escape(e.get('summary', ''))
        cat     = htmllib.escape(e.get('category', ''))
        status  = htmllib.escape(e.get('evidence_status', ''))
        note    = e.get('source_note', '').strip()

        cite_html = ''
        if note:
            # Distinguish substantive citations from internal placeholder notes
            placeholder_markers = ('needs', 'verify', 'confirm', 'inferred',
                                   'inference', 'placeholder', 'general chronology',
                                   'portal synthesis')
            is_placeholder = any(note.lower().startswith(p) or
                                 'needs ' in note.lower() or
                                 note.lower().startswith('general') or
                                 note.lower().startswith('portal synthesis') or
                                 note.lower().startswith('infer')
                                 for p in placeholder_markers)
            cite_class = 'event-cite event-cite-placeholder' if is_placeholder else 'event-cite'
            cite_html = f'<div class="{cite_class}">&#128218; {htmllib.escape(note)}</div>'

        parts.append(
            f"<div class='event'>"
            f"<strong>{date}: {title}</strong>"
            f"<div class='small'>{cat} &middot; {status}</div>"
            f"<p>{summary}</p>"
            f"{cite_html}"
            f"</div>"
        )
    parts.append('\n</div>')
    return ''.join(parts)

NEW_LIST_HTML = build_timeline_html(events)

# ── Replace old timelineList block ───────────────────────────────────────────
tl_start   = content.find('<section id="timeline"')
mapsec_start = content.find('<section id="mapsec"')
timeline_block = content[tl_start:mapsec_start]

list_open_marker = '<div class="timeline" id="timelineList">'
list_open_pos = timeline_block.find(list_open_marker)
list_close_pos = timeline_block.rfind('</div>') + 6  # outer div close

old_list = timeline_block[list_open_pos:list_close_pos]
new_timeline_block = timeline_block[:list_open_pos] + NEW_LIST_HTML + timeline_block[list_close_pos:]

content = content[:tl_start] + new_timeline_block + content[mapsec_start:]

# ── Add CSS for citations ─────────────────────────────────────────────────────
CSS_ANCHOR = ".event strong { color:var(--gold); }"
CITE_CSS = (
    "\n.event-cite {"
    "\n  margin-top:8px; padding-top:7px;"
    "\n  border-top:1px solid var(--line);"
    "\n  color:var(--blue); font-size:12px; font-style:italic; line-height:1.4;"
    "\n}"
    "\n.event-cite-placeholder { color:var(--muted); }"
)

if CSS_ANCHOR in content:
    content = content.replace(CSS_ANCHOR, CSS_ANCHOR + CITE_CSS)
    print("OK: Citation CSS added")
else:
    print("WARN: CSS anchor not found")

with open(r'C:\Dev\PicoDB\site\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"OK: Timeline regenerated ({len(events)} events). File: {len(content)} bytes")
