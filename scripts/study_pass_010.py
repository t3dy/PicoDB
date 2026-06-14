"""Study pass 010: Pico and astrology synthesis."""

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
    "akopyan_book": "Brill_s_Studies_in_Intellectual_History_325_Ovanes_Akopyan_Debating_the_Stars_in_the_Italian_Ren_pdf_c6917f0c",
    "akopyan_article": "I_Tatti_Studies_Essays_in_the_Renaissance_2018-mar_vol._21_iss._1_Giovanni_Pico_della_Mirandola__pdf_8bbca9be",
    "rabin": "Explorations_in_Renaissance_Culture_2010-dec_02_vol._36_iss._2_Pico_and_the_Historiography_of_Re_pdf_352c5bd9",
    "rutkin": "Studies_in_History_and_Philosophy_of_Science_Part_C__Studies_in_History_and_Philosophy_of_Biolog_pdf_8521a36b",
    "vanden_broecke": "Medieval_and_early_modern_science_Broecke_Vanden_-_The_Limits_of_Influence__Pico_Louvain_and_the_pdf_0a6d0353",
    "boner_review": "Centaurus_2009-may_vol._51_iss._2_The_Limits_of_Influence__Pico_Louvain_and_the_Crisis_of_Renais_pdf_ec31da6e",
    "azzolini_review": "Journal_for_the_History_of_Astronomy_2006-aug_vol._37_iss._3_Book_Review__Astrology_in_the_Low_C_pdf_bb5c281e",
    "farmer": "Medieval_Renaissance_Texts_Studies_167_Stephen_A_Farmer_Giovanni_Pico_Della_Mirandola_Syncretism_pdf_c99b971b",
    "allen": "Studies_in_the_Platonism_of_Marsilio_Ficino_and_Giovanni_PicoMichael_J._B._AllenRoutledge1080299_epub_65585d05",
    "black": "Studies_in_Medieval_and_Reformation_Traditions_66_Crofton_Black_-_Picos_Heptaplus_and_Biblical_H_pdf_98e6bcc6",
}

FILES = {
    "docs/ASTROLOGY_READING_PROTOCOL.md": """# Astrology Reading Protocol

Status: DRAFT  
Created in study pass 010.

## Purpose

Pico's astrology must be read as a developmental, technical, and historiographical problem. Do not summarize it as simple rejection. Track early neutral or positive uses of celestial language, Kabbalistic and magical contexts, the late attack on divinatory astrology, the relation to natural philosophy, and the posthumous reception of the Disputationes.

## Required Fields

- pico_work: Oration, 900 Conclusions, Commento, Heptaplus, On Being and Unity, Disputationes, letters, reception text.
- astrology_register: natural astrology, judicial/divinatory astrology, astral magic, celestial causation, horoscope/nativity, conjunctionism, medical astrology, poetic astrology, anti-astrology, reception.
- attitude_status: accepts, uses neutrally, reformulates, criticizes, rejects, satirizes, posthumously appropriated, uncertain.
- causation_model: celestial light, heat, spiritus, formative virtue, matter-reception, Aristotelian physics, Platonic vehicle, Kabbalistic correspondence, providence/free will, empirical/mathematical critique.
- scholar_governor: Akopyan, Rabin, Rutkin, Vanden Broecke, Farmer, Copenhaver, Allen, Black.
- chronology: early Pico, 1486-1493 transition, late Disputationes, posthumous reception.
- genre: thesis, commentary, biblical exegesis, polemic, edition, review, reception.
- textual_risk: primary text present, secondary reconstruction, posthumous edition risk, duplicate extraction, missing critical edition.
- reception_target: Savonarola, Gianfrancesco, Bellanti, Pontano, Zorzi, Louvain, Kepler, Dee, modern historiography.

## Style Rules

1. Separate astrology from astronomy only when the source does; early modern sources often treat the science of the stars as a mixed field.
2. Distinguish judicial astrology from natural celestial influence.
3. Do not call the Disputationes a total rejection of all celestial causation unless the passage proves it.
4. Mark early Pico's astrological language in Commento, Oration, 900 Conclusions, and Heptaplus separately from late anti-divinatory polemic.
5. Treat the Disputationes as unfinished/posthumous and therefore requiring textual-transmission caution.
6. Always record whether a claim concerns Pico's own view, a reported authority, a poetic convention, or a later reception use.
""",
    "artifacts/historiography/pico_astrology_scholar_matrix.md": """# Historiography Node: Pico and Astrology Scholar Matrix

- Artifact ID: `hist_pico_astrology_scholar_matrix`
- Type: historiography node
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Problem

Pico's astrology has been overloaded with modern stories: liberation from fatalism, the triumph of human dignity, Renaissance rationality, Hermetic magic, or simple late religious repudiation. The current corpus points toward a more technical account.

## Scholar Matrix

| Scholar | Governing Value | PicoDB Rule |
|---|---|---|
| Ovanes Akopyan | Development from scientia naturalis and celestial/Kabbalistic interests to the Disputationes and its reception. | Track Pico's astrology chronologically from 1486 to 1493 rather than reading late rejection backward into early works. |
| Sheila Rabin | Historiography and correction of Burckhardt, Cassirer, Yates, Garin, Thorndike, Craven, Walker. | Every broad claim about Pico and astrology must declare which modern myth it is revising. |
| H. Darrel Rutkin | Early Pico's astrological language in love, desire, natural philosophy, and Commento. | Early astrology may be neutral, poetic, or auxiliary; do not treat it as identical with late divinatory astrology. |
| Steven Vanden Broecke | Reform/rejection boundary, Louvain reception, astrology as academic practice. | The Disputationes critiques astrological practice and boundary claims, but its reception can enable reform as well as rejection. |
| Farmer | Posthumous textual/transmission risk and Savonarolan appropriation. | Disputationes claims require edition and reception caution. |
| Allen | Ficino relation, Platonist natural philosophy, On Being and Unity shift. | Ask where Pico diverges from Ficino's astral/Platonic natural philosophy. |
| Black | Heptaplus celestial order, Arabic/Jewish philosophy, Genesis and natural knowledge. | The Heptaplus provides a biblical-cosmological bridge between early celestial thinking and later critique. |

## Synthesis

Pico's astrology is best treated as a problem of discriminating influence. He does not move from irrational astrology to rational anti-astrology. He moves through a sequence of distinctions: celestial order versus fatal prediction, natural causation versus divinatory judgment, poetic/Platonic language versus technical practice, Kabbalistic correspondences versus horoscope craft, reform versus rejection, and authorial intention versus posthumous use.
""",
    "artifacts/source_packets/astrology_new_documents_pass010.md": """# Source Packet: New Astrology Documents, Pass 010

- Artifact ID: `source_astrology_new_docs_pass010`
- Type: source packet
- Status: SOURCE_ANCHORED
- Evidence status: likely

## Ingested Sources

| Document | Role |
|---|---|
| Akopyan, "Giovanni Pico della Mirandola and Astrology (1486-1493)" | Developmental arc from early scientia naturalis, celestial/Kabbalistic materials, and natural philosophy to the Disputationes. Duplicate of an earlier local article by hash, but now sourced from Downloads. |
| Sheila J. Rabin, "Pico and the Historiography of Renaissance Astrology" | Historiographical map: Burckhardt, Cassirer, Garin, Thorndike, Craven, Walker, Yates, Kepler, and modern reassessment. |
| H. Darrel Rutkin, "Mysteries of attraction" | Early Pico's use of astrology in the Commento and desire/love materials; revises Yates and complicates early/late distinction. |
| Steven Vanden Broecke, The Limits of Influence | Reform/rejection problem, Louvain reception, academic astrology, conjunctionism, mathematical astronomy, and the Disputationes as boundary-work. |
| Boner and Azzolini reviews | Reception checks for Vanden Broecke's book and its placement in history of astrology scholarship. |

## Immediate Claims

- Pico's late Disputationes cannot be read as evidence that early Pico always rejected astrology.
- Early Pico uses astrology as part of learned natural philosophy, poetic interpretation, and celestial correspondence, often without making astrology a central doctrine.
- The Disputationes attacks divinatory/judicial astrology and challenges astrological causation, practice, tradition, and evidence, but the scope of its rejection requires careful classification.
- The afterlife of Pico's anti-astrology is not simple decline of astrology; it becomes material for reformers, opponents, and institutional debates.
""",
    "artifacts/section_summaries/astrology/astrology_new_documents_chapter_summaries_pass010.md": """# Section Summary: New Astrology Documents Pass 010

- Artifact ID: `summary_astrology_new_docs_pass010`
- Type: section summary
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Rabin, Pico and the Historiography of Renaissance Astrology

Rabin's essay is a historiographical warning system. Burckhardt and Cassirer turned Pico's anti-astrology into a drama of Renaissance freedom against astrological necessity. Garin gave Pico major importance in astrology's decline. Thorndike and Craven attacked Pico's originality and reputation from different directions. Walker complicated the rejection story by noting that Pico can accept some celestial influence while rejecting particular astrological claims. Yates overreached by turning the Disputationes into a defense of Ficinian astral magic. Rabin's value for PicoDB is the demand to identify which modern story is being repeated before making claims about Pico and astrology.

## Rutkin, Mysteries of Attraction

Rutkin makes early Pico's astrology visible in the Commento on Benivieni's love poetry. Pico uses astrologically informed natural philosophy to explain attraction, desire, bodily difference, celestial vehicles, formative virtues, and the descent of souls. Rutkin's conclusion is deliberately cautious: early Pico is not primarily an astrologer, and the evidence may show neutral or auxiliary use rather than full endorsement. This is exactly the kind of distinction the ontology needs.

## Akopyan, Giovanni Pico della Mirandola and Astrology (1486-1493)

Akopyan gives the best developmental account: early Pico links astrology with Neoplatonic ideas, Kabbalah, magic, celestial spheres, and natural philosophy; later Pico turns toward a more Aristotelian critique in the Disputationes. The late polemic has two main lines: textual/historiographical criticism of astrological authority and a physical critique of astrological prognostication.

## Vanden Broecke, The Limits of Influence

Vanden Broecke places Pico inside a longer crisis and reform of Renaissance astrology. The Disputationes is not simply a terminal blow. It becomes part of academic, Louvain, conjunctionist, reformist, theological, and mathematical debate. Vanden Broecke's key value is "boundary-work": Pico challenges what astrology may legitimately claim, how it relates to astronomy and natural philosophy, and what counts as experience or evidence.

## Reviews

The Boner and Azzolini reviews confirm that Vanden Broecke's study matters for reception, Louvain, and the institutional consequences of Pico's critique. They are not primary guides for Pico's own doctrine, but they help position the work historiographically.
""",
    "artifacts/essays/pico_astrology_synthesis_draft.md": """# Essay Draft: Pico and Astrology

- Artifact ID: `essay_pico_astrology_synthesis`
- Status: DRAFT
- Evidence status: SOURCE_ANCHORED_DRAFT

## Thesis

Pico's attitude toward astrology cannot be summarized as a single rejection. The strongest scholarship now in PicoDB suggests a developmental and discriminating account. Early Pico uses astrological language and celestial causation inside poetry, Platonist natural philosophy, Kabbalah, magic, and cosmology. Late Pico attacks divinatory astrology in the Disputationes adversus astrologiam divinatricem. The afterlife of that attack is not the disappearance of astrology but a complicated reception in reform, controversy, theology, academic practice, and modern historiography.

The first rule, supplied by Akopyan, is chronological. The Disputationes does not appear from nowhere. From 1486 to 1493 Pico's language of the heavens passes through several contexts: the 900 Conclusions, the Oration, the Commento on Benivieni, the Heptaplus, On Being and Unity, and the late anti-astrology project. In the earlier works, astrology can appear as scientia naturalis, celestial hierarchy, poetic explanation, Kabbalistic correspondence, astral image theory, or learned commonplace. These are not yet the same thing as the judicial astrology later attacked.

Rutkin's "Mysteries of attraction" is especially useful because it catches early Pico at work in a domain that is neither a horoscope manual nor a late polemic. In the Commento, Pico discusses love and desire with astrologically informed natural philosophy. Celestial vehicles, formative virtues, bodily difference, and the descent of souls help explain why one person is attracted to another. Rutkin is careful: these passages do not prove that astrology was Pico's central doctrine. They show that Pico knew astrological language well enough to use it as an explanatory support for problems he reached by other means. That gives PicoDB a necessary middle category: astrological use without strong astrological commitment.

Rabin then tells us why that distinction matters. The historiography of Pico and astrology is full of large stories. Burckhardt and Cassirer made Pico a defender of freedom against astrological necessity. Garin emphasized the importance of his critique. Thorndike and Craven deflated Pico's importance. Walker complicated the rejection story by finding room for celestial influence in the Disputationes. Yates overreached by turning the anti-astrology book into a defense of Ficinian astral magic. Rabin's lesson is methodological: before claiming what Pico "means" for astrology, say which modern myth or counter-myth is being revised.

The late Disputationes should therefore be read narrowly before it is read grandly. Pico's title targets divinatory astrology. The work attacks astrological prognostication, the authority of the astrological tradition, the reliability of astronomical and astrological evidence, and the physical plausibility of claims that particular celestial configurations determine particular human outcomes. Akopyan shows that the late critique involves both textual/historiographical criticism and natural-philosophical criticism. Pico does not simply shout "superstition." He contests astrology's sources, its internal contradictions, its empirical pretensions, and its causal model.

Vanden Broecke deepens this by making the Disputationes part of boundary-work. Astrology in the Renaissance was not a single thing. It could be natural, judicial, medical, mathematical, academic, courtly, prophetic, secretive, public, reformist, or superstitious. Pico's attack helped define the limits of legitimate influence. His critique could be used by people who rejected astrology, but also by reformers who wanted better astrology: better astronomy, better evidence, narrower claims, and cleaner causal assumptions. The phrase "limits of influence" is therefore exact. Pico's problem is not merely whether the stars influence the lower world; it is what kind of influence, under what model, and with what epistemic warrant.

This also reframes Pico's relation to Ficino. Ficino's De vita coelitus comparanda and broader astral medicine/magic made room for celestial influence, spiritus, images, music, and the soul's relation to the heavens. Pico's early works can stand near that world, though not simply inside it. Allen and Rutkin both help here: Pico and Ficino share Platonist materials, but they do not have the same program. By the time of On Being and Unity and the Disputationes, Pico's movement toward Aristotle and scholastic distinctions becomes more visible. His critique of astrology is part of a larger effort to discipline Platonist, magical, and celestial claims.

Kabbalah complicates the matter further. Early Pico can link astrology, magic, and Kabbalistic correspondences, especially in the 900 Conclusions. But Busi and Wirszubski's lessons still apply: tag the source, the operation, the translation witness, and the Christianizing move. "Astrology" in a Kabbalistic or magical thesis may involve names, letters, celestial hierarchies, correspondences, or proof of Christian mysteries, not simply horoscope prediction. The astrology protocol must therefore separate astral correspondence from judicial divination.

The Heptaplus adds a biblical-cosmological middle point. Black's reading of the Heptaplus shows Pico treating Genesis as a hidden map of created orders. The celestial world, angelic world, elemental world, and human microcosm correspond. This is not the Disputationes' target in the same way that horoscope prediction is. Pico's biblical cosmology can affirm ordered celestial structure while still rejecting the astrologer's claim to read individual destinies from configurations.

Farmer adds a final caution: the Disputationes is a posthumous, transmission-risk text. Its late anti-astrology role was shaped by Gianfrancesco, Savonarolan proximity, and later ideological uses. This does not make the text unusable. It means we must separate Pico's unfinished late project from its publication, appropriation, and reception. Savonarola's anti-astrology, Gianfrancesco's editorial work, Bellanti's response, Pontano, Zorzi, Louvain, Kepler, Dee, and later debates each make a different Pico.

The resulting position is not weak or evasive. It is stronger because it is more precise. Early Pico was neither simply pro-astrology nor secretly anti-astrology. He used astrological language and celestial natural philosophy where it helped explain love, souls, bodies, cosmic order, Kabbalah, and correspondences. Late Pico mounted a severe critique of divinatory astrology, especially its claims to prediction, authority, and causal precision. The afterlife of that critique helped reorganize astrology's boundaries rather than abolishing astrology in one blow.

For PicoDB, the next task is table-building. We need a passage table for every astrological locus in Pico's works: Commento, 900 Conclusions, Oration, Heptaplus, On Being and Unity, Disputationes, and letters. Each row should identify whether the passage concerns celestial causation, astrology proper, divination, magic, Kabbalah, natural philosophy, poetic convention, or reception. Only then can the larger essay become reviewed.
""",
    "artifacts/concepts/pico_astrology_taxonomy_pass010.md": """# Concept Dossier: Pico and Astrology Taxonomy

- Artifact ID: `concept_pico_astrology_taxonomy`
- Type: concept dossier
- Status: SOURCE_ANCHORED_DRAFT
- Evidence status: likely

## Working Taxonomy

1. Natural celestial influence: stars and planets as causes or signs in nature.
2. Judicial/divinatory astrology: prediction of contingent human events from celestial configurations.
3. Astral magic: operations using celestial images, timing, or correspondences.
4. Poetic astrology: astrological motifs used for love, character, desire, or literary explanation.
5. Kabbalistic-astral correspondence: names, letters, spheres, angels, and celestial orders linked to Kabbalah.
6. Biblical cosmology: Heptaplus celestial order and Genesis interpretation.
7. Anti-astrology: Disputationes critique of authority, evidence, causation, and prediction.
8. Reception astrology: Savonarola, Gianfrancesco, Bellanti, Pontano, Zorzi, Louvain, Kepler, Dee, modern historians.

## Use Rule

No future artifact should use the tag "astrology" alone. It must choose one or more taxonomy fields and state whether Pico accepts, uses, reforms, rejects, or reports the astrological material.
""",
}

ARTIFACT_ROWS = [
    ("hist_pico_astrology_scholar_matrix", "historiography_node", "Pico and Astrology Scholar Matrix", "artifacts/historiography/pico_astrology_scholar_matrix.md", DOCS_BY_KEY["rabin"], "Pico astrology historiography", "SOURCE_ANCHORED", "likely"),
    ("source_astrology_new_docs_pass010", "source_packet", "New Astrology Documents Pass 010", "artifacts/source_packets/astrology_new_documents_pass010.md", DOCS_BY_KEY["akopyan_article"], "Pico astrology new documents", "SOURCE_ANCHORED", "likely"),
    ("summary_astrology_new_docs_pass010", "section_summary", "Astrology New Documents Chapter Summaries", "artifacts/section_summaries/astrology/astrology_new_documents_chapter_summaries_pass010.md", DOCS_BY_KEY["rabin"], "Pico astrology scholarship", "SOURCE_ANCHORED_DRAFT", "likely"),
    ("concept_pico_astrology_taxonomy", "concept_dossier", "Pico and Astrology Taxonomy", "artifacts/concepts/pico_astrology_taxonomy_pass010.md", DOCS_BY_KEY["akopyan_book"], "Pico astrology", "SOURCE_ANCHORED_DRAFT", "likely"),
    ("essay_pico_astrology_synthesis", "website_page", "Pico and Astrology", "artifacts/essays/pico_astrology_synthesis_draft.md", DOCS_BY_KEY["akopyan_article"], "Pico astrology", "DRAFT", "SOURCE_ANCHORED_DRAFT"),
]

CLAIMS = [
    ("claim_astrology_010_001", "essay_pico_astrology_synthesis", DOCS_BY_KEY["akopyan_article"], "Pico's astrology must be read developmentally from early natural-philosophical and celestial materials to the late Disputationes.", "interpretive", "astrology", "Pico astrology", "Akopyan synthesis", "high", "DRAFT", "Pass 010."),
    ("claim_astrology_010_002", "essay_pico_astrology_synthesis", DOCS_BY_KEY["rutkin"], "Early Pico uses astrological language in the Commento to explain desire and attraction without making astrology his central doctrine.", "interpretive", "Commento", "early Pico astrology", "Rutkin synthesis", "high", "DRAFT", "Pass 010."),
    ("claim_astrology_010_003", "hist_pico_astrology_scholar_matrix", DOCS_BY_KEY["rabin"], "Claims about Pico and astrology must identify the historiographical myth they revise, especially Burckhardt/Cassirer liberation narratives and Yatesian astral-magic overreach.", "historiographical", "historiography", "Pico astrology", "Rabin synthesis", "high", "DRAFT", "Pass 010."),
    ("claim_astrology_010_004", "essay_pico_astrology_synthesis", DOCS_BY_KEY["vanden_broecke"], "The Disputationes should be read as astrological boundary-work, not only as total rejection: it challenges legitimate influence, evidence, and practice.", "interpretive", "Disputationes", "Pico astrology", "Vanden Broecke synthesis", "high", "DRAFT", "Pass 010."),
    ("claim_astrology_010_005", "essay_pico_astrology_synthesis", DOCS_BY_KEY["farmer"], "The Disputationes requires posthumous transmission and reception caution because its anti-astrology role was shaped by Gianfrancesco, Savonarolan proximity, and later uses.", "textual", "Disputationes", "textual transmission", "Farmer synthesis", "medium", "DRAFT", "Pass 010."),
    ("claim_astrology_010_006", "concept_pico_astrology_taxonomy", DOCS_BY_KEY["akopyan_book"], "Future astrology artifacts must distinguish natural celestial influence, judicial astrology, astral magic, poetic astrology, Kabbalistic correspondence, biblical cosmology, anti-astrology, and reception.", "methodological", "ontology", "Pico astrology", "Pass 010 taxonomy", "high", "DRAFT", "Pass 010."),
    ("claim_astrology_010_007", "essay_pico_astrology_synthesis", DOCS_BY_KEY["black"], "The Heptaplus can affirm ordered celestial cosmology without endorsing horoscope prediction, so it must be separated from the Disputationes target.", "interpretive", "Heptaplus", "Pico astrology", "Black synthesis", "medium", "DRAFT", "Pass 010."),
    ("claim_astrology_010_008", "source_astrology_new_docs_pass010", DOCS_BY_KEY["akopyan_article"], "The downloaded Akopyan article duplicates an existing local article by hash but is now represented as part of the pass 010 source custody trail.", "bibliographic", "ingest", "Akopyan article", "single-source ingest", "high", "DRAFT", "Pass 010."),
]

CARDS = [
    ("essay-pico-astrology", "essay", "Pico and Astrology", "From celestial use to anti-divination", "A new synthesis essay reads Pico's astrology developmentally: early celestial and poetic uses, Kabbalistic/magical contexts, late critique of divinatory astrology, and complex reception.", "DRAFT", "essay_pico_astrology_synthesis"),
    ("hist-pico-astrology-scholars", "historiography", "Astrology Scholar Matrix", "Akopyan, Rabin, Rutkin, Vanden Broecke", "A new matrix assigns guide roles for Pico's astrology: developmental arc, historiography, early Commento evidence, reform/reception, transmission risk, Ficino relation, and Heptaplus cosmology.", "DRAFT", "hist_pico_astrology_scholar_matrix"),
    ("concept-pico-astrology-taxonomy", "concept", "Astrology Taxonomy", "Do not tag astrology alone", "PicoDB now separates natural celestial influence, judicial astrology, astral magic, poetic astrology, Kabbalistic correspondences, biblical cosmology, anti-astrology, and reception.", "DRAFT", "concept_pico_astrology_taxonomy"),
    ("source-astrology-pass010", "source_packet", "Astrology Source Packet", "Six new astrology documents", "The pass 010 source packet records Akopyan, Rabin, Rutkin, Vanden Broecke, and review materials newly copied from Downloads and ingested into PicoDB.", "DRAFT", "source_astrology_new_docs_pass010"),
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
    payload["version"] = "0.9.0"
    payload["astrology_reading_fields"] = [
        "pico_work",
        "astrology_register",
        "attitude_status",
        "causation_model",
        "scholar_governor",
        "chronology",
        "genre",
        "textual_risk",
        "reception_target",
        "confidence",
    ]
    payload["astrology_taxonomy"] = [
        "natural_celestial_influence",
        "judicial_divinatory_astrology",
        "astral_magic",
        "poetic_astrology",
        "kabbalistic_astral_correspondence",
        "biblical_cosmology",
        "anti_astrology",
        "reception_astrology",
    ]
    payload["astrology_scholar_synthesis"] = {
        "Akopyan": "developmental_arc_and_disputationes_structure",
        "Rabin": "historiographical_myth_correction",
        "Rutkin": "early_astrology_commento_desire",
        "Vanden_Broecke": "reform_rejection_boundary_and_louvain_reception",
        "Farmer": "posthumous_transmission_and_savonarolan_risk",
        "Allen": "ficino_relation_and_platonic_natural_philosophy",
        "Black": "heptaplus_celestial_cosmology_and_arabic_jewish_context",
    }
    payload["guide_scholars"]["Akopyan"] = [
        "astrology_developmental_arc",
        "disputationes_structure",
        "natural_philosophy",
        "astrology_reception",
    ]
    payload["guide_scholars"]["Rabin"] = [
        "astrology_historiography",
        "burckhardt_cassirer_correction",
        "yates_correction",
    ]
    payload["guide_scholars"]["Rutkin"] = [
        "early_astrology",
        "commento_desire",
        "astrology_magic_kabbalah_historiography",
    ]
    payload["guide_scholars"]["Vanden Broecke"] = [
        "astrological_boundary_work",
        "louvain_reception",
        "reform_vs_rejection",
        "academic_astrology",
    ]
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
        "## Pass 010 Astrology Overlay",
        """## Pass 010 Astrology Overlay

When summarizing astrology passages, identify the astrology register, attitude status, causation model, chronology, and textual risk. Do not use "astrology" as a naked tag. Distinguish natural celestial influence, judicial/divinatory astrology, astral magic, poetic astrology, Kabbalistic-astral correspondence, biblical cosmology, anti-astrology, and reception.
""",
    )
    append_once(
        DOCS / "PICO_TEXT_GAPS.md",
        "## Disputationes Primary Text Status Pass 010",
        """## Disputationes Primary Text Status Pass 010

- Status: `secondary_and_reception_rich_primary_text_still_needs_control`
- Reason: Akopyan, Vanden Broecke, Rabin, Rutkin, and related reviews are now ingested, but the project still needs a controlled standalone primary text / critical edition record for the *Disputationes adversus astrologiam divinatricem* and its posthumous publication history.
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
        ("page-pico-astrology", "essay", "Pico and Astrology", "artifacts/essays/pico_astrology_synthesis_draft.md", "DRAFT", "essay_pico_astrology_synthesis"),
    )
    conn.commit()
    refresh_catalog_and_manifest(conn)
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print("Study pass 010 complete.")


if __name__ == "__main__":
    main()
