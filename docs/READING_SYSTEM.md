# Pico Portal Reading System

## Purpose

This project treats the local corpus as the source of truth for a Pico della Mirandola knowledge portal. The first pass is deterministic: every document is converted into Markdown, cataloged in SQLite, indexed for full-text search, and split into page/bookmark reading units. Later LLM passes should produce exhaustive summaries only against these stored texts.

## Reading Passes

1. **Bibliographic audit**: verify title, author/editor/translator, date, publication venue, language, and whether the item is primary text, edition, article, review, or monograph.
2. **Structure pass**: confirm PDF bookmarks or create human-readable section/chapter units.
3. **Section summary pass**: summarize every section with claims, concepts, named figures, Pico works, and exact page anchors.
4. **Argument pass**: extract each scholar's thesis, opponent, method, evidence base, historiographical intervention, and limits.
5. **Pico work dossier pass**: aggregate every claim about each Pico text across the corpus.
6. **Gap pass**: update `pico_text_gaps` when a missing primary text, edition, manuscript, or debate appears.
7. **Portal pass**: promote reviewed cards/pages into the static site data.

## Provenance Rules

- Full text lives in `Markdown/` and `db/pages`.
- Generated summaries must identify document id, page range, and review status.
- Distinguish bibliographic fact, direct textual claim, scholarly interpretation, and portal synthesis.
- Do not collapse debates about magic, Kabbalah, concordism, or human dignity into a single consensus position.
