# PicoDB

PicoDB is a digital humanities knowledge portal for Giovanni Pico della Mirandola, his primary texts, and modern Pico scholarship.

The repository contains the deployable project layer:

- `Markdown/`: full-text Markdown conversions of the local Pico PDF/EPUB corpus.
- `db/pico.db`: SQLite catalog with document metadata, page text, section records, scholar seeds, reading tasks, text gaps, and FTS5.
- `scripts/init_pico_portal.py`: deterministic bootstrap script used to build the corpus layer.
- `data/`: manifest, ontology, conversion report, and portable corpus catalog.
- `docs/`: operating notes for the reading system, pipeline, schema, and Pico text gap register.
- `templates/`: section summary, scholar profile, and Pico work dossier templates.
- `site/index.html`: static corpus viewer.

Raw PDFs/EPUBs are not committed here. They remain in the source archive at `E:\pdf\renaissance magic\Pico`, while the database and manifests preserve source paths for provenance.

## Current State

- 73 source documents processed
- 73 Markdown full-text files
- 3,924,024 extracted words
- 10,538 page / EPUB-section records
- 1,829 section or reading-unit records
- 25 scholar-profile seeds
- 207 reading tasks
- 5 Pico primary-text gap records

## Local Viewer

From the repository root:

```powershell
python -m http.server 8876 --directory site
```

Then open:

```text
http://localhost:8876/index.html
```

## Rebuild

The original conversion script expects source PDFs/EPUBs at the project root. In this deployed repo, the raw sources are intentionally ignored, so use the source archive folder for a full rebuild unless you intentionally copy sources into a local, uncommitted working tree.
