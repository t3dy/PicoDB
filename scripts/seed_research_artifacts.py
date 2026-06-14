"""Seed the PicoDB research artifact system.

Adds a first-class markup/writing layer on top of the extracted corpus:
- artifact ontology and operating docs
- SQLite tables for claims, notes, timeline events, locations, map routes
- starter reading notes for biographies, work summaries, and scholar positions
- a Pico life timeline dataset and an interactive map dataset
- an expanded static viewer with Research, Timeline, and Map sections
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
TEMPLATES = ROOT / "templates"
ARTIFACTS = ROOT / "artifacts"
SITE = ROOT / "site"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")


def init_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS artifact_types (
            id TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            description TEXT NOT NULL,
            file_pattern TEXT,
            promotes_to TEXT
        );
        CREATE TABLE IF NOT EXISTS reading_artifacts (
            id TEXT PRIMARY KEY,
            artifact_type TEXT NOT NULL,
            title TEXT NOT NULL,
            path TEXT,
            document_id TEXT,
            target_entity TEXT,
            status TEXT NOT NULL DEFAULT 'DRAFT',
            evidence_status TEXT NOT NULL DEFAULT 'needs_review',
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        );
        CREATE TABLE IF NOT EXISTS claims (
            id TEXT PRIMARY KEY,
            artifact_id TEXT,
            document_id TEXT,
            claim_text TEXT NOT NULL,
            claim_type TEXT NOT NULL,
            theme TEXT,
            target_entity TEXT,
            evidence_page TEXT,
            confidence TEXT NOT NULL DEFAULT 'medium',
            review_status TEXT NOT NULL DEFAULT 'DRAFT',
            notes TEXT,
            FOREIGN KEY(artifact_id) REFERENCES reading_artifacts(id),
            FOREIGN KEY(document_id) REFERENCES documents(id)
        );
        CREATE TABLE IF NOT EXISTS website_cards (
            id TEXT PRIMARY KEY,
            entity_type TEXT NOT NULL,
            title TEXT NOT NULL,
            subtitle TEXT,
            summary TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'DRAFT',
            source_artifact_id TEXT
        );
        CREATE TABLE IF NOT EXISTS website_pages (
            id TEXT PRIMARY KEY,
            entity_type TEXT NOT NULL,
            title TEXT NOT NULL,
            markdown_path TEXT,
            status TEXT NOT NULL DEFAULT 'DRAFT',
            source_artifact_id TEXT
        );
        CREATE TABLE IF NOT EXISTS timeline_events (
            id TEXT PRIMARY KEY,
            start_date TEXT NOT NULL,
            end_date TEXT,
            date_label TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            location_id TEXT,
            category TEXT NOT NULL,
            evidence_status TEXT NOT NULL DEFAULT 'needs_review',
            source_note TEXT,
            importance INTEGER DEFAULT 2
        );
        CREATE TABLE IF NOT EXISTS locations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            modern_country TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            location_type TEXT NOT NULL,
            pico_role TEXT NOT NULL,
            evidence_status TEXT NOT NULL DEFAULT 'needs_review'
        );
        CREATE TABLE IF NOT EXISTS map_routes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            sequence_json TEXT NOT NULL,
            summary TEXT,
            evidence_status TEXT NOT NULL DEFAULT 'needs_review'
        );
        """
    )


ARTIFACT_TYPES = [
    ("source_packet", "Source Packet", "Smallest verified source unit: document id, page range, extracted passage summary, key names, and claim candidates.", "artifacts/source_packets/{document_id}/{section}.md", "claims"),
    ("section_summary", "Section Summary", "Exhaustive summary of a section/chapter/page range with claims, concepts, persons, and evidence anchors.", "artifacts/section_summaries/{document_id}/{section}.md", "website_pages"),
    ("claim_record", "Claim Record", "Atomic historical, textual, bibliographic, or interpretive assertion with evidence and review status.", "db.claims", "website_cards"),
    ("scholar_profile", "Scholar Profile", "Biography, corpus works, arguments, historiographical position, contribution to Pico/Renaissance/magic studies.", "artifacts/scholar_profiles/{scholar_id}.md", "website_pages"),
    ("pico_work_dossier", "Pico Work Dossier", "Aggregated notes on a Pico primary text, including structure, themes, debates, editions, and open problems.", "artifacts/pico_work_dossiers/{work_id}.md", "website_pages"),
    ("concept_dossier", "Concept Dossier", "Concept history and usage across Pico and scholarship, with debate map and related terms.", "artifacts/concepts/{concept_id}.md", "website_pages"),
    ("historiography_node", "Historiography Node", "Named debate or interpretive position with scholars, claims, tensions, and revisions.", "artifacts/historiography/{node_id}.md", "website_pages"),
    ("timeline_event", "Timeline Event", "Life, publication, controversy, travel, reception, or scholarship event with date/place/source note.", "db.timeline_events", "timeline"),
    ("location_record", "Location Record", "Geocoded place tied to Pico's life, education, travel, trouble, publication, or reception.", "db.locations", "map"),
    ("website_card", "Website Card", "Short browsable card for the public site.", "db.website_cards", "site"),
    ("website_page", "Website Page", "Long-form reviewed essay/page for the public site.", "artifacts/pages/{entity_id}.md", "site"),
]


def seed_artifact_types(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO artifact_types(id,label,description,file_pattern,promotes_to) VALUES (?,?,?,?,?)",
        ARTIFACT_TYPES,
    )


LOCATIONS = [
    ("mirandola", "Mirandola", "Italy", 44.8896, 11.0667, "birthplace_lordship", "Pico's family lordship and birthplace; later a site of civic memory and commemoration."),
    ("modena", "Modena", "Italy", 44.6471, 10.9252, "regional_center", "Este-region political and ecclesiastical context near Mirandola."),
    ("bologna", "Bologna", "Italy", 44.4949, 11.3426, "university_city", "Early legal/university studies; later remembered as part of Pico and Savonarola's overlapping educational world."),
    ("ferrara", "Ferrara", "Italy", 44.8381, 11.6198, "court_university_city", "Este court and educational setting where Pico and Savonarola are said to have crossed paths."),
    ("padua", "Padua", "Italy", 45.4064, 11.8768, "university_city", "Major Aristotelian university context for Pico's philosophical education."),
    ("pavia", "Pavia", "Italy", 45.1847, 9.1582, "university_city", "Northern Italian scholastic/university context relevant to Pico's legal and philosophical formation."),
    ("florence", "Florence", "Italy", 43.7696, 11.2558, "patronage_city", "Medici city, Ficinian/Platonic milieu, later Savonarolan context, and Pico's final residence."),
    ("fiesole_careggi", "Fiesole / Careggi", "Italy", 43.8060, 11.2931, "villa_milieu", "Florentine villa/intellectual setting associated with Ficino and Medici Platonism."),
    ("arezzo", "Arezzo", "Italy", 43.4633, 11.8796, "route_stop", "Tuscan route context; used here as a tentative travel node pending source confirmation."),
    ("perugia", "Perugia", "Italy", 43.1107, 12.3908, "study_city", "Central Italian study and travel context often associated with Pico's language and philosophical formation."),
    ("rome", "Rome", "Italy", 41.9028, 12.4964, "papal_city", "Site of Pico's planned disputation, papal scrutiny, condemnation of theses, and later absolution politics."),
    ("paris", "Paris", "France", 48.8566, 2.3522, "university_city", "Scholastic university center associated with Pico's northern studies and French intellectual ambit."),
    ("lyon", "Lyon", "France", 45.7640, 4.8357, "route_city", "Major France-Italy route node; included for map routing pending direct evidence."),
    ("grenoble", "Grenoble", "France", 45.1885, 5.7245, "route_city", "Alpine route node between France and Italy pending direct evidence."),
    ("aix_en_provence", "Aix-en-Provence", "France", 43.5297, 5.4474, "route_region", "Southern France/provençal travel context pending direct evidence."),
    ("vincennes", "Vincennes", "France", 48.8478, 2.4392, "detention_site", "Traditional location associated with Pico's detention after the papal case; verify exact imprisonment details in Copenhaver/trial literature."),
    ("san_marco_florence", "San Marco, Florence", "Italy", 43.7787, 11.2598, "religious_site", "Dominican convent/library connected with Savonarola, Pico's late religious circle, burial, and posthumous memory."),
    ("reggio_emilia", "Reggio Emilia", "Italy", 44.6983, 10.6312, "encounter_site", "Reported Dominican chapter/disputation context for a young Pico encountering Savonarola."),
]


TIMELINE = [
    ("1463-02-24", None, "24 February 1463", "Birth at Mirandola", "Giovanni Pico is born into the ruling Pico family of Mirandola, a small but politically connected lordship in northern Italy.", "mirandola", "life", "verified", "Basic chronology; verify against biographical chapter and DBI.", 5),
    ("1463", None, "1463", "Born into a princely household", "Pico's noble status shaped his education, ecclesiastical prospects, patronage access, and the unusual freedom with which he moved among universities and courts.", "mirandola", "family", "likely", "Howlett, Life and Works; Copenhaver, modern memory chapters.", 4),
    ("1460s", None, "1460s", "Family prepares ecclesiastical career", "Pico was groomed from childhood for a church career, a background later scholarship uses to complicate stories of sudden religious conversion.", "mirandola", "education", "likely", "Walden notes Pico was groomed for an ecclesiastical career from childhood.", 3),
    ("1470", None, "early 1470s", "Humanist education begins", "Pico receives the kind of elite grammatical, rhetorical, and classical education expected of a northern Italian noble prodigy.", "mirandola", "education", "placeholder", "Needs full source anchoring in life chapter.", 2),
    ("1477", None, "1477", "Studies canon law at Bologna", "As a teenager Pico is associated with Bologna, where legal study would have suited the ecclesiastical career planned for him.", "bologna", "education", "likely", "Walden places Pico and Savonarola at Bologna in the late 1470s.", 4),
    ("1478", None, "late 1470s", "Overlap with Savonarola's educational world", "Pico and Savonarola probably first occupy the same intellectual geography while studying in Bologna.", "bologna", "network", "likely", "Walden, p. 2.", 3),
    ("1479", None, "c. 1479", "Ferrara connection", "Pico's path intersects with Ferrara, an Este court/university context also important to Savonarola's formation.", "ferrara", "education", "likely", "Walden, p. 2.", 3),
    ("1480", None, "c. 1480", "Possible encounter with Savonarola at Reggio Emilia", "A definite encounter is reported around 1480 when the young Pico was invited to a Dominican chapter for a disputation by Savonarola.", "reggio_emilia", "network", "likely", "Walden, p. 2.", 4),
    ("1480", None, "c. 1480", "Pico hears Dominican disputation culture", "The Reggio Emilia episode places Pico in a scholastic-religious disputation setting before the Roman controversy of 1486-87.", "reggio_emilia", "education", "interpretive", "Inference from Walden's Reggio Emilia note.", 3),
    ("1480", None, "early 1480s", "Studies in Padua", "Pico's philosophical formation is associated with Padua, a key Aristotelian university environment.", "padua", "education", "likely", "Needs precise source anchor from Howlett/Copenhaver.", 4),
    ("1481", None, "early 1480s", "Aristotelian formation intensifies", "Pico's later concordist work depends on serious Aristotelian and scholastic training, not only Florentine Platonism.", "padua", "intellectual", "interpretive", "Howlett frames the need to re-evaluate Pico through Aristotelianism, Kabbalism, and Platonism.", 4),
    ("1482", None, "early 1480s", "Northern Italian university circuit", "Pico's movement among Bologna, Ferrara, Padua, and perhaps Pavia places him in a mobile university culture before his Florentine fame.", "pavia", "education", "placeholder", "Confirm exact Pavia chronology.", 2),
    ("1483", None, "c. 1483", "Contacts with Florence deepen", "Pico comes increasingly into the orbit of Florentine humanists, Medici patronage, and Ficinian Platonism.", "florence", "network", "likely", "Needs close reading of Allen/Howlett.", 4),
    ("1484", None, "1484", "Turns toward Hebrew and Kabbalistic sources", "Pico's mature project begins to draw on Jewish sources, Hebrew learning, and Kabbalistic materials that later become central to Pico studies.", "florence", "intellectual", "likely", "Howlett preface emphasizes later Pico studies' turn toward Kabbalism.", 5),
    ("1484", None, "mid-1480s", "Contacts with Jewish intellectuals", "Pico's Kabbalistic and Hebrew interests require mediators, translators, and interlocutors such as Flavius Mithridates and wider Jewish learned networks.", "florence", "network", "likely", "Copenhaver Magic and Dignity contents: Secrets and Codes, Counting on Flavius.", 4),
    ("1485", None, "1485", "Composes and gathers theses", "Pico begins assembling the enormous concordist program that will become the 900 Conclusions.", "florence", "writing", "likely", "Farmer/Copenhaver corpus to verify.", 5),
    ("1485", None, "1485", "Concord becomes a public project", "The project to reconcile philosophical and theological traditions moves from private study toward public disputation.", "florence", "intellectual", "interpretive", "Inferred from 900 Theses trajectory.", 4),
    ("1486", None, "1486", "Writes the Oration", "Pico writes the text later famous as the Oration on the Dignity of Man, originally tied to the proposed Roman disputation.", "florence", "writing", "likely", "Walden says in 1486 Pico wrote his Oration.", 5),
    ("1486", None, "1486", "Publishes or circulates the 900 Conclusions", "Pico issues the 900 Conclusions as the basis for a spectacular public philosophical-theological disputation.", "rome", "publication", "likely", "Walden and Farmer/Copenhaver corpus.", 5),
    ("1486", None, "late 1486", "Travels toward Rome for disputation", "The Roman disputation project brings Pico's learned ambition into direct contact with papal authority.", "rome", "travel", "likely", "General chronology; verify in Copenhaver On Trial.", 4),
    ("1486-12", None, "December 1486", "Roman disputation planned", "Pico's proposed debate over the 900 Conclusions is expected to gather learned opponents in Rome.", "rome", "controversy", "likely", "Copenhaver/Farmer to verify exact date.", 4),
    ("1487", None, "1487", "Disputation rejected", "The planned debate over the 900 Theses is stopped, initiating the crisis that makes Pico a case for heresy, freedom, and philosophy.", "rome", "controversy", "likely", "Walden, p. 2.", 5),
    ("1487", None, "1487", "Papal commission examines the theses", "A commission identifies problematic propositions among Pico's Conclusions, focusing attention on a subset later central to Copenhaver's trial analysis.", "rome", "controversy", "likely", "Copenhaver On Trial contents: Thirteen Conclusions.", 5),
    ("1487", None, "1487", "Thirteen conclusions become focal", "The controversy concentrates on thirteen condemned or suspect conclusions, turning Pico's universal concord into a juridical-theological problem.", "rome", "controversy", "likely", "Copenhaver On Trial chapter 1 contents.", 5),
    ("1487", None, "1487", "Pico writes the Apologia", "Pico produces a defense of his conclusions, sharpening the conflict with papal authority.", "rome", "writing", "likely", "Apologia file present; Copenhaver On Trial bibliography abbreviates Apo. Pico (1487).", 5),
    ("1487", None, "1487", "Flees toward France", "After the Roman project collapses, Pico flees toward France.", "rome", "travel", "likely", "Walden, p. 2.", 5),
    ("1487", None, "1487", "Imprisoned in France", "Pico is imprisoned in France as a heretic by papal servants after fleeing the failed Roman disputation.", "vincennes", "trouble", "likely", "Walden, p. 2; exact place needs verification.", 5),
    ("1487", None, "1487", "French episode becomes part of the Pico myth", "The flight and imprisonment help turn Pico from prodigy into a dramatic figure of intellectual danger and ecclesiastical risk.", "vincennes", "reception", "interpretive", "Portal synthesis from trial narrative.", 4),
    ("1488", None, "1488", "Lorenzo de' Medici secures safe harbor", "Lorenzo offers Pico safe harbor in Florence after the crisis.", "florence", "patronage", "likely", "Walden, p. 2.", 5),
    ("1488", None, "1488", "Pico returns to Florence", "Pico's post-crisis life becomes increasingly tied to Florence, Medici protection, and later Savonarolan religion.", "florence", "life", "likely", "Walden, p. 2.", 4),
    ("1488", None, "c. 1488", "Religious intensification after papal danger", "Pico's renewed religious seriousness is linked by some scholarship to his brush with church authority rather than simple Savonarolan discipleship.", "florence", "religion", "interpretive", "Walden, pp. 2-3.", 4),
    ("1489", None, "c. 1489", "Heptaplus", "Pico writes the Heptaplus, a sevenfold exposition of Genesis central to later debates over theology, Kabbalah, and posthumous editing.", "florence", "writing", "likely", "Copenhaver On Trial abbreviates Hep. Pico (c.1489); Walden p. 1 describes Heptaplus.", 5),
    ("1489", None, "c. 1489", "Genesis becomes a major interpretive field", "Pico's Heptaplus shifts attention from the famous Oration to biblical hermeneutics and creation theology.", "florence", "intellectual", "interpretive", "Walden and Crofton Black corpus.", 4),
    ("1490", None, "1490", "Savonarola returns to Florence", "Pico helps persuade Lorenzo to request Savonarola's presence at Florence.", "florence", "network", "likely", "Walden, p. 2.", 5),
    ("1490", None, "1490", "Pico begins attending Savonarola's sermons", "Pico begins attending Savonarola's sermons and remains close to him until death.", "florence", "religion", "likely", "Walden, p. 2.", 5),
    ("1490", None, "1490", "Florence becomes Pico's late religious-intellectual setting", "Pico's late life is shaped by a triangular field of Medici patronage, Ficinian Platonism, and Savonarolan reform.", "florence", "context", "interpretive", "Walden/Edelheit synthesis.", 4),
    ("1491", None, "c. 1491", "Disputes at San Marco", "Piero Crinito reports Pico and Savonarola engaging in regular intellectual disputes at San Marco's Greek library.", "san_marco_florence", "network", "likely", "Walden, p. 2.", 5),
    ("1491", None, "c. 1491", "San Marco becomes a thinking site", "San Marco functions as more than a devotional space: it is a library, disputation setting, and later burial/memory site.", "san_marco_florence", "location", "interpretive", "Inferred from Walden's San Marco note.", 4),
    ("1491", None, "1491", "Mutual respect with Savonarola", "Crinito's account frames the relationship as affectionate and intellectually serious, not merely master-disciple.", "san_marco_florence", "network", "likely", "Walden, p. 2.", 4),
    ("1492", None, "c. 1492", "Ficino and Pico diverge", "Scholarship notes a divergence between Ficino and Pico around this period, especially in relation to astrology and religious orientation.", "florence", "intellectual", "likely", "Walden note citing Weinstein and Edelheit.", 4),
    ("1492", None, "1492", "Death of Lorenzo de' Medici", "Lorenzo's death changes the political and patronage environment in Florence during Pico's final years.", "florence", "politics", "verified", "General chronology; connect to Florentine context in close reading.", 4),
    ("1492", None, "1492", "Medici protection weakens", "The death of Lorenzo alters the conditions under which Pico's post-trial life and Savonarola's influence unfold.", "florence", "politics", "interpretive", "Portal synthesis; needs source anchor.", 3),
    ("1493", None, "1493", "Compiles work against astrology with Savonarola's help", "Savonarola assists Pico in compiling his work against astrology.", "florence", "writing", "likely", "Walden, p. 3.", 5),
    ("1493", None, "1493", "Anti-astrology work links Pico and Savonarola", "The Disputationes adversus astrologiam divinatricem becomes a key text for assessing shared religious concern and differences from Ficino.", "florence", "intellectual", "interpretive", "Walden, pp. 2-3; Akopyan corpus.", 5),
    ("1493", None, "1493", "Pico considers Dominican life", "Pico dispenses with worldly wealth and considers joining the Dominican order, though he never takes vows.", "florence", "religion", "likely", "Walden, pp. 2-3.", 4),
    ("1493", None, "1493", "Late ascetic turn intensifies", "Pico's late religious posture becomes central to hagiographic and revisionist readings of his life.", "florence", "reception", "interpretive", "Copenhaver Magic and Dignity chapter 'Pico Sainted'; Walden.", 4),
    ("1494", None, "1494", "Disputationes near completion/publication context", "Pico's anti-astrology work belongs to his final year and later reception as an attack on judicial astrology.", "florence", "writing", "likely", "Walden note; Akopyan corpus.", 4),
    ("1494-11", None, "November 1494", "French invasion reaches Florence", "Charles VIII's Italian campaign creates the political crisis surrounding Florence in Pico's last days.", "florence", "politics", "verified", "General chronology; verify against Florence/Savonarola context.", 3),
    ("1494-11-17", None, "17 November 1494", "Death in Florence", "Pico dies in Florence at age thirty-one.", "florence", "life", "verified", "Basic chronology; verify exact date in life chapter.", 5),
    ("1494-11", None, "November 1494", "Burial at San Marco", "After his death, Pico is buried at San Marco in the Dominican habit at his request and by Savonarola's hands.", "san_marco_florence", "death", "likely", "Walden, p. 3.", 5),
    ("1494", None, "1494", "Pico's death fixes an unfinished career", "Pico's early death leaves his project fragmentary, making later scholarship especially dependent on editions, letters, and reception narratives.", "florence", "reception", "interpretive", "Howlett preface notes incomplete career and puzzles.", 4),
    ("1495", None, "1495", "Savonarola's Compendium appears", "Savonarola's Compendium of Revelations becomes a comparison point for claims about shared theological imagery and reform concerns.", "florence", "context", "likely", "Walden, p. 2.", 3),
    ("1496", None, "1496", "Posthumous editing begins shaping Pico", "Posthumous editorial work by family and Piagnoni circles becomes part of the problem of defining the authentic Pico.", "mirandola", "reception", "likely", "Walden note on posthumous tampering and Farmer.", 4),
    ("1498", None, "1498", "Savonarola executed", "Savonarola's execution changes the reception of Pico's late religious associations and the political-theological memory of Florence.", "florence", "reception", "verified", "General chronology; connect through Savonarola scholarship.", 3),
    ("1536", None, "1536", "Later anti-astrology print pairing", "A later Savonarola work on astrology is printed and cited as corroborated by Pico.", "florence", "reception", "likely", "Walden note 10.", 2),
    ("1942", None, "1942", "Cassirer frames Pico in Renaissance ideas", "Ernst Cassirer's article becomes one twentieth-century landmark in constructing Pico as a Renaissance philosophical figure.", None, "scholarship", "likely", "Cassirer article in corpus.", 3),
    ("1965", None, "1965", "English anthology canonizes the Oration package", "The widely used On the Dignity of Man / On Being and One / Heptaplus anthology helps shape Anglophone access to Pico.", None, "scholarship", "likely", "Heptaplus anthology in corpus; verify publication metadata.", 3),
    ("1989", None, "1989", "Wirszubski foregrounds Jewish mysticism", "Wirszubski and Kristeller's study becomes a major landmark for Pico's encounter with Jewish mysticism.", None, "scholarship", "likely", "Wirszubski/Kristeller corpus files.", 4),
    ("1998", None, "1998", "Farmer's 900 Theses project", "Stephen Farmer's Syncretism in the West provides a major modern edition/interpretive framework for the 900 Theses.", None, "scholarship", "likely", "Farmer corpus files.", 4),
    ("2017", None, "2017", "Allen collected studies", "Michael J. B. Allen's collected studies consolidate work on Ficino-Pico Platonism and the controversies between them.", None, "scholarship", "likely", "Allen Variorum file.", 3),
    ("2019", None, "2019", "Copenhaver's Magic and the Dignity of Man", "Copenhaver reframes the Oration through modern memory, dignity, magic, Kabbalah, and the history of Pico's afterlives.", None, "scholarship", "verified", "Copenhaver 2019 title/contents in corpus.", 5),
    ("2021", None, "2021", "Howlett's Re-evaluating Pico", "Howlett revisits Pico through Aristotelianism, Kabbalism, Platonism, and the changing field of Pico studies.", None, "scholarship", "verified", "Howlett title/preface in corpus.", 4),
    ("2022", None, "2022", "Copenhaver's Pico on Trial", "Copenhaver analyzes the heresy case, scholastic logic, freedom, and the thirteen conclusions.", None, "scholarship", "verified", "Copenhaver 2022 title/contents in corpus.", 5),
]


ROUTES = [
    ("student_circuit", "Student and University Circuit", ["mirandola", "bologna", "ferrara", "padua", "pavia", "florence"], "A working route for Pico's educational and intellectual formation across northern Italy and Florence."),
    ("roman_crisis_route", "Roman Crisis and Flight", ["florence", "rome", "vincennes", "florence"], "A schematic route for the 1486-88 public disputation, papal case, French detention, and return under Medici protection."),
    ("late_florence_route", "Late Florentine Religious World", ["florence", "fiesole_careggi", "san_marco_florence"], "The late-life triangle of Medici/Platonic, Florentine, and Dominican-Savonarolan settings."),
    ("italy_france_corridor", "Italy-France Corridor", ["florence", "arezzo", "perugia", "rome", "aix_en_provence", "grenoble", "lyon", "paris", "vincennes"], "A broad map corridor for travel and trouble between Italy and France; several waypoints remain provisional until close reading confirms exact itinerary."),
]


CARDS = [
    ("bio-pico", "biography", "Giovanni Pico della Mirandola", "1463-1494", "Prodigy, count, disputant, theologian-philosopher, and unstable emblem of Renaissance dignity. The portal treats Pico as a figure whose short life moved between university scholasticism, Florentine Platonism, Hebrew/Kabbalistic study, papal trouble, and late Savonarolan religion.", "DRAFT", "note_pico_bio_seed"),
    ("bio-copenhaver", "scholar", "Brian P. Copenhaver", "Renaissance philosophy, magic, Pico reception", "Copenhaver is a central modern interpreter for this portal because his corpus here ties Pico's Oration to magic, Kabbalah, modern memory, and the scholastic-juridical details of the Roman heresy case.", "DRAFT", "note_copenhaver_profile_seed"),
    ("bio-howlett", "scholar", "Sophia Howlett", "Aristotelianism, Kabbalism, Platonism", "Howlett re-enters Pico studies from Ficino studies and frames Pico as a contested site whose allure depends on the interplay of exceptionalism, Kabbalah, Aristotelianism, Platonism, and modern scholarly shifts away from an Oration-only Pico.", "DRAFT", "note_howlett_profile_seed"),
    ("work-oration", "work", "Oration on the Dignity of Man", "Roman disputation preface turned modern emblem", "The Oration must be treated both as a text attached to the failed 900 Theses debate and as a later object of modern memory, humanist canonization, and debate over dignity, freedom, magic, and Kabbalah.", "DRAFT", "note_oration_seed"),
    ("work-900", "work", "900 Conclusions", "Concordist disputation program", "The 900 Conclusions are the structural engine behind Pico's Roman crisis: a massive public program of philosophical and theological theses whose condemned subset produced the trial archive.", "DRAFT", "note_900_seed"),
    ("work-heptaplus", "work", "Heptaplus", "Genesis, creation, biblical hermeneutics", "Heptaplus shifts Pico away from a simplified secular dignity myth and toward biblical exegesis, creation theology, and the problem of posthumous textual transmission.", "DRAFT", "note_heptaplus_seed"),
    ("work-disputationes", "work", "Disputationes adversus astrologiam divinatricem", "Anti-astrology and late Savonarolan proximity", "The anti-astrology work belongs to Pico's late Florentine years and is central for mapping the divergence from Ficino and the shared terrain with Savonarola.", "DRAFT", "note_disputationes_seed"),
]


NOTES = {
    "artifacts/website_notes/biographies/pico_biography_seed.md": """# Giovanni Pico della Mirandola Biography Seed

Status: DRAFT  
Artifact type: website_page_seed  
Promotes to: biography page and timeline spine

## Working Thesis

Pico should not be introduced only as the author of a triumphant Renaissance manifesto about human dignity. The corpus already points toward a denser biography: noble child prepared for an ecclesiastical career, mobile university student, Aristotelian and scholastic reader, Florentine Platonist interlocutor, Hebrew/Kabbalistic experimenter, Roman disputant, papal suspect, French prisoner, Medici-protected returnee, and late religious figure close to Savonarola.

## Early Life and Education

- Born at Mirandola in 1463.
- His princely status matters: it enabled mobility, elite education, patronage access, and a public audacity not available to ordinary scholars.
- Walden notes that Pico was groomed for an ecclesiastical career from childhood, which complicates any simple story of a late Savonarolan conversion.
- Bologna and Ferrara belong to the early Pico-Savonarola contact zone; Padua and the northern university circuit belong to the Aristotelian/scholastic formation that Howlett and Copenhaver insist cannot be flattened into Platonism.

## Public Crisis

- In 1486 Pico writes the Oration and prepares the 900 Conclusions for public disputation.
- In 1487 the Roman project is stopped, the theses are examined, and Pico's defense becomes part of the heresy archive.
- Walden summarizes the crisis as rejection of the debate, flight to France, imprisonment as a heretic by papal servants, and Lorenzo de' Medici's offer of safe harbor in Florence.

## Late Florence

- Florence after the crisis becomes the key final setting: Medici protection, Ficinian memory, and Savonarolan reform all overlap.
- In 1490 Pico begins attending Savonarola's sermons.
- Around 1491 Crinito places Pico and Savonarola in regular disputes at San Marco's Greek library.
- In 1493 Savonarola assists Pico with the anti-astrology work.
- Pico dies in Florence in 1494 and is buried at San Marco in a Dominican habit.

## Website Treatment

The biography page should be organized as a map-linked life:

1. Mirandola: birth, family, ecclesiastical expectation.
2. Bologna/Ferrara/Padua/Pavia: university and scholastic formation.
3. Florence/Careggi: Ficino, Medici, Platonism, Hebrew/Kabbalah.
4. Rome: public disputation and papal danger.
5. France/Vincennes: flight and imprisonment.
6. Florence/San Marco: return, Savonarola, anti-astrology, death, burial.
""",
    "artifacts/website_notes/scholars/copenhaver_profile_seed.md": """# Brian P. Copenhaver Profile Seed

Status: DRAFT  
Artifact type: scholar_profile

## Corpus Basis

Primary corpus items:

- *Magic and the Dignity of Man: Pico della Mirandola and His Oration in Modern Memory* (2019)
- *Pico della Mirandola on Trial: Heresy, Freedom, and Philosophy* (2022)

## Contribution

Copenhaver is central to the portal because he pushes against an uncomplicated humanist Pico. In *Magic and the Dignity of Man*, the Oration is studied through its modern memory: dignity, magic, Kabbalah, and the history of how later readers made Pico useful. In *Pico on Trial*, the focus shifts to the scholastic, semantic, theological, and juridical detail of the Roman controversy.

## Historiographical Position

Working position for the portal: Copenhaver treats Pico as a philologically and philosophically difficult figure whose modern reputation has often outrun the actual textual and doctrinal situation. He is especially useful for resisting textbook Pico: the simple hero of modern freedom, dignity, and secular humanism.

## Notes for Website

- Scholar card should foreground Copenhaver as a revisionary interpreter of the Oration and trial.
- Longer page should separate the 2019 modern-memory argument from the 2022 trial/scholastic-logic argument.
- His work should anchor portal sections on magic, Kabbalah, dignity, heresy, and the thirteen conclusions.
""",
    "artifacts/website_notes/scholars/howlett_profile_seed.md": """# Sophia Howlett Profile Seed

Status: DRAFT  
Artifact type: scholar_profile

## Corpus Basis

Primary corpus item:

- *Re-evaluating Pico: Aristotelianism, Kabbalism, and Platonism in the Philosophy of Giovanni Pico della Mirandola* (2021)

## Contribution

Howlett's preface is already useful as a map of the field. She describes beginning from Ficino studies, initially seeing Pico as Ficino's disciple or satellite, then encountering a transformed Pico studies shaped by challenges to the Platonic Academy model and by a shift away from the Oration toward Kabbalism.

## Historiographical Position

Howlett frames Pico as a contested site. She emphasizes the allure of Pico's multiplicity: incomplete career, many sources, Kabbalistic puzzles, Aristotelian and Platonic strands, and a modern reception that makes him more widely recognizable than Ficino despite his brevity.

## Notes for Website

- Use Howlett for the section explaining why Pico cannot be reduced to Ficino.
- Use her preface to introduce the state of twenty-first-century Pico studies: Bori, Papio, Riva, Borghesi, Busi, Ciliberto, Idel, Copenhaver, Wirszubski, and Scholem as part of the Kabbalah turn.
""",
    "artifacts/website_notes/scholars/walden_savonarola_profile_seed.md": """# Justine Walden / Savonarola-Pico Article Seed

Status: DRAFT  
Artifact type: scholar_profile + thematic note

## Corpus Basis

Primary corpus item:

- “An Anatomy of Influence: Savonarola and Pico's Hidden Affinities” (RSA 2012)

## Argument

Walden argues against the easy opposition between a medieval Savonarola and a secular, Neoplatonic Pico. The article proposes shared theological concerns and mutual affinity, while cautioning against treating Pico as simply Savonarola's pupil.

## Useful Claims

- Pico and Savonarola probably overlapped in Bologna and Ferrara.
- A definite encounter is placed around 1480 at Reggio Emilia.
- Pico writes the Oration in 1486; after the 900 Theses crisis he flees to France and is imprisoned.
- Lorenzo offers safe harbor in Florence.
- Pico begins attending Savonarola's sermons in 1490.
- Crinito reports regular disputes at San Marco around 1491.
- Savonarola assists Pico with the anti-astrology work in 1493.
- Pico is buried at San Marco in a Dominican habit.

## Website Use

This article should support:

- Late-life biography.
- Savonarola relationship section.
- Timeline events for 1480, 1490, 1491, 1493, 1494.
- Map nodes for Reggio Emilia, Florence, and San Marco.
""",
    "artifacts/website_notes/works/oration_seed.md": """# Oration on the Dignity of Man Work Dossier Seed

Status: DRAFT  
Artifact type: pico_work_dossier

## Working Position

The Oration should be treated as a preface to a failed disputation and as a later modern-memory machine. It is not merely a freestanding manifesto.

## Reading Tasks

- Summarize Copenhaver's Oration sections paragraph by paragraph.
- Separate dignity/freedom reception from Pico's own disputational purpose.
- Track where magic and Kabbalah enter the Oration rather than assuming they are peripheral.
- Compare the Oration's ladder/ascent imagery with the Commentary, Heptaplus, and Savonarolan materials.

## Website Sections

- Textual occasion: 900 Conclusions and Roman debate.
- Human dignity: ancient, Christian, and modern meanings.
- Magic and Kabbalah: defended practices or theological signs?
- Reception: why the text became a modern emblem.
""",
    "artifacts/website_notes/works/conclusions_900_seed.md": """# 900 Conclusions Work Dossier Seed

Status: DRAFT  
Artifact type: pico_work_dossier

## Working Position

The 900 Conclusions are the architecture behind Pico's public project. The portal should use them as the organizing grid for concord, controversy, and the trial, rather than treating them as a mere appendix to the Oration.

## Reading Tasks

- Use Farmer as the primary structural guide.
- Use Copenhaver On Trial for the thirteen problematic conclusions.
- Mark each thesis by tradition, theme, source lineage, and controversy status where possible.
""",
    "artifacts/website_notes/works/heptaplus_seed.md": """# Heptaplus Work Dossier Seed

Status: DRAFT  
Artifact type: pico_work_dossier

## Working Position

Heptaplus should be a major portal section because it pulls Pico studies away from the secular Oration myth and toward Genesis, creation, biblical hermeneutics, angelology, and theological concord.

## Reading Tasks

- Summarize the Heptaplus edition in the corpus.
- Read Crofton Black on biblical hermeneutics.
- Track creation, sevenfold structure, Moses, Homer/catena aurea claims, and Kabbalistic resonances.
""",
    "artifacts/website_notes/works/disputationes_seed.md": """# Disputationes adversus astrologiam divinatricem Work Dossier Seed

Status: DRAFT  
Artifact type: pico_work_dossier

## Working Position

The Disputationes belong to late Pico and should be read beside Savonarola, Ficino, Akopyan, and broader Renaissance astrology debates. This is a major map between philosophy, theology, prophecy, and anti-divinatory polemic.

## Reading Tasks

- Use Akopyan's book and articles as the initial guide.
- Verify whether a standalone primary text is absent from the current corpus.
- Track divergence from Ficino and relation to Savonarolan prophecy.
""",
}


def seed_locations_timeline(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO locations(id,name,modern_country,latitude,longitude,location_type,pico_role,evidence_status) VALUES (?,?,?,?,?,?,?,?)",
        [(id_, name, country, lat, lon, typ, role, "needs_review" if "pending" in role or "tentative" in typ else "likely") for id_, name, country, lat, lon, typ, role in LOCATIONS],
    )
    conn.executemany(
        """
        INSERT OR REPLACE INTO timeline_events
        (id,start_date,end_date,date_label,title,summary,location_id,category,evidence_status,source_note,importance)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        [(f"tl_{i:03d}", *row) for i, row in enumerate(TIMELINE, start=1)],
    )
    conn.executemany(
        "INSERT OR REPLACE INTO map_routes(id,title,sequence_json,summary,evidence_status) VALUES (?,?,?,?,?)",
        [(id_, title, json.dumps(seq), summary, "needs_review" if "provisional" in summary or "pending" in summary else "likely") for id_, title, seq, summary in ROUTES],
    )


def seed_cards(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id,entity_type,title,subtitle,summary,status,source_artifact_id) VALUES (?,?,?,?,?,?,?)",
        CARDS,
    )


def seed_artifact_rows(conn: sqlite3.Connection) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute("DELETE FROM website_pages WHERE status='DRAFT'")
    for path, text in NOTES.items():
        full = ROOT / path
        write(full, text)
        art_id = "note_" + full.stem.replace("_seed", "") + "_seed"
        if "scholars" in path:
            art_type = "scholar_profile"
        elif "works" in path:
            art_type = "pico_work_dossier"
        elif "biographies" in path:
            art_type = "website_page"
        else:
            art_type = "source_packet"
        conn.execute(
            """
            INSERT OR REPLACE INTO reading_artifacts
            (id,artifact_type,title,path,document_id,target_entity,status,evidence_status,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (art_id, art_type, full.stem.replace("_", " ").title(), str(full), None, full.stem, "DRAFT", "needs_review", now, now),
        )
        entity_type = "scholar" if "scholars" in path else "work" if "works" in path else "biography"
        page_id = "page_" + full.stem
        conn.execute(
            "INSERT OR REPLACE INTO website_pages(id,entity_type,title,markdown_path,status,source_artifact_id) VALUES (?,?,?,?,?,?)",
            (page_id, entity_type, full.stem.replace("_", " ").title(), str(full), "DRAFT", art_id),
        )


def seed_claims(conn: sqlite3.Connection) -> None:
    claims = [
        ("claim_walden_001", "note_walden_savonarola_profile_seed", "An_Anatomy_of_Influence_Savonarola_and_P_pdf_2910b592", "Pico and Savonarola probably first overlapped in the late 1470s at Bologna and a few years later at Ferrara.", "historical", "biography", "Pico-Savonarola relationship", "pp. 2-3", "medium", "DRAFT", "Needs exact page verification against PDF pagination."),
        ("claim_walden_002", "note_walden_savonarola_profile_seed", "An_Anatomy_of_Influence_Savonarola_and_P_pdf_2910b592", "Pico began attending Savonarola's sermons in 1490 and remained close to him until Pico's death.", "historical", "religion", "Pico late Florence", "p. 2", "high", "DRAFT", ""),
        ("claim_walden_003", "note_walden_savonarola_profile_seed", "An_Anatomy_of_Influence_Savonarola_and_P_pdf_2910b592", "Savonarola assisted Pico in compiling the anti-astrology work in 1493.", "historical", "astrology", "Disputationes", "p. 3", "high", "DRAFT", ""),
        ("claim_howlett_001", "note_howlett_profile_seed", "Critical_Political_Theory_and_Radical_Practice_Sophia_Howlett_-_Re-evaluating_Pico__Aristotelian_pdf_3c6c4fa3", "Howlett presents recent Pico studies as moving away from an Oration-centered approach and toward Kabbalism and source multiplicity.", "historiographical", "historiography", "Pico Studies", "preface", "high", "DRAFT", ""),
        ("claim_copenhaver_001", "note_copenhaver_profile_seed", "Brian_P_Copenhaver_Magic_and_the_Dignity_of_Man__Pico_della_Mirandola_and_His_Oration_in_Modern__pdf_f7f272e1", "Copenhaver's 2019 book treats the Oration through modern memory, dignity, magic, Kabbalah, and reception history.", "historiographical", "historiography", "Oration reception", "contents", "high", "DRAFT", ""),
        ("claim_copenhaver_002", "note_copenhaver_profile_seed", "Brian_P_Copenhaver_Pico_della_Mirandola_on_Trial__Heresy_Freedom_and_Philosophy_libgen_li_pdf_753eb1fa", "Copenhaver's 2022 book focuses on the heresy case, scholastic semantics, theological logic, and the thirteen conclusions.", "historiographical", "heresy", "Pico trial", "contents", "high", "DRAFT", ""),
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO claims
        (id,artifact_id,document_id,claim_text,claim_type,theme,target_entity,evidence_page,confidence,review_status,notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        claims,
    )


def write_docs() -> None:
    ontology = {
        "id": "reading_artifact_ontology",
        "version": "0.2.0",
        "purpose": "Markup and writing ontology for turning systematic readings into website cards, pages, timelines, maps, and scholarly syntheses.",
        "artifact_types": [
            {
                "id": id_,
                "label": label,
                "description": desc,
                "file_pattern": pattern,
                "promotes_to": promotes,
            }
            for id_, label, desc, pattern, promotes in ARTIFACT_TYPES
        ],
        "claim_types": ["historical", "bibliographic", "textual", "interpretive", "historiographical", "philological", "geographical", "open_problem"],
        "evidence_statuses": ["verified", "likely", "interpretive", "needs_review", "placeholder", "contradicted"],
        "review_statuses": ["DRAFT", "SOURCE_ANCHORED", "REVIEWED", "PROMOTED", "RETIRED"],
        "promotion_rules": {
            "source_packet": "May produce claims and section summaries only after page anchors are recorded.",
            "section_summary": "May promote to website page when every claim has a source page and confidence.",
            "scholar_profile": "May promote when biography, corpus works, arguments, and historiographical position are separated.",
            "pico_work_dossier": "May promote when primary text structure, themes, editions, scholarship, and open problems are recorded.",
            "timeline_event": "May show publicly as DRAFT if evidence_status is likely or verified; provisional route events stay visually marked.",
            "location_record": "May show on map if coordinates are known; uncertain historical role must be labeled.",
        },
    }
    write_json(DATA / "reading_artifact_ontology.json", ontology)

    write(
        DOCS / "ARTIFACT_SYSTEM.md",
        """# Reading Artifact System

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
""",
    )

    write(
        TEMPLATES / "source_packet_template.md",
        """# Source Packet Template

- Artifact ID:
- Document ID:
- Source file:
- Page range:
- Section / chapter:
- Evidence status:
- Review status:

## Local Summary

## Extracted Claims

| Claim | Type | Theme | Evidence page | Confidence |
|---|---|---|---|---|

## Persons / Places / Works

## Terms and Concepts

## Candidate Promotions

- Timeline event:
- Location record:
- Scholar profile:
- Work dossier:
- Website card/page:
""",
    )

    write(
        TEMPLATES / "historiography_node_template.md",
        """# Historiography Node Template

- Node:
- Debate:
- Evidence status:
- Review status:

## Problem

## Positions

| Scholar | Position | Source | Evidence |
|---|---|---|---|

## Stakes

## Related Pico Texts

## Open Problems
""",
    )


def export_data(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    locations = [dict(r) for r in conn.execute("SELECT * FROM locations ORDER BY name")]
    timeline = [dict(r) for r in conn.execute("SELECT * FROM timeline_events ORDER BY start_date, id")]
    routes = [dict(r) for r in conn.execute("SELECT * FROM map_routes ORDER BY id")]
    for r in routes:
        r["sequence"] = json.loads(r.pop("sequence_json"))
    cards = [dict(r) for r in conn.execute("SELECT * FROM website_cards ORDER BY entity_type, title")]
    artifacts = [dict(r) for r in conn.execute("SELECT * FROM reading_artifacts ORDER BY artifact_type, title")]
    claims = [dict(r) for r in conn.execute("SELECT * FROM claims ORDER BY id")]
    write_json(DATA / "pico_life_timeline.json", timeline)
    write_json(DATA / "pico_locations.json", locations)
    write_json(DATA / "pico_map_routes.json", routes)
    write_json(DATA / "website_cards.json", cards)
    write_json(DATA / "reading_artifacts.json", artifacts)
    write_json(DATA / "seed_claims.json", claims)


def build_site(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    docs_count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    words = conn.execute("SELECT SUM(word_count) FROM documents").fetchone()[0]
    timeline = [dict(r) for r in conn.execute("SELECT * FROM timeline_events ORDER BY start_date, id")]
    locations = [dict(r) for r in conn.execute("SELECT * FROM locations ORDER BY name")]
    routes = [dict(r) for r in conn.execute("SELECT * FROM map_routes ORDER BY id")]
    cards = [dict(r) for r in conn.execute("SELECT * FROM website_cards ORDER BY entity_type, title")]
    artifacts = [dict(r) for r in conn.execute("SELECT * FROM reading_artifacts ORDER BY artifact_type, title")]
    claims = [dict(r) for r in conn.execute("SELECT * FROM claims ORDER BY id")]
    doc_rows = [dict(r) for r in conn.execute("SELECT id,title,document_type,page_count,word_count,themes_json,pico_works_json,markdown_path FROM documents ORDER BY title")]
    concept_artifacts = [
        a for a in artifacts
        if a["artifact_type"] == "concept_dossier" or a["id"].startswith("encyclopedia_concept_")
    ]

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PicoDB Knowledge Portal</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
:root {{ --bg:#111318; --panel:#181c24; --panel2:#202633; --text:#f2efe7; --muted:#b9b0a0; --gold:#d8b45a; --blue:#8fc7ff; --green:#6fb18a; --line:#343b4a; font-family: Inter, Segoe UI, Arial, sans-serif; }}
body {{ margin:0; background:var(--bg); color:var(--text); line-height:1.55; }}
header {{ padding:28px 36px 18px; border-bottom:1px solid var(--line); background:#151922; }}
h1 {{ margin:0 0 8px; font-size:30px; letter-spacing:0; }}
p {{ color:var(--muted); }}
main {{ padding:24px 36px 44px; }}
nav {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:16px; }}
button {{ background:var(--panel2); color:var(--text); border:1px solid var(--line); border-radius:6px; padding:8px 12px; cursor:pointer; }}
button.active {{ border-color:var(--gold); color:var(--gold); }}
.section {{ display:none; }}
.section.active {{ display:block; }}
.stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:18px 0 26px; }}
.stat,.card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; }}
.num {{ font-size:26px; color:var(--gold); font-weight:700; }}
.label,.small {{ color:var(--muted); font-size:13px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }}
h2 {{ margin-top:30px; color:var(--gold); font-size:20px; }}
h3 {{ margin:0 0 6px; }}
.pill {{ display:inline-block; margin:3px 5px 3px 0; padding:3px 8px; border-radius:999px; background:var(--panel2); color:var(--text); font-size:13px; border:1px solid var(--line); }}
input {{ width:100%; max-width:720px; box-sizing:border-box; background:#0d1016; color:var(--text); border:1px solid var(--line); border-radius:6px; padding:10px 12px; font-size:15px; }}
table {{ width:100%; border-collapse:collapse; margin-top:14px; font-size:14px; }}
th,td {{ border-bottom:1px solid var(--line); padding:9px; text-align:left; vertical-align:top; }}
th {{ color:var(--gold); background:#151922; position:sticky; top:0; }}
a {{ color:var(--blue); }}
#map {{ height:620px; border:1px solid var(--line); border-radius:8px; background:#0d1016; }}
.timeline {{ border-left:2px solid var(--line); margin-left:12px; padding-left:18px; }}
.event {{ margin:0 0 14px; padding:12px; background:var(--panel); border:1px solid var(--line); border-radius:8px; }}
.event strong {{ color:var(--gold); }}
.draft {{ color:var(--gold); }}
</style>
</head>
<body>
<header>
<h1>PicoDB Knowledge Portal</h1>
<p>Research environment for Pico's texts, scholarship, reading artifacts, timeline, and Italy-France intellectual geography.</p>
<nav>
<button class="active" onclick="showSection('overview', this)">Overview</button>
<button onclick="showSection('concepts', this)">Concepts</button>
<button onclick="showSection('research', this)">Research Artifacts</button>
<button onclick="showSection('timeline', this)">Timeline</button>
<button onclick="showSection('mapsec', this)">Map</button>
<button onclick="showSection('catalog', this)">Catalog</button>
</nav>
</header>
<main>
<section id="overview" class="section active">
<div class="stats">
<div class="stat"><div class="num">{docs_count}</div><div class="label">Documents</div></div>
<div class="stat"><div class="num">{words:,}</div><div class="label">Extracted words</div></div>
<div class="stat"><div class="num">{len(artifacts)}</div><div class="label">Reading artifacts</div></div>
<div class="stat"><div class="num">{len(timeline)}</div><div class="label">Timeline events</div></div>
<div class="stat"><div class="num">{len(locations)}</div><div class="label">Map locations</div></div>
</div>
<h2>Website Seeds</h2>
<div class="grid">
{''.join(card_html(c) for c in cards)}
</div>
</section>
<section id="concepts" class="section">
<h2>Concept Encyclopedia</h2>
<p>The concept encyclopedia gathers Pico's philosophical, theological, philological, magical, Kabbalistic, and historiographical vocabulary into reusable reference essays.</p>
<input id="conceptSearch" placeholder="Search concepts..." oninput="filterConcepts()">
<div class="grid" id="conceptGrid">
{''.join(concept_html(a) for a in concept_artifacts)}
</div>
</section>
<section id="research" class="section">
<h2>Artifact System</h2>
<p>The portal now tracks source packets, section summaries, claims, scholar profiles, Pico work dossiers, concept dossiers, historiography nodes, timeline events, map locations, and promoted website cards/pages.</p>
<div class="grid">
{''.join(artifact_html(a) for a in artifacts)}
</div>
<h2>Seed Claims</h2>
<table><thead><tr><th>Claim</th><th>Type</th><th>Theme</th><th>Evidence</th><th>Status</th></tr></thead><tbody>
{''.join(claim_html(c) for c in claims)}
</tbody></table>
</section>
<section id="timeline" class="section">
<h2>Pico Life and Reception Timeline</h2>
<p>This is a {len(timeline)}-entry working timeline. Items marked likely or interpretive are useful for writing but still need close source anchoring before final publication.</p>
<input id="timelineSearch" placeholder="Search timeline..." oninput="filterTimeline()">
<div class="timeline" id="timelineList">
{''.join(event_html(e) for e in timeline)}
</div>
</section>
<section id="mapsec" class="section">
<h2>Italy-France Pico Map</h2>
<p>Locations include birth, study, patronage, papal trouble, French detention, late Florence, and provisional route nodes. Provisional nodes are labeled in their popups.</p>
<div id="map"></div>
</section>
<section id="catalog" class="section">
<h2>Corpus Catalog</h2>
<input id="q" placeholder="Search visible catalog rows..." oninput="filterRows()">
<table id="catalogTable"><thead><tr><th>Title</th><th>Type</th><th>Pages</th><th>Words</th><th>Themes</th><th>Pico Works</th><th>Text</th></tr></thead><tbody>
{''.join(doc_html(d) for d in doc_rows)}
</tbody></table>
</section>
</main>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const locations = {json.dumps(locations, ensure_ascii=False)};
const routes = {json.dumps(routes, ensure_ascii=False)};
function showSection(id, btn) {{
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  if (id === 'mapsec') setTimeout(initMap, 50);
}}
function filterRows() {{
  const q = document.getElementById('q').value.toLowerCase();
  for (const tr of document.querySelectorAll('#catalogTable tbody tr')) tr.style.display = tr.innerText.toLowerCase().includes(q) ? '' : 'none';
}}
function filterTimeline() {{
  const q = document.getElementById('timelineSearch').value.toLowerCase();
  for (const el of document.querySelectorAll('#timelineList .event')) el.style.display = el.innerText.toLowerCase().includes(q) ? '' : 'none';
}}
function filterConcepts() {{
  const q = document.getElementById('conceptSearch').value.toLowerCase();
  for (const el of document.querySelectorAll('#conceptGrid .card')) el.style.display = el.innerText.toLowerCase().includes(q) ? '' : 'none';
}}
let map;
function initMap() {{
  if (map) {{ map.invalidateSize(); return; }}
  map = L.map('map').setView([45.0, 8.5], 5);
  L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 18, attribution: '&copy; OpenStreetMap' }}).addTo(map);
  const byId = Object.fromEntries(locations.map(l => [l.id, l]));
  for (const l of locations) {{
    L.circleMarker([l.latitude, l.longitude], {{ radius: 7, color: l.evidence_status === 'needs_review' ? '#d8b45a' : '#6fb18a', fillOpacity: 0.85 }})
      .addTo(map)
      .bindPopup(`<strong>${{l.name}}</strong><br>${{l.location_type}}<br>${{l.pico_role}}<br><em>${{l.evidence_status}}</em>`);
  }}
  for (const r of routes) {{
    const seq = JSON.parse(r.sequence_json || '[]').map(id => byId[id]).filter(Boolean);
    if (seq.length > 1) L.polyline(seq.map(l => [l.latitude, l.longitude]), {{ color:'#8fc7ff', weight:2, opacity:0.5 }}).addTo(map).bindPopup(`<strong>${{r.title}}</strong><br>${{r.summary || ''}}`);
  }}
}}
</script>
</body>
</html>"""
    write(SITE / "index.html", html)


def card_html(c):
    return f"<div class='card'><h3>{esc(c['title'])}</h3><div class='small'>{esc(c['entity_type'])} · {esc(c['subtitle'] or '')}</div><p>{esc(c['summary'])}</p><span class='pill'>{esc(c['status'])}</span></div>"


def artifact_html(a):
    if a["path"]:
        path = Path(a["path"])
        full_path = path if path.is_absolute() else ROOT / path
        rel = full_path.relative_to(ROOT).as_posix()
    else:
        rel = ""
    link = f"<a href='../{rel}'>{esc(rel)}</a>" if rel else ""
    return f"<div class='card'><h3>{esc(a['title'])}</h3><div class='small'>{esc(a['artifact_type'])} · {esc(a['status'])} · {esc(a['evidence_status'])}</div><p>{link}</p></div>"


def concept_html(a):
    if a["path"]:
        path = Path(a["path"])
        full_path = path if path.is_absolute() else ROOT / path
        rel = full_path.relative_to(ROOT).as_posix()
        link = f"<a href='../{rel}'>Open entry</a>"
    else:
        link = ""
    target = a.get("target_entity") or ""
    return f"<div class='card'><h3>{esc(a['title'])}</h3><div class='small'>{esc(target)} · {esc(a['status'])}</div><p>{link}</p></div>"


def claim_html(c):
    return f"<tr><td>{esc(c['claim_text'])}</td><td>{esc(c['claim_type'])}</td><td>{esc(c['theme'] or '')}</td><td>{esc(c['evidence_page'] or '')}</td><td>{esc(c['review_status'])}</td></tr>"


def event_html(e):
    return f"<div class='event'><strong>{esc(e['date_label'])}: {esc(e['title'])}</strong><div class='small'>{esc(e['category'])} · {esc(e['evidence_status'])}</div><p>{esc(e['summary'])}</p></div>"


def doc_html(d):
    themes = ", ".join(json.loads(d["themes_json"] or "[]"))
    works = ", ".join(json.loads(d["pico_works_json"] or "[]"))
    href = "../Markdown/" + Path(d["markdown_path"]).name
    return f"<tr><td>{esc(d['title'])}</td><td>{esc(d['document_type'])}</td><td>{d['page_count']}</td><td>{d['word_count']}</td><td>{esc(themes)}</td><td>{esc(works)}</td><td><a href='{href}'>Markdown</a></td></tr>"


def esc(value) -> str:
    import html

    return html.escape("" if value is None else str(value), quote=True)


def main() -> None:
    for folder in [DATA, DOCS, TEMPLATES, ARTIFACTS, SITE]:
        folder.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB)
    init_tables(conn)
    seed_artifact_types(conn)
    seed_locations_timeline(conn)
    seed_cards(conn)
    seed_artifact_rows(conn)
    seed_claims(conn)
    conn.commit()
    write_docs()
    export_data(conn)
    build_site(conn)
    conn.close()
    print("Seeded reading artifact system, timeline, map, notes, and site.")


if __name__ == "__main__":
    main()
