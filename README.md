# PicoDB

PicoDB is a digital humanities knowledge portal for Giovanni Pico della Mirandola, his primary texts, and modern Pico scholarship.

The repository contains the deployable project layer:

- `Markdown/`: full-text Markdown conversions of the local Pico PDF/EPUB corpus.
- `db/pico.db`: SQLite catalog with document metadata, page text, section records, scholar seeds, reading tasks, text gaps, and FTS5.
- `scripts/init_pico_portal.py`: deterministic bootstrap script used to build the corpus layer.
- `data/`: manifest, ontology, conversion report, and portable corpus catalog.
- `docs/`: operating notes for the reading system, artifact system, pipeline, schema, and Pico text gap register.
- `artifacts/`: working notes that turn readings into claims, scholar profiles, work dossiers, timeline events, map entries, and website sections.
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
- 11 artifact types
- 8 starter reading artifacts
- 6 seed claims
- 63 timeline events
- 18 mapped locations
- 4 map routes

## Reading Artifact System

The portal is designed for systematic reading and writing, not just storage. Readings should move through durable artifacts:

1. source packet
2. claim record
3. section summary
4. scholar profile
5. Pico work dossier
6. concept dossier
7. historiography node
8. timeline event
9. location record
10. website card/page

The governing files are:

- `docs/ARTIFACT_SYSTEM.md`
- `data/reading_artifact_ontology.json`
- `templates/source_packet_template.md`
- `templates/historiography_node_template.md`

The artifact tables are stored in `db/pico.db` and exported to JSON in `data/`.

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
