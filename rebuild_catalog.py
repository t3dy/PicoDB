#!/usr/bin/env python3
"""
Rebuild the PicoDB website catalog to display scholarly sources with citations.
"""

import json
import re

# Read the current HTML
with open(r"C:\Dev\PicoDB\site\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Read the sources database
with open(r"C:\Dev\PicoDB\data\sources.json", "r", encoding="utf-8") as f:
    sources_data = json.load(f)

# New catalog HTML section
new_catalog = '''
<!-- SOURCES CATALOG -->
<div id="catalog-section" style="display:none;">
  <div style="margin-bottom:24px;">
    <input type="text" id="source-search" placeholder="Search by title, author, or year..."
           style="margin-bottom:16px;">
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
      <button onclick="filterSources('all')" class="filter-btn active" data-filter="all">All</button>
      <button onclick="filterSources('primary')" class="filter-btn" data-filter="primary">Primary</button>
      <button onclick="filterSources('secondary')" class="filter-btn" data-filter="secondary">Secondary</button>
    </div>
  </div>

  <div id="sources-container" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(380px,1fr)); gap:16px;">
    <!-- Populated by JavaScript -->
  </div>
</div>

<script>
let allSources = null;
let currentFilter = 'all';

async function loadSources() {
  try {
    const response = await fetch('./data/sources.json');
    allSources = await response.json();
    renderSources(allSources.sources);
  } catch (e) {
    console.error('Failed to load sources:', e);
    document.getElementById('sources-container').innerHTML =
      '<p style="color:#c4785c;">Failed to load sources catalog.</p>';
  }
}

function renderSources(sources) {
  const container = document.getElementById('sources-container');
  if (!sources || sources.length === 0) {
    container.innerHTML = '<p style="color:#b9b0a0;">No sources found.</p>';
    return;
  }

  container.innerHTML = sources.map(source => `
    <div class="card" style="border-left:3px solid ${source.type === 'primary' ? '#6fb18a' : '#8fc7ff'};">
      <div style="margin-bottom:8px;">
        <div style="color:#d8b45a; font-size:11px; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:4px;">
          ${source.type === 'primary' ? 'Primary Source' : 'Scholarship'}
        </div>
        <h3 style="margin:0 0 4px; font-size:15px; line-height:1.3;">${escapeHtml(source.title)}</h3>
        <div style="color:#8fc7ff; font-size:13px; margin-bottom:8px;">
          ${source.authors.map(a => escapeHtml(a)).join('; ')}
        </div>
        <div style="color:#b9b0a0; font-size:13px; margin-bottom:8px;">
          ${source.year}
        </div>
      </div>

      <p style="margin:0 0 12px; color:#b9b0a0; font-size:14px; line-height:1.4;">
        ${escapeHtml(source.summary)}
      </p>

      <div style="border-top:1px solid #343b4a; padding-top:12px; margin-top:12px;">
        <div style="font-size:12px; color:#b9b0a0; margin-bottom:8px;">
          <strong>Cite:</strong>
        </div>
        <div style="display:flex; gap:6px; flex-wrap:wrap;">
          <button onclick="copyCitation(${JSON.stringify(source.citation.chicago).replace(/"/g, '&quot;')}, 'Chicago')"
                  style="padding:4px 8px; font-size:11px;">Chicago</button>
          <button onclick="copyCitation(${JSON.stringify(source.citation.mla).replace(/"/g, '&quot;')}, 'MLA')"
                  style="padding:4px 8px; font-size:11px;">MLA</button>
          <button onclick="copyCitation(${JSON.stringify(source.citation.bibtex).replace(/"/g, '&quot;')}, 'BibTeX')"
                  style="padding:4px 8px; font-size:11px;">BibTeX</button>
        </div>
      </div>
    </div>
  `).join('');
}

function filterSources(type) {
  currentFilter = type;

  // Update active button
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
    if (btn.dataset.filter === type) btn.classList.add('active');
  });

  // Filter and render
  const filtered = type === 'all'
    ? allSources.sources
    : allSources.sources.filter(s => s.type === type);

  const searchTerm = document.getElementById('source-search').value.toLowerCase();
  const results = filtered.filter(s =>
    s.title.toLowerCase().includes(searchTerm) ||
    s.authors.some(a => a.toLowerCase().includes(searchTerm)) ||
    s.year.toString().includes(searchTerm)
  );

  renderSources(results);
}

function copyCitation(citation, format) {
  // Decode HTML entities first
  const textarea = document.createElement('textarea');
  textarea.innerHTML = citation;
  const decoded = textarea.value;

  navigator.clipboard.writeText(decoded).then(() => {
    const btn = event.target;
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    btn.style.color = '#6fb18a';
    setTimeout(() => {
      btn.textContent = orig;
      btn.style.color = 'var(--muted)';
    }, 2000);
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Search in real-time
document.addEventListener('DOMContentLoaded', function() {
  loadSources();

  const searchInput = document.getElementById('source-search');
  if (searchInput) {
    searchInput.addEventListener('input', () => filterSources(currentFilter));
  }
});
</script>
'''

# Find and replace the catalog button to show the new section
html = html.replace(
    "showSection('catalog', this)",
    "document.getElementById('catalog-section').style.display='block'; document.querySelectorAll('#catalog-section').forEach(e => e.classList.add('active')); this.classList.add('active'); document.querySelectorAll('nav button').forEach(b => b.classList.remove('active')); this.classList.add('active')"
)

# Find the position to insert the new catalog
# Look for where the sections start
catalog_marker = html.find("showSection('catalog'")
if catalog_marker > 0:
    # Find the next major section after the buttons
    next_section = html.find("<h2>", catalog_marker + 200)

    if next_section > 0:
        # Insert the new catalog section before the first h2
        html = html[:next_section] + new_catalog + "\n\n" + html[next_section:]

# Save the modified HTML
with open(r"C:\Dev\PicoDB\site\index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] Catalog section rebuilt")
print("[OK] Sources catalog added with search, filter, and citation features")
