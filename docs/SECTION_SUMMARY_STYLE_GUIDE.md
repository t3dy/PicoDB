# Section Summary Style Guide

## Purpose

Every Pico text and every scholarly work must eventually have a section-by-section summary that is detailed enough to support website pages, biographies, timelines, maps, concept dossiers, and new scholarship without rereading the source from scratch.

This style guide defines the minimum standard for a `section_summary` artifact.

## Definition of a Section

A section is the smallest stable unit that can be summarized without distorting the argument.

Use, in order:

1. Authorial chapter/section headings.
2. Translator/editor section divisions.
3. PDF bookmark units.
4. Printed-page ranges when no stable headings exist.
5. A controlled reading unit created by PicoDB, with a short rationale.

When a generated section crosses authorial boundaries, split it. When an authorial section is too long to summarize responsibly in one artifact, create part summaries and a parent synthesis.

## Required Coverage

Each section summary must cover:

- Bibliographic anchor: document id, source file, title, author/editor/translator when known, page range, language, and text type.
- Section function: what this section does in the work as a whole.
- Exhaustive argument summary: every step in the reasoning, not only the conclusion.
- Claims and subclaims: each separable historical, textual, interpretive, philological, or bibliographic claim.
- Evidence used: passages, authorities, examples, citations, primary texts, manuscripts, editions, dates, places, persons, and conceptual distinctions.
- References and allusions: classical, biblical, patristic, scholastic, Jewish, Arabic, Hermetic, Orphic, Kabbalistic, Renaissance, and modern scholarly references.
- Technical vocabulary: terms in Latin, Greek, Hebrew, Italian, or modern scholarly terminology, with local meaning.
- Historiographical stakes: what debate this section changes, supports, rejects, or complicates.
- Relation to Pico works: which Pico text, thesis, letter, edition, or doctrinal problem is affected.
- Knowledge product hooks: timeline events, map locations, biography facts, concept pages, scholar profile updates, and open problems.
- Uncertainties: OCR problems, translation limits, edition problems, doubtful dates, uncertain identifications, and claims needing external verification.

## Exhaustive Summary Standard

An exhaustive summary is not a paraphrase of every sentence. It is a complete reconstruction of the section's intellectual work.

For primary texts by Pico, include:

- Opening problem or occasion.
- Sequence of conceptual moves.
- Authorities invoked and why they matter.
- Images, metaphors, allegories, and scriptural figures.
- Philosophical/theological distinctions.
- Claims about method.
- Relation to Pico's other works and later controversy.
- Points where modern readers are likely to misread the section.

For scholarly works, include:

- Thesis.
- Opponent or prior interpretation.
- Method.
- Evidence base.
- Structure of proof.
- Claims about primary texts.
- Claims about other scholars.
- Historiographical intervention.
- Limits, caveats, and unresolved problems.

## Reference Register Rules

Every named or implied reference should be listed when it contributes to the argument.

Record:

- Name or title.
- Tradition or field.
- Type: person, work, doctrine, event, place, manuscript, edition, concept.
- Local role in the section.
- Evidence page.
- Follow-up action if uncertain.

Do not silently normalize uncertain references. Mark them as `needs_review`.

## Claim Discipline

Claims should be atomic enough to reuse.

Bad: "Pico talks about philosophy and theology."

Good: "In the Oration opening, moral philosophy purifies appetite and anger before dialectic, natural philosophy, and theology can complete the ascent."

Every claim needs:

- Claim type.
- Target entity.
- Theme.
- Evidence page or extracted page range.
- Confidence.
- Review status.

## Prose Style

Write in dense scholarly prose, but keep the structure scannable.

Use short headings. Prefer precise verbs: argues, distinguishes, rejects, reconciles, reorders, cites, allegorizes, historicizes, qualifies, transmits.

Avoid inflated claims. Do not say a section "proves" something unless the source itself demonstrates it and the evidence has been reviewed.

## Promotion Standard

A section summary can support a public website page only when:

- The page range is explicit.
- All core arguments are represented.
- References are registered.
- Claims are atomic and source-tethered.
- Uncertainties are marked.
- The summary says how the section contributes to larger PicoDB products.

## Pass 005 Scholarly Values Overlay

Each section summary must include a short Scholarly Values Overlay:

- guide scholars applied;
- myth or label being tested;
- technical terms and source languages to check;
- scholastic, Kabbalistic, Platonic, Aristotelian, magical, biblical, or juridical register;
- concord outcome: success, failure, unresolved tension, or forced synthesis;
- Kabbalah protocol fields when relevant.

## Pass 006 Ficino-Pico Overlay

When a section touches Ficino or Platonism, include: Ficino relation, Platonic dialogue source, Neoplatonic structure, Pico transformation, dispute status, edition/witness issue, Christian transformation, and concord outcome. See `docs/FICINO_PICO_READING_PROTOCOL.md`.

## Pass 009 Heptaplus Black Overlay

When summarizing the Heptaplus or Crofton Black, add a Black overlay:

- Identify the Heptaplus unit: proem, exposition, Bereshit, sabbath, or conclusion.
- Identify the Genesis anchor and the source family.
- Distinguish Aquinas, Pseudo-Dionysius, Proclus, Arabic intellect tradition, Jewish exegesis, and Kabbalah.
- State whether the passage repeats, recodes, or corrects a problem from the 900 Conclusions, Apology, Commento, or Oration.
- Mark the kind of ascent: cosmological, anagogical, intellectual, mystical, or salvific.

## Pass 010 Astrology Overlay

When summarizing astrology passages, identify the astrology register, attitude status, causation model, chronology, and textual risk. Do not use "astrology" as a naked tag. Distinguish natural celestial influence, judicial/divinatory astrology, astral magic, poetic astrology, Kabbalistic-astral correspondence, biblical cosmology, anti-astrology, and reception.

## Pass 011 Angelology Overlay

When summarizing angelology passages, identify the angelology register, source family, authority named, metaphysical level, function in the argument, transformation status, and textual risk. Do not use "angelology" as a naked tag. Separate angelic imitation, angelic hierarchy, angelic/intellectual world, angelic mind, Kabbalistic angels, Arabic intellect, Ficinian/Neoplatonic mediation, Thomistic separate substances, Christological access, and demonic boundary questions. See `docs/ANGELOLOGY_READING_PROTOCOL.md`.

## Pass 012 Corpus-Control Overlay

When summarizing reviews, editions, or source surveys, extract every work-title, edition, manuscript witness, early print, reception text, and source-family clue. Mark whether the passage changes access status, edition priority, source ecology, or corpus-formation risk. See `docs/PICO_PRIMARY_TEXT_ACQUISITION_PROTOCOL.md`.

## Pass 013 Missing-Writings Overlay

When summarizing a text from an early Opera witness, begin with a witness note: edition, source, OCR/image status, authorial boundary, posthumous frame, and whether the passage is Giovanni Pico, Gianfrancesco Pico, papal/editorial apparatus, or later reception. Every section summary must separate textual content from edition history and must mark whether the evidence is safe for quotation, safe only for search, or only a bibliographic lead.
