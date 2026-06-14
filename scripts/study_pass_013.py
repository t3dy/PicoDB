"""Study pass 013: missing writings acquisition and corpus-control correction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
MARKDOWN = ROOT / "Markdown"

OPERA_TXT = ROOT / "sources" / "missing_writings_pass013" / "Opera_omnia_Ioannis_Pici_1557_IA_fulltext.txt"
MORE_DOC_ID = "Thomas_More_Rigg_Life_of_Pico_1890_exclassics_pdf_a5a78b5d"
OPERA_DOC_ID = "Opera_omnia_Ioannis_Pici_1557_IA_fulltext_txt_b9ebd3a5"


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, text: str) -> None:
    original = path.read_text(encoding="utf-8")
    if marker not in original:
        path.write_text(original.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8", newline="\n")


def load_seed_module():
    spec = importlib.util.spec_from_file_location("seed_research_artifacts", ROOT / "scripts" / "seed_research_artifacts.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load seed_research_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def chunks(words: list[str], size: int = 2200) -> list[str]:
    return [" ".join(words[i : i + size]) for i in range(0, len(words), size)]


def ingest_opera_txt(conn: sqlite3.Connection) -> None:
    text = OPERA_TXT.read_text(encoding="utf-8", errors="replace")
    words = re.findall(r"\S+", text)
    pages = chunks(words)
    markdown_path = MARKDOWN / f"{OPERA_DOC_ID}.md"
    metadata = {
        "title": "Opera omnia Ioannis Pici, Mirandulae Concordiaeque comitis",
        "author": "Giovanni Pico della Mirandola",
        "publication_year": "1557",
        "publisher": "Heinrich Petri",
        "source": "Internet Archive FULL TEXT OCR",
        "source_url": "https://archive.org/details/bub_gb_nBiG1zAsseQC",
        "note": "OCR control witness for the Basel 1557 Opera; not a critical edition and not yet structurally segmented.",
    }
    md_pages = "\n\n".join(f"## OCR Reading Unit {i}\n\n{page}" for i, page in enumerate(pages, start=1))
    md = f"""---
id: "{OPERA_DOC_ID}"
source_file: "{OPERA_TXT.name}"
source_path: "{OPERA_TXT.resolve()}"
document_type: "primary_source"
themes: ["corpus control", "Pico works", "early print", "posthumous reception"]
pico_works_discussed: ["Heptaplus", "900 Conclusions", "Apologia", "On Being and One", "Oration", "Letters", "Disputationes", "Commento", "Pico poems"]
conversion_method: "Internet Archive OCR text chunked into reading units"
converted_at: "{datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')}"
review_status: "UNREVIEWED_OCR_CONTROL_WITNESS"
source_url: "https://archive.org/details/bub_gb_nBiG1zAsseQC"
---

# Opera omnia Ioannis Pici (Basel 1557 OCR Control Witness)

> This is an OCR control witness from the Internet Archive full-text download. It is useful for corpus inventory, search, and section planning, but it must be checked against images and modern critical editions before textual claims are promoted.

{md_pages}
"""
    MARKDOWN.mkdir(exist_ok=True)
    markdown_path.write_text(md, encoding="utf-8", errors="replace", newline="\n")

    sha = digest(OPERA_TXT)
    conn.execute(
        """
        INSERT OR REPLACE INTO documents
        (id,title,source_file,source_path,markdown_path,extension,sha256,duplicate_of,document_type,
         themes_json,pico_works_json,page_count,word_count,extraction_status,metadata_json,source_method,review_status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            OPERA_DOC_ID,
            metadata["title"],
            OPERA_TXT.name,
            str(OPERA_TXT.resolve()),
            str(markdown_path.resolve()),
            ".txt",
            sha,
            None,
            "primary_source",
            json.dumps(["corpus control", "Pico works", "early print", "posthumous reception"]),
            json.dumps(["Heptaplus", "900 Conclusions", "Apologia", "On Being and One", "Oration", "Letters", "Disputationes", "Commento", "Pico poems"]),
            len(pages),
            count_words(text),
            "OK_OCR_UNREVIEWED",
            json.dumps(metadata, ensure_ascii=False),
            "internet_archive_ocr_text_chunking",
            "UNREVIEWED_OCR_CONTROL_WITNESS",
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    for table in ["pages", "sections", "document_fts", "reading_tasks"]:
        conn.execute(f"DELETE FROM {table} WHERE document_id=?", (OPERA_DOC_ID,))
    conn.executemany(
        "INSERT INTO pages(document_id,page_number,heading,text,word_count) VALUES (?,?,?,?,?)",
        [(OPERA_DOC_ID, i, f"OCR Reading Unit {i}", page, count_words(page)) for i, page in enumerate(pages, start=1)],
    )
    section_titles = [
        "Title and work list",
        "Alexander VI censure and defense frame",
        "Heptaplus",
        "Conclusiones nongentae",
        "Apologia",
        "De ente et uno",
        "De hominis dignitate",
        "Devotional works and psalm commentary",
        "Epistolarum liber",
        "Disputationes adversus astrologiam",
        "Commento on Benivieni and Reuchlin Cabala apparatus",
    ]
    conn.executemany(
        "INSERT INTO sections(document_id,level,title,start_page,notes) VALUES (?,?,?,?,?)",
        [(OPERA_DOC_ID, 1, title, 1, "Provisional control section from title-page inventory; requires image/OCR cleanup.") for title in section_titles],
    )
    conn.execute(
        "INSERT INTO document_fts(document_id,title,source_file,text,themes) VALUES (?,?,?,?,?)",
        (OPERA_DOC_ID, metadata["title"], OPERA_TXT.name, text, "corpus control early print Pico works Opera omnia"),
    )
    tasks = [
        ("primary_text_structural_segmentation", "Basel 1557 Opera", 1, "Use images and OCR to split the Opera into individual Pico works and editorial/reception apparatus."),
        ("pico_text_close_reading", "Disputationes adversus astrologiam divinatricem", 1, "Locate the twelve books in the Opera OCR and compare with better witnesses before book-by-book summary."),
        ("pico_text_close_reading", "Commento on Benivieni", 1, "Locate the Italian Commento in the Opera OCR and compare against Bibliotecaitaliana/Garin witnesses."),
        ("corpus_control", "Giovanni versus Gianfrancesco separation", 1, "Keep bound Opera witnesses from collapsing uncle and nephew into a single authorial corpus."),
    ]
    conn.executemany(
        "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
        [(OPERA_DOC_ID, *task) for task in tasks],
    )


def normalize_more_record(conn: sqlite3.Connection) -> None:
    conn.execute(
        "UPDATE documents SET title=?, document_type=?, review_status=? WHERE id=?",
        (
            "The Life of Pico della Mirandola, translated by Thomas More, edited by J. M. Rigg",
            "reception_witness",
            "UNREVIEWED_RECEPTION_WITNESS",
            MORE_DOC_ID,
        ),
    )
    conn.execute(
        "UPDATE document_fts SET title=?, themes=? WHERE document_id=?",
        (
            "The Life of Pico della Mirandola, translated by Thomas More, edited by J. M. Rigg",
            "reception biography Thomas More Gianfrancesco Pico devotional Pico",
            MORE_DOC_ID,
        ),
    )


def update_ontology() -> None:
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.12.0"
    payload["corpus_control_acquisition_statuses"] = [
        "full_primary_controlled",
        "full_primary_unsegmented",
        "ocr_control_witness_acquired",
        "reception_witness_acquired",
        "public_digital_text_identified",
        "bibliographic_lead_identified",
        "secondary_rich_primary_gap",
        "manuscript_witness_needed",
        "related_non_giovanni_text",
        "licensing_unclear",
    ]
    payload["missing_writings_priority_queue"] = [
        "Basel_1557_Opera_Omnia_structural_segmentation",
        "Commento_on_Benivieni_public_text_retry_and_witness_comparison",
        "Disputationes_adversus_astrologiam_primary_witness_control",
        "Carmina_latina_and_poem_witnesses",
        "Lettere_letter_by_letter",
        "Apologia_condemned_theses",
        "Gianfrancesco_Vita_and_More_Life_reception_analysis",
        "Bologna_1496_posthumous_collection",
        "source_ecology_Averroes_Recanati_Lull_Cusa_Chaldean_Orphic",
        "Gianfrancesco_De_imaginatione_related_text",
    ]
    payload["corpus_control_rules"] = [
        "Separate a missing Giovanni text from a related Gianfrancesco or reception text.",
        "Treat early Opera OCR as a search and inventory witness until image checks and modern editions confirm readings.",
        "Promote a work from gap to controlled only after full text, edition metadata, section plan, and source-risk notes are present.",
        "Record licensing and access status separately from bibliographic existence.",
        "When an early table of contents lists a work, create acquisition tasks for the work and for the edition frame that transmits it.",
    ]
    payload["guide_scholars"]["Gianfrancesco Pico"] = sorted(
        set(payload["guide_scholars"].get("Gianfrancesco Pico", []) + ["vita_reception", "corpus_formation", "posthumous_editing", "de_imaginatione_related_text"])
    )
    payload["guide_scholars"]["Thomas More"] = sorted(
        set(payload["guide_scholars"].get("Thomas More", []) + ["english_reception", "life_of_pico", "devotional_pico", "translation_witness"])
    )
    write_json(path, payload)


def write_artifacts() -> None:
    write(
        "docs/MISSING_WRITINGS_ACQUISITION_LOG.md",
        """# Missing Writings Acquisition Log

Status: DRAFT  
Created in study pass 013.

## Acquired This Pass

| Object | Status | Local Result | Use |
|---|---|---|---|
| Basel 1557 Opera Omnia OCR | `ocr_control_witness_acquired` | `Markdown/Opera_omnia_Ioannis_Pici_1557_IA_fulltext_txt_b9ebd3a5.md` | Search, corpus inventory, section planning, work-list control. |
| Thomas More / Rigg Life of Pico | `reception_witness_acquired` | `Markdown/Thomas_More_Rigg_Life_of_Pico_1890_exclassics_pdf_a5a78b5d.md` | Anglophone devotional reception, Life/Vita comparison, biography-source caution. |

## Identified But Not Yet Controlled

- `Commento sopra una canzone d'amore`: public Bibliotecaitaliana text identified, but automated download failed; retry manually or through a browser pass.
- `Disputationes adversus astrologiam divinatricem`: Noscemus and early-print leads identified; a 2025 web translation exists, but licensing and scholarly status are unclear. Treat as a lead, not as a controlled source.
- `Carmina latina`: still requires Speyer/Kristeller and manuscript-witness mapping.
- `Bologna 1496 posthumous collection`: still needed for Gianfrancesco's first corpus-making frame.

## Corrected Gap

`De imaginatione` should no longer be listed as an unidentified Giovanni Pico primary text. The local scholarly hit comes through Dougherty's discussion of Gianfrancesco Pico's well-known 1501 work. It remains important for reception, imagination, demonology, and nephewly corpus ecology, but it belongs in the related-source queue unless new evidence identifies a Giovanni text with that title.
""",
    )
    write(
        "artifacts/source_packets/missing_writings_web_acquisition_pass013.md",
        """# Source Packet: Missing Writings Web Acquisition Pass 013

- Artifact ID: `source_missing_writings_web_pass013`
- Type: source packet
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Internet Archive Basel Opera

The Internet Archive record for *Opera omnia Ioannis Pici, Mirandulae Concordiaeque comitis* identifies a public-domain 1557 Latin edition published by Heinrich Petri and offers full-text/PDF access. PicoDB ingested the full-text OCR as a control witness. The title-page inventory is already valuable because it lists the works transmitted in this witness: Heptaplus, 900 Conclusions, Apologia, De ente et uno, De hominis dignitate, devotional rules and psalm commentary, De Christi regno, letters, twelve books of Disputationes against astrology, hymns, the Italian Commento on Plato's Symposium/Benivieni tradition, and Reuchlin's Cabala apparatus.

## More/Rigg Life of Pico

The Exclassics/Rigg public-domain PDF has been converted to Markdown. Its contents include Walter Pater's essay, Rigg's introduction, More's translation of the Life, three letters, Pico on Psalm 15/16, Twelve Rules, Twelve Weapons, Twelve Properties of a Lover, and a prayer. This is not neutral biography: it is an English reception witness that participates in the devotional and exemplary construction of Pico.

## Web Leads

Bibliotecaitaliana hosts a public text page for the Commento, but the download attempt failed in this pass. Noscemus identifies the 1496 Bologna *Disputationes adversus astrologiam divinatricem* record. A modern web translation of the Disputationes was discovered, but licensing and scholarly controls require caution before ingestion.
""",
    )
    write(
        "artifacts/source_packets/opera_omnia_1557_control_witness_pass013.md",
        """# Source Packet: Basel 1557 Opera Control Witness

- Artifact ID: `source_opera_omnia_1557_control_pass013`
- Type: source packet
- Document ID: `Opera_omnia_Ioannis_Pici_1557_IA_fulltext_txt_b9ebd3a5`
- Status: OCR_CONTROL_WITNESS
- Evidence status: likely

## Control Value

The Basel Opera witness is now locally searchable. Its value is not that it settles Pico's text, but that it gives PicoDB a single early printed corpus frame. It can answer questions like: which works are grouped together, where the Alexander VI censure and defense material appears, how devotional materials sit beside the 900 Conclusions and anti-astrology, and how Reuchlin's Cabala apparatus is attached to Pico's legacy.

## Reading Rules

1. Do not quote this OCR as authoritative without image verification.
2. Use the title-page inventory to create work-level segmentation tasks.
3. Compare every work against modern editions where available.
4. Mark every editorial/reception apparatus item separately from Giovanni Pico's own text.
5. Keep the uncle/nephew boundary visible.

## Immediate Work Units

- Split Heptaplus, Conclusions, Apologia, De ente et uno, Oration, letters, Disputationes, hymns, Commento, Reuchlin Cabala, and censure/defense material.
- Create a Basel-to-modern-edition comparison table.
- Track where this witness changes the missing-writings dashboard.
""",
    )
    write(
        "artifacts/source_packets/more_life_pico_reception_witness_pass013.md",
        """# Source Packet: More/Rigg Life of Pico Reception Witness

- Artifact ID: `source_more_life_pico_pass013`
- Type: source packet
- Document ID: `Thomas_More_Rigg_Life_of_Pico_1890_exclassics_pdf_a5a78b5d`
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Contents

The converted witness contains bibliographic notes, Walter Pater's essay, Rigg's introduction, More's Life of Pico, three Pico letters, devotional and Psalm materials, rules, weapons, lover-properties, a prayer, and notes. It therefore links biography, reception, English humanism, devotional Pico, and the long afterlife of Gianfrancesco's saintly portrait.

## Interpretive Caution

Use this witness for reception and biography-source analysis, not as a direct factual biography. Its scholarly value lies in how Pico is made exemplary: learned, ascetic, converted, devout, and useful for English Christian humanism.

## Next Reading Tasks

- Summarize Pater, Rigg, More's Life, each letter, Psalm commentary, rules, weapons, lover-properties, prayer, and notes separately.
- Compare More's Life against Gianfrancesco's Vita and modern biographies.
- Extract claims about chronology, virtue, conversion, learning, illness, and death into the biography source register.
""",
    )
    write(
        "artifacts/concepts/pico_corpus_control_dashboard_pass013.md",
        """# Concept Dossier: Pico Corpus Control Dashboard

- Artifact ID: `concept_pico_corpus_control_dashboard`
- Type: concept dossier
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Current Dashboard

| Work or Witness | Status | Next Action |
|---|---|---|
| Basel 1557 Opera Omnia | `ocr_control_witness_acquired` | Segment by work and verify against images/critical editions. |
| Oration | `full_primary_present_section_summary_deepening` | Re-read with metaphysics, Kabbalah, angelology, and dignity overlays. |
| Heptaplus | `full_primary_present_section_summary_deepening` | Re-read with Black, Busi, Wirszubski, biblical hermeneutics, and angelology overlays. |
| 900 Conclusions | `full_primary_present_thesis_table_needed` | Build thesis-by-thesis source, theme, and "according to own opinion" tables. |
| Apologia | `primary_present_condemned_theses_dossier_needed` | Link condemned theses, papal process, and Copenhaver/Farmer commentary. |
| De ente et uno | `full_primary_present_metaphysics_reread_needed` | Use Allen, Aquinas, Dionysius, Ficino, Aristotle/Plato concord. |
| Commento | `public_digital_text_identified_download_retry_needed` | Acquire Bibliotecaitaliana/Garin witness and compare to Opera OCR. |
| Disputationes | `primary_witness_leads_identified_full_control_needed` | Locate reliable Latin/edition witness and summarize book by book. |
| Carmina | `manuscript_and_edition_control_needed` | Acquire Speyer/Kristeller; map Vat., Munich, Muenster, Laurenziana witnesses. |
| Lettere | `primary_present_letter_by_letter_needed` | Extract sender, recipient, date, place, work, theme, and biography claims. |
| More/Rigg Life | `reception_witness_acquired` | Summarize as Anglophone devotional reception and biography-source witness. |
| Gianfrancesco De imaginatione | `related_non_giovanni_text` | Treat as nephewly source ecology, not a missing Giovanni work. |

## Dashboard Rule

A text is not "covered" until it has acquisition status, edition/witness status, section plan, close-reading status, linked claims, and website destination.
""",
    )
    write(
        "artifacts/essays/pico_missing_writings_next_steps_draft.md",
        """# Essay Draft: Pico Writings We Still Need

- Artifact ID: `essay_pico_missing_writings_next_steps`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Revised Thesis

The missing-writings problem is now less vague and more useful. PicoDB no longer needs simply to ask "what do we not have?" It needs to distinguish at least five cases: a primary text not yet acquired, a primary text acquired but not structurally controlled, a reception witness acquired but not yet evaluated, a public digital witness identified but not downloaded, and a related text that belongs to the Pico family or reception ecology but not to Giovanni Pico's own corpus.

The most important gain in this pass is the acquisition of the Basel 1557 *Opera omnia* OCR from the Internet Archive. This is not a critical edition, and OCR is not a safe quotation base. But it is a major control witness. Its title-page inventory places together the Heptaplus, 900 Conclusions, Apologia, De ente et uno, De hominis dignitate, Christian rules and devotional works, letters, twelve books against astrology, hymns, the Italian Commento tradition, and Reuchlin's Cabala apparatus. That list gives the project a concrete segmentation agenda. We can now use the Opera witness to ask where each work sits, how posthumous defense material frames Pico, and how later readers encountered his theology, metaphysics, anti-astrology, devotion, and Kabbalah as a bound corpus.

The second gain is the acquisition of the Thomas More/Rigg *Life of Pico* witness. This belongs in the biography project, but it must be read as reception. More's English Pico is not simply Giovanni Pico as he was. It is a devotional, exemplary Pico mediated through Gianfrancesco's Vita and early modern English Christian humanism. Its contents are especially useful because the volume gathers Pater, Rigg, the Life, three letters, Psalm commentary, rules, spiritual weapons, lover-properties, and a prayer. That means the witness can help us study how biography, moral conversion, letters, and devotional practice were bundled for later readers.

The highest open primary gap remains the *Commento sopra una canzone d'amore*. The pass identified a public Bibliotecaitaliana text page, but the automated download failed. The next move is to acquire that witness manually or through a browser-controlled download, then compare it with the Opera OCR and the Garin/Allen story of expurgation, correction, and Pico's dispute with Ficino. This text is central because it joins love theory, Platonic exegesis, poetic theology, Venus, Mind, beauty, Benivieni, Ficino, and Pico's independence from Ficinian Platonism.

The *Disputationes adversus astrologiam divinatricem* remains a primary-control problem. The project has strong scholarship on Pico and astrology, but the full text still needs a reliable local witness, edition metadata, and book-by-book summaries. Noscemus gives a clear bibliographic lead for the 1496 Bologna edition. A modern web translation was found, but licensing and scholarly controls are uncertain, so it should be treated as a discovery lead rather than an ingestible foundation. The next serious pass should locate a dependable Latin witness, split the twelve books, and read them for natural influence, judicial prediction, empirical criticism, providence, free will, and posthumous editorial risk.

The poetry remains a manuscript-control gap. Speyer, Kristeller, Sottili, Vat. lat. 5225, Clm 485, Muenster 29.II.276, Laur. 90 sup. 37, Costanzo Landi, Paolo Manuzio, and Lodovico Domenichi form the working map. The poems are not ornamental leftovers. They can illuminate Pico's humanist education, Latin voice, relation to Poliziano and Benivieni, and the literary textures behind his philosophical self-presentation.

The letters are present but not yet really read as a corpus. The Borghesi Lettere file should become a letter-by-letter database: sender, recipient, date, place, occasion, works mentioned, doctrinal themes, people, movement, illness, conflict, patronage, and biography claims. The letters are likely the best spine for the timeline and map because they can join intellectual work to movement among Mirandola, Ferrara, Padua, Florence, Rome, France, and the later Florentine orbit.

The Apologia and condemned theses need a juridical-theological dossier. A primary file is present, but PicoDB still needs to join the thirteen condemned theses, the papal commission, Alexander VI's censure, Pico's defense, Copenhaver's trial analysis, Farmer's thesis commentary, and later reception. This is where the 900 Conclusions become an event, not just a text.

The key correction is *De imaginatione*. Earlier gap language treated it as a missing Giovanni Pico text. The better local evidence points to Gianfrancesco Pico's well-known 1501 work. That makes it important, but differently important. It belongs in the related-source and reception ecology queue: imagination, demonology, cognition, magic, and the nephew's intellectual profile. It should not be used to inflate Giovanni's missing primary corpus unless new evidence warrants that move.

The practical next step is a corpus-control dashboard rather than another undifferentiated wish list. Each row should record acquisition status, source or witness, edition status, segmentation status, summary status, governing scholars, risks, and next action. A text is not covered merely because it is mentioned by a scholar or present in OCR. It becomes usable for PicoDB only when it can be cited, segmented, summarized, compared, and linked to claims.
""",
    )


def update_docs() -> None:
    write(
        "docs/PICO_TEXT_GAPS.md",
        """# Pico Text Gap Register

## Commento sopra una canzone d'amore composta da Girolamo Benivieni

- Status: `public_digital_text_identified_download_retry_needed`
- Reason: A Bibliotecaitaliana public text page has been identified, and the Basel Opera OCR appears to include the Italian Commento tradition, but PicoDB still needs a controlled modern/critical witness and section-by-section Markdown.

## Complete correspondence corpus

- Status: `primary_present_letter_by_letter_summary_needed`
- Reason: A Lettere file is present; the next work is extraction by individual letter: sender, recipient, date, place, occasion, works mentioned, claims, and biography/timeline/map evidence.

## De imaginatione

- Status: `related_non_giovanni_text`
- Reason: The local scholarly evidence points to Gianfrancesco Pico's well-known 1501 De imaginatione, not to a missing Giovanni Pico primary work. Keep it in the related-source queue for imagination, demonology, reception, and nephewly corpus ecology.

## Disputationes adversus astrologiam divinatricem

- Status: `primary_witness_leads_identified_full_control_needed`
- Reason: Scholarship is strong and the Basel Opera OCR has been acquired as a control witness, but the project still needs a reliable Latin/edition witness, segmentation of all twelve books, and book-by-book close reading.

## Disputationes against astrology manuscript/critical edition details

- Status: `metadata_needed`
- Reason: Catalog editions, translations, and manuscript witnesses as they appear in scholarship. Noscemus identifies the 1496 Bologna lead; modern web translations require licensing and scholarly review before use.

## Angelology Primary Text Control Pass 011

- Status: `primary_loci_identified_passage_table_needed`
- Reason: Oration and Heptaplus primary passages are locally available, and Farmer/Wirszubski/Black/Copenhaver/Allen give strong scholarly controls. The project still needs a thesis-by-thesis angelology table for the 900 Conclusions.

## Opera Reviews Pass 012 Gap Update

- `Basel 1557/1573 Opera Omnia`: `early_print_reprint_needed_for_corpus_control`; useful long-used Opera witness, but incomplete and not a substitute for critical editions.
- `Bologna 1496 posthumous collection`: `early_print_needed`; needed for Gianfrancesco's corpus-making and posthumous Pico.
- `Commento sopra una canzone d'amore`: `high_priority_full_primary_text_and_witness_control`; needed for Ficino dispute, poetic theology, love, Venus, Mind, and suppression/recovery history.
- `Disputationes adversus astrologiam divinatricem`: `high_priority_full_primary_text`; scholarship is strong, but primary-text and posthumous-edition control remain inadequate.
- `Carmina latina / Latin poems`: `partial_secondary_and_review_control_manuscripts_needed`; Speyer/Kristeller and manuscript witnesses must be mapped poem by poem.
- `Lettere`: `primary_present_letter_by_letter_summary_needed`; use Borghesi edition for chronology, network, works, and biographical claims.
- `Gianfrancesco Vita and Thomas More Life`: `reception_witnesses_needed`; needed for saintly Pico, Anglophone reception, and corpus formation.

## Missing Writings Pass 013 Gap Update

- `Basel 1557 Opera Omnia`: `ocr_control_witness_acquired`; IA full-text OCR is now in Markdown and SQLite. It must be structurally segmented and checked against images/critical editions.
- `Thomas More / Rigg Life of Pico`: `reception_witness_acquired`; now in Markdown and SQLite. Summarize Pater, Rigg, Life, letters, Psalm, rules, weapons, lover-properties, prayer, and notes separately.
- `Commento`: `public_digital_text_identified_download_retry_needed`; Bibliotecaitaliana page identified, automated download failed.
- `Disputationes`: `primary_witness_leads_identified_full_control_needed`; Noscemus/Bologna lead identified; modern web translation lead is not yet an ingestible scholarly base.
- `De imaginatione`: `related_non_giovanni_text`; correct previous wording that implied a missing Giovanni text.
""",
    )
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 013 Missing-Writings Overlay",
        """## Pass 013 Missing-Writings Overlay

When summarizing a text from an early Opera witness, begin with a witness note: edition, source, OCR/image status, authorial boundary, posthumous frame, and whether the passage is Giovanni Pico, Gianfrancesco Pico, papal/editorial apparatus, or later reception. Every section summary must separate textual content from edition history and must mark whether the evidence is safe for quotation, safe only for search, or only a bibliographic lead.
""",
    )
    append_once(
        DOCS / "PICO_PRIMARY_TEXT_ACQUISITION_PROTOCOL.md",
        "## Pass 013 Control Upgrade",
        """## Pass 013 Control Upgrade

Acquisition status now requires two separate fields: `access_status` and `control_status`. A public text may be identified but not downloaded; a full OCR may be acquired but not citation-safe; a reception witness may be acquired but not biographically transparent; a related Pico-family text may be important without being a Giovanni Pico text. Use `data/reading_artifact_ontology.json` version 0.12.0 for these distinctions.
""",
    )


def db_rows(conn: sqlite3.Connection) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    artifacts = [
        ("source_missing_writings_web_pass013", "source_packet", "Missing Writings Web Acquisition Pass 013", "artifacts/source_packets/missing_writings_web_acquisition_pass013.md", OPERA_DOC_ID, "Pico missing writings", "SOURCE_ANCHORED_DRAFT", "likely"),
        ("source_opera_omnia_1557_control_pass013", "source_packet", "Basel 1557 Opera Control Witness", "artifacts/source_packets/opera_omnia_1557_control_witness_pass013.md", OPERA_DOC_ID, "Basel Opera Omnia", "OCR_CONTROL_WITNESS", "likely"),
        ("source_more_life_pico_pass013", "source_packet", "More/Rigg Life of Pico Reception Witness", "artifacts/source_packets/more_life_pico_reception_witness_pass013.md", MORE_DOC_ID, "More Life of Pico", "SOURCE_ANCHORED_DRAFT", "likely"),
        ("concept_pico_corpus_control_dashboard", "concept_dossier", "Pico Corpus Control Dashboard", "artifacts/concepts/pico_corpus_control_dashboard_pass013.md", OPERA_DOC_ID, "Pico missing writings", "SOURCE_ANCHORED_DRAFT", "likely"),
        ("essay_pico_missing_writings_next_steps", "website_page", "Pico Writings We Still Need", "artifacts/essays/pico_missing_writings_next_steps_draft.md", OPERA_DOC_ID, "Pico missing writings", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO reading_artifacts
        (id, artifact_type, title, path, document_id, target_entity, status, evidence_status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM reading_artifacts WHERE id = ?), ?), ?)
        """,
        [row + (row[0], now, now) for row in artifacts],
    )
    claims = [
        ("claim_missing_013_001", "source_opera_omnia_1557_control_pass013", OPERA_DOC_ID, "The Basel 1557 Opera OCR is now locally searchable and should be treated as a corpus-control witness rather than as a critical edition.", "bibliographic", "corpus control", "Basel Opera Omnia", "IA OCR title inventory", "high", "DRAFT", "Pass 013."),
        ("claim_missing_013_002", "source_opera_omnia_1557_control_pass013", OPERA_DOC_ID, "The Opera title inventory lists Heptaplus, 900 Conclusions, Apologia, De ente et uno, Oration, devotional materials, letters, Disputationes, hymns, Commento, and Reuchlin's Cabala apparatus.", "bibliographic", "work inventory", "Pico corpus", "OCR reading unit 1", "medium", "DRAFT", "Requires image verification."),
        ("claim_missing_013_003", "source_more_life_pico_pass013", MORE_DOC_ID, "The More/Rigg Life of Pico witness should be read as English devotional reception and biography-source construction, not as transparent access to Pico's life.", "historiographical", "reception", "More Life of Pico", "PDF contents", "high", "DRAFT", "Pass 013."),
        ("claim_missing_013_004", "concept_pico_corpus_control_dashboard", OPERA_DOC_ID, "A text is not controlled merely because it is present in OCR; PicoDB requires acquisition status, edition metadata, segmentation, close reading, and linked claims.", "methodological", "ontology", "Pico missing writings", "Dashboard rule", "high", "DRAFT", "Pass 013."),
        ("claim_missing_013_005", "essay_pico_missing_writings_next_steps", OPERA_DOC_ID, "De imaginatione should be downgraded from a missing Giovanni Pico text to a related Gianfrancesco Pico text unless new evidence identifies a Giovanni work with that title.", "bibliographic", "corpus correction", "De imaginatione", "Dougherty local search plus pass 013 correction", "high", "DRAFT", "Pass 013."),
        ("claim_missing_013_006", "essay_pico_missing_writings_next_steps", OPERA_DOC_ID, "The Commento remains high priority because a public digital text is identified but not yet controlled locally, and because Allen makes it central to the Ficino/Pico dispute.", "open_problem", "Commento", "Commento on Benivieni", "Pass 013 web lead", "medium", "DRAFT", "Pass 013."),
        ("claim_missing_013_007", "essay_pico_missing_writings_next_steps", OPERA_DOC_ID, "The Disputationes remains a primary-control problem: early-print leads exist, but PicoDB still needs a reliable witness and book-by-book summary.", "open_problem", "astrology", "Disputationes", "Pass 013 web lead", "high", "DRAFT", "Pass 013."),
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO claims
        (id, artifact_id, document_id, claim_text, claim_type, theme, target_entity, evidence_page, confidence, review_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        claims,
    )
    cards = [
        ("source-opera-omnia-1557-pass013", "source_packet", "Basel Opera OCR Acquired", "Corpus-control witness", "The 1557 Opera Omnia OCR is now in Markdown and the database for search, segmentation, and edition-control work.", "DRAFT", "source_opera_omnia_1557_control_pass013"),
        ("source-more-life-pico-pass013", "source_packet", "More's Life of Pico Acquired", "English reception witness", "The More/Rigg public-domain Life of Pico volume is now converted and ready for reception-aware biography notes.", "DRAFT", "source_more_life_pico_pass013"),
        ("concept-pico-corpus-control-dashboard", "concept", "Corpus Control Dashboard", "What is acquired, controlled, or still missing", "A new dashboard distinguishes OCR control witnesses, reception witnesses, public digital leads, manuscript gaps, and related non-Giovanni texts.", "DRAFT", "concept_pico_corpus_control_dashboard"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id, entity_type, title, subtitle, summary, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        cards,
    )
    pages = [
        ("page-pico-missing-writings", "essay", "Pico Writings We Still Need", "artifacts/essays/pico_missing_writings_next_steps_draft.md", "DRAFT", "essay_pico_missing_writings_next_steps"),
        ("page-pico-corpus-control-dashboard", "concept", "Pico Corpus Control Dashboard", "artifacts/concepts/pico_corpus_control_dashboard_pass013.md", "DRAFT", "concept_pico_corpus_control_dashboard"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        pages,
    )


def refresh_catalog_and_manifest(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    docs = []
    for row in conn.execute(
        "SELECT id,title,source_file,markdown_path,document_type,themes_json,pico_works_json,page_count,word_count,duplicate_of FROM documents ORDER BY title"
    ):
        d = dict(row)
        d["themes"] = json.loads(d.pop("themes_json") or "[]")
        d["pico_works_discussed"] = json.loads(d.pop("pico_works_json") or "[]")
        docs.append(d)
    write_json(DATA / "corpus_catalog.json", {"documents": docs})
    manifest_path = DATA / "pico_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["corpus_counts"] = {
        "documents": conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
        "pages": conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0],
        "sections": conn.execute("SELECT COUNT(*) FROM sections").fetchone()[0],
        "words": conn.execute("SELECT COALESCE(SUM(word_count), 0) FROM documents").fetchone()[0],
    }
    write_json(manifest_path, manifest)


def main() -> None:
    conn = sqlite3.connect(DB)
    ingest_opera_txt(conn)
    normalize_more_record(conn)
    update_ontology()
    write_artifacts()
    update_docs()
    db_rows(conn)
    conn.commit()
    refresh_catalog_and_manifest(conn)
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 013 complete.")


if __name__ == "__main__":
    main()
