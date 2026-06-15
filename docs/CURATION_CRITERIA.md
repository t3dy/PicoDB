# Curation Criteria

This document defines the editorial standards for deciding which content appears in the PicoDB portal and how it is classified.

## Portal Scope

PicoDB covers the scholarly study of Giovanni Pico della Mirandola (1463–1494) and his intellectual context. This includes:

- Primary texts by Pico and his contemporaries
- Scholarly monographs, articles, and editions on Pico's works and thought
- Works covering the broader Renaissance context: Ficino, Florentine Platonism, Christian Kabbalah, Renaissance magic, Neoplatonism
- Reception history: how Pico was read from the 16th century onward
- Historiographical debates: the development of Pico scholarship

The portal has a secondary scope covering the broader history of Western esotericism, Renaissance philosophy, and the scholarly study of magic, Kabbalah, and occult philosophy — when that content is relevant to understanding Pico's intellectual world.

## The News Aggregator Pipeline

The news aggregator identifies, evaluates, and publishes short link-cards for recent podcasts, articles, videos, and events relevant to the portal's scope. The curation stage for aggregator content is where most quality decisions are made.

### Inclusion criteria for the aggregator

**Publish or feature if the content:**
- Offers new primary-source discussion, transcription, or translation
- Reports recent peer-reviewed scholarship or book publications
- Covers historiographical debates within the scope above
- Discusses methodology in the history of Western esotericism or Renaissance philosophy
- Reviews or analyzes a significant edition, anthology, or reference work
- Documents a conference, lecture series, or public talk by recognized scholars in the field
- Covers manuscript discoveries, digitization projects, or archival access affecting the corpus

**Archive (visible but not highlighted) if the content:**
- Provides a general introduction to esotericism or Renaissance philosophy at an accurate but non-specialist level
- Is a popular or journalistic piece that accurately represents the scholarly consensus without adding new analysis
- Is a podcast episode with a serious scholar discussing their work, but the content is already covered by published sources in the corpus

**Review (hold for human decision) if the content:**
- Makes significant historical claims but lacks clear scholarly grounding
- Seems potentially interesting but is difficult to classify without reading more carefully
- Covers a topic adjacent to the scope but whose relevance is unclear

**Reject if the content:**
- Is lifestyle occultism with no scholarly dimension
- Makes historical claims that contradict established scholarship without argument
- Is AI-generated spam or bulk-produced content with no original research
- Is primarily about contemporary spiritual practice rather than historical study
- Promotes conspiracy theories or pseudohistorical narratives about esotericism
- Is sensationalist (occult celebrities, "secrets of the ancients," etc.)

## Distinguishing Serious Scholarship from Pop Occult

This is the central curation judgment. The distinction is not about the subject matter (serious scholars study magic, alchemy, and Kabbalah) but about method, evidence, and intent.

### Signals of serious scholarship

- Author is affiliated with a university, research institute, or recognized scholarly society
- Work cites primary sources with specific page references or manuscript signatures
- Work engages with the existing scholarly debate, not just with the tradition itself
- Publication is peer-reviewed, or if not, the content demonstrates equivalent rigor
- Claims are qualified: the author distinguishes what is known from what is reconstructed or speculative
- The tone is analytical rather than promotional or reverential

### Signals of pop occultism / low-relevance content

- Author's primary identity is as a practitioner, not a historian or philologist
- Claims lack source citations or are supported only by other popular works
- The piece celebrates or promotes the esoteric tradition rather than analyzing it historically
- Language is reverential: "ancient wisdom," "secret teachings," "rediscovered mysteries"
- Historical figures are presented as heroes or enemies rather than as subjects of inquiry
- The piece is structured around personal revelation, transformation, or practice

### The boundary case: serious practice-based writing

Some content occupies genuine middle ground: a practicing astrologer who also holds a PhD in history of science; an artist who has spent years with primary sources. Apply these criteria:

- Is there a serious argument or piece of evidence that would be useful to a historian?
- Does the piece acknowledge scholarly debates and position itself within them?
- Would a historian in the field recognize this as making a contribution, even a modest one?

If yes to all three, consider `archive` or `review`. If only to some, `archive`. If none, `reject`.

## Content Quality Flags

Use these `content_quality_flags` values from `artifacts/schemas/curation.schema.json`:

| Flag | Use when |
|------|----------|
| `serious_scholarship` | Peer-reviewed or equivalent rigor |
| `peer_reviewed` | Explicitly in a peer-reviewed venue |
| `primary_source_discussion` | Analyzes primary texts with citations |
| `edition_or_translation` | Is or discusses an edition or translation |
| `revisionary_argument` | Challenges received historiography with evidence |
| `specialist_audience` | Written for academic specialists |
| `popular_scholarship` | Written for general educated audience, accurate |
| `accessible_introduction` | Survey or primer, accurate but non-specialist |
| `pop_occult` | Generic lifestyle occultism |
| `lifestyle_spirituality` | Spirituality or self-help framing |
| `vague_spirituality` | Vague claims about spiritual wisdom or energy |
| `ai_generated_spam` | Bulk-produced AI content with no original research |
| `low_scholarly_relevance` | Accurate but not relevant to this portal's scope |
| `unverifiable_claims` | Historical claims that cannot be checked |
| `conspiracy_adjacent` | Touches on esoteric conspiracy theories |
| `sensationalist` | "Secrets," "forbidden," "hidden," frame |

## Link Card Format

For the news aggregator, a `public_prose` artifact serving as a link card should include:

```json
{
  "title": "...",
  "short_description": "One-line dek",
  "summary": "2-4 sentences: what it is, why it matters for the portal",
  "tags": ["..."],
  "citations": [{ "citation_text": "...", "url": "..." }],
  "editorial_status": "draft"
}
```

The `body_markdown` of a link card should be 100–300 words covering:
- What the source is (format, author, venue)
- What it contributes (main argument or content)
- Why it is relevant to this portal
- Any caveats (e.g., introductory level, practitioner perspective)

Do not write "why it matters" in generic terms ("this is an important contribution"). Say specifically what it adds: "provides the first English translation of X," "argues against the Garin humanist-Pico thesis," "documents a previously unknown manuscript witness."

## Quality Standard for Public Prose

Portal content should be:

- **Accessible to intelligent non-specialists** — assume a reader who reads the *New York Review of Books* but is not a specialist in Renaissance philosophy
- **Grounded in evidence** — specific claims reference specific sources; vague claims are avoided
- **Neutral but not bland** — take positions when the evidence supports them; acknowledge when it does not
- **Historiographically aware** — note when claims are contested; do not present a single scholarly view as consensus
- **Clear about uncertainty** — distinguish verified from interpretive from speculative
- **Resistant to overinterpretation** — do not assert what Pico "believed" or "intended" without warrant
- **Able to distinguish description from interpretation** — what the source says versus what the scholar argues it means
