"""
Extract Latin text from PicoOpera.htm (Internet Archive OCR HTML).
Applies basic cleanup for common early-print OCR errors.
Saves to artifacts/primary_texts/pico_opera_omnia_1557.md
"""
import re, os

with open(r'C:\Dev\PicoDB\PicoOpera.htm', encoding='utf-8', errors='replace') as f:
    html = f.read()

# Extract content inside <pre>...</pre>
pre_match = re.search(r'<pre>(.*?)</pre>', html, re.DOTALL)
if not pre_match:
    print("FAIL: <pre> block not found")
    exit(1)

raw = pre_match.group(1)

# Decode HTML entities
raw = raw.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
raw = raw.replace('&#39;', "'").replace('&nbsp;', ' ')

# Remove any remaining HTML tags
raw = re.sub(r'<[^>]+>', '', raw)

# Basic OCR cleanup for early-print Latin
# Long-s: 'f' at start of syllable was often misread; this is heuristic only
# We'll keep the text as-is but do light normalization

# Fix obvious split words (space after every 2-char fragments)
# Collapse excessive whitespace within lines
lines = raw.split('\n')
cleaned = []
for line in lines:
    # Collapse internal multiple spaces to single
    line = re.sub(r'  +', ' ', line)
    line = line.strip()
    cleaned.append(line)

# Remove sequences of blank lines (keep max 2)
result = []
blank_count = 0
for line in cleaned:
    if line == '':
        blank_count += 1
        if blank_count <= 2:
            result.append('')
    else:
        blank_count = 0
        result.append(line)

text = '\n'.join(result)

# Count approximate words
words = len(text.split())
print(f"Extracted ~{words:,} words from OCR text")

# Identify major section headings (all-caps lines or lines matching title patterns)
title_pattern = re.compile(r'^[A-Z\s\.\,\-\&]{10,}$')
headings = []
for i, line in enumerate(result):
    if title_pattern.match(line) and len(line) > 10:
        headings.append(f"  Line {i+1}: {line[:80]}")

print(f"\nFound {len(headings)} potential section headings:")
for h in headings[:30]:
    print(h)

# Save
out_dir = r'C:\Dev\PicoDB\artifacts\primary_texts'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'pico_opera_omnia_1557.md')

header = """# Opera Omnia Ioannis Pici Mirandulae Concordiaeque Comitis

*Basel: Heinrich Petri, 1557*

Extracted from Internet Archive OCR (archive.org/details/bub_gb_nBiG1zAsseQC).
Source: PicoOpera.htm — Internet Archive full-text OCR of the 1557 Basel edition.
OCR quality: fair to poor; long-s (ſ) frequently read as 'f'; ligatures cause errors;
v/u interchangeable; many spacing issues. Treat as a working text, not a critical edition.

---

"""

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(header + text)

print(f"\nSaved to {out_path}")
print(f"File size: {os.path.getsize(out_path):,} bytes")
