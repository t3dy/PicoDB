"""Bootstrap the Pico della Mirandola knowledge portal.

This script performs deterministic setup:
- converts root-level PDFs/EPUBs to Markdown files in Markdown/
- extracts basic metadata, page text, PDF table-of-contents entries, hashes
- builds db/pico.db with catalog, full_text, sections, ontology seeds, gaps
- generates JSON manifests and a static HTML viewer in site/

LLM-authored scholarship summaries are deliberately represented as pending
work items. The database stores full text and reading targets so later passes
can produce audited section-by-section summaries with provenance.
"""

from __future__ import annotations

import hashlib
import html
import io
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

import fitz
from bs4 import BeautifulSoup
from ebooklib import epub

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = ROOT / "Markdown"
DB_DIR = ROOT / "db"
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
SITE_DIR = ROOT / "site"
TEMPLATE_DIR = ROOT / "templates"
DB_PATH = DB_DIR / "pico.db"

SOURCE_EXTS = {".pdf", ".epub"}

PICO_WORK_PATTERNS = {
    "Oration on the Dignity of Man": [
        "oration on the dignity",
        "de hominis dignitate",
        "dignity of man",
    ],
    "900 Theses / Conclusiones": [
        "900 theses",
        "nongentae",
        "conclusiones",
        "conclusioni",
    ],
    "Apologia": ["apologia"],
    "Heptaplus": ["heptaplus"],
    "On Being and the One": ["being and one", "de ente et uno", "of being and unity", "pico being"],
    "Disputationes adversus astrologiam divinatricem": [
        "disputationes",
        "astrologiam divinatricem",
        "debating the stars",
    ],
    "Commento / Commentary on Benivieni's Canzone": [
        "canzone",
        "benivieni",
        "commento",
    ],
    "Letters": ["lettere", "letters"],
    "Poems": ["latin poems", "poems"],
}

THEME_PATTERNS = {
    "kabbalah": ["kabbal", "cabbal", "qabbal", "jewish mysticism", "sefir", "sefirot"],
    "magic": ["magic", "magia", "hermetic", "orphic", "natural magic", "theurgy"],
    "astrology": ["astrolog", "stars", "zodiac", "divination"],
    "platonism": ["platon", "ficino", "academy", "neoplaton"],
    "aristotelianism": ["aristotel", "scholastic", "thomist", "aquinas"],
    "human_dignity": ["dignity", "hominis dignitate", "human freedom", "freedom"],
    "concord": ["concord", "syncret", "peace", "harmony", "prisca"],
    "philology": ["philolog", "hebrew", "translation", "transmission", "language"],
    "theology": ["theolog", "christ", "pater noster", "creation", "genesis"],
    "historiography": ["yates", "copenhaver", "cassirer", "kristeller", "garin", "farmer"],
}

SCHOLAR_HINTS = [
    "Brian P. Copenhaver",
    "Chaim Wirszubski",
    "Paul Oskar Kristeller",
    "Michael J. B. Allen",
    "Amos Edelheit",
    "Ovanes Akopyan",
    "Stephen A. Farmer",
    "M. V. Dougherty",
    "Giulio Busi",
    "Raphael Ebgi",
    "Sophia Howlett",
    "Crofton Black",
    "Ernst Cassirer",
    "Quirinus Breen",
    "B. C. Novak",
    "Giacomo Corazzol",
    "Victor M. Salas",
    "Lesley Arthur",
    "Craig Truglia",
    "Scott Michael Girdner",
    "Jean-Marc Mandosio",
    "Anna Paola Toscano",
    "Paola Zambelli",
    "David Marsh",
    "David Rijser",
    "Francesco Lamanna",
    "Eva Del Soldato",
    "Pearl Kibre",
    "Sherry Roush",
    "Georgios Steiris",
]

MISSING_PICO_WORKS = [
    {
        "title": "Disputationes adversus astrologiam divinatricem",
        "status": "likely_secondary_only",
        "reason": "The corpus includes Akopyan on the Disputationes, but no obvious standalone primary-text file by Pico has been identified yet.",
    },
    {
        "title": "Commento sopra una canzone d'amore composta da Girolamo Benivieni",
        "status": "partial_or_uncertain",
        "reason": "The corpus has reviews and Benivieni materials; verify whether a complete primary text is present in the collected editions.",
    },
    {
        "title": "De imaginatione",
        "status": "not_identified",
        "reason": "Known Pico text not obvious from filenames; search within collected editions during close reading.",
    },
    {
        "title": "Disputationes against astrology manuscript/critical edition details",
        "status": "metadata_needed",
        "reason": "Catalog editions, translations, and manuscript witnesses as they appear in scholarship.",
    },
    {
        "title": "Complete correspondence corpus",
        "status": "partial",
        "reason": "A Lettere file is present; verify completeness and edition details.",
    },
]


def slugify(value: str, max_len: int = 120) -> str:
    value = value.replace("&", " and ")
    value = re.sub(r"[^\w\s.-]+", "", value, flags=re.UNICODE)
    value = re.sub(r"\s+", "_", value.strip())
    value = value.strip("._")
    return value[:max_len] or "document"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify_doc(path: Path, text_sample: str) -> tuple[str, list[str], list[str]]:
    haystack = f"{path.stem} {text_sample[:8000]}".lower()
    primary_hits = [
        work for work, needles in PICO_WORK_PATTERNS.items() if any(n in haystack for n in needles)
    ]
    themes = [theme for theme, needles in THEME_PATTERNS.items() if any(n in haystack for n in needles)]
    if any(x in haystack for x in ["review by", "review", "book review"]):
        doc_type = "review"
    elif "giovanni pico della mirandola" in haystack and any(
        x in haystack for x in ["heptaplus", "apologia", "lettere", "oration", "conclusiones", "conclusioni"]
    ):
        doc_type = "primary_or_edition"
    elif path.suffix.lower() == ".epub":
        doc_type = "book"
    elif len(text_sample) > 120_000:
        doc_type = "book"
    else:
        doc_type = "article"
    return doc_type, primary_hits, themes


def extract_pdf(path: Path) -> tuple[list[dict], list[dict], dict]:
    pages: list[dict] = []
    toc_rows: list[dict] = []
    metadata: dict = {}
    with fitz.open(path) as doc:
        metadata = dict(doc.metadata or {})
        for pno, page in enumerate(doc, start=1):
            text = page.get_text("text", sort=True)
            pages.append({"page": pno, "title": f"Page {pno}", "text": text})
        for level, title, page in doc.get_toc(simple=True):
            toc_rows.append({"level": level, "title": title.strip(), "page": page})
        metadata["page_count"] = doc.page_count
    return pages, toc_rows, metadata


def extract_epub(path: Path) -> tuple[list[dict], list[dict], dict]:
    book = epub.read_epub(str(path))
    pages: list[dict] = []
    toc_rows: list[dict] = []
    metadata = {
        "title": first_meta(book, "DC", "title"),
        "creator": first_meta(book, "DC", "creator"),
        "language": first_meta(book, "DC", "language"),
        "page_count": 0,
    }
    n = 0
    for item in book.get_items():
        if item.get_type() != 9:
            continue
        soup = BeautifulSoup(item.get_content(), "html.parser")
        title = soup.find(["h1", "h2", "title"])
        text = soup.get_text("\n")
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if not text:
            continue
        n += 1
        heading = title.get_text(" ", strip=True) if title else f"EPUB section {n}"
        pages.append({"page": n, "title": heading, "text": text})
        toc_rows.append({"level": 1, "title": heading, "page": n})
    metadata["page_count"] = n
    return pages, toc_rows, metadata


def first_meta(book, namespace: str, name: str) -> str:
    vals = book.get_metadata(namespace, name)
    if not vals:
        return ""
    return str(vals[0][0])


def markdown_for(path: Path, doc_id: str, doc_type: str, themes: list[str], works: list[str], pages: list[dict], meta: dict) -> str:
    frontmatter = {
        "id": doc_id,
        "source_file": path.name,
        "source_path": str(path.resolve()),
        "document_type": doc_type,
        "themes": themes,
        "pico_works_discussed": works,
        "conversion_method": "PyMuPDF text extraction" if path.suffix.lower() == ".pdf" else "ebooklib + BeautifulSoup text extraction",
        "converted_at": datetime.now().isoformat(timespec="seconds"),
        "review_status": "UNREVIEWED_FULL_TEXT",
    }
    if meta.get("title"):
        frontmatter["source_title"] = meta.get("title")
    if meta.get("author"):
        frontmatter["source_author"] = meta.get("author")
    if meta.get("creator"):
        frontmatter["source_creator"] = meta.get("creator")
    lines = ["---"]
    for key, value in frontmatter.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.extend(["---", "", f"# {path.stem}", ""])
    lines.append("> Deterministic full-text extraction. Page/section boundaries are retained for later scholarly summarization and citation checks.")
    lines.append("")
    for page in pages:
        text = page["text"].replace("\x00", "").strip()
        if not text:
            continue
        heading = f"## {html.escape(str(page['title']))}"
        if str(page["title"]).startswith("Page "):
            heading = f"## Page {page['page']}"
        lines.extend([heading, "", text, ""])
    return "\n".join(lines).strip() + "\n"


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            source_file TEXT NOT NULL,
            source_path TEXT NOT NULL,
            markdown_path TEXT,
            extension TEXT,
            sha256 TEXT,
            duplicate_of TEXT,
            document_type TEXT,
            themes_json TEXT,
            pico_works_json TEXT,
            page_count INTEGER,
            word_count INTEGER,
            extraction_status TEXT,
            metadata_json TEXT,
            source_method TEXT,
            review_status TEXT,
            created_at TEXT
        );
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            heading TEXT,
            text TEXT,
            word_count INTEGER,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        );
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,
            level INTEGER NOT NULL,
            title TEXT NOT NULL,
            start_page INTEGER,
            summary_status TEXT DEFAULT 'PENDING',
            summary TEXT,
            notes TEXT,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        );
        CREATE TABLE IF NOT EXISTS scholars (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            source_count INTEGER DEFAULT 0,
            biography_status TEXT DEFAULT 'PENDING_CORPUS_BASED_PROFILE',
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS ontology_terms (
            id TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            class TEXT NOT NULL,
            description TEXT,
            evidence_status TEXT DEFAULT 'seed'
        );
        CREATE TABLE IF NOT EXISTS reading_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT,
            task_type TEXT NOT NULL,
            target TEXT NOT NULL,
            priority INTEGER DEFAULT 2,
            status TEXT DEFAULT 'PENDING',
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS pico_text_gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            reason TEXT NOT NULL,
            evidence TEXT,
            updated_at TEXT
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS document_fts USING fts5(
            document_id UNINDEXED,
            title,
            source_file,
            text,
            themes
        );
        """
    )


def seed_ontology(conn: sqlite3.Connection) -> None:
    terms = [
        ("entity.work", "Work", "entity_class", "Primary text, edition, article, monograph, review, chapter, or manuscript witness."),
        ("entity.person", "Person", "entity_class", "Historical person, Pico interlocutor, modern scholar, editor, translator, reviewer."),
        ("entity.concept", "Concept", "entity_class", "Philosophical, theological, magical, kabbalistic, philological, or historiographical concept."),
        ("entity.argument", "Argument", "entity_class", "A source-specific claim, thesis, objection, or scholarly position."),
        ("entity.section", "Section", "entity_class", "A chapter, page range, bookmark, argumentative unit, or generated reading segment."),
        ("theme.kabbalah", "Kabbalah / Cabala / Qabbalah", "theme", "Jewish and Christian Kabbalah, Hebrew sources, sefirot, exegetical methods."),
        ("theme.magic", "Magic / Magia", "theme", "Natural, astral, ceremonial, Hermetic, Orphic, and debated categories of magic."),
        ("theme.astrology", "Astrology", "theme", "Astrological causation, divination, anti-astrological polemic, celestial influence."),
        ("theme.concord", "Concord / Syncretism", "theme", "Pico's concordist project, harmonization, prisca theologia, 900 theses."),
        ("theme.dignity", "Human Dignity and Freedom", "theme", "Modern memory and textual arguments around the Oration and human self-fashioning."),
        ("theme.scholarship", "Historiography of Pico Studies", "theme", "Cassirer, Kristeller, Wirszubski, Farmer, Copenhaver, and later debates."),
        ("relation.influences", "influences", "relationship", "One figure/text shapes another."),
        ("relation.disputes", "disputes", "relationship", "A scholar contests another scholar's reading."),
        ("relation.interprets", "interprets", "relationship", "A source interprets a Pico text, concept, or historical episode."),
        ("relation.translates", "translates/edits", "relationship", "A scholar, editor, or edition transmits a primary text."),
        ("status.verified", "Verified", "evidence_status", "Directly supported by corpus text or bibliographic metadata."),
        ("status.interpretive", "Interpretive", "evidence_status", "A scholarly judgment or generated synthesis needing citation anchors."),
        ("status.placeholder", "Placeholder", "evidence_status", "Known slot awaiting close reading."),
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO ontology_terms(id,label,class,description,evidence_status) VALUES (?,?,?,?,?)",
        [(term_id, label, cls, desc, "seed") for term_id, label, cls, desc in terms],
    )


def detect_scholars(source_name: str, text: str) -> list[str]:
    haystack = source_name + "\n" + text[:5000]
    found = []
    for name in SCHOLAR_HINTS:
        simple = name.replace(".", "")
        if name in haystack or simple in haystack:
            found.append(name)
    return sorted(set(found))


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def process_sources(conn: sqlite3.Connection) -> dict:
    MARKDOWN_DIR.mkdir(exist_ok=True)
    seen_hash: dict[str, str] = {}
    stats = Counter()
    scholar_counts = Counter()
    failures = []
    for path in sorted(p for p in ROOT.iterdir() if p.is_file() and p.suffix.lower() in SOURCE_EXTS):
        stats["sources"] += 1
        digest = sha256(path)
        ext = path.suffix.lower().lstrip(".")
        doc_id = f"{slugify(path.stem, max_len=96)}_{ext}_{digest[:8]}"
        markdown_path = MARKDOWN_DIR / f"{doc_id}.md"
        duplicate_of = seen_hash.get(digest)
        seen_hash.setdefault(digest, doc_id)
        try:
            if path.suffix.lower() == ".pdf":
                pages, toc_rows, meta = extract_pdf(path)
            else:
                pages, toc_rows, meta = extract_epub(path)
            full_text = "\n\n".join(p["text"] for p in pages)
            doc_type, works, themes = classify_doc(path, full_text)
            md = markdown_for(path, doc_id, doc_type, themes, works, pages, meta)
            markdown_path.write_text(md, encoding="utf-8", errors="replace")
            word_count = count_words(full_text)
            conn.execute(
                """
                INSERT OR REPLACE INTO documents
                (id,title,source_file,source_path,markdown_path,extension,sha256,duplicate_of,document_type,
                 themes_json,pico_works_json,page_count,word_count,extraction_status,metadata_json,source_method,review_status,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    doc_id,
                    meta.get("title") or path.stem,
                    path.name,
                    str(path.resolve()),
                    str(markdown_path.resolve()),
                    path.suffix.lower(),
                    digest,
                    duplicate_of,
                    doc_type,
                    json.dumps(themes, ensure_ascii=False),
                    json.dumps(works, ensure_ascii=False),
                    len(pages),
                    word_count,
                    "OK",
                    json.dumps(meta, ensure_ascii=False, default=str),
                    "deterministic_extraction",
                    "UNREVIEWED",
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
            conn.execute("DELETE FROM pages WHERE document_id=?", (doc_id,))
            conn.execute("DELETE FROM document_fts WHERE document_id=?", (doc_id,))
            conn.execute("DELETE FROM reading_tasks WHERE document_id=?", (doc_id,))
            conn.executemany(
                "INSERT INTO pages(document_id,page_number,heading,text,word_count) VALUES (?,?,?,?,?)",
                [(doc_id, p["page"], p["title"], p["text"], count_words(p["text"])) for p in pages],
            )
            conn.execute("DELETE FROM sections WHERE document_id=?", (doc_id,))
            if toc_rows:
                conn.executemany(
                    "INSERT INTO sections(document_id,level,title,start_page) VALUES (?,?,?,?)",
                    [(doc_id, r["level"], r["title"], r["page"]) for r in toc_rows],
                )
            else:
                # Fallback sections provide manageable reading units for article PDFs.
                for p in pages:
                    if p["page"] == 1 or (p["page"] - 1) % 10 == 0:
                        conn.execute(
                            "INSERT INTO sections(document_id,level,title,start_page,notes) VALUES (?,?,?,?,?)",
                            (doc_id, 1, f"Generated reading unit starting page {p['page']}", p["page"], "No PDF bookmarks found."),
                        )
            conn.execute(
                "INSERT INTO document_fts(document_id,title,source_file,text,themes) VALUES (?,?,?,?,?)",
                (doc_id, meta.get("title") or path.stem, path.name, full_text, " ".join(themes + works)),
            )
            for name in detect_scholars(path.name, full_text):
                scholar_counts[name] += 1
            for work in works:
                conn.execute(
                    "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
                    (doc_id, "pico_text_close_reading", work, 1, "Summarize every section and extract doctrinal claims."),
                )
            conn.execute(
                "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
                (doc_id, "document_section_summary", path.stem, 2, "Create exhaustive section-by-section summary with claims and citations."),
            )
            stats["converted"] += 1
            stats[f"type_{doc_type}"] += 1
            if duplicate_of:
                stats["duplicates"] += 1
            conn.commit()
            print(f"OK {path.name} -> {markdown_path.name}")
        except Exception as exc:
            failures.append({"source_file": path.name, "error": repr(exc)})
            stats["failed"] += 1
            print(f"FAIL {path.name}: {exc}")
    for name, n in scholar_counts.items():
        conn.execute(
            "INSERT OR REPLACE INTO scholars(id,name,source_count,notes) VALUES (?,?,?,?)",
            (slugify(name).lower(), name, n, "Seeded from filename/front-matter/full-text hints; biography pending corpus-based pass."),
        )
    conn.execute("DELETE FROM pico_text_gaps")
    conn.executemany(
        "INSERT INTO pico_text_gaps(title,status,reason,evidence,updated_at) VALUES (?,?,?,?,?)",
        [(g["title"], g["status"], g["reason"], "", datetime.now().isoformat(timespec="seconds")) for g in MISSING_PICO_WORKS],
    )
    conn.commit()
    return {"stats": dict(stats), "failures": failures}


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def generate_artifacts(conn: sqlite3.Connection, result: dict) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)
    TEMPLATE_DIR.mkdir(exist_ok=True)
    SITE_DIR.mkdir(exist_ok=True)

    docs = [
        dict(row)
        for row in conn.execute(
            "SELECT id,title,source_file,markdown_path,document_type,themes_json,pico_works_json,page_count,word_count,duplicate_of FROM documents ORDER BY title"
        )
    ]
    for d in docs:
        d["themes"] = json.loads(d.pop("themes_json") or "[]")
        d["pico_works_discussed"] = json.loads(d.pop("pico_works_json") or "[]")

    manifest = {
        "id": "pico_portal",
        "title": "Pico della Mirandola Knowledge Portal",
        "status": "initialized",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(ROOT.resolve()),
        "database": str(DB_PATH.resolve()),
        "markdown_folder": str(MARKDOWN_DIR.resolve()),
        "site_folder": str(SITE_DIR.resolve()),
        "corpus_counts": result["stats"],
        "pipeline": [
            "scripts/init_pico_portal.py",
            "Markdown/*.md full-text extraction files",
            "db/pico.db SQLite catalog + FTS5",
            "data/pico_manifest.json and data/pico_ontology.json",
            "site/index.html static viewer",
        ],
    }
    write_json(DATA_DIR / "pico_manifest.json", manifest)

    ontology = {
        "id": "pico_ontology",
        "version": "0.1.0",
        "purpose": "Seed ontology for systematic Pico reading, scholarship synthesis, and portal generation.",
        "entity_classes": [
            "work",
            "edition",
            "section",
            "argument",
            "claim",
            "concept",
            "person",
            "scholar",
            "source",
            "manuscript_witness",
            "language",
            "tradition",
            "controversy",
            "reception_event",
        ],
        "themes": list(THEME_PATTERNS.keys()),
        "relationship_types": [
            "interprets",
            "edits",
            "translates",
            "cites",
            "depends_on",
            "disputes",
            "revises",
            "influences",
            "borrows_from",
            "harmonizes_with",
            "condemns",
            "defends",
            "classifies_as_magic",
            "classifies_as_kabbalah",
        ],
        "evidence_statuses": ["verified", "likely", "interpretive", "placeholder", "needs_review"],
        "reading_questions": [
            "What Pico text, passage, or thesis is under discussion?",
            "Which intellectual traditions are being harmonized, subordinated, or contested?",
            "Does the source treat magic/Kabbalah as practice, rhetoric, philology, theology, or historiographical construct?",
            "What is the scholar's explicit argument and what prior interpretation is being revised?",
            "What primary-text evidence anchors the claim?",
            "What open problem or missing text does this source expose?",
        ],
    }
    write_json(DATA_DIR / "pico_ontology.json", ontology)
    write_json(DATA_DIR / "corpus_catalog.json", {"documents": docs})
    write_json(DATA_DIR / "conversion_report.json", result)

    (DOCS_DIR / "READING_SYSTEM.md").write_text(reading_system_md(), encoding="utf-8")
    (DOCS_DIR / "PIPELINE.md").write_text(pipeline_md(), encoding="utf-8")
    (DOCS_DIR / "DATABASE_SCHEMA.md").write_text(schema_md(), encoding="utf-8")
    (DOCS_DIR / "PICO_TEXT_GAPS.md").write_text(gaps_md(conn), encoding="utf-8")
    (TEMPLATE_DIR / "section_summary_template.md").write_text(section_template_md(), encoding="utf-8")
    (TEMPLATE_DIR / "scholar_profile_template.md").write_text(scholar_template_md(), encoding="utf-8")
    (TEMPLATE_DIR / "pico_work_dossier_template.md").write_text(work_template_md(), encoding="utf-8")
    build_site(conn)


def reading_system_md() -> str:
    return """# Pico Portal Reading System

## Purpose

This project treats the local corpus as the source of truth for a Pico della Mirandola knowledge portal. The first pass is deterministic: every document is converted into Markdown, cataloged in SQLite, indexed for full-text search, and split into page/bookmark reading units. Later LLM passes should produce exhaustive summaries only against these stored texts.

## Reading Passes

1. **Bibliographic audit**: verify title, author/editor/translator, date, publication venue, language, and whether the item is primary text, edition, article, review, or monograph.
2. **Structure pass**: confirm PDF bookmarks or create human-readable section/chapter units.
3. **Section summary pass**: summarize every section with claims, concepts, named figures, Pico works, and exact page anchors.
4. **Argument pass**: extract each scholar's thesis, opponent, method, evidence base, historiographical intervention, and limits.
5. **Pico work dossier pass**: aggregate every claim about each Pico text across the corpus.
6. **Gap pass**: update `pico_text_gaps` when a missing primary text, edition, manuscript, or debate appears.
7. **Portal pass**: promote reviewed cards/pages into the static site data.

## Provenance Rules

- Full text lives in `Markdown/` and `db/pages`.
- Generated summaries must identify document id, page range, and review status.
- Distinguish bibliographic fact, direct textual claim, scholarly interpretation, and portal synthesis.
- Do not collapse debates about magic, Kabbalah, concordism, or human dignity into a single consensus position.
"""


def pipeline_md() -> str:
    return """# Pipeline

Run from the project root:

```powershell
python scripts/init_pico_portal.py
```

Outputs:

- `Markdown/`: extracted full text for every root-level PDF/EPUB.
- `db/pico.db`: source catalog, page text, section units, scholars, ontology seeds, reading tasks, FTS5.
- `data/pico_manifest.json`: project manifest and paths.
- `data/pico_ontology.json`: evolving ontology seed.
- `data/corpus_catalog.json`: portable corpus catalog for website generation.
- `docs/`: operating notes for the research system.
- `templates/`: repeatable note-taking and profile templates.
- `site/index.html`: local database viewer.

The script is idempotent for document/page/section/catalog rows, but it appends reading tasks. If reading tasks need a clean rebuild, delete `db/pico.db` and rerun.
"""


def schema_md() -> str:
    return """# Database Schema

Core tables:

- `documents`: bibliographic and extraction metadata, source path, Markdown path, type, themes, Pico works, hash, duplicate link.
- `pages`: page- or EPUB-section-level full text.
- `sections`: PDF bookmark rows or generated reading units; summary fields are pending.
- `scholars`: seeded scholar names detected from filenames/full text; biographies pending.
- `ontology_terms`: entity classes, themes, relationship vocabulary, evidence statuses.
- `reading_tasks`: queue for section summaries, scholar profiles, Pico work dossiers, and gap audits.
- `pico_text_gaps`: living accounting of primary texts/editions still to locate or verify.
- `document_fts`: FTS5 index for source search.
"""


def gaps_md(conn: sqlite3.Connection) -> str:
    rows = conn.execute("SELECT title,status,reason FROM pico_text_gaps ORDER BY title").fetchall()
    lines = ["# Pico Text Gap Register", ""]
    for row in rows:
        lines.append(f"## {row['title']}")
        lines.append("")
        lines.append(f"- Status: `{row['status']}`")
        lines.append(f"- Reason: {row['reason']}")
        lines.append("")
    return "\n".join(lines)


def section_template_md() -> str:
    return """# Section Summary Template

- Document ID:
- Source file:
- Section title:
- Page range:
- Review status: DRAFT / REVIEWED

## Exhaustive Summary

## Claims

| Claim | Evidence page | Claim type | Confidence |
|---|---:|---|---|

## Pico Texts Discussed

## Concepts and Themes

## Named Persons and Scholars

## Historiographical Position

## Quotations to Verify

## Follow-Up Tasks
"""


def scholar_template_md() -> str:
    return """# Scholar Profile Template

- Scholar:
- Fields:
- Major Pico works:
- Corpus sources:
- Review status: DRAFT / REVIEWED

## Biography

## Contribution to Pico Studies

## Contribution to Renaissance / Magic / Kabbalah Studies

## Main Arguments

## Historiographical Position

## Debates and Disagreements

## Works in This Corpus

## Sources Needed
"""


def work_template_md() -> str:
    return """# Pico Work Dossier Template

- Pico work:
- Languages/editions in corpus:
- Missing editions/translations:
- Review status: DRAFT / REVIEWED

## Textual Overview

## Section-by-Section Summary

## Concepts

## Magic / Kabbalah / Astrology Relevance

## Reception and Modern Memory

## Scholarly Debates

## Open Problems
"""


def build_site(conn: sqlite3.Connection) -> None:
    docs = conn.execute("SELECT * FROM documents ORDER BY title").fetchall()
    themes = Counter()
    works = Counter()
    for d in docs:
        themes.update(json.loads(d["themes_json"] or "[]"))
        works.update(json.loads(d["pico_works_json"] or "[]"))
    scholars = conn.execute("SELECT * FROM scholars ORDER BY source_count DESC, name").fetchall()
    gaps = conn.execute("SELECT * FROM pico_text_gaps ORDER BY title").fetchall()
    rows = []
    for d in docs:
        t = ", ".join(json.loads(d["themes_json"] or "[]"))
        w = ", ".join(json.loads(d["pico_works_json"] or "[]"))
        rows.append(
            f"<tr><td>{html.escape(d['title'])}</td><td>{d['document_type']}</td><td>{d['page_count']}</td><td>{d['word_count']}</td><td>{html.escape(t)}</td><td>{html.escape(w)}</td><td><a href=\"{rel_link(d['markdown_path'])}\">Markdown</a></td></tr>"
        )
    html_text = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pico della Mirandola Knowledge Portal</title>
<style>
:root {{ --bg:#111318; --panel:#181c24; --panel2:#202633; --text:#f2efe7; --muted:#b9b0a0; --gold:#d8b45a; --red:#b8644f; --green:#6fb18a; --line:#343b4a; font-family: Inter, Segoe UI, Arial, sans-serif; }}
body {{ margin:0; background:var(--bg); color:var(--text); line-height:1.55; }}
header {{ padding:28px 36px 18px; border-bottom:1px solid var(--line); background:#151922; }}
h1 {{ margin:0 0 8px; font-size:30px; letter-spacing:0; }}
p {{ color:var(--muted); max-width:980px; }}
main {{ padding:24px 36px 44px; }}
.stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:18px 0 26px; }}
.stat {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:14px; }}
.num {{ font-size:26px; color:var(--gold); font-weight:700; }}
.label {{ color:var(--muted); font-size:13px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; }}
h2 {{ margin-top:30px; color:var(--gold); font-size:20px; }}
.pill {{ display:inline-block; margin:3px 5px 3px 0; padding:3px 8px; border-radius:999px; background:var(--panel2); color:var(--text); font-size:13px; border:1px solid var(--line); }}
input {{ width:100%; max-width:720px; box-sizing:border-box; background:#0d1016; color:var(--text); border:1px solid var(--line); border-radius:6px; padding:10px 12px; font-size:15px; }}
table {{ width:100%; border-collapse:collapse; margin-top:14px; font-size:14px; }}
th,td {{ border-bottom:1px solid var(--line); padding:9px; text-align:left; vertical-align:top; }}
th {{ color:var(--gold); background:#151922; position:sticky; top:0; }}
a {{ color:#8fc7ff; }}
.small {{ font-size:13px; color:var(--muted); }}
</style>
</head>
<body>
<header>
<h1>Pico della Mirandola Knowledge Portal</h1>
<p>Corpus viewer for extracted full text, source cataloging, theme triage, reading tasks, scholar profiles, and future section-by-section summaries. Full text is stored in <code>Markdown/</code> and <code>db/pico.db</code>.</p>
</header>
<main>
<section class="stats">
<div class="stat"><div class="num">{len(docs)}</div><div class="label">Documents cataloged</div></div>
<div class="stat"><div class="num">{sum(d['word_count'] or 0 for d in docs):,}</div><div class="label">Extracted words</div></div>
<div class="stat"><div class="num">{sum(d['page_count'] or 0 for d in docs):,}</div><div class="label">Pages / EPUB sections</div></div>
<div class="stat"><div class="num">{len(scholars)}</div><div class="label">Scholar seeds</div></div>
</section>
<h2>Themes</h2>
<div>{''.join(f'<span class="pill">{html.escape(k)} ({v})</span>' for k,v in themes.most_common())}</div>
<h2>Pico Texts Detected</h2>
<div>{''.join(f'<span class="pill">{html.escape(k)} ({v})</span>' for k,v in works.most_common())}</div>
<h2>Scholar Profile Queue</h2>
<div class="grid">{''.join(f'<div class="card"><strong>{html.escape(s["name"])}</strong><div class="small">{s["source_count"]} source hints. Biography pending corpus-based pass.</div></div>' for s in scholars[:24])}</div>
<h2>Primary Text Gap Register</h2>
<div class="grid">{''.join(f'<div class="card"><strong>{html.escape(g["title"])}</strong><div class="small">{html.escape(g["status"])}</div><p>{html.escape(g["reason"])}</p></div>' for g in gaps)}</div>
<h2>Corpus Catalog</h2>
<input id="q" placeholder="Search visible catalog rows..." oninput="filterRows()">
<table id="catalog">
<thead><tr><th>Title</th><th>Type</th><th>Pages</th><th>Words</th><th>Themes</th><th>Pico Works</th><th>Text</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</main>
<script>
function filterRows() {{
  const q = document.getElementById('q').value.toLowerCase();
  for (const tr of document.querySelectorAll('#catalog tbody tr')) {{
    tr.style.display = tr.innerText.toLowerCase().includes(q) ? '' : 'none';
  }}
}}
</script>
</body>
</html>"""
    (SITE_DIR / "index.html").write_text(html_text, encoding="utf-8")


def rel_link(abs_path: str | None) -> str:
    if not abs_path:
        return "#"
    try:
        return Path(abs_path).resolve().relative_to(SITE_DIR.resolve()).as_posix()
    except Exception:
        return "../" + Path(abs_path).resolve().relative_to(ROOT.resolve()).as_posix()


def main() -> None:
    for d in [MARKDOWN_DIR, DB_DIR, DATA_DIR, DOCS_DIR, SITE_DIR, TEMPLATE_DIR]:
        d.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    init_db(conn)
    seed_ontology(conn)
    result = process_sources(conn)
    generate_artifacts(conn, result)
    conn.close()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Database: {DB_PATH}")
    print(f"Viewer: {SITE_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
