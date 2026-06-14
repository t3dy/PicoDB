"""Study pass 014: Commento full-text control and Stanley translation witness."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sqlite3
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
MARKDOWN = ROOT / "Markdown"
SRC = ROOT / "sources" / "commento_pass014"

COMMENTO_XML = SRC / "Pico_Commento_BibliotecaItaliana_TEI_bibit000827.xml"
COMMENTO_JSON = SRC / "Pico_Commento_BibliotecaItaliana_texto_bibit000827.json"
STANLEY_TXT = SRC / "Pico_Stanley_Platonick_Discourse_1914_IA_fulltext.txt"

COMMENTO_DOC_ID = "Pico_Commento_BibliotecaItaliana_TEI_bibit000827_xml_2e50ef08"
STANLEY_DOC_ID = "Pico_Stanley_Platonick_Discourse_1914_IA_fulltext_txt_6a4507d9"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, payload) -> None:
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


def div_text(elem: ET.Element) -> str:
    parts: list[str] = []
    for child in elem:
        if child.tag == "head":
            continue
        parts.append(" ".join(child.itertext()))
    return clean(" ".join(parts))


def div_head(elem: ET.Element, fallback: str) -> str:
    for child in elem:
        if child.tag == "head":
            value = clean(" ".join(child.itertext()))
            if value:
                return value
    return fallback


def ingest_commento(conn: sqlite3.Connection) -> None:
    root = ET.fromstring(COMMENTO_XML.read_text(encoding="utf-8", errors="replace"))
    sections: list[dict] = []
    pages: list[dict] = []
    page_no = 1
    for div1 in root.findall(".//text//div1"):
        d1_head = div_head(div1, div1.attrib.get("n") or f"Section {page_no}")
        d1_text = div_text(div1)
        if d1_text:
            pages.append({"page": page_no, "heading": d1_head, "text": d1_text})
            sections.append({"level": 1, "title": d1_head, "start_page": page_no, "notes": div1.attrib.get("type", "")})
            page_no += 1
        for div2 in div1.findall("./div2"):
            d2_head = f"{d1_head}: {div_head(div2, div2.attrib.get('n') or f'Chapter {page_no}')}"
            d2_text = div_text(div2)
            if d2_text:
                pages.append({"page": page_no, "heading": d2_head, "text": d2_text})
                sections.append({"level": 2, "title": d2_head, "start_page": page_no, "notes": div2.attrib.get("type", "")})
                page_no += 1

    full_text = "\n\n".join(p["text"] for p in pages)
    metadata = {
        "title": "Commento sopra una canzone d'amore di Girolamo Benivieni",
        "author": "Giovanni Pico della Mirandola",
        "digital_publisher": "Biblioteca Italiana",
        "digital_place": "Roma",
        "digital_year": "2004",
        "source_edition": "Opere complete, ed. Francesco Bausi, Roma/Torino, Lexis/Nino Aragno, 2000; electronic text refers to Garin 1942",
        "source_url": "http://backend.bibliotecaitaliana.it/wp-json/muruca-core/v1/xml/bibit000827",
        "availability_note": "Biblioteca Italiana marks the resource freely accessible for personal or scientific use; commercial use prohibited.",
        "tei_id": "bibit000827",
        "section_count": len(sections),
    }
    md_pages = "\n\n".join(f"## {p['heading']}\n\n{p['text']}" for p in pages)
    md = f"""---
id: "{COMMENTO_DOC_ID}"
source_file: "{COMMENTO_XML.name}"
source_path: "{COMMENTO_XML.resolve()}"
document_type: "primary_text"
themes: ["Commento", "Platonic love", "Ficino dispute", "Benivieni", "poetic theology", "Platonism"]
pico_works_discussed: ["Commento sopra una canzone d'amore"]
conversion_method: "Biblioteca Italiana TEI/XML parsed by div1/div2"
converted_at: "{datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')}"
review_status: "CONTROLLED_PRIMARY_TEXT_NEEDS_CLOSE_READING"
source_url: "{metadata['source_url']}"
---

# Commento sopra una canzone d'amore di Girolamo Benivieni

> Controlled Italian primary text from Biblioteca Italiana TEI. This witness is suitable for systematic section summaries, with edition and licensing notes retained in metadata.

{md_pages}
"""
    MARKDOWN.mkdir(exist_ok=True)
    md_path = MARKDOWN / f"{COMMENTO_DOC_ID}.md"
    md_path.write_text(md, encoding="utf-8", newline="\n")

    conn.execute(
        """
        INSERT OR REPLACE INTO documents
        (id,title,source_file,source_path,markdown_path,extension,sha256,duplicate_of,document_type,
         themes_json,pico_works_json,page_count,word_count,extraction_status,metadata_json,source_method,review_status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            COMMENTO_DOC_ID,
            metadata["title"],
            COMMENTO_XML.name,
            str(COMMENTO_XML.resolve()),
            str(md_path.resolve()),
            ".xml",
            sha256(COMMENTO_XML),
            None,
            "primary_text",
            json.dumps(["Commento", "Platonic love", "Ficino dispute", "Benivieni", "poetic theology", "Platonism"]),
            json.dumps(["Commento sopra una canzone d'amore"]),
            len(pages),
            count_words(full_text),
            "OK_TEI_CONTROLLED",
            json.dumps(metadata, ensure_ascii=False),
            "biblioteca_italiana_tei_div_parse",
            "CONTROLLED_PRIMARY_TEXT_NEEDS_CLOSE_READING",
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    for table in ["pages", "sections", "document_fts", "reading_tasks"]:
        conn.execute(f"DELETE FROM {table} WHERE document_id=?", (COMMENTO_DOC_ID,))
    conn.executemany(
        "INSERT INTO pages(document_id,page_number,heading,text,word_count) VALUES (?,?,?,?,?)",
        [(COMMENTO_DOC_ID, p["page"], p["heading"], p["text"], count_words(p["text"])) for p in pages],
    )
    conn.executemany(
        "INSERT INTO sections(document_id,level,title,start_page,notes) VALUES (?,?,?,?,?)",
        [(COMMENTO_DOC_ID, s["level"], s["title"], s["start_page"], s["notes"]) for s in sections],
    )
    conn.execute(
        "INSERT INTO document_fts(document_id,title,source_file,text,themes) VALUES (?,?,?,?,?)",
        (COMMENTO_DOC_ID, metadata["title"], COMMENTO_XML.name, full_text, "Commento Ficino Benivieni Platonic love poetic theology Platonism"),
    )
    tasks = [
        ("document_section_summary", "Commento complete TEI", 1, "Summarize every dedication, canzone, book chapter, and stanza commentary."),
        ("pico_text_close_reading", "Commento Book I", 1, "Track being modes, intelligible hierarchy, God, mind, soul, angelic nature, Plotinus, Dionysius, Avicenna."),
        ("pico_text_close_reading", "Commento Book II", 1, "Track love theory, beauty, desire, celestial/natural explanations, Ficino corrections, Aristotelian/Platonic moves."),
        ("pico_text_close_reading", "Commento Book III and Commento particulare", 1, "Track felicity, return, ascent, poetic-theological interpretation, biblical/Kabbalistic hints."),
        ("witness_comparison", "Commento TEI versus Basel Opera OCR and Stanley translation", 1, "Compare section order, omitted/softened Ficino polemic, and English reception transformations."),
    ]
    conn.executemany(
        "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
        [(COMMENTO_DOC_ID, *task) for task in tasks],
    )


def ingest_stanley(conn: sqlite3.Connection) -> None:
    text = STANLEY_TXT.read_text(encoding="utf-8", errors="replace")
    # The IA OCR preserves many section names as running headers rather than
    # clean display headings, so line-number cuts are more stable than regex
    # headings for this small translation witness.
    lines = text.splitlines()
    cut_lines = [
        ("Introduction", 44),
        ("The First Book", 727),
        ("The Second Book", 1130),
        ("The Sonnet", 1771),
        ("The Third Book", 2016),
        ("Notes and Bibliographical Note", 2406),
    ]
    offsets: list[tuple[int, str]] = []
    cursor = 0
    for lineno, line in enumerate(lines, start=1):
        if lineno == cut_lines[cursor][1]:
            offsets.append((sum(len(x) + 1 for x in lines[: lineno - 1]), cut_lines[cursor][0]))
            cursor += 1
            if cursor >= len(cut_lines):
                break
    positions = offsets
    pages = []
    for idx, (start, title) in enumerate(positions):
        end = positions[idx + 1][0] if idx + 1 < len(positions) else len(text)
        section_text = clean(text[start:end])
        if section_text:
            pages.append({"page": len(pages) + 1, "heading": title, "text": section_text})
    if not pages:
        words = re.findall(r"\S+", text)
        pages = [{"page": i + 1, "heading": f"OCR chunk {i+1}", "text": " ".join(words[i * 1800 : (i + 1) * 1800])} for i in range((len(words) + 1799) // 1800)]
    full_text = "\n\n".join(p["text"] for p in pages)
    metadata = {
        "title": "A Platonick discourse upon love",
        "author": "Giovanni Pico della Mirandola",
        "translator": "Thomas Stanley",
        "editor": "Edmund G. Gardner",
        "publication_year": "1914",
        "translation_first_publication": "1651 in Thomas Stanley, Poems",
        "source": "Internet Archive FULL TEXT OCR",
        "source_url": "https://archive.org/details/platonickdiscour00picouoft",
        "copyright_status_ia": "NOT_IN_COPYRIGHT",
        "note": "1914 reprint of Stanley's early modern English translation of Pico's Commento.",
    }
    md_pages = "\n\n".join(f"## {p['heading']}\n\n{p['text']}" for p in pages)
    md = f"""---
id: "{STANLEY_DOC_ID}"
source_file: "{STANLEY_TXT.name}"
source_path: "{STANLEY_TXT.resolve()}"
document_type: "translation_reception_witness"
themes: ["Commento", "Platonic love", "early modern English reception", "Thomas Stanley", "Benivieni"]
pico_works_discussed: ["Commento sopra una canzone d'amore"]
conversion_method: "Internet Archive OCR text sectioned by printed headings"
converted_at: "{datetime.now(UTC).isoformat(timespec='seconds').replace('+00:00', 'Z')}"
review_status: "TRANSLATION_RECEPTION_WITNESS_NEEDS_COLLATION"
source_url: "{metadata['source_url']}"
---

# A Platonick discourse upon love

> Early modern English translation witness: Thomas Stanley's 1651 translation, here through Edmund G. Gardner's 1914 reprint. Use for reception and comparison; verify wording against page images before quotation.

{md_pages}
"""
    md_path = MARKDOWN / f"{STANLEY_DOC_ID}.md"
    md_path.write_text(md, encoding="utf-8", newline="\n")
    conn.execute(
        """
        INSERT OR REPLACE INTO documents
        (id,title,source_file,source_path,markdown_path,extension,sha256,duplicate_of,document_type,
         themes_json,pico_works_json,page_count,word_count,extraction_status,metadata_json,source_method,review_status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            STANLEY_DOC_ID,
            metadata["title"],
            STANLEY_TXT.name,
            str(STANLEY_TXT.resolve()),
            str(md_path.resolve()),
            ".txt",
            sha256(STANLEY_TXT),
            None,
            "translation_reception_witness",
            json.dumps(["Commento", "Platonic love", "early modern English reception", "Thomas Stanley", "Benivieni"]),
            json.dumps(["Commento sopra una canzone d'amore"]),
            len(pages),
            count_words(full_text),
            "OK_OCR_UNREVIEWED",
            json.dumps(metadata, ensure_ascii=False),
            "internet_archive_ocr_sectioning",
            "TRANSLATION_RECEPTION_WITNESS_NEEDS_COLLATION",
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    for table in ["pages", "sections", "document_fts", "reading_tasks"]:
        conn.execute(f"DELETE FROM {table} WHERE document_id=?", (STANLEY_DOC_ID,))
    conn.executemany(
        "INSERT INTO pages(document_id,page_number,heading,text,word_count) VALUES (?,?,?,?,?)",
        [(STANLEY_DOC_ID, p["page"], p["heading"], p["text"], count_words(p["text"])) for p in pages],
    )
    conn.executemany(
        "INSERT INTO sections(document_id,level,title,start_page,notes) VALUES (?,?,?,?,?)",
        [(STANLEY_DOC_ID, 1, p["heading"], p["page"], "OCR section from 1914 reprint") for p in pages],
    )
    conn.execute(
        "INSERT INTO document_fts(document_id,title,source_file,text,themes) VALUES (?,?,?,?,?)",
        (STANLEY_DOC_ID, metadata["title"], STANLEY_TXT.name, full_text, "Commento Stanley Platonick discourse love English reception"),
    )
    conn.executemany(
        "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
        [
            (STANLEY_DOC_ID, "translation_collation", "Stanley Platonick discourse upon love", 1, "Collate against Italian TEI by book and sonnet."),
            (STANLEY_DOC_ID, "reception_summary", "Early modern English Pico", 2, "Summarize Gardner introduction and Stanley's English reception of Pico's love theory."),
        ],
    )


def update_ontology() -> None:
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.13.0"
    payload["commento_close_reading_fields"] = [
        "witness",
        "book_or_stanza",
        "chapter",
        "argument_function",
        "being_mode",
        "hierarchy_level",
        "love_doctrine",
        "beauty_doctrine",
        "mind_soul_body_relation",
        "angelic_or_intelligible_reference",
        "ficino_agreement_or_correction",
        "platonic_source",
        "aristotelian_or_arabic_source",
        "dionysian_or_christian_theological_control",
        "poetic_theology_claim",
        "biblical_or_kabbalistic_hint",
        "translation_reception_difference",
        "open_problem",
    ]
    payload["corpus_control_rules"] = sorted(set(payload.get("corpus_control_rules", []) + [
        "A TEI primary text can upgrade a work from public-digital-lead to controlled-primary-text, but only section summaries and witness comparison make it research-ready.",
        "Early modern translations should be tagged as reception witnesses and collated rather than silently substituted for Pico's Italian.",
    ]))
    payload["guide_scholars"]["Thomas Stanley"] = sorted(set(payload["guide_scholars"].get("Thomas Stanley", []) + ["early_modern_translation", "english_platonism", "commento_reception"]))
    payload["guide_scholars"]["Sears Jayne"] = sorted(set(payload["guide_scholars"].get("Sears Jayne", []) + ["modern_commento_translation", "ficino_english_platonism", "translation_history"]))
    write_json(path, payload)


def write_artifacts() -> None:
    write(
        "artifacts/source_packets/commento_full_text_control_pass014.md",
        """# Source Packet: Commento Full-Text Control Pass 014

- Artifact ID: `source_commento_control_pass014`
- Type: source packet
- Document ID: `Pico_Commento_BibliotecaItaliana_TEI_bibit000827_xml_2e50ef08`
- Status: CONTROLLED_PRIMARY_TEXT
- Evidence status: verified

## Acquisition

PicoDB now has the full Italian *Commento sopra una canzone d'amore di Girolamo Benivieni* from Biblioteca Italiana's TEI/XML endpoint. The digital record identifies Giovanni Pico as author, Biblioteca Italiana as digital publisher, Rome 2004 as digital publication context, and the source edition as Bausi's *Opere complete* with reference to Garin's 1942 text. The record states that the resource is freely accessible for personal or scientific use, with commercial use prohibited.

## Structure

The TEI structure gives a reliable close-reading grid: title, Blasius Bonacursius dedication, Benivieni's address to the reader, Benivieni's canzone, Book I with 13 chapters, Book II with 24 chapters, Book III with 4 chapters, and the *Commento particulare* on individual stanzas.

## Research Value

This upgrades the Commento from `public_digital_text_identified` to `controlled_primary_text_needs_close_reading`. It should now govern future work on Ficino/Pico, Platonic love, poetic theology, astrology in desire theory, angelic/intelligible hierarchy, and the relation between early Commento metaphysics and Oration/Heptaplus.
""",
    )
    write(
        "artifacts/source_packets/stanley_platonick_discourse_pass014.md",
        """# Source Packet: Stanley's Platonick Discourse upon Love

- Artifact ID: `source_stanley_platonick_discourse_pass014`
- Type: source packet
- Document ID: `Pico_Stanley_Platonick_Discourse_1914_IA_fulltext_txt_6a4507d9`
- Status: TRANSLATION_RECEPTION_WITNESS
- Evidence status: likely

## Acquisition

PicoDB now has the Internet Archive OCR of *A Platonick discourse upon love*, Edmund G. Gardner's 1914 edition of Thomas Stanley's early modern English translation. The Internet Archive record identifies it as a reprint of Stanley's translation first published in *Poems* in London, 1651, under the title *A Platonick discourse upon love, written in Italian, by John Picus Mirandula in explication of a sonnet by Hieronimo Benevieni*.

## Use

Use Stanley as an English reception and translation witness, not as a substitute for Pico's Italian. It can help track how the Commento entered English Platonism and how its vocabulary of love, mind, beauty, and ascent was domesticated for seventeenth-century readers.
""",
    )
    write(
        "artifacts/section_summaries/commento/commento_structure_summary_pass014.md",
        """# Section Summary: Commento Structure Pass 014

- Artifact ID: `summary_commento_structure_pass014`
- Type: section summary
- Status: STRUCTURAL_SUMMARY
- Evidence status: verified

## Whole-Text Structure

The *Commento* begins with paratextual mediation before Pico's philosophical exposition: a dedicatory epistle by Blasius Bonacursius, Benivieni's address to the reader, and Benivieni's canzone. This matters because the work is never just a treatise; it is a poem-commentary event involving friendship, publication, correction, and the problem of Christianizing Platonic love.

Book I establishes the metaphysical scaffold: modes of being, created hierarchy, God, angelic or intellectual nature, rational soul, causality, formal and ideal being, and the Platonist language through which Pico can talk about divine transcendence without immediately collapsing into Ficino.

Book II is the largest section and should be read as the central doctrinal field for love, beauty, desire, mediation, celestial/natural explanation, and the relation between Platonic and Christian vocabularies. It is the first place to test Rutkin on astrology, Allen on Ficino, and the ontology's tags for mind, soul, body, attraction, and poetic theology.

Book III narrows toward felicity, return, and ascent. It should be linked to the Oration's ladder, Heptaplus allegory, and the 900 Conclusions' metaphysical and Kabbalistic ascent patterns.

The *Commento particulare* returns from systematic exposition to stanza-by-stanza interpretation. This is where Pico's poetic theology can be marked most explicitly: allegorical reading, mythic images, veiled doctrine, scriptural or theological corrections, and the relation between Benivieni's poetic form and Pico's philosophical architecture.
""",
    )
    write(
        "artifacts/concepts/commento_reading_ontology_pass014.md",
        """# Concept Dossier: Commento Reading Ontology

- Artifact ID: `concept_commento_reading_ontology`
- Type: concept dossier
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Required Tags

Every Commento section summary should tag: book/stanza, argument function, being mode, hierarchy level, love doctrine, beauty doctrine, mind/soul/body relation, angelic or intelligible reference, Ficino agreement or correction, Platonic source, Aristotelian or Arabic source, Dionysian or Christian theological control, poetic theology claim, biblical or Kabbalistic hint, translation/reception difference, and open problem.

## Scholar Governors

- Allen governs Ficino dispute, Venus, Mind, Platonic exegesis, and the concealed/softened polemical history.
- Rutkin governs early astrological language in desire and attraction.
- Black governs later links to Heptaplus, allegory, felicity, and anagogical structure.
- Busi and Wirszubski govern any claim that the Commento anticipates Kabbalistic structures.
- Copenhaver governs anti-mythic caution and juridical/theological danger when claims drift toward the later Roman crisis.
- Stanley and Jayne govern English reception and translation history.
""",
    )
    write(
        "artifacts/essays/commento_control_and_reading_plan_pass014.md",
        """# Essay Draft: How We Can Now Read Pico's Commento

- Artifact ID: `essay_commento_control_and_reading_plan`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

The Commento is no longer a missing or merely secondary-rich text for PicoDB. With the Biblioteca Italiana TEI in Markdown and SQLite, it becomes a controlled primary text whose structure can now govern close reading. This changes the project because the Commento is one of the best early places to see Pico thinking at the intersection of Ficino, Platonism, poetry, love, celestial causality, angelic/intelligible hierarchy, and Christian theological correction.

The first reading task is structural. The work is not simply three books. It is a paratextual and poetic event: dedication, Benivieni's reader-address, the canzone, three books of general exposition, and the particular commentary on the poem's stanzas. That structure matters because it stages the relation between poem and philosophy. Pico is not writing an abstract textbook on love; he is interpreting a friend's poem under the pressure of Ficino's Symposium commentary and the larger Florentine conversation about Platonic love.

The second task is metaphysical. Book I should be read for modes of being, causality, divine transcendence, intellectual nature, rational soul, and the hierarchy that allows Pico to talk about God, angelic mind, and soul while correcting Platonist excess through Christian theological controls. This belongs directly beside On Being and Unity and the Oration.

The third task is doctrinal. Book II, the largest book, should be mined for love, beauty, desire, attraction, celestial/natural explanation, body-soul mediation, and the boundaries between poetic astrology, natural philosophy, and theological ascent. This is where Rutkin's work on early Pico and astrology should be tested passage by passage.

The fourth task is reception. Stanley's 1651 English translation, now available through the 1914 reprint, should be collated against the Italian. Its importance is not only linguistic. It shows how Pico's Commento became usable for English Platonism and for the history of "Platonic love" as a literary and moral vocabulary.

The result should be a Commento dossier with every chapter summarized, every reference registered, every Ficino correction marked, and every later essay link made explicit: Ficino dispute, astrology, angelology, Kabbalah, Heptaplus, Oration, On Being and Unity, and poetic theology.
""",
    )


def update_docs() -> None:
    append_once(
        DOCS / "PICO_TEXT_GAPS.md",
        "## Commento Pass 014 Gap Update",
        """## Commento Pass 014 Gap Update

- `Commento sopra una canzone d'amore`: `controlled_primary_text_needs_close_reading`; Biblioteca Italiana TEI/XML has been ingested and sectioned by dedication, canzone, books, chapters, and stanza commentary.
- `A Platonick discourse upon love`: `translation_reception_witness_acquired`; Thomas Stanley's 1651 English translation is available through the 1914 Gardner reprint OCR and should be collated against the Italian.
""",
    )
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 014 Commento Overlay",
        """## Pass 014 Commento Overlay

For the Commento, summarize at chapter or stanza level. Each summary must state the section's role in the poem-commentary structure, reconstruct the argument, register Ficino agreement or correction, identify Platonist/Aristotelian/Arabic/Dionysian sources where visible, and mark whether love, beauty, desire, celestial causality, angelic/intelligible hierarchy, poetic theology, or biblical/Kabbalistic hints are active.
""",
    )


def db_rows(conn: sqlite3.Connection) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    artifacts = [
        ("source_commento_control_pass014", "source_packet", "Commento Full-Text Control Pass 014", "artifacts/source_packets/commento_full_text_control_pass014.md", COMMENTO_DOC_ID, "Commento", "CONTROLLED_PRIMARY_TEXT", "verified"),
        ("source_stanley_platonick_discourse_pass014", "source_packet", "Stanley's Platonick Discourse upon Love", "artifacts/source_packets/stanley_platonick_discourse_pass014.md", STANLEY_DOC_ID, "Commento reception", "TRANSLATION_RECEPTION_WITNESS", "likely"),
        ("summary_commento_structure_pass014", "section_summary", "Commento Structure Summary", "artifacts/section_summaries/commento/commento_structure_summary_pass014.md", COMMENTO_DOC_ID, "Commento", "STRUCTURAL_SUMMARY", "verified"),
        ("concept_commento_reading_ontology", "concept_dossier", "Commento Reading Ontology", "artifacts/concepts/commento_reading_ontology_pass014.md", COMMENTO_DOC_ID, "Commento", "SOURCE_ANCHORED_DRAFT", "likely"),
        ("essay_commento_control_and_reading_plan", "website_page", "How We Can Now Read Pico's Commento", "artifacts/essays/commento_control_and_reading_plan_pass014.md", COMMENTO_DOC_ID, "Commento", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
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
        ("claim_commento_014_001", "source_commento_control_pass014", COMMENTO_DOC_ID, "The full Italian Commento is now locally controlled from Biblioteca Italiana TEI/XML and sectioned for systematic close reading.", "bibliographic", "Commento", "Commento", "TEI acquisition", "high", "DRAFT", "Pass 014."),
        ("claim_commento_014_002", "summary_commento_structure_pass014", COMMENTO_DOC_ID, "The Commento's structure includes dedication, Benivieni's address, the canzone, Book I with 13 chapters, Book II with 24 chapters, Book III with 4 chapters, and a stanza-by-stanza Commento particulare.", "textual", "structure", "Commento", "TEI div tree", "high", "DRAFT", "Pass 014."),
        ("claim_commento_014_003", "source_stanley_platonick_discourse_pass014", STANLEY_DOC_ID, "Thomas Stanley's early modern English translation of Pico's Commento appeared in 1651 and is accessible through Gardner's 1914 reprint as A Platonick discourse upon love.", "bibliographic", "translation", "Commento reception", "IA record", "high", "DRAFT", "Pass 014."),
        ("claim_commento_014_004", "concept_commento_reading_ontology", COMMENTO_DOC_ID, "Future Commento summaries must mark Ficino agreement or correction, being mode, hierarchy, love doctrine, beauty doctrine, source family, poetic theology, and translation/reception differences.", "methodological", "ontology", "Commento", "Pass 014 ontology", "high", "DRAFT", "Pass 014."),
        ("claim_commento_014_005", "essay_commento_control_and_reading_plan", COMMENTO_DOC_ID, "Book II should become the main testing field for early Pico on love, beauty, desire, attraction, celestial/natural explanation, and the boundary between astrology and poetic theology.", "open_problem", "Commento", "early Pico astrology", "Pass 014 plan", "medium", "DRAFT", "Pass 014."),
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
        ("source-commento-control-pass014", "source_packet", "Commento Full Text Acquired", "Biblioteca Italiana TEI", "The Commento is now a controlled primary text in Markdown and SQLite, sectioned by paratext, books, chapters, and stanza commentary.", "DRAFT", "source_commento_control_pass014"),
        ("source-stanley-platonick-pass014", "source_packet", "Stanley's Platonick Discourse", "1651 English reception witness", "Thomas Stanley's early modern English translation of Pico's Commento is now available for collation through the 1914 Gardner reprint.", "DRAFT", "source_stanley_platonick_discourse_pass014"),
        ("concept-commento-reading-ontology", "concept", "Commento Reading Ontology", "Love, beauty, hierarchy, Ficino", "A new ontology layer tells future summaries what to mark in every Commento chapter and stanza.", "DRAFT", "concept_commento_reading_ontology"),
        ("essay-commento-reading-plan", "essay", "How We Can Now Read the Commento", "Controlled text, translation witness, close reading", "A new essay plan turns the acquired Commento into work on Ficino, love, poetic theology, astrology, hierarchy, and English reception.", "DRAFT", "essay_commento_control_and_reading_plan"),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id, entity_type, title, subtitle, summary, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        cards,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("page-commento-reading-plan", "essay", "How We Can Now Read Pico's Commento", "artifacts/essays/commento_control_and_reading_plan_pass014.md", "DRAFT", "essay_commento_control_and_reading_plan"),
            ("page-commento-reading-ontology", "concept", "Commento Reading Ontology", "artifacts/concepts/commento_reading_ontology_pass014.md", "DRAFT", "concept_commento_reading_ontology"),
        ],
    )


def refresh(conn: sqlite3.Connection) -> None:
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
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)


def main() -> None:
    conn = sqlite3.connect(DB)
    ingest_commento(conn)
    ingest_stanley(conn)
    update_ontology()
    write_artifacts()
    update_docs()
    db_rows(conn)
    conn.commit()
    refresh(conn)
    conn.close()
    print("Study pass 014 complete.")


if __name__ == "__main__":
    main()
