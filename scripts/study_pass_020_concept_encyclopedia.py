"""Study pass 020: concept encyclopedia seed and Concepts website tab."""

from __future__ import annotations

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
CONCEPT_DIR = ROOT / "artifacts" / "concepts" / "encyclopedia"


CONCEPTS = [
    ("Neoplatonism", "The late antique and Renaissance philosophical tradition through which Pico reads hierarchy, procession, return, intellect, soul, symbol, and ascent.", ["Oration", "900 Conclusions", "Commento", "Heptaplus", "On Being and Unity"], ["Allen", "Howlett", "Copenhaver", "Black"]),
    ("Kabbalah", "The Jewish mystical and exegetical source field that Pico translates, Christianizes, and uses for theology, magic, and concord.", ["Oration", "900 Conclusions", "Apology", "Heptaplus"], ["Wirszubski", "Busi", "Copenhaver", "Farmer"]),
    ("Hermes Trismegistus", "The ancient-theology figure whose Hermetic authority helps Renaissance thinkers imagine a prisca sapientia before Greek philosophy.", ["900 Conclusions", "Oration"], ["Copenhaver", "Farmer", "Howlett"]),
    ("Being", "The metaphysical term at the center of Pico's effort to reconcile Plato, Aristotle, Aquinas, and Dionysian transcendence.", ["On Being and Unity", "900 Conclusions", "Oration"], ["Allen", "Edelheit", "Salas"]),
    ("Unity", "The one, unity, and the metaphysical convertibility problem that exposes Pico's correction of Ficino's Proclean Plato.", ["On Being and Unity", "900 Conclusions"], ["Allen", "Edelheit", "Salas"]),
    ("The One", "The Neoplatonic first principle whose relation to being marks the dispute between Ficinian-Proclean transcendence and Pico's Christian concord.", ["On Being and Unity", "900 Conclusions"], ["Allen", "Copenhaver", "Edelheit"]),
    ("Mind", "The intelligible level of reality, often called mens or intellectus, where Ideas, angelic mind, and metaphysical mediation become contested.", ["Commento", "900 Conclusions", "Heptaplus"], ["Allen", "Farmer", "Black"]),
    ("Soul", "The principle of life, motion, mediation, ascent, and embodiment in Pico's anthropology and cosmology.", ["Oration", "Commento", "900 Conclusions"], ["Allen", "Howlett", "Edelheit"]),
    ("World Soul", "A Ficinian and Platonic mediation concept that Pico can use, discipline, or displace through angelic/intellectual and Christian structures.", ["Commento", "900 Conclusions", "Heptaplus"], ["Allen", "Howlett"]),
    ("Ideas", "The divine or intelligible exemplars through which Pico thinks form, beauty, creation, and the Idea of Man.", ["Commento", "Oration", "Heptaplus"], ["Allen", "Edelheit"]),
    ("Idea of Man", "Allen's key term for Pico's anthropology, where the human being's indeterminacy and perfection become Christological in the Heptaplus.", ["Oration", "Heptaplus"], ["Allen", "Black"]),
    ("Dignity", "The famous but often mythologized concept in the Oration that must be read inside ascent, discipline, hierarchy, and the 900 Conclusions.", ["Oration"], ["Copenhaver", "Howlett"]),
    ("Free Will", "Pico's account of human self-formation, not as modern autonomy but as metaphysical potentiality within a created hierarchy.", ["Oration", "Apology", "Disputationes"], ["Copenhaver", "Allen", "Edelheit"]),
    ("Indeterminacy", "The condition of Adam as unfixed image and metaphysical potential, central to non-modern readings of the Oration.", ["Oration"], ["Allen", "Copenhaver"]),
    ("Ascent", "The movement from lower life through intellectual and angelic forms toward God, joining ethics, metaphysics, Kabbalah, and prayer.", ["Oration", "Heptaplus", "Commento"], ["Copenhaver", "Black", "Howlett"]),
    ("Angels", "Created intellectual beings and models of human ascent that connect Dionysius, Aquinas, Proclus, Kabbalah, and Arabic intellect theory.", ["Oration", "900 Conclusions", "Heptaplus"], ["Black", "Wirszubski", "Allen"]),
    ("Angelology", "The systematic study of angelic hierarchy, intellect, imitation, separate substances, and Kabbalistic angelic orders in Pico.", ["Oration", "900 Conclusions", "Heptaplus"], ["Black", "Wirszubski", "Farmer"]),
    ("Dionysius", "Pseudo-Dionysius as authority for hierarchy, apophasis, symbol, anagogy, and Christian Neoplatonic ascent.", ["Oration", "On Being and Unity", "Heptaplus"], ["Black", "Allen", "Edelheit"]),
    ("Anagogy", "The upward interpretive movement by which symbols, Scripture, and hierarchy lead the intellect toward God.", ["Heptaplus", "Oration"], ["Black", "Copenhaver"]),
    ("Apophasis", "Negative theology and the disciplined recognition that divine reality exceeds names, concepts, and ordinary predication.", ["On Being and Unity", "Heptaplus"], ["Allen", "Edelheit"]),
    ("Aquinas", "The scholastic authority through whom Pico disciplines being, unity, creation, names, angels, and Christian metaphysics.", ["On Being and Unity", "900 Conclusions"], ["Edelheit", "Salas"]),
    ("Aristotle", "The philosopher whose concord with Plato Pico repeatedly asserts, tests, and reconfigures across metaphysics and natural philosophy.", ["900 Conclusions", "On Being and Unity"], ["Howlett", "Edelheit", "Allen"]),
    ("Plato", "Pico's central ancient authority, read through Ficino, late Neoplatonism, scholastic correction, and the concord project.", ["Oration", "900 Conclusions", "On Being and Unity", "Commento"], ["Allen", "Howlett"]),
    ("Ficino", "Marsilio Ficino as translator, mentor, co-Platonist, love theorist, and target of Pico's correction.", ["Commento", "On Being and Unity", "Heptaplus"], ["Allen", "Jayne", "Pugliese"]),
    ("Concord", "Pico's practice of testing agreement among Plato, Aristotle, scholasticism, Kabbalah, magic, and theology without erasing difference.", ["900 Conclusions", "On Being and Unity", "Oration"], ["Howlett", "Farmer", "Edelheit"]),
    ("Syncretism", "The modern term often applied to Pico's source-combining project, useful only when tied to debate form, hierarchy, and evidence.", ["900 Conclusions"], ["Farmer", "Howlett"]),
    ("Prisca Theologia", "The ancient theology framework connecting Moses, Hermes, Zoroaster, Orpheus, Plato, and Christian truth.", ["Oration", "900 Conclusions"], ["Copenhaver", "Farmer"]),
    ("Magic", "The natural, angelic, Kabbalistic, and theological practice-field that made some of Pico's theses dangerous.", ["900 Conclusions", "Apology", "Oration"], ["Copenhaver", "Farmer", "Busi"]),
    ("Natural Magic", "The licit or contested use of hidden natural powers, correspondences, and celestial sympathies under philosophical discipline.", ["900 Conclusions", "Apology"], ["Copenhaver", "Farmer"]),
    ("Astral Magic", "The field where Ficinian celestial mediation, images, music, spiritus, and Pico's later astrology critique must be carefully separated.", ["Commento", "Disputationes", "900 Conclusions"], ["Rutkin", "Copenhaver", "Akopyan"]),
    ("Astrology", "The science, art, and divinatory practice Pico uses, limits, and attacks across his career.", ["Commento", "Disputationes"], ["Akopyan", "Rutkin", "Rabin"]),
    ("Disputationes", "Pico's late attack on divinatory astrology and a major textual-transmission problem in the posthumous corpus.", ["Disputationes"], ["Akopyan", "Vanden Broecke", "Farmer"]),
    ("Heptaplus", "Pico's sevenfold Genesis commentary and the central text for biblical hermeneutics, cosmic order, and post-crisis recoding.", ["Heptaplus"], ["Black", "Busi", "Wirszubski"]),
    ("Oration", "The speech prefacing the 900 Conclusions, often misread as a modern manifesto rather than an ascetic, mystical, and disputational program.", ["Oration"], ["Copenhaver", "Howlett"]),
    ("900 Conclusions", "Pico's massive thesis system and public debate machine, requiring cluster-level source and doctrine mapping.", ["900 Conclusions"], ["Farmer", "Copenhaver", "Busi"]),
    ("Apology", "Pico's defense of condemned theses and the key juridical-theological witness for his dangerous formulations.", ["Apology"], ["Copenhaver", "Farmer"]),
    ("Commento", "Pico's commentary on Benivieni's canzone, a love-metaphysics and anti-Ficinian text with a complex transmission history.", ["Commento"], ["Allen", "Jayne", "Pugliese"]),
    ("De amore", "Ficino's commentary/treatise on Plato's Symposium and the main comparator for Pico's Commento.", ["Commento"], ["Jayne", "Allen"]),
    ("Benivieni", "Poet, collaborator, translator, and mediator whose canzone occasions the Commento and whose later activity shapes Pico reception.", ["Commento", "Pater Noster Commentary"], ["Pugliese", "Jayne"]),
    ("Poetic Theology", "The use of myth, poetry, and veiled language as vehicles for metaphysical and theological doctrine.", ["Commento", "Oration"], ["Allen", "Howlett"]),
    ("Myth", "The symbolic narrative medium through which Pico interprets Venus, Love, Orpheus, Moses, and ancient theology.", ["Commento", "Heptaplus"], ["Allen", "Black"]),
    ("Venus", "The mythological and metaphysical figure through whom Ficino and Pico debate beauty, love, soul, and intelligible origin.", ["Commento"], ["Allen", "Jayne"]),
    ("Love", "A central philosophical, cosmological, and theological force in Ficino and Pico, requiring distinction among personal, cosmic, divine, and intellectual registers.", ["Commento", "Oration"], ["Jayne", "Allen"]),
    ("Beauty", "The intelligible and sensible radiance of form that connects love theory, metaphysics, and poetic theology.", ["Commento"], ["Allen", "Jayne"]),
    ("Orpheus", "Ancient poet-theologian whose mythic authority supports poetic theology and Pico's corrections of Ficinian mythography.", ["Commento", "900 Conclusions"], ["Allen", "Copenhaver"]),
    ("Eurydice", "The mythic figure through whom Pico's Commento sharpens death-to-imagination and ascent beyond lower cognition.", ["Commento"], ["Allen"]),
    ("Porus", "The resource figure in Symposium love mythology, central to Ficino-Pico debate over love's parentage and metaphysical status.", ["Commento"], ["Jayne", "Allen"]),
    ("Penia", "The poverty figure in Symposium love mythology, paired with Porus in arguments about desire, lack, and ascent.", ["Commento"], ["Jayne", "Allen"]),
    ("Moses", "The biblical sage and philosopher whose hidden wisdom grounds Pico's claims about Genesis, Kabbalah, and ancient theology.", ["Heptaplus", "Oration", "900 Conclusions"], ["Black", "Busi"]),
    ("Genesis", "The biblical text Pico reads as cosmology, anthropology, angelology, and hidden philosophy in the Heptaplus.", ["Heptaplus"], ["Black"]),
    ("Bereshit", "The Hebrew opening of Genesis and a concentrated locus for Pico's Kabbalistic and Mosaic hermeneutics.", ["Heptaplus"], ["Black", "Busi", "Wirszubski"]),
    ("Sabbath", "The scriptural and symbolic endpoint of creation, rest, jubilee, knowledge, and spiritual ascent in the Heptaplus.", ["Heptaplus"], ["Black"]),
    ("Jubilee", "A symbolic and Kabbalistic structure in the Heptaplus tied to sevenfold order, completion, and liberation.", ["Heptaplus"], ["Black", "Busi"]),
    ("Forty-Nine Gates", "The Kabbalistic structure of understanding that shapes Pico's final Heptaplus architecture.", ["Heptaplus"], ["Black", "Busi"]),
    ("Mithridates", "Flavius Mithridates, translator and mediator of Hebrew/Kabbalistic materials for Pico.", ["900 Conclusions", "Apology"], ["Wirszubski", "Busi"]),
    ("Hebrew", "The source language and symbolic medium through which Pico's Kabbalah, divine names, and philology must be controlled.", ["900 Conclusions", "Heptaplus"], ["Wirszubski", "Busi"]),
    ("Divine Names", "Names of God as theological, Kabbalistic, magical, and philological objects in Pico's claims.", ["900 Conclusions", "Apology"], ["Wirszubski", "Busi"]),
    ("Sefirot", "The Kabbalistic emanational structures Pico interprets and Christianizes in the 900 Conclusions and related works.", ["900 Conclusions"], ["Wirszubski", "Busi"]),
    ("Eyn-Sof", "The infinite divine principle in Kabbalah, requiring strict source control before use in Pico interpretation.", ["900 Conclusions"], ["Wirszubski"]),
    ("Abulafia", "The ecstatic Kabbalist whose materials enter Pico through translation and Christian transformation.", ["900 Conclusions"], ["Wirszubski", "Busi"]),
    ("Recanati", "A major Kabbalistic source behind Pico's theses, especially exegetical and angelic materials.", ["900 Conclusions", "Heptaplus"], ["Wirszubski", "Busi"]),
    ("Gematria", "Letter-number interpretation that supports some Kabbalistic and symbolic arguments in Pico's source field.", ["900 Conclusions"], ["Busi", "Wirszubski"]),
    ("Tetragrammaton", "The four-letter divine name and a key object of Kabbalistic, Christological, and magical interpretation.", ["900 Conclusions", "Apology"], ["Wirszubski", "Busi"]),
    ("Christology", "The doctrine of Christ as it shapes Pico's anthropology, Kabbalah, Heptaplus, and theological defenses.", ["Heptaplus", "Oration", "Apology"], ["Allen", "Copenhaver"]),
    ("Trinity", "The Christian doctrine Pico seeks to confirm, illuminate, or defend through metaphysics and Kabbalistic materials.", ["900 Conclusions", "Apology"], ["Copenhaver", "Wirszubski"]),
    ("Creation", "The metaphysical and biblical problem of how all things proceed from God and are intelligible through hierarchy and Scripture.", ["Heptaplus", "On Being and Unity"], ["Black", "Edelheit"]),
    ("Participation", "The metaphysical relation by which created beings receive limited forms of divine or intelligible reality.", ["On Being and Unity", "Heptaplus"], ["Edelheit", "Allen"]),
    ("Predication", "The logic of how names such as being, one, good, intellect, and angel apply differently across levels of reality.", ["On Being and Unity", "900 Conclusions"], ["Edelheit", "Allen"]),
    ("Transcendentals", "Being, unity, truth, and goodness as convertible or contested concepts in scholastic and Platonic metaphysics.", ["On Being and Unity"], ["Edelheit", "Salas"]),
    ("Act and Potency", "Aristotelian vocabulary crucial for reading Pico's anthropology of indeterminate potentiality and metaphysical ascent.", ["Oration", "On Being and Unity"], ["Edelheit", "Allen"]),
    ("Intellect", "The cognitive and ontological principle linking human knowing, angelic mind, Arabic philosophy, and felicity.", ["900 Conclusions", "Heptaplus"], ["Black", "Edelheit"]),
    ("Active Intellect", "The Arabic and Aristotelian concept central to debates over conjunction, felicity, and human perfection.", ["900 Conclusions", "Heptaplus"], ["Black", "Farmer"]),
    ("Felicity", "The goal of intellectual and spiritual life, debated through Aristotelian, Arabic, Christian, and biblical frameworks.", ["Heptaplus", "900 Conclusions"], ["Black", "Edelheit"]),
    ("Averroes", "Arabic commentator on Aristotle whose theories of intellect and felicity enter Pico's thesis and Heptaplus fields.", ["900 Conclusions", "Heptaplus"], ["Black", "Edelheit"]),
    ("Avicenna", "Arabic philosopher whose metaphysics, psychology, and intellect theory help shape Pico's source network.", ["900 Conclusions", "Heptaplus"], ["Black", "Edelheit"]),
    ("Al-Farabi", "Arabic philosopher relevant to political, intellectual, and felicity traditions behind Pico's source ecology.", ["900 Conclusions", "Heptaplus"], ["Black"]),
    ("Ibn Bajja", "Arabic philosopher tied to intellect, solitude, and felicity debates relevant to Pico's Heptaplus source field.", ["Heptaplus"], ["Black"]),
    ("Maimonides", "Jewish philosopher whose biblical interpretation and negative theology form part of Pico's Jewish philosophical environment.", ["Heptaplus", "900 Conclusions"], ["Black", "Busi"]),
    ("Gersonides", "Jewish philosopher and exegete relevant to Genesis, intellect, and biblical hermeneutics in Pico's Heptaplus context.", ["Heptaplus"], ["Black"]),
    ("Nahmanides", "Jewish biblical commentator and Kabbalistic source relevant to Genesis and Heptaplus interpretation.", ["Heptaplus"], ["Black", "Busi"]),
    ("Proclus", "Late Neoplatonist central to hierarchy, the One, henads, and the Ficino-Pico dispute over Plato.", ["On Being and Unity", "900 Conclusions"], ["Allen", "Farmer"]),
    ("Plotinus", "Founder of Neoplatonism whose One, Intellect, Soul, and ascent structures underlie Ficino and Pico.", ["Commento", "900 Conclusions"], ["Allen", "Howlett"]),
    ("Iamblichus", "Neoplatonist associated with theurgy, hierarchy, and ancient wisdom in the 900 Conclusions source field.", ["900 Conclusions"], ["Farmer", "Copenhaver"]),
    ("Porphyry", "Neoplatonic author and logical source relevant to predication, hierarchy, and ancient authority.", ["900 Conclusions"], ["Farmer", "Edelheit"]),
    ("Chaldean Oracles", "Ancient theological verses used in Renaissance Platonism and Pico's esoteric source environment.", ["900 Conclusions"], ["Farmer", "Copenhaver"]),
    ("Orphic Hymns", "Poetic-theological materials used in ancient theology, magic, and symbolic interpretation.", ["900 Conclusions", "Commento"], ["Copenhaver", "Farmer"]),
    ("Zoroaster", "Prisca-theologia authority and ancient wisdom figure in Pico's esoteric genealogy.", ["900 Conclusions", "Oration"], ["Copenhaver", "Farmer"]),
    ("Pythagoras", "Ancient philosopher of number, harmony, and symbolic wisdom in Pico's concordist source field.", ["900 Conclusions"], ["Farmer", "Howlett"]),
    ("Number", "Mathematical, symbolic, Kabbalistic, and Pythagorean principle in Pico's metaphysics and hermeneutics.", ["900 Conclusions", "Heptaplus"], ["Busi", "Farmer"]),
    ("Correspondence", "The relation linking levels of reality, symbols, names, stars, angels, and human ascent.", ["900 Conclusions", "Heptaplus", "Commento"], ["Busi", "Black"]),
    ("Microcosm", "The human being as little world and interpretive key to cosmic order.", ["Oration", "Heptaplus"], ["Allen", "Black"]),
    ("Macrocosm", "The great world whose structure is mirrored, interpreted, and perfected through human and Christological order.", ["Heptaplus", "Commento"], ["Black", "Allen"]),
    ("Hierarchy", "Ordered levels of being, knowledge, angels, worlds, and symbols across Pico's metaphysics and exegesis.", ["Oration", "Heptaplus"], ["Black", "Allen"]),
    ("Four Worlds", "Pico's ordering of angelic, celestial, elemental, and human worlds, especially in Heptaplus interpretation.", ["Heptaplus"], ["Black"]),
    ("Celestial Influence", "The disputed natural action of stars and heavens on lower bodies, love, medicine, and events.", ["Commento", "Disputationes"], ["Rutkin", "Akopyan"]),
    ("Spiritus", "The subtle mediating vehicle in Ficinian and Renaissance physiology, astral medicine, and love theory.", ["Commento", "Disputationes"], ["Rutkin", "Allen"]),
    ("Melancholy", "A Renaissance medical and philosophical condition linked to genius, Saturn, imagination, and Ficinian context.", ["Commento", "Disputationes"], ["Rutkin"]),
    ("Imagination", "A faculty involved in love, ascent, error, images, magic, and the boundary between intellect and body.", ["Commento", "Disputationes"], ["Allen", "Copenhaver"]),
    ("Heresy", "The juridical-theological danger field around the 900 Conclusions, Apology, magic, Kabbalah, and doctrinal language.", ["900 Conclusions", "Apology"], ["Copenhaver"]),
    ("Condemned Theses", "The thirteen theses judged suspect or dangerous in the Roman crisis and defended in the Apology.", ["900 Conclusions", "Apology"], ["Copenhaver", "Farmer"]),
    ("Roman Crisis", "The 1486-1487 failure of Pico's public disputation and the papal/juridical crisis that reshaped his work.", ["Oration", "900 Conclusions", "Apology"], ["Copenhaver", "Howlett"]),
    ("Savonarola", "Florentine reformer and late religious presence in Pico's final years and posthumous reception.", ["Letters", "Biography"], ["Howlett", "Edelheit"]),
    ("Gianfrancesco Pico", "Pico's nephew, editor, biographer, and possible mediator of posthumous textual and religious framing.", ["Biography", "Disputationes"], ["Farmer", "Dougherty"]),
    ("Textual Transmission", "The history of drafts, manuscripts, editions, translations, omissions, expurgations, and reception shaping Pico's corpus.", ["Commento", "Disputationes", "Opera"], ["Dougherty", "Pugliese", "Farmer"]),
    ("Translation", "The movement among Latin, Italian, Hebrew, Greek, English, and French that mediates Pico's sources and reception.", ["Commento", "900 Conclusions", "Heptaplus"], ["Dougherty", "Jayne", "Wirszubski"]),
    ("Reception", "The afterlife of Pico's works through editors, translators, readers, myths, national literatures, and modern scholarship.", ["Oration", "Commento", "Biography"], ["Copenhaver", "Jayne", "Dougherty"]),
]


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def load_seed_module():
    spec = importlib.util.spec_from_file_location("seed_research_artifacts", ROOT / "scripts" / "seed_research_artifacts.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load seed_research_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def concept_markdown(name: str, definition: str, works: list[str], scholars: list[str]) -> str:
    slug = slugify(name)
    work_text = ", ".join(f"*{w}*" for w in works)
    scholar_text = ", ".join(scholars)
    related = ", ".join(sorted({c[0] for c in CONCEPTS if c[0] != name and (set(c[1].lower().split()) & set(definition.lower().split()))})[:8])
    if not related:
        related = "To be assigned during close reading."
    return f"""# {name}

- Artifact ID: `encyclopedia_concept_{slug}`
- Type: concept encyclopedia entry
- Status: ENCYCLOPEDIA_SEED_EXPANSION_REQUIRED
- Target length: 2,000-6,000 words
- Current function: controlled encyclopedia seed for future expansion
- Primary Pico loci: {work_text}
- Guide scholars: {scholar_text}

## Definition

{definition} In PicoDB this concept is not a free-floating keyword. It is a controlled research object: every use should be attached to passages, works, source traditions, guide scholars, and a confidence level. The concept should therefore be read as both a term in Pico's intellectual vocabulary and a modern historiographical category that can clarify or distort the evidence.

## Place in Pico's Works

The concept belongs especially to {work_text}. Future close reading should identify where the term appears explicitly, where it operates implicitly, and where later scholarship imposes the label for analytic convenience. Pico's writings often move across genres: public disputation, commentary, apology, biblical exegesis, devotional writing, polemic, and poetic theology. A concept such as {name} may therefore change function as it moves from one genre to another.

In the *900 Conclusions*, concepts frequently appear as compressed theses whose meaning depends on cluster, source family, and debate function. In the *Oration*, the same concept may be rhetorical, ascetic, protreptic, or mystical. In the *Commento*, it may be embedded in mythography, love theory, or the dispute with Ficino. In the *Heptaplus*, it may be recoded as biblical hermeneutics and anagogical ascent. In *On Being and Unity*, concepts usually demand scholastic and Platonic precision.

## Scholarly Stakes

The initial guide scholars for this entry are {scholar_text}. Their role is methodological as well as informational. PicoDB should ask what each scholar teaches us to notice: source language, textual transmission, scholastic terminology, Kabbalistic mediation, reception history, edition status, genre, or philosophical architecture. No concept entry should rely on one label when the evidence requires a layered account.

The chief danger is anachronism. Modern readers often turn Pico into a symbol of Renaissance humanism, modern freedom, syncretic openness, or occult exoticism. The encyclopedia should resist that flattening. Each entry must distinguish Pico's own formulations, inherited source traditions, later editorial mediation, early modern reception, and modern scholarly reconstruction.

## Reading Questions

- Which passages in Pico explicitly name or enact {name}?
- Which source traditions control the concept: Platonic, Aristotelian, scholastic, Dionysian, Hermetic, Kabbalistic, magical, biblical, Arabic, Jewish philosophical, or humanist?
- Does Pico harmonize the traditions, subordinate one to another, or leave a productive tension unresolved?
- Which manuscripts, editions, translations, or reception witnesses affect the evidence?
- Which arguments in current scholarship disagree about this concept?
- What should a website reader learn from this entry before reading the primary text?

## Cross-References

Related concept entries: {related}.

## Expansion Plan

This seed should be expanded into a 2,000-6,000 word encyclopedia essay after the next close-reading pass. The full essay should include a concise definition, primary-text map, source genealogy, scholarly debate section, historiographical cautions, bibliography, and links to claims, section summaries, timeline events, and other concepts.
"""


def write_docs() -> None:
    CONCEPT_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for name, definition, works, scholars in CONCEPTS:
        slug = slugify(name)
        path = CONCEPT_DIR / f"{slug}.md"
        path.write_text(concept_markdown(name, definition, works, scholars), encoding="utf-8", newline="\n")
        entries.append({"id": f"encyclopedia_concept_{slug}", "title": name, "path": str(path.relative_to(ROOT)).replace("\\", "/"), "works": works, "scholars": scholars})
    index = ["# PicoDB Concept Encyclopedia Index", "", "- Artifact ID: `concept_encyclopedia_index_pass020`", "- Status: ACTIVE_INDEX", "", "## Entries", ""]
    for entry in entries:
        index.append(f"- [{entry['title']}](./encyclopedia/{Path(entry['path']).name})")
    (ROOT / "artifacts" / "concepts" / "concept_encyclopedia_index_pass020.md").write_text("\n".join(index) + "\n", encoding="utf-8", newline="\n")
    style = """# Concept Encyclopedia Style Guide

- Artifact ID: `concept_encyclopedia_style_guide_pass020`
- Status: ACTIVE

## Purpose

The concept encyclopedia turns PicoDB's reading artifacts into reference essays for the website. Every entry should eventually become a 2,000-6,000 word academic encyclopedia article that defines the concept, maps it across Pico's works, identifies source traditions, summarizes scholarly debates, and links to claims, summaries, and primary witnesses.

## Required Sections

1. Definition and scope.
2. Primary-text map across Pico's corpus.
3. Source genealogy.
4. Argument and function in each relevant work.
5. Scholarly positions and historiographical cautions.
6. Related concepts and cross-links.
7. Bibliography and local artifact links.
8. Open problems and next reading tasks.

## Style

Write in an academic but readable encyclopedia style. Avoid promotional prose, vague Renaissance generalities, and unmarked speculation. Prefer precise distinctions: direct source versus mediated source, Pico's term versus modern label, doctrine versus practice, primary text versus reception, and secure claim versus interpretive hypothesis.
"""
    (DOCS / "CONCEPT_ENCYCLOPEDIA_STYLE_GUIDE.md").write_text(style, encoding="utf-8", newline="\n")


def update_ontology() -> None:
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.19.0"
    payload["concept_encyclopedia_fields"] = [
        "definition",
        "primary_pico_loci",
        "source_genealogy",
        "guide_scholars",
        "scholarly_debates",
        "historiographical_cautions",
        "related_concepts",
        "website_entry_status",
        "expansion_target_words",
    ]
    payload["concept_encyclopedia_target_count"] = len(CONCEPTS)
    write_json(path, payload)


def db_rows(conn: sqlite3.Connection) -> None:
    now = now_utc()
    artifact_rows = []
    card_rows = []
    page_rows = []
    claim_rows = []
    for name, definition, works, scholars in CONCEPTS:
        slug = slugify(name)
        artifact_id = f"encyclopedia_concept_{slug}"
        rel_path = f"artifacts/concepts/encyclopedia/{slug}.md"
        artifact_rows.append((artifact_id, "concept_dossier", name, rel_path, None, name, "ENCYCLOPEDIA_SEED_EXPANSION_REQUIRED", "interpretive", artifact_id, now, now))
        card_rows.append((f"concept-entry-{slug}", "concept", name, ", ".join(works[:3]), definition[:220], "ENCYCLOPEDIA_SEED", artifact_id))
        page_rows.append((f"page-concept-entry-{slug}", "concept", name, rel_path, "ENCYCLOPEDIA_SEED", artifact_id))
        claim_rows.append((f"claim_concept_{slug}", artifact_id, None, f"{name} is a controlled encyclopedia concept for PicoDB and should be expanded through close reading of {', '.join(works)}.", "methodological", "concept encyclopedia", name, "Pass 020 concept seed", "medium", "DRAFT", "Generated seed; expand to 2,000-6,000 words."))
    artifact_rows.append(("concept_encyclopedia_index_pass020", "concept_dossier", "PicoDB Concept Encyclopedia Index", "artifacts/concepts/concept_encyclopedia_index_pass020.md", None, "Concept Encyclopedia", "ACTIVE_INDEX", "high", "concept_encyclopedia_index_pass020", now, now))
    conn.executemany(
        """
        INSERT OR REPLACE INTO reading_artifacts
        (id, artifact_type, title, path, document_id, target_entity, status, evidence_status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM reading_artifacts WHERE id = ?), ?), ?)
        """,
        artifact_rows,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id, entity_type, title, subtitle, summary, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        card_rows,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        page_rows,
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO claims
        (id, artifact_id, document_id, claim_text, claim_type, theme, target_entity, evidence_page, confidence, review_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        claim_rows,
    )


def refresh(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)


def main() -> None:
    write_docs()
    update_ontology()
    conn = sqlite3.connect(DB)
    db_rows(conn)
    conn.commit()
    refresh(conn)
    conn.close()
    print(f"Study pass 020 concept encyclopedia complete: {len(CONCEPTS)} entries.")


if __name__ == "__main__":
    main()
