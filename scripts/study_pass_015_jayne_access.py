"""Study pass 015: Jayne Commento translation access record.

This pass intentionally does not extract or store the full text of the
copyrighted/controlled digital loan. It creates a bibliographic control record
and a workflow for notes, collation, and short quotation anchors.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
MARKDOWN = ROOT / "Markdown"

JAYNE_DOC_ID = "Sears_Jayne_Commentary_on_a_Canzone_of_Benivieni_1984_restricted_ia"
JAYNE_URL = "https://archive.org/details/commentaryoncanz0019pico"


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def stable_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def ingest_stub(conn: sqlite3.Connection) -> None:
    MARKDOWN.mkdir(exist_ok=True)
    md_path = MARKDOWN / f"{JAYNE_DOC_ID}.md"
    md = f"""---
id: "{JAYNE_DOC_ID}"
source_file: "Internet Archive controlled digital loan"
source_path: "{JAYNE_URL}"
document_type: "restricted_modern_translation_witness"
themes: ["Commento", "Platonic love", "modern English translation", "Sears Jayne", "Benivieni"]
pico_works_discussed: ["Commento sopra una canzone d'amore"]
conversion_method: "bibliographic/access stub only; no transcript extracted"
converted_at: "{now_utc()}"
review_status: "RESTRICTED_ACCESS_NO_FULL_TEXT"
source_url: "{JAYNE_URL}"
---

# Commentary on a Canzone of Benivieni

Sears Jayne's 1984 English translation is available to consult through Internet Archive controlled digital lending at {JAYNE_URL}. PicoDB records it as a restricted modern translation witness. Do not use this file as a transcript.

## Use Protocol

- Read in the Internet Archive borrower interface or another lawful copy.
- Record page-level summaries in artifacts rather than full-text transcription.
- Quote only short, necessary passages and always include page anchors.
- Collate translation choices against the controlled Italian TEI and the Stanley reception witness.
- Mark each note as `summary`, `translation_choice`, `terminology`, `source_note`, or `collation_problem`.

## Collation Targets

- Book I: being modes, God, mind, soul, angelic/intellectual hierarchy, Dionysius, Plotinus, Avicenna.
- Book II: love, beauty, desire, celestial causality, Ficino agreement/correction, natural and poetic astrology.
- Book III: felicity, ascent, return, Christian theological controls.
- Commento particulare: stanza-level interpretation, poetic theology, secrecy, Kabbalah/biblical hints.
"""
    md_path.write_text(md, encoding="utf-8", newline="\n")
    metadata = {
        "title": "Commentary on a Canzone of Benivieni",
        "author": "Giovanni Pico della Mirandola",
        "translator_editor": "Sears Jayne",
        "publication_year": "1984",
        "publisher": "Peter Lang",
        "source_url": JAYNE_URL,
        "access_mode": "Internet Archive controlled digital lending / printdisabled item",
        "rights_protocol": "No full-text extraction or repository transcript; use page-level notes and short quotation anchors only.",
    }
    conn.execute(
        """
        INSERT OR REPLACE INTO documents
        (id,title,source_file,source_path,markdown_path,extension,sha256,duplicate_of,document_type,
         themes_json,pico_works_json,page_count,word_count,extraction_status,metadata_json,source_method,review_status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            JAYNE_DOC_ID,
            metadata["title"],
            "Internet Archive controlled digital loan",
            JAYNE_URL,
            str(md_path.resolve()),
            ".remote",
            stable_sha(json.dumps(metadata, sort_keys=True)),
            None,
            "restricted_modern_translation_witness",
            json.dumps(["Commento", "Platonic love", "modern English translation", "Sears Jayne", "Benivieni"]),
            json.dumps(["Commento sopra una canzone d'amore"]),
            0,
            0,
            "BIBLIOGRAPHIC_STUB_ONLY",
            json.dumps(metadata, ensure_ascii=False),
            "restricted_ia_bibliographic_record",
            "RESTRICTED_ACCESS_NO_FULL_TEXT",
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    for table in ["pages", "sections", "document_fts", "reading_tasks"]:
        conn.execute(f"DELETE FROM {table} WHERE document_id=?", (JAYNE_DOC_ID,))
    conn.execute(
        "INSERT INTO document_fts(document_id,title,source_file,text,themes) VALUES (?,?,?,?,?)",
        (
            JAYNE_DOC_ID,
            metadata["title"],
            "Internet Archive controlled digital loan",
            "Sears Jayne 1984 Commentary on a Canzone of Benivieni restricted modern English translation witness for Pico Commento",
            "Commento Sears Jayne modern English translation collation",
        ),
    )
    tasks = [
        ("restricted_translation_note_taking", "Jayne borrower notes", 1, "Create page-level summaries and short quotation anchors only; do not transcribe the full text."),
        ("translation_collation", "Jayne versus Italian TEI", 1, "Track translation choices for intellect, mind, angelic nature, beauty, love, desire, return, and felicity."),
        ("translation_collation", "Jayne versus Stanley", 2, "Compare modern scholarly English with Stanley's early modern reception vocabulary."),
    ]
    conn.executemany(
        "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
        [(JAYNE_DOC_ID, *task) for task in tasks],
    )


def write_artifacts() -> None:
    write(
        "artifacts/source_packets/jayne_commento_translation_access_pass015.md",
        """# Source Packet: Sears Jayne Commento Translation Access

- Artifact ID: `source_jayne_commento_translation_access_pass015`
- Type: source packet
- Document ID: `Sears_Jayne_Commentary_on_a_Canzone_of_Benivieni_1984_restricted_ia`
- Status: RESTRICTED_MODERN_TRANSLATION_WITNESS
- Evidence status: verified access lead

## Access

Sears Jayne's *Commentary on a Canzone of Benivieni* is available through Internet Archive controlled digital lending at `https://archive.org/details/commentaryoncanz0019pico`. PicoDB records this as a restricted modern translation witness. It is not a repository transcript and should not be converted into one from the borrowed reader.

## Research Use

Use Jayne for modern English terminology, translation choices, and scholarly apparatus. Notes should be page-level summaries, collation observations, and short quotation anchors. The controlling full text remains the Biblioteca Italiana Italian TEI. Stanley remains the early modern reception witness.

## Note Template

```markdown
### Jayne Note: p. [page]

- Passage/section:
- Summary:
- Translation choice:
- Italian TEI comparison:
- Stanley comparison:
- Source/apparatus note:
- Short quotation, if necessary:
- Follow-up:
```
""",
    )
    write(
        "artifacts/concepts/commento_translation_collation_protocol_pass015.md",
        """# Concept Dossier: Commento Translation Collation Protocol

- Artifact ID: `concept_commento_translation_collation_protocol_pass015`
- Type: concept dossier
- Status: WORKFLOW
- Evidence status: source-governed

## Witness Roles

- Italian TEI: controlling primary text for full-text summaries.
- Stanley 1651/Gardner 1914: early modern English reception witness.
- Jayne 1984: modern scholarly English translation witness under restricted access.

## Required Collation Fields

Every Jayne note should record section, page, Italian phrase or concept, Jayne rendering, Stanley rendering where applicable, doctrinal stakes, and whether the translation affects one of the portal's major problem fields: Ficino dispute, love doctrine, beauty doctrine, angelic/intellectual hierarchy, celestial causality, poetic theology, Kabbalah/biblical secrecy, or Christian theological correction.
""",
    )


def update_docs_and_ontology() -> None:
    append_once(
        DOCS / "PICO_TEXT_GAPS.md",
        "## Jayne Translation Pass 015 Access Update",
        """## Jayne Translation Pass 015 Access Update

- `Sears Jayne, Commentary on a Canzone of Benivieni`: `restricted_modern_translation_witness`; accessible through Internet Archive controlled digital lending, but no full transcript should be extracted into the repository. Use page-level notes, short quotation anchors, and collation observations.
""",
    )
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.14.0"
    payload["restricted_translation_note_fields"] = [
        "witness",
        "page",
        "commento_section",
        "summary",
        "translation_choice",
        "italian_tei_anchor",
        "stanley_comparison",
        "doctrinal_stakes",
        "short_quote_if_needed",
        "rights_note",
    ]
    payload["corpus_control_rules"] = sorted(set(payload.get("corpus_control_rules", []) + [
        "Controlled digital loans and copyrighted modern translations must be represented as bibliographic/access stubs plus notes, not as repository transcripts.",
        "Restricted translation witnesses can guide collation and terminology, but the controlling full text must remain a lawfully stored primary-text witness.",
    ]))
    write_json(path, payload)


def db_rows(conn: sqlite3.Connection) -> None:
    now = now_utc()
    artifacts = [
        (
            "source_jayne_commento_translation_access_pass015",
            "source_packet",
            "Sears Jayne Commento Translation Access",
            "artifacts/source_packets/jayne_commento_translation_access_pass015.md",
            JAYNE_DOC_ID,
            "Commento",
            "RESTRICTED_MODERN_TRANSLATION_WITNESS",
            "verified_access_lead",
        ),
        (
            "concept_commento_translation_collation_protocol_pass015",
            "concept_dossier",
            "Commento Translation Collation Protocol",
            "artifacts/concepts/commento_translation_collation_protocol_pass015.md",
            JAYNE_DOC_ID,
            "Commento translation collation",
            "WORKFLOW",
            "source_governed",
        ),
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
        (
            "claim_jayne_015_001",
            "source_jayne_commento_translation_access_pass015",
            JAYNE_DOC_ID,
            "Sears Jayne's 1984 English translation of Pico's Commento is available as a restricted Internet Archive controlled digital loan and should be used through page-level notes rather than repository transcription.",
            "bibliographic",
            "Commento",
            "Jayne translation",
            "IA access record",
            "high",
            "DRAFT",
            "Pass 015.",
        ),
        (
            "claim_jayne_015_002",
            "concept_commento_translation_collation_protocol_pass015",
            JAYNE_DOC_ID,
            "Jayne should be collated against the Italian TEI and Stanley to track modern scholarly terminology for love, beauty, mind, angelic hierarchy, and ascent.",
            "methodological",
            "translation",
            "Commento collation",
            "Pass 015 protocol",
            "high",
            "DRAFT",
            "Pass 015.",
        ),
    ]
    conn.executemany(
        """
        INSERT OR REPLACE INTO claims
        (id, artifact_id, document_id, claim_text, claim_type, theme, target_entity, evidence_page, confidence, review_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        claims,
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_cards(id, entity_type, title, subtitle, summary, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "source-jayne-commento-pass015",
                "source_packet",
                "Jayne Commento Translation Access",
                "Restricted modern English witness",
                "Jayne's modern English translation is registered for page-level notes and collation, not full-text transcription.",
                "DRAFT",
                "source_jayne_commento_translation_access_pass015",
            ),
            (
                "concept-commento-translation-collation-pass015",
                "concept",
                "Commento Translation Collation",
                "Italian TEI, Stanley, Jayne",
                "A workflow separates controlling primary text, early modern reception, and restricted modern translation witness.",
                "DRAFT",
                "concept_commento_translation_collation_protocol_pass015",
            ),
        ],
    )
    conn.execute(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        (
            "page-commento-translation-collation-pass015",
            "concept",
            "Commento Translation Collation Protocol",
            "artifacts/concepts/commento_translation_collation_protocol_pass015.md",
            "DRAFT",
            "concept_commento_translation_collation_protocol_pass015",
        ),
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
    ingest_stub(conn)
    write_artifacts()
    update_docs_and_ontology()
    db_rows(conn)
    conn.commit()
    refresh(conn)
    conn.close()
    print("Study pass 015 Jayne access record complete.")


if __name__ == "__main__":
    main()
