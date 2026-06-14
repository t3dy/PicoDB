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
