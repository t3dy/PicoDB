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
