# Reading Artifact System

The Pico portal now has a markup-and-writing layer that sits between raw extracted text and polished website prose.

## Why This Exists

The corpus is too rich to summarize directly into final essays. Each reading pass should create durable intermediate artifacts: claims, section summaries, source packets, scholar profiles, work dossiers, concept dossiers, timeline events, and map locations. These artifacts let us audit where an interpretation came from and reuse the same work in biographies, summaries, maps, and long-form scholarship.

## Artifact Flow

1. `source_packet`: smallest reading unit with document id, page range, and evidence notes.
2. `claim_record`: one atomic claim extracted from a source packet.
3. `section_summary`: exhaustive summary of a chapter/section/page range.
4. `scholar_profile`: biography plus arguments and historiographical position.
5. `pico_work_dossier`: aggregated notes on a primary text by Pico.
6. `concept_dossier`: theme/concept history across Pico and scholarship.
7. `historiography_node`: debate map, including scholars who disagree.
8. `timeline_event`: dated life/reception/scholarship event.
9. `location_record`: geocoded site for the interactive map.
10. `website_card` and `website_page`: promoted public-facing forms.

## Database Tables

- `artifact_types`
- `reading_artifacts`
- `claims`
- `website_cards`
- `website_pages`
- `timeline_events`
- `locations`
- `map_routes`

## File Folders

- `artifacts/source_packets/`
- `artifacts/section_summaries/`
- `artifacts/scholar_profiles/`
- `artifacts/pico_work_dossiers/`
- `artifacts/concepts/`
- `artifacts/historiography/`
- `artifacts/website_notes/`

## Review Discipline

Every artifact has both a status and an evidence status. A useful draft is allowed, but final website prose should not erase the distinction between verified source fact, likely reconstruction, interpretation, and placeholder.

## Section Summary Discipline

Section summaries are the backbone of the project. They must follow `docs/SECTION_SUMMARY_STYLE_GUIDE.md` and include:

- section function;
- exhaustive argument summary;
- argument map;
- claims and subclaims;
- reference register;
- textual and philological notes;
- knowledge product hooks;
- open problems and follow-up tasks.

No Pico work dossier or scholar profile should be considered complete until its underlying sections have been summarized to this standard.

## Direct Essay Path (Pass 021 onwards)

For website-facing encyclopedia essays and scholar profiles, the pipeline above is supplemented by a **direct essay path** in which an agent reads scholarship from `E:\pdf\renaissance magic\pico\Markdown\` and writes a prose essay directly to the target file. This is appropriate when:

1. The relevant scholarship files are available as Markdown
2. The essay topic is well-defined and scoped to a concept or scholar
3. The goal is a standalone readable article (not a claims database)

**Status values for direct essays:**
- `COMPLETE` — full prose essay written from scholarship sources
- `DRAFT_ESSAY` — prose essay drafted but may need revision
- `ENCYCLOPEDIA_SEED_EXPANSION_REQUIRED` — old seed template NOT YET converted (deprecated format)

The old ENCYCLOPEDIA_SEED format (with Definition / Place in Pico's Works / Scholarly Stakes / Reading Questions / Expansion Plan sections) is **deprecated**. All new and revised essays must follow the CONCEPT_ENCYCLOPEDIA_STYLE_GUIDE (pass021): continuous prose, no section headings, no reading questions.

## Primary Texts Folder

`artifacts/primary_texts/` — holds extracted and translated primary source texts:
- `pico_opera_omnia_1557.md` — full Latin text extraction from the 1557 Basel Opera Omnia (~114k words, OCR quality: fair)
- `pico_letters_1557_translated.md` — English translations of Pico's letters from the 1557 edition

The PDF source is `PicoOpera.pdf` (47MB); the OCR source HTML is `PicoOpera.htm`.
