"""Study pass 012: Pico Opera reviews and missing writings roadmap."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"
DATA = ROOT / "data"
DOCS = ROOT / "docs"

DOCS_BY_KEY = {
    "opera_omnia_review": "Mediaevistik_vol._20_Giovanni_Pico_della_Mirandola_Gian_Francesco_Pico_Opera_Omniaby_Cesare_Vaso_pdf_70455a35",
    "carmina_review": "Romanische_Forschungen_vol._78_iss._1_Carmina_latinaby_Giovanni_Pico_Della_Mirandola__Wolfgang_S_pdf_27cec604",
    "rq_congress_review": "Renaissance_Quarterly_vol._20_iss._1_L_and__039_Opera_e_il_pensiero_di_Giovanni_Pico_della_Miran_pdf_f27cfe43",
    "chr_congress_review": "The_Catholic_Historical_Review_1968-jul_vol._54_iss._2_L_and__039_opera_e_il_pensiero_di_Giovann_pdf_f097dc9f",
    "latomus_congress_review": "Latomus_1967-jan-mar_vol._26_iss._1_L_and__039_opera_e_il_pensiero_di_Giovanni_Pico_della_Mirand_pdf_cde73721",
    "bhr_congress_review": "Bibliothèque_d_and__039_Humanisme_et_Renaissance_vol._28_iss._1_L_and__039_opera_e_il_pensiero_d_pdf_41bfc523",
}

FILES = {
    "docs/PICO_PRIMARY_TEXT_ACQUISITION_PROTOCOL.md": """# Pico Primary Text Acquisition Protocol

Status: DRAFT  
Created in study pass 012.

## Purpose

This protocol governs the next phase of PicoDB: moving from secondary-rich thematic study toward controlled access to Pico's writings, early editions, manuscript witnesses, and reception texts that shaped the corpus. Every missing-work note must distinguish absence of a work from absence of a critical edition, absence of a translation, absence of manuscript control, or absence of section-level summaries.

## Required Fields

- work_title
- genre: speech, thesis collection, defense, commentary, metaphysical treatise, biblical exegesis, letter, poem, anti-astrology, devotional work, reception/life, edition/reprint.
- current_access_status: full_primary, partial_primary, anthology_excerpt, secondary_only, review_only, early_print_needed, manuscript_needed, not_identified.
- edition_priority: critical_edition, early_print, modern_translation, manuscript_witness, reception_witness.
- reason_needed: chronology, source control, philosophical doctrine, Kabbalah, magic, astrology, reception, biography, corpus formation, website product.
- known_witness_or_edition: local file, Basel 1557/1573, Bologna 1496, Garin, Bausi/Vasoli, Speyer, Kristeller, Borghesi, PRDL/online, manuscript shelfmark if known.
- next_action: acquire, ingest, collate, section_summarize, translate, compare witnesses, mark duplicate.
- scholar_governor: Dougherty/Borghesi, Garin, Bausi/Vasoli, Kristeller, Speyer, Farmer, Copenhaver, Black, Allen, Wirszubski, Akopyan, Howlett, Edelheit.
- risk: posthumous editing, nephewly correction, expurgation, anthology distortion, manuscript branch, OCR/extraction problem, language barrier.

## Style Rules

1. Treat Opera Omnia reprints as corpus-control tools, not as final critical texts.
2. Separate Giovanni Pico's writings from Gianfrancesco Pico's writings even when editions bind them together.
3. Record posthumous mediation whenever the 1496 Bologna edition, Gianfrancesco's editorial work, or later Basel reprints are involved.
4. Do not say "we have the work" merely because an anthology or review mentions it. A work counts as controlled only when the full text, edition metadata, and section plan are present.
5. Poetry requires manuscript-witness control. Speyer, Kristeller, Vatican, Munich, Laurenziana, and Landi/Manuzio/Domenichi traditions must be kept visible.
6. Reception texts such as Thomas More's English Life of Pico and Gianfrancesco's Vita are not transparent biography; they are corpus-forming witnesses.
""",
    "artifacts/source_packets/opera_reviews_pass012_source_packet.md": """# Source Packet: Opera Reviews Pass 012

- Artifact ID: `source_opera_reviews_pass012`
- Type: source packet
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Ingested Reviews

| Review | Main Value |
|---|---|
| Dinzelbacher on Giovanni and Gianfrancesco Pico, Opera Omnia, Basel 1557/1573, reprint with Cesare Vasoli introduction | Confirms the Basel Opera reprint remains useful because it reproduces a long-used edition and gathers most works, but it is not complete and must be checked against modern critical editions. |
| Sottili on Speyer's Carmina latina and the Mirandola congress volumes | Gives the strongest gap signal for Pico's Latin poems: newly recovered poems, manuscript witnesses, Vatican and Munich branches, Laurenziana witness, and Kristeller's additional manuscript lists. |
| Carmody, Margolin, Breen, Van Bever on L'opera e il pensiero di Giovanni Pico | Map the 1963 Mirandola congress as a major research index: Kristeller on sources, Yates on magic, Marcel on France, Lullism, Cusa, Ockhamism, Hebrew philosophers, Mithridates, Orphic materials, astrology/medicine, England, Campanella, Bruno, Hungary, iconography, and reception. |

## Immediate Bibliographic Consequences

- PicoDB needs a primary corpus dashboard separating full text, anthology text, secondary-only access, and review-only evidence.
- Basel Opera and the early posthumous editions should be acquired or located as corpus-control witnesses even when modern editions exist.
- The Latin poems require a focused acquisition and collation pass: Speyer's Carmina latina, Kristeller's article on the poems, Vat. lat. 5225, Clm 485, Muenster 29.II.276, Laur. 90 sup. 37, and the Landi/Manuzio/Domenichi transmission chain.
- The Commento remains high priority because Allen and the reviews show a textual history of suppression, correction, and recovery.
- The Disputationes remains high priority because the Opera reviews confirm its centrality while Farmer/Akopyan warn about posthumous transmission.
- De imaginatione remains not identified locally and should stay a named acquisition target.
""",
    "artifacts/section_summaries/opera_reviews/opera_reviews_section_summaries_pass012.md": """# Section Summary: Pico Opera Reviews Pass 012

- Artifact ID: `summary_opera_reviews_pass012`
- Type: section summary
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Dinzelbacher on the Opera Omnia Reprint

The review treats the Olms reprint of the Basel 1557/1573 Opera Omnia as a necessary research instrument because the Basel edition was long used in Pico scholarship. Its value is convenience, breadth, indexes, prefatory materials, and the fact that it gathers many works of Giovanni Pico and Gianfrancesco Pico. But the review explicitly cautions that many twentieth-century critical editions of individual works had appeared, especially through Garin's pioneering work, and that the Opera does not contain all writings of both authors. The review also reminds PicoDB to separate Giovanni from Gianfrancesco: the nephew wrote the Vita, promoted his uncle's works, produced his own substantial writings, and had strong interests in demonology, Kabbalah, letter symbolism, and related boundary fields.

## Sottili on Carmina latina and the Mirandola Congress

Sottili's review is the most important new text for Pico's poetry. It reports Speyer's discovery and edition of a significant group of Latin poems in the Muenster copy of a manuscript collection, then links that witness to Vat. lat. 5225, a Paolo Manuzio manuscript copied from Costanzo Landi. Sottili compares this with Kristeller's publication of the same poems in Clm 485 and notes that Kristeller also prints other unknown Pico poems, supplies a manuscript list, and gives a long bibliography. The review also notes additional manuscript and source discoveries: a Pliny copied for Pico in Venice and Elia del Medigo's Latin translation of Averroes' paraphrase of Plato's Republic, once considered lost. For PicoDB, this means poems are not a marginal literary ornament; they are a manuscript-control problem and a window into Pico's humanist formation.

## Carmody on L'opera e il pensiero

Carmody praises the congress volumes while pointing to open research problems. Kristeller's source survey is treated as the orienting scaffold. Carmody stresses fields underdeveloped or requiring better method: Averroes, pre-Socratics, Anaxagoras, Cusanus, Lullism, medicine, astrological medicine, magic, Kabbalah beyond generic Zohar references, Chaldean/Zoroastrian materials, Orphic hymns, graphic images, talismans, alchemy, and comparative religion. The review is a warning against thin source labels. It asks whether Pico used massive primary corpora or compilations, and whether alleged Kabbalistic material may come through Recanati or parallel magical and iconographic traditions.

## Margolin on the Congress

Margolin sees a transformed Pico scholarship emerging from the congress. Pico is no longer adequately described as vague eclectic, merely Ficinian, revolutionary modernist, or simple syncretist. The new Pico must be situated historically among teachers, sources, contemporaries, enemies, later readers, and medieval/quattrocento traditions. Margolin highlights concord as dialogue rather than easy eclecticism, and emphasizes the subtle relation between Plato, Aristotle, Avicenna, Averroes, Thomism, Scotism, astrology, prophecy, Kabbalah, Hermetism, demonology, Cusa, Bodin, Campanella, Bruno, France, England, Lullism, medicine, and iconography.

## Breen and Van Bever

Breen provides a concise map of the congress papers and confirms the dominant themes: 900 Theses, Oration, universality of truth, anti-astrology, human freedom, Kabbalah, philosophy of love, and interiorized religion. Van Bever highlights Garin's method: a work must be read through its past roots, its present dialogue, and its future persistence. Van Bever's phrase about restoring the tesserae of the Conclusions to their proper ensembles is now a rule for PicoDB: the 900 Conclusions must be reconstructed by clusters and source-families, not by isolated aphorisms.
""",
    "artifacts/concepts/pico_missing_writings_taxonomy_pass012.md": """# Concept Dossier: Pico Missing Writings Taxonomy

- Artifact ID: `concept_pico_missing_writings_taxonomy`
- Type: concept dossier
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Access Categories

1. Full primary text present but not fully summarized: Oration, Heptaplus, On Being and Unity, Apologia, Lettere, selected anthology materials.
2. Partial or uncertain primary text: Commento on Benivieni, Latin poems/Carmina, some letter materials, selected theses embedded in scholarship.
3. Secondary-rich but primary-text control incomplete: Disputationes adversus astrologiam divinatricem.
4. Named but not identified locally: De imaginatione.
5. Edition/reprint needed for corpus control: Basel 1557/1573 Opera Omnia, Bologna 1496 posthumous collection, early Opera witnesses, Garin/Bausi/Vasoli critical apparatus where not present.
6. Manuscript-witness needed: Latin poems, letter witnesses, Vat. lat. 5225, Clm 485, Muenster 29.II.276, Laur. 90 sup. 37, Costanzo Landi, Paolo Manuzio, Lodovico Domenichi.
7. Reception/corpus-forming texts: Gianfrancesco's Vita, Thomas More's English Life of Pico, Gianfrancesco's editions and apologetic framing.
8. Related-source texts needed for context: Elia del Medigo's translation of Averroes' paraphrase of Plato's Republic, Pliny copied for Pico, Recanati, Lullist materials, Cusanus parallels, astrological/medical compilations, Chaldean/Orphic materials.

## Priority Rule

Prioritize works that change corpus control before works that merely add another interpretation: full Disputationes, Commento, poems, De imaginatione, letters-by-letter, and early Opera witnesses come before additional thematic scholarship.
""",
    "artifacts/essays/pico_missing_writings_next_steps_draft.md": """# Essay Draft: Pico Writings We Still Need

- Artifact ID: `essay_pico_missing_writings_next_steps`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

The next phase of PicoDB should become more bibliographical, not less ambitious. The thematic essays on Kabbalah, astrology, angelology, Ficino, Heptaplus, biography, and concord have created a usable intellectual map, but the new Opera reviews show the limit of that map: we still need tighter control over Pico's actual corpus. The highest-value next steps are not simply more articles. They are editions, early prints, manuscript witnesses, and full-text primary sources that let us say exactly which Pico text we are reading, in which form, through which editorial history, and with what degree of completeness.

The first missing object is not a single text but the corpus witness supplied by the Basel Opera Omnia. Dinzelbacher's review of the Olms reprint of the Basel 1557/1573 Opera makes its status clear. The Basel Opera was long used by scholars and remains useful because it gathers many works, indexes, prefatory materials, and the intertwined legacy of Giovanni Pico and Gianfrancesco Pico. But it is not a critical edition and it is not complete. PicoDB therefore needs the Basel Opera as a control witness, not as an authority that settles readings. It should be ingested and indexed so every work, prefatory notice, editorial frame, and Gianfrancesco item can be mapped against modern critical editions.

The second priority is the early posthumous edition history, especially the 1496 Bologna collection and Gianfrancesco's editorial work. Farmer has already taught the project to worry about posthumous manipulation, especially around the Disputationes and the late anti-astrology, anti-magic, and anti-Cabala image of Pico. The Opera reviews reinforce the same point from another angle: the corpus itself is a historical construction. Gianfrancesco wrote the Vita, promoted his uncle's works, omitted or framed some materials, and supplied a saintly or orthodox image that later readers inherited. PicoDB needs a "Pico corpus formation" dossier that treats the nephew's editorial activity as evidence, not transparent preservation.

The third priority is the Commento on Benivieni's canzone. We have strong secondary guidance from Allen and related scholarship, and the corpus includes Benivieni materials and scholarship on the Commento, but our primary-text status is still partial or uncertain. This is not a minor gap. The Commento is one of the best places to see Pico in live dispute with Ficino over love, Venus, Mind, beauty, poetic theology, and Platonic exegesis. Allen shows that the text's history includes correction by Ficino, partial rebuttal by Pico, later suppression or softening, and Garin's recovery of the unexpurgated version. A full Commento pass would connect the Ficino dispute, the Kabbalah essay, the astrology essay, angelology, and the Heptaplus.

The fourth priority is the Disputationes adversus astrologiam divinatricem as a primary text. PicoDB is now rich in scholarship on astrology: Akopyan, Rabin, Rutkin, Vanden Broecke, Farmer, and the reviews give us a good interpretive frame. But the full primary text still needs controlled access, edition metadata, and section-by-section summary. This is urgent because the Disputationes is too often used as a slogan: Pico rejects astrology, Pico becomes rational, Pico turns Savonarolan, Pico repudiates magic. Our own work has already complicated that story. The next step is to read the text book by book, distinguishing natural celestial influence, judicial astrology, empirical critique, source criticism, providence, free will, and posthumous editorial risk.

The fifth priority is De imaginatione. The gap register has named it from early in the project, but no obvious local primary text has been identified. This matters because imagination sits near several live PicoDB problems: poetic theology, magic, astrology, demons, images, cognition, body-soul mediation, Ficino's psychology, and the boundary between philosophical anthropology and occult practice. If De imaginatione is extant and accessible in a modern edition or early Opera witness, it should be acquired and processed as a bridge text between the Commento, Oration, magic, and anti-astrology materials.

The sixth priority is the Latin poems. Sottili's review of Speyer's Carmina latina changes the stakes. Pico's poetry is not merely a youthful ornament. The rediscovered poems have a manuscript tradition: Muenster 29.II.276, Vat. lat. 5225, Clm 485, Laur. 90 sup. 37, and a chain involving Costanzo Landi, Paolo Manuzio, and Lodovico Domenichi. Kristeller's parallel publication adds other unknown poems, manuscript lists, and bibliography. The poetry can illuminate Pico's humanist training, Latin models, erotic and philosophical vocabulary, relation to Poliziano and Benivieni, and the literary side of his self-fashioning. PicoDB should acquire Speyer if not already present as full text, collate it with Kristeller's article, and create a poem-by-poem table.

The seventh priority is the letters. A modern Lettere file is present, but the work is not yet letter-by-letter summarized. The reviews and the biography pass both show why this matters: Pico's letters are the spine of chronology, networks, intellectual friendship, patronage, conflict, illness, devotion, and reception. They also help test stories about Ficino, Poliziano, Lorenzo, Elia del Medigo, Mithridates, Savonarola, Rome, France, and the return to Florence. The next task is not acquisition alone; it is systematic extraction: sender, recipient, date, place, occasion, works mentioned, intellectual theme, and biographical claim.

The eighth priority is a controlled Apologia and condemned-theses dossier. We do have an Apologia file, but the project still needs a full map of the thirteen condemned conclusions, the papal commission, Pico's defense, Copenhaver's trial analysis, Farmer's thesis commentary, and later reception. The Apologia is where the 900 Conclusions become a juridical-theological event. It is therefore the bridge between the thesis database and the biography.

The ninth priority is reception and corpus-making texts: Gianfrancesco's Vita and Thomas More's English Life of Pico. These should not be used naively as biography. They are evidence for how Pico was made into a saintly, orthodox, exemplary figure. The biography essay already warns against "St. Pico"; now the project needs the texts that built him. More's translation matters especially for the English Pico and for the reception line traced by the Mirandola congress reviews.

The tenth priority is related-source material that is not by Pico but changes how Pico's writings are read. Sottili notes a Pliny manuscript copied for Pico and Elia del Medigo's Latin translation of Averroes' paraphrase of Plato's Republic, once thought lost. Carmody points to a cluster of source problems: Averroes, pre-Socratics, Anaxagoras, Cusanus, Lullism, astrological medicine, magic images, talismans, alchemy, Chaldean and Orphic materials, Recanati, and the danger of thin Zohar labels. These are not all immediate acquisition targets, but they should become a "source ecology" queue. Some will explain why Pico reads the way he does; others will prevent false attributions.

The practical next step is a primary-corpus dashboard. Each Pico work should have a row: title, genre, date, current access status, local files, edition/witness status, section-summary status, scholar governors, themes, and next action. The highest priorities are: Basel Opera witness; Commento full text; Disputationes full text; De imaginatione; poem corpus and manuscript dossier; letters-by-letter extraction; Apologia/condemned-theses dossier; Gianfrancesco Vita and More's Life; and related Averroes/Recanati/Lull/Cusa source texts. This would let PicoDB move from being a brilliant reading notebook into a serious research instrument for Pico's whole corpus.
""",
}

ARTIFACT_ROWS = [
    ("source_opera_reviews_pass012", "source_packet", "Opera Reviews Pass 012 Source Packet", "artifacts/source_packets/opera_reviews_pass012_source_packet.md", DOCS_BY_KEY["opera_omnia_review"], "Pico Opera reviews", "SOURCE_ANCHORED", "likely"),
    ("summary_opera_reviews_pass012", "section_summary", "Opera Reviews Section Summaries", "artifacts/section_summaries/opera_reviews/opera_reviews_section_summaries_pass012.md", DOCS_BY_KEY["carmina_review"], "Pico Opera reviews", "SOURCE_ANCHORED_DRAFT", "likely"),
    ("concept_pico_missing_writings_taxonomy", "concept_dossier", "Pico Missing Writings Taxonomy", "artifacts/concepts/pico_missing_writings_taxonomy_pass012.md", DOCS_BY_KEY["rq_congress_review"], "Pico missing writings", "SOURCE_ANCHORED_DRAFT", "likely"),
    ("essay_pico_missing_writings_next_steps", "website_page", "Pico Writings We Still Need", "artifacts/essays/pico_missing_writings_next_steps_draft.md", DOCS_BY_KEY["opera_omnia_review"], "Pico missing writings", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]

CLAIMS = [
    ("claim_missing_012_001", "essay_pico_missing_writings_next_steps", DOCS_BY_KEY["opera_omnia_review"], "The Basel 1557/1573 Opera Omnia reprint is a necessary corpus-control witness but not a complete or critical edition of all Pico writings.", "bibliographic", "corpus control", "Basel Opera Omnia", "Dinzelbacher review", "high", "DRAFT", "Pass 012."),
    ("claim_missing_012_002", "essay_pico_missing_writings_next_steps", DOCS_BY_KEY["carmina_review"], "The Latin poems require manuscript-witness control involving Speyer, Kristeller, Vat. lat. 5225, Clm 485, Muenster 29.II.276, Laur. 90 sup. 37, and the Landi/Manuzio/Domenichi chain.", "bibliographic", "poems", "Pico Carmina", "Sottili review", "high", "DRAFT", "Pass 012."),
    ("claim_missing_012_003", "summary_opera_reviews_pass012", DOCS_BY_KEY["rq_congress_review"], "Carmody treats Kristeller's source survey as an orienting scaffold and highlights open problems around Averroes, Anaxagoras, Cusa, Lull, medicine, astrology, Kabbalah, Chaldean/Orphic materials, magic images, talismans, and alchemy.", "historiographical", "source ecology", "Mirandola congress", "Carmody review", "medium", "DRAFT", "Pass 012."),
    ("claim_missing_012_004", "summary_opera_reviews_pass012", DOCS_BY_KEY["bhr_congress_review"], "Margolin frames the Mirandola congress as a shift from reductive Pico myths toward a historically situated Pico defined by teachers, sources, contemporaries, enemies, later readers, and concord as dialogue.", "historiographical", "historiography", "Pico scholarship", "Margolin review", "medium", "DRAFT", "Pass 012."),
    ("claim_missing_012_005", "essay_pico_missing_writings_next_steps", DOCS_BY_KEY["chr_congress_review"], "Breen's review confirms the dominant congress themes: 900 Theses, Oration, universality of truth, anti-astrology, human freedom, Kabbalah, love, and interiorized religion.", "historiographical", "congress themes", "Pico works", "Breen review", "medium", "DRAFT", "Pass 012."),
    ("claim_missing_012_006", "essay_pico_missing_writings_next_steps", DOCS_BY_KEY["latomus_congress_review"], "Van Bever's Garin summary gives PicoDB a rule: recover a work's roots, present dialogue, and future persistence, and restore the tesserae of the Conclusions to their proper ensembles.", "methodological", "Garin method", "900 Conclusions", "Van Bever review", "high", "DRAFT", "Pass 012."),
    ("claim_missing_012_007", "concept_pico_missing_writings_taxonomy", DOCS_BY_KEY["opera_omnia_review"], "Future gap records must distinguish full primary access, partial access, secondary-rich access, review-only evidence, early-print need, manuscript need, and section-summary need.", "methodological", "ontology", "Pico missing writings", "Pass 012 taxonomy", "high", "DRAFT", "Pass 012."),
    ("claim_missing_012_008", "essay_pico_missing_writings_next_steps", DOCS_BY_KEY["rq_congress_review"], "The next acquisition queue should prioritize corpus-control texts before additional thematic scholarship: Basel Opera, Commento, Disputationes, De imaginatione, poems, letters, Apologia, Vita/More, and source ecology texts.", "open_problem", "acquisition", "Pico missing writings", "Pass 012 synthesis", "high", "DRAFT", "Pass 012."),
]

CARDS = [
    ("essay-pico-missing-writings", "essay", "Pico Writings We Still Need", "Next primary-text acquisitions", "A new essay uses Opera reviews to prioritize missing or undercontrolled Pico writings: Basel Opera, Commento, Disputationes, De imaginatione, Carmina, letters, Apologia, Vita/More, and source ecology texts.", "DRAFT", "essay_pico_missing_writings_next_steps"),
    ("source-opera-reviews-pass012", "source_packet", "Opera Reviews Source Packet", "Six new reviews ingested", "The pass 012 source packet records reviews of the Basel Opera Omnia, Speyer's Carmina latina, and the Mirandola congress volumes.", "DRAFT", "source_opera_reviews_pass012"),
    ("concept-pico-missing-writings", "concept", "Missing Writings Taxonomy", "Primary access versus corpus control", "PicoDB now separates full primary text, partial primary text, secondary-rich gaps, review-only evidence, early-print needs, manuscript needs, and reception witnesses.", "DRAFT", "concept_pico_missing_writings_taxonomy"),
]


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


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


def update_ontology() -> None:
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.11.0"
    payload["primary_text_acquisition_fields"] = [
        "work_title",
        "genre",
        "current_access_status",
        "edition_priority",
        "reason_needed",
        "known_witness_or_edition",
        "next_action",
        "scholar_governor",
        "risk",
        "confidence",
    ]
    payload["primary_text_access_statuses"] = [
        "full_primary",
        "partial_primary",
        "anthology_excerpt",
        "secondary_only",
        "review_only",
        "early_print_needed",
        "manuscript_needed",
        "not_identified",
        "section_summary_needed",
    ]
    payload["missing_writings_priority_queue"] = [
        "Basel_1557_1573_Opera_Omnia",
        "Bologna_1496_posthumous_collection",
        "Commento_on_Benivieni",
        "Disputationes_adversus_astrologiam_divinatricem",
        "De_imaginatione",
        "Carmina_latina_and_poem_witnesses",
        "Lettere_letter_by_letter",
        "Apologia_condemned_theses",
        "Gianfrancesco_Vita_and_More_Life",
        "source_ecology_Averroes_Recanati_Lull_Cusa_Chaldean_Orphic",
    ]
    payload["guide_scholars"]["Garin"] = sorted(set(payload["guide_scholars"].get("Garin", []) + ["opera_e_pensiero", "historical_context", "concord_as_dialogue", "critical_editions"]))
    payload["guide_scholars"]["Kristeller"] = sorted(set(payload["guide_scholars"].get("Kristeller", []) + ["source_survey", "manuscript_lists", "latin_poems", "humanist_sources"]))
    payload["guide_scholars"]["Speyer"] = sorted(set(payload["guide_scholars"].get("Speyer", []) + ["carmina_latina", "poem_witnesses", "poetic_collection_structure"]))
    write_json(path, payload)


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


def update_docs() -> None:
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 012 Corpus-Control Overlay",
        """## Pass 012 Corpus-Control Overlay

When summarizing reviews, editions, or source surveys, extract every work-title, edition, manuscript witness, early print, reception text, and source-family clue. Mark whether the passage changes access status, edition priority, source ecology, or corpus-formation risk. See `docs/PICO_PRIMARY_TEXT_ACQUISITION_PROTOCOL.md`.
""",
    )
    append_once(
        DOCS / "PICO_TEXT_GAPS.md",
        "## Opera Reviews Pass 012 Gap Update",
        """## Opera Reviews Pass 012 Gap Update

- `Basel 1557/1573 Opera Omnia`: `early_print_reprint_needed_for_corpus_control`; useful long-used Opera witness, but incomplete and not a substitute for critical editions.
- `Bologna 1496 posthumous collection`: `early_print_needed`; needed for Gianfrancesco's corpus-making and posthumous Pico.
- `Commento sopra una canzone d'amore`: `high_priority_full_primary_text_and_witness_control`; needed for Ficino dispute, poetic theology, love, Venus, Mind, and suppression/recovery history.
- `Disputationes adversus astrologiam divinatricem`: `high_priority_full_primary_text`; scholarship is strong, but primary-text and posthumous-edition control remain inadequate.
- `De imaginatione`: `not_identified_high_priority`; needed for imagination, magic, psychology, images, and Ficinian boundary questions.
- `Carmina latina / Latin poems`: `partial_secondary_and_review_control_manuscripts_needed`; Speyer/Kristeller and manuscript witnesses must be mapped poem by poem.
- `Lettere`: `primary_present_letter_by_letter_summary_needed`; use Borghesi edition for chronology, network, works, and biographical claims.
- `Gianfrancesco Vita and Thomas More Life`: `reception_witnesses_needed`; needed for saintly Pico, Anglophone reception, and corpus formation.
""",
    )


def main() -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    for path, text in FILES.items():
        write(path, text)
    update_ontology()
    update_docs()

    conn = sqlite3.connect(DB)
    conn.executemany(
        """
        INSERT OR REPLACE INTO reading_artifacts
        (id, artifact_type, title, path, document_id, target_entity, status, evidence_status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM reading_artifacts WHERE id = ?), ?), ?)
        """,
        [row + (row[0], now, now) for row in ARTIFACT_ROWS],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO claims
        (id, artifact_id, document_id, claim_text, claim_type, theme, target_entity, evidence_page, confidence, review_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        CLAIMS,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id, entity_type, title, subtitle, summary, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        CARDS,
    )
    conn.execute(
        """
        INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("page-pico-missing-writings", "essay", "Pico Writings We Still Need", "artifacts/essays/pico_missing_writings_next_steps_draft.md", "DRAFT", "essay_pico_missing_writings_next_steps"),
    )
    conn.commit()
    refresh_catalog_and_manifest(conn)
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 012 complete.")


if __name__ == "__main__":
    main()
