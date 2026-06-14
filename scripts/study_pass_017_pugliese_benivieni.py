"""Study pass 017: Pugliese on Benivieni, Commento transmission, and Pater Noster."""

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
PUGLIESE_DOC_ID = "Bibliothèque_d_Humanisme_et_Renaissance_vol_65_iss_2_Olga_Zorzi_Pugliese_GIROLAMO_BENIVIENI_AMIC_pdf_80f46aa9"


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
    payload["version"] = "0.16.0"
    payload["commento_transmission_fields"] = sorted(set(payload.get("commento_transmission_fields", []) + [
        "benivieni_mediation",
        "ficino_softening",
        "publication_frame",
        "authorial_revision",
        "poem_commentary_noncoincidence",
        "related_pico_devotional_work",
        "manuscript_witness_needed",
    ]))
    payload["pico_primary_text_acquisition_queue"] = sorted(set(payload.get("pico_primary_text_acquisition_queue", []) + [
        "Expositio singularis in Orationem Dominicam / Pater Noster commentary: Latin witnesses and Benivieni vernacular translation",
    ]))
    write_json(path, payload)


def update_docs() -> None:
    append_once(
        DOCS / "PICO_TEXT_GAPS.md",
        "## Pass 017 Pater Noster Gap Update",
        """## Pass 017 Pater Noster Gap Update

- `Expositio singularis in Orationem Dominicam / Pater Noster commentary`: `new_primary_text_acquisition_priority`; Pugliese identifies Benivieni's unpublished vernacular translation and three manuscript witnesses/locations that may affect reconstruction of Pico's text.
- `Commento sopra una canzone d'amore`: `transmission_warning_reinforced`; Pugliese supports treating Benivieni as a mediator who could alter Pico's text to soften criticism of Ficino.
""",
    )
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 017 Pugliese Commento Transmission Overlay",
        """## Pass 017 Pugliese Commento Transmission Overlay

When summarizing Commento passages involving Ficino, love theory, Venus, beauty, Mind, or the canzone/commentary relation, mark whether the point depends on Pico's own argument, Benivieni's poetic pretext, later Benivieni mediation, or a softened publication frame. Use Pugliese with Allen for transmission cautions.
""",
    )


def db_rows(conn: sqlite3.Connection) -> None:
    now = now_utc()
    artifacts = [
        (
            "source_pugliese_benivieni_pass017",
            "source_packet",
            "Pugliese on Benivieni, Pico, Commento, and Pater Noster",
            "artifacts/source_packets/pugliese_benivieni_commento_pater_pass017.md",
            PUGLIESE_DOC_ID,
            "Benivieni and Commento",
            "SOURCE_ANCHORED",
            "high",
        ),
        (
            "transmission_commento_pugliese_pass017",
            "textual_transmission",
            "Pugliese and the Commento Transmission Problem",
            "artifacts/textual_transmission/commento_pugliese_transmission_note_pass017.md",
            PUGLIESE_DOC_ID,
            "Commento",
            "SOURCE_ANCHORED_DRAFT",
            "high",
        ),
        (
            "gap_pico_pater_noster_pugliese_pass017",
            "source_gap",
            "Pico Pater Noster Commentary and Benivieni Translation",
            "artifacts/source_gaps/pico_pater_noster_pugliese_gap_pass017.md",
            PUGLIESE_DOC_ID,
            "Expositio singularis in Orationem Dominicam",
            "ACQUISITION_PRIORITY",
            "high",
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
            "claim_pugliese_017_001",
            "source_pugliese_benivieni_pass017",
            PUGLIESE_DOC_ID,
            "Pugliese treats Benivieni as a close collaborator and posthumous mediator of Pico, not merely as the poet whose canzone occasioned the Commento.",
            "historiographical",
            "Benivieni",
            "Pico-Benivieni collaboration",
            "pp. 347-351",
            "high",
            "DRAFT",
            "Pass 017.",
        ),
        (
            "claim_pugliese_017_002",
            "transmission_commento_pugliese_pass017",
            PUGLIESE_DOC_ID,
            "Pugliese says Benivieni introduced changes into Pico's Commento in order to soften criticism of Ficino's theory of love.",
            "textual_transmission",
            "Commento",
            "Ficino softening",
            "p. 351",
            "high",
            "DRAFT",
            "Pass 017.",
        ),
        (
            "claim_pugliese_017_003",
            "source_pugliese_benivieni_pass017",
            PUGLIESE_DOC_ID,
            "Pugliese argues that Benivieni's canzone and Pico's prose commentary do not fully coincide doctrinally, making the poem partly a pretext for Pico's own theory of love.",
            "interpretive",
            "Commento",
            "poem-commentary relation",
            "p. 351",
            "high",
            "DRAFT",
            "Pass 017.",
        ),
        (
            "claim_pugliese_017_004",
            "gap_pico_pater_noster_pugliese_pass017",
            PUGLIESE_DOC_ID,
            "Pugliese identifies Benivieni's unpublished Florentine vernacular translation of Pico's Pater Noster commentary and argues that it may affect reconstruction of Pico's Latin text.",
            "bibliographic",
            "Pater Noster",
            "Expositio singularis in Orationem Dominicam",
            "pp. 352-359",
            "high",
            "DRAFT",
            "Pass 017.",
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
                "source-pugliese-benivieni-pass017",
                "source_packet",
                "Pugliese on Benivieni and Pico",
                "Commento mediation and Pater Noster translation",
                "Pugliese strengthens Benivieni's role as Pico's collaborator, Commento mediator, and translator of Pico's Pater Noster commentary.",
                "DRAFT",
                "source_pugliese_benivieni_pass017",
            ),
            (
                "transmission-commento-pugliese-pass017",
                "textual_transmission",
                "Commento Softening Problem",
                "Benivieni, Ficino, and textual mediation",
                "A new transmission note links Pugliese to Allen: Benivieni may have softened Pico's criticism of Ficino's theory of love.",
                "DRAFT",
                "transmission_commento_pugliese_pass017",
            ),
            (
                "gap-pico-pater-noster-pass017",
                "source_gap",
                "Pico's Pater Noster Commentary",
                "New acquisition priority",
                "Pugliese adds Pico's Pater Noster commentary and Benivieni's unpublished vernacular translation to the primary-text queue.",
                "DRAFT",
                "gap_pico_pater_noster_pugliese_pass017",
            ),
        ],
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                "page-pugliese-benivieni-pass017",
                "source_packet",
                "Pugliese on Benivieni, Pico, Commento, and Pater Noster",
                "artifacts/source_packets/pugliese_benivieni_commento_pater_pass017.md",
                "DRAFT",
                "source_pugliese_benivieni_pass017",
            ),
            (
                "page-commento-pugliese-transmission-pass017",
                "textual_transmission",
                "Pugliese and the Commento Transmission Problem",
                "artifacts/textual_transmission/commento_pugliese_transmission_note_pass017.md",
                "DRAFT",
                "transmission_commento_pugliese_pass017",
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
    print("Study pass 017 Pugliese/Benivieni complete.")


if __name__ == "__main__":
    main()
