# Pico Portal Reading System

## Purpose

This project treats the local corpus as the source of truth for a Pico della Mirandola knowledge portal. The first pass is deterministic: every document is converted into Markdown, cataloged in SQLite, indexed for full-text search, and split into page/bookmark reading units. Later LLM passes should produce exhaustive summaries only against these stored texts.

## Reading Passes

1. **Bibliographic audit**: verify title, author/editor/translator, date, publication venue, language, and whether the item is primary text, edition, article, review, or monograph.
2. **Structure pass**: confirm PDF bookmarks or create human-readable section/chapter units.
3. **Source packet pass**: create an artifact for the smallest useful reading unit with document id, page range, local summary, persons, places, terms, and candidate claims.
4. **Claim pass**: extract atomic claims into `claims` with claim type, theme, target entity, evidence page, confidence, and review status.
5. **Section summary pass**: summarize every section with claims, concepts, named figures, Pico works, and exact page anchors.
6. **Argument pass**: extract each scholar's thesis, opponent, method, evidence base, historiographical intervention, and limits.
7. **Scholar profile pass**: build biographies of Pico scholars with their arguments and field contributions.
8. **Pico work dossier pass**: aggregate every claim about each Pico text across the corpus.
9. **Concept / historiography pass**: create concept dossiers and debate nodes for magic, Kabbalah, concordism, dignity, astrology, Aristotelianism, and Platonism.
10. **Timeline / map pass**: promote dated life events and geocoded locations to `timeline_events`, `locations`, and `map_routes`.
11. **Gap pass**: update `pico_text_gaps` when a missing primary text, edition, manuscript, or debate appears.
12. **Portal pass**: promote reviewed cards/pages into the static site data.

## Required Artifact Layer

The markup and note-taking system is defined in `docs/ARTIFACT_SYSTEM.md` and `data/reading_artifact_ontology.json`.

Working artifacts live in:

- `artifacts/source_packets/`
- `artifacts/section_summaries/`
- `artifacts/scholar_profiles/`
- `artifacts/pico_work_dossiers/`
- `artifacts/concepts/`
- `artifacts/historiography/`
- `artifacts/website_notes/`

Database-backed artifacts live in:

- `artifact_types`
- `reading_artifacts`
- `claims`
- `website_cards`
- `website_pages`
- `timeline_events`
- `locations`
- `map_routes`

## Provenance Rules

- Full text lives in `Markdown/` and `db/pages`.
- Generated summaries must identify document id, page range, and review status.
- Every interpretive paragraph intended for the website must be traceable back to at least one claim, source packet, section summary, or dossier.
- Distinguish bibliographic fact, direct textual claim, scholarly interpretation, and portal synthesis.
- Do not collapse debates about magic, Kabbalah, concordism, or human dignity into a single consensus position.
