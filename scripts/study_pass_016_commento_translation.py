"""Study pass 016: original English translation layer for Pico's Commento."""

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
COMMENTO_DOC_ID = "Pico_Commento_BibliotecaItaliana_TEI_bibit000827_xml_2e50ef08"


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


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


def update_ontology() -> None:
    path = DATA / "reading_artifact_ontology.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version"] = "0.15.0"
    payload["commento_original_translation_fields"] = [
        "source_section",
        "italian_witness",
        "english_translation",
        "technical_terms",
        "translator_notes",
        "stanley_comparison",
        "jayne_comparison_if_available",
        "doctrinal_stakes",
        "revision_status",
    ]
    payload["corpus_control_rules"] = sorted(set(payload.get("corpus_control_rules", []) + [
        "Original project translations must be made from controlled source-language witnesses, not reconstructed from copyrighted or reception translations.",
        "Each original translation section should preserve technical vocabulary and link to section-summary, glossary, and witness-collation artifacts.",
    ]))
    write_json(path, payload)


def update_docs() -> None:
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 016 Commento Translation Overlay",
        """## Pass 016 Commento Translation Overlay

When translating the Commento, keep translation, summary, and collation separate. Translation artifacts should render the Italian into readable scholarly English; section summaries should reconstruct the argument; collation notes should compare Stanley and Jayne only where they clarify reception or terminology.
""",
    )


def db_rows(conn: sqlite3.Connection) -> None:
    now = now_utc()
    artifacts = [
        (
            "translation_policy_commento_original_english",
            "translation_policy",
            "Commento Original Translation Policy",
            "artifacts/translations/commento/commento_original_translation_policy.md",
            COMMENTO_DOC_ID,
            "Commento",
            "ACTIVE",
            "source_governed",
        ),
        (
            "translation_commento_opening_pass016",
            "translation",
            "Commento Opening: Original English Translation",
            "artifacts/translations/commento/commento_original_translation_opening_pass016.md",
            COMMENTO_DOC_ID,
            "Commento opening paratexts",
            "DRAFT_TRANSLATION",
            "source_governed",
        ),
        (
            "translation_queue_commento_pass016",
            "translation_queue",
            "Commento Translation Queue",
            "artifacts/translations/commento/commento_translation_queue_pass016.md",
            COMMENTO_DOC_ID,
            "Commento",
            "ACTIVE",
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
            "claim_translation_016_001",
            "translation_policy_commento_original_english",
            COMMENTO_DOC_ID,
            "PicoDB can create an original English translation of the Commento from the controlled Italian TEI witness without reconstructing the text from Stanley or Jayne.",
            "methodological",
            "translation",
            "Commento",
            "Pass 016 translation policy",
            "high",
            "DRAFT",
            "Pass 016.",
        ),
        (
            "claim_translation_016_002",
            "translation_commento_opening_pass016",
            COMMENTO_DOC_ID,
            "The opening paratexts frame the Commento as a posthumous, partially reluctant publication whose Platonic doctrine is explicitly subordinated to Christian truth.",
            "interpretive",
            "Commento",
            "Bonacursius and Benivieni",
            "Opening translation",
            "high",
            "DRAFT",
            "Pass 016.",
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
                "translation-commento-opening-pass016",
                "translation",
                "Commento Opening Translation",
                "Original English from the Italian TEI",
                "PicoDB has begun its own English translation of the Commento from the Italian, starting with the title, Bonacursius dedication, and Benivieni's reader address.",
                "DRAFT",
                "translation_commento_opening_pass016",
            ),
            (
                "translation-policy-commento-original",
                "system",
                "Commento Translation Policy",
                "Italian TEI controls the translation",
                "A translation protocol keeps our original English rendering distinct from Stanley, Jayne, summaries, and collation notes.",
                "ACTIVE",
                "translation_policy_commento_original_english",
            ),
        ],
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                "page-commento-opening-translation-pass016",
                "translation",
                "Commento Opening: Original English Translation",
                "artifacts/translations/commento/commento_original_translation_opening_pass016.md",
                "DRAFT",
                "translation_commento_opening_pass016",
            ),
            (
                "page-commento-translation-policy-pass016",
                "system",
                "Commento Translation Protocol",
                "docs/COMMENTO_TRANSLATION_PROTOCOL.md",
                "ACTIVE",
                "translation_policy_commento_original_english",
            ),
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
    update_ontology()
    update_docs()
    db_rows(conn)
    conn.commit()
    refresh(conn)
    conn.close()
    print("Study pass 016 Commento translation layer complete.")


if __name__ == "__main__":
    main()
