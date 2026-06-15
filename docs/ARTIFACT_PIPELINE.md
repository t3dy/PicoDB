# Artifact Pipeline

PicoDB treats scholarly content production as a staged data pipeline. Each stage has its own schema, storage location, validation rules, and downstream consumers. **No stage may be skipped without explicit justification.**

## Core Principle

Agents must not jump from source material to polished prose. Every interpretive claim must be traceable to a source location. Every piece of public-facing content must be generated from prior artifacts, not from unstructured reading.

## Pipeline Stages

```
source material
  → A. SourceMetadataArtifact    (ingestion)
  → B. RawExtractionArtifact     (description only — no interpretation)
  → C. ValidationArtifact        (quality gate)
  → D. OntologyTaggingArtifact   (classification)
  → E. InterpretiveArtifact      (bounded scholarly interpretation)
  → F. CurationArtifact          (publish/reject decision)
  → G. PublicProseArtifact       (final public content)
```

Specialized types that can be produced at stages B–E:

- **H. TextComparisonArtifact** — comparing versions of a text or manuscript witness
- **I. ScholarCitationArtifact** — capturing what a specific scholar claims about a specific topic

## Artifact Contract

Every artifact MUST include: `artifact_id`, `artifact_type`, `schema_version`, `source_id`, `generated_at`.

These fields may NEVER be omitted. `artifact_id` must be unique across the entire project.

Additional per-type contracts:

| Type | Required beyond the core five |
|------|-------------------------------|
| validation | `target_artifact_id`, `validation_status` |
| ontology_tagging | `input_artifact_id` |
| interpretive | `input_artifact_ids` (array, ≥1) |
| curation | `input_artifact_ids`, `relevance_status`; if publish/feature → `reasons_for_inclusion` (≥1 item) |
| public_prose | `input_artifact_ids`, `title`, `body_markdown`, `editorial_status` |
| scholar_citation | `scholar_name`, `claim_summary` |
| text_comparison | `source_a_id`, `source_b_id`, `difference_type` |
| interpretive claims | each claim: `confidence`; if not speculative → `evidence_links` (≥1) |
| public_prose reviewed/published | must NOT have `emergency_prose_mode: true`; `input_artifact_ids` must reference at least one extraction and one validation artifact |

**Validation failures prevent publishing.** Validation warnings allow publishing with notation.

## Stage A: SourceMetadataArtifact

Purpose: represent an ingested source before any interpretation takes place.

Schema: `artifacts/schemas/source_metadata.schema.json`

Storage: `artifacts/generated/{source_id}/source_metadata.json`

Who produces it: ingestion scripts or human operators.

Key fields: `source_type`, `authors`, `local_path`, `raw_text_available`, `db_document_id`.

Rule: one artifact per source. A source with multiple editions needs one artifact per edition.

## Stage B: RawExtractionArtifact

Purpose: capture what is explicitly present in one section of a source — entities, terms, topics, passages, claims made by the source itself. **Must not make high-level interpretive claims.**

Schema: `artifacts/schemas/raw_extraction.schema.json`

Storage: `artifacts/generated/{source_id}/raw_extraction.{section_id}.json`

Who produces it: extraction agents reading one chapter or section at a time.

Key rule: `interpretive_claims_present` must be `false`. If an extraction agent makes interpretive claims, the artifact is flagged and must not feed an ontology_tagging or interpretive stage until reviewed.

Relation to existing types: replaces/supplements the legacy `source_packet` type in pico.db.

## Stage C: ValidationArtifact

Purpose: check whether an extraction or downstream artifact is complete, grounded, and schema-valid.

Schema: `artifacts/schemas/validation.schema.json`

Storage: `artifacts/generated/{source_id}/validation.{target_artifact_id}.json`

Who produces it: validation agents or `scripts/validate_artifacts.py` (automated structural check).

Statuses:
- `pass` — artifact is clean; downstream stages may proceed
- `warn` — artifact has issues but can proceed with notation
- `fail` — artifact is blocked; must be fixed before downstream use

Key checks: schema errors, missing required fields, grounding issues (claims without page references), suspected hallucinations, interpretive overreach in raw_extraction artifacts.

## Stage D: OntologyTaggingArtifact

Purpose: map a raw extraction onto the portal's controlled vocabulary. **Classifies; does not write public prose.**

Schema: `artifacts/schemas/ontology_tagging.schema.json`

Storage: `artifacts/generated/{source_id}/ontology_tagging.{section_id}.json`

Who produces it: ontology agents consuming a `raw_extraction` artifact.

Controlled vocabularies: `traditions`, `periods`, `genres`, `methods`, `historiographical_categories` — all use enum values defined in the schema. Tags link to `data/pico_ontology.json` entity IDs.

Esoteric-studies specific: `traditions` includes the full Western-esotericism domain vocabulary. `pop_occult_flag` is a boolean sentinel for content curation.

## Stage E: InterpretiveArtifact

Purpose: make bounded scholarly interpretations from prior descriptive and tagging artifacts.

Schema: `artifacts/schemas/interpretive.schema.json`

Storage: `artifacts/generated/{source_id}/interpretive.{topic}.json`

Who produces it: interpretation agents consuming `raw_extraction` + `ontology_tagging` artifacts.

Key rule: **every interpretive claim must have either `evidence_links` (with page references) or `confidence: "speculative"`.** Speculative claims are allowed but must be flagged. Claims without evidence links and without the speculative flag fail validation.

Relate to existing types: replaces/supplements the legacy `claim_record` type in pico.db.

## Stage F: CurationArtifact

Purpose: decide whether and how a source should appear in the portal. For the esoteric portal, this stage distinguishes serious scholarship from generic lifestyle content.

Schema: `artifacts/schemas/curation.schema.json`

Storage: `artifacts/generated/{source_id}/curation.json`

Who produces it: curation agents (for the news aggregator pipeline) or human editors.

Statuses: `reject | archive | review | publish | feature`

Rule: `publish` and `feature` require `reasons_for_inclusion` with at least one item.

For the news aggregator: this stage distinguishes `serious_scholarship`, `peer_reviewed`, `primary_source_discussion` content from `pop_occult`, `lifestyle_spirituality`, `ai_generated_spam`. See `docs/CURATION_CRITERIA.md`.

## Stage G: PublicProseArtifact

Purpose: produce final reader-facing prose only after prior stages exist.

Schema: `artifacts/schemas/public_prose.schema.json`

Storage: `artifacts/generated/{source_id}/public_prose.{slug}.json`

Who produces it: writing agents consuming prior artifacts.

Key rules:
- `input_artifact_ids` must list the prior artifacts consumed
- `editorial_status: reviewed` or `published` requires `input_artifact_ids` to include at least one extraction and one validation artifact
- `emergency_prose_mode: true` is an explicit escape hatch for prototype work; must be justified in `emergency_justification`; may not be marked `reviewed` or `published`

Relation to existing types: feeds into legacy `website_card` and `website_page` in pico.db, tracked by `db_website_card_id` and `db_website_page_id`.

## Specialized Types

### H. TextComparisonArtifact

Use when comparing edition variants, manuscript witnesses, or translations of the same text.

Schema: `artifacts/schemas/text_comparison.schema.json`

Storage: `artifacts/generated/{source_id}/text_comparison.{section_id}.json`

`difference_type` vocabulary: `addition | omission | substitution | reordering | expansion | compression | terminology_shift | doctrinal_shift | uncertain`

### I. ScholarCitationArtifact

Use to capture a specific, atomic, page-tethered claim made by a scholar about a topic. These are the building blocks of scholar profiles and concept dossiers.

Schema: `artifacts/schemas/scholar_citation.schema.json`

Storage: `artifacts/generated/{source_id}/scholar_citation.{scholar}.{topic}.{seq}.json`

`historiographical_angle` vocabulary maps to the guide-scholar matrix in `data/reading_artifact_ontology.json`.

## Storage Layout

```
artifacts/
  schemas/           — JSON Schema files (A–I above)
  fixtures/          — Example artifacts using real PicoDB content
  generated/
    {source_id}/
      source_metadata.json
      raw_extraction.{section_id}.json
      validation.raw_extraction.{section_id}.json
      ontology_tagging.{section_id}.json
      interpretive.{topic}.json
      curation.json
      public_prose.{slug}.json
      scholar_citation.{scholar}.{topic}.{seq}.json
      text_comparison.{section_id}.json
```

## Validation

Run `python scripts/validate_artifacts.py` to validate all files in `artifacts/fixtures/` and `artifacts/generated/`.

Requires: `pip install jsonschema`

Exit codes: 0 = pass, 1 = errors found.

The validator checks: schema conformance, required provenance fields, unique artifact_ids, interpretive claim evidence rules, public_prose status requirements, curation publish rules, and known artifact_type values.

## Relation to Legacy Artifact Types

The new typed artifact system is additive. The following legacy types in `pico.db` remain in use:

| Legacy type | Superseded or extended by |
|-------------|--------------------------|
| `source_packet` | `raw_extraction` (richer schema) |
| `claim_record` | `interpretive` + `scholar_citation` |
| `section_summary` | produced from `raw_extraction` artifacts; not yet typed in this schema system |
| `scholar_profile` | produced from `scholar_citation` artifacts; not yet typed |
| `concept_dossier` | produced from `interpretive` artifacts; not yet typed |
| `website_card` | `public_prose` (with `db_website_card_id`) |
| `website_page` | `public_prose` (with `db_website_page_id`) |

The typed JSON artifact system does not replace the database; it provides the structured intermediate layer that was previously absent.
