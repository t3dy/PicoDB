# Summary Coverage Protocol

## Goal

The portal needs a complete accounting of every section of every text. This protocol defines how to track progress.

## Coverage Levels

- `UNREAD`: cataloged but not summarized.
- `SKIMMED`: inspected for structure only.
- `SOURCE_PACKETED`: a source packet exists for a page range or reading unit.
- `SECTION_SUMMARIZED`: a section summary exists with argument and reference coverage.
- `CLAIM_EXTRACTED`: reusable claims have been entered in `claims`.
- `CROSS_LINKED`: concepts, persons, places, Pico works, and debates are linked to dossiers.
- `REVIEWED`: a human or later audit pass checked coverage against the source.
- `PROMOTED`: the section contributes to a public website page or knowledge product.

## Required Manifests

Each study pass that creates section summaries should update or create a manifest in:

`data/section_summary_coverage.json`

Each record should include:

- `id`
- `document_id`
- `work_or_book`
- `section_title`
- `page_range`
- `artifact_path`
- `coverage_level`
- `argument_coverage`
- `reference_coverage`
- `claim_count`
- `open_issues`

## Pass Order

1. Build or verify table of contents.
2. Define section boundaries.
3. Create section summaries in order.
4. Extract claims.
5. Create reference registers for dense sections.
6. Update work dossiers and concept dossiers.
7. Update gap register if a missing text, edition, manuscript, or source appears.
8. Rebuild viewer and coverage exports.

## Completeness Tests

Before marking a section `SECTION_SUMMARIZED`, check:

- Does the summary name the section's function?
- Are all major argument moves listed?
- Are all named authorities registered or explicitly deferred?
- Are all Pico works mentioned recorded?
- Are all dates and places captured for timeline/map review?
- Are all uncertain readings marked?
- Are open problems separated from established claims?

