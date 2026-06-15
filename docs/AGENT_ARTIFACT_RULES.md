# Agent Artifact Rules

This document defines which artifact types each agent role is allowed to produce or consume.

**Core rule: agents must not skip from source material to public prose.** Every stage in the pipeline produces a typed artifact that the next stage consumes. The only exception is `emergency_prose_mode: true`, which must be explicitly justified and cannot be marked `reviewed` or `published`.

## Agent Roles and Permitted Artifacts

### Extraction Agent

Reads one section of one source. Produces `raw_extraction` artifacts only.

**May produce:**
- `RawExtractionArtifact` (type: `raw_extraction`)
- `ScholarCitationArtifact` (type: `scholar_citation`) — atomic citations extracted during reading
- `TextComparisonArtifact` (type: `text_comparison`) — when assigned a comparison task

**Must not produce:**
- `InterpretiveArtifact` — no interpretation; only describe what is present
- `PublicProseArtifact` — cannot skip stages
- `CurationArtifact` — curation is a separate role

**Rules:**
- `interpretive_claims_present` MUST be `false` on every `raw_extraction` output
- Every `claims_made_by_source` item must quote or cite a specific page or passage
- Do not make `historiographical` or `synthetic` claim types in extractions
- Read one chapter or section per invocation; do not merge multiple sections into one artifact

### Validation Agent

Reads a prior artifact and checks it against the schema and evidence rules. Produces `validation` artifacts only.

**May produce:**
- `ValidationArtifact` (type: `validation`)

**May consume:**
- Any prior artifact type

**Rules:**
- Set `validation_status: fail` if any required field is missing or a schema error exists
- Set `validation_status: warn` for grounding issues that do not block publishing
- `suspected_hallucinations` should only be flagged when the claim cannot be found in the cited source, not merely for uncertainty
- Do not correct the artifact being validated — report issues and recommended fixes only

### Ontology Agent

Reads a validated `raw_extraction` and maps it onto the controlled vocabulary. Produces `ontology_tagging` artifacts only.

**May produce:**
- `OntologyTaggingArtifact` (type: `ontology_tagging`)

**May consume:**
- `RawExtractionArtifact` (required input)
- `ValidationArtifact` on the extraction (recommended before tagging)
- `SourceMetadataArtifact` (for context)

**Rules:**
- `input_artifact_id` must reference a `raw_extraction` artifact, not the source directly
- Do not write any prose description in the output — only controlled vocabulary values and tag IDs
- `pop_occult_flag: true` only for content that is demonstrably generic lifestyle spirituality; serious scholarly work on historical magic, alchemy, or Kabbalah is NOT pop occult

### Interpretation Agent

Reads prior descriptive and tagging artifacts to make bounded scholarly interpretations. Produces `interpretive` artifacts.

**May produce:**
- `InterpretiveArtifact` (type: `interpretive`)

**May consume:**
- `RawExtractionArtifact` (required)
- `OntologyTaggingArtifact` (strongly recommended)
- `ScholarCitationArtifact` (for cross-scholar synthesis)
- `ValidationArtifact` (to know what is reliable)

**Must not consume:**
- Source PDFs/Markdowns directly — use the extraction artifacts

**Rules:**
- Every `interpretive_claims` item must include either:
  - `evidence_links` with at least one entry (page-tethered), OR
  - `confidence: "speculative"` with a `limitations` explanation
- `alternative_reading` should be populated for any claim where a reasonable counter-interpretation exists
- `historiographical_relevance` must say something specific, not generic ("this is important for Pico studies")

### Curation Agent

Evaluates sources for portal inclusion. Produces `curation` artifacts.

**May produce:**
- `CurationArtifact` (type: `curation`)

**May consume:**
- `SourceMetadataArtifact`
- `OntologyTaggingArtifact`
- `InterpretiveArtifact`

**Rules:**
- `publish` or `feature` requires `reasons_for_inclusion` with at least one substantive reason
- `relevance_score` must reflect actual relevance to the esoteric studies portal, not generic scholarly quality
- Use `content_quality_flags` from the schema vocabulary — do not invent new flag values
- For the news aggregator pipeline: apply `pop_occult`, `lifestyle_spirituality`, or `ai_generated_spam` flags liberally; default to `archive` or `review` when unsure

### Writing Agent

Generates public-facing prose from prior artifacts. Produces `public_prose` artifacts.

**May produce:**
- `PublicProseArtifact` (type: `public_prose`)

**May consume:**
- `InterpretiveArtifact` (required for non-emergency prose)
- `OntologyTaggingArtifact` (for tags)
- `CurationArtifact` (for editorial angle)
- `ScholarCitationArtifact` (for specific citations to embed)
- `ValidationArtifact` (to know what has been cleared)

**Must not:**
- Read source PDFs/Markdowns directly unless `emergency_prose_mode: true` is set and justified
- Set `editorial_status: reviewed` or `published` without prior artifacts in `input_artifact_ids`
- Set `editorial_status: reviewed` or `published` in `emergency_prose_mode`

**Rules:**
- `input_artifact_ids` must list every artifact consumed, not just the most recent
- `body_markdown` must be grounded in the prior artifacts, not in the agent's background knowledge
- For encyclopedia concept essays and scholar profiles: see also `docs/CONCEPT_ENCYCLOPEDIA_STYLE_GUIDE.md` and `docs/SECTION_SUMMARY_STYLE_GUIDE.md`

### Section Summary Agent

A specialized extraction agent that reads one chapter of one scholarly text and produces a structured section summary in Markdown.

**Artifact produced:** Markdown file in `artifacts/section_summaries/{author}/`

This is a legacy format from before the typed JSON artifact system. Section summaries are not yet `raw_extraction` JSON artifacts; they occupy the same conceptual stage but use the Markdown format defined in `docs/SECTION_SUMMARY_STYLE_GUIDE.md`.

**Rules:**
- One chapter per invocation
- Must include page-tethered claims
- Must include Knowledge Product Hooks flagging downstream artifact work
- Must not jump to public prose

## Emergency Prose Mode

Setting `emergency_prose_mode: true` on a `PublicProseArtifact` is allowed for:
- Rapid prototyping when schemas are not yet populated
- Time-critical portal updates where the pipeline cannot be completed
- Writing agents that have been given explicit explicit instruction to bypass stages

Emergency prose MUST:
- Include a specific `emergency_justification`
- Be marked `editorial_status: draft`
- Never be promoted to `reviewed` or `published` without going through the normal pipeline first

Emergency prose MUST NOT be the default. If the pipeline is functioning, use it.

## Prohibited Shortcuts

The following actions are never permitted regardless of instructions:

1. Producing `public_prose` directly from source material without prior extraction, validation, and interpretation artifacts
2. Setting `interpretive_claims_present: true` on a `raw_extraction` and then using that artifact as an interpretation input without validation
3. Setting `editorial_status: published` on `public_prose` with no `input_artifact_ids`
4. Setting `relevance_status: publish` or `feature` on `curation` with empty `reasons_for_inclusion`
5. Omitting `evidence_links` on a non-speculative interpretive claim
6. Using an `artifact_type` value not in the known vocabulary
7. Re-using an existing `artifact_id` for a new artifact
