# Database Schema

Core tables:

- `documents`: bibliographic and extraction metadata, source path, Markdown path, type, themes, Pico works, hash, duplicate link.
- `pages`: page- or EPUB-section-level full text.
- `sections`: PDF bookmark rows or generated reading units; summary fields are pending.
- `scholars`: seeded scholar names detected from filenames/full text; biographies pending.
- `ontology_terms`: entity classes, themes, relationship vocabulary, evidence statuses.
- `reading_tasks`: queue for section summaries, scholar profiles, Pico work dossiers, and gap audits.
- `pico_text_gaps`: living accounting of primary texts/editions still to locate or verify.
- `document_fts`: FTS5 index for source search.

**New in pass021:** The `artifacts/primary_texts/` folder holds extracted and translated primary source texts directly (not database-backed): `pico_opera_omnia_1557.md` (114k word Latin extraction from the 1557 Basel edition) and `pico_letters_1557_translated.md` (English translations of Pico's letters). These complement the database schema below.

Research artifact tables:

- `artifact_types`: controlled vocabulary for source packets, claims, section summaries, scholar profiles, work dossiers, concept dossiers, historiography nodes, timeline events, location records, and website outputs.
- `reading_artifacts`: file-backed working notes with type, target entity, status, and evidence status.
- `claims`: atomic source-tethered assertions with claim type, theme, target, evidence page, confidence, and review status.
- `website_cards`: short public-facing browse cards seeded from reviewed or draft artifacts.
- `website_pages`: long-form public pages when dossiers or profiles are promoted.
- `timeline_events`: dated life, publication, controversy, travel, reception, and scholarship events.
- `locations`: geocoded places for Pico's life, study, patronage, trouble, and reception.
- `map_routes`: named sequences of locations for interactive map routes.
