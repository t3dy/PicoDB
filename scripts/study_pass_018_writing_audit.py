"""Study pass 018: audit existing writing after Commento, Jayne, translation, and Pugliese passes."""

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
PUGLIESE_DOC_ID = "BibliothÃ¨que_d_Humanisme_et_Renaissance_vol_65_iss_2_Olga_Zorzi_Pugliese_GIROLAMO_BENIVIENI_AMIC_pdf_80f46aa9"


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
    payload["version"] = "0.17.0"
    payload["revision_audit_fields"] = sorted(set(payload.get("revision_audit_fields", []) + [
        "affected_artifact",
        "stale_claim",
        "new_source_anchor",
        "revision_priority",
        "governing_scholar",
        "affected_theme",
        "required_new_artifact",
        "website_destination",
        "status_after_revision",
    ]))
    payload["commento_benivieni_fields"] = sorted(set(payload.get("commento_benivieni_fields", []) + [
        "poetic_occasion",
        "commentary_independence",
        "benivieni_mediation",
        "ficino_softening",
        "vernacular_translation",
        "posthumous_publication_frame",
        "translation_witness_status",
    ]))
    payload["priority_revision_queue"] = [
        "missing_writings_status_correction",
        "ficino_dispute_benivieni_pugliese_expansion",
        "commento_section_summary_witness_matrix",
        "biography_benivieni_pater_noster_update",
        "astrology_benivieni_disputationes_update",
        "platonism_aristotelianism_commento_update",
        "kabbalah_benivieni_reception_update",
        "heptaplus_pater_noster_adjacent_exegesis_update",
        "scholar_profile_expansion",
        "900_conclusions_thesis_tables",
    ]
    write_json(path, payload)


def update_docs() -> None:
    append_once(
        DOCS / "SCHOLARLY_VALUES_STYLE_GUIDE.md",
        "## Pass 018 Revision-Audit Overlay",
        """## Pass 018 Revision-Audit Overlay

Every major new reading pass must now ask what existing writing it changes. Record stale claims, newly anchored claims, affected essays, affected scholar profiles, required section-summary updates, and website destinations. A source packet is incomplete if it does not tell us which earlier essays, summaries, profiles, or source gaps should be revised.

Add Olga Zorzi Pugliese as the guide scholar for Benivieni as collaborator, vernacular translator, Commento mediator, and Pater Noster source-gap witness. Use her with Allen for the Ficino softening problem, with Dougherty for corpus/edition awareness, and with biography work for late Florentine reception.
""",
    )
    append_once(
        DOCS / "SECTION_SUMMARY_STYLE_GUIDE.md",
        "## Pass 018 Audit-to-Revision Rule",
        """## Pass 018 Audit-to-Revision Rule

Every section summary should include an `Updates Existing Writing` note when a passage changes a prior essay, scholar profile, source gap, timeline event, or website page. This keeps close reading tied to the writing system instead of producing isolated notes.
""",
    )


def db_rows(conn: sqlite3.Connection) -> None:
    now = now_utc()
    artifacts = [
        (
            "audit_pico_writing_update_pass018",
            "editorial_audit",
            "Writing Audit After Commento, Jayne, Translation, and Pugliese Passes",
            "artifacts/audits/pico_writing_update_audit_pass018.md",
            None,
            "PicoDB writing system",
            "ACTIONABLE_AUDIT",
            "high",
        ),
        (
            "profile_olga_zorzi_pugliese_pass018",
            "scholar_profile",
            "Olga Zorzi Pugliese",
            "artifacts/scholar_profiles/olga_zorzi_pugliese_profile_pass018.md",
            PUGLIESE_DOC_ID,
            "Pugliese",
            "SOURCE_ANCHORED_DRAFT",
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
            "claim_audit_018_001",
            "audit_pico_writing_update_pass018",
            None,
            "PicoDB's missing-writings essay must be corrected because the Commento is now acquired in a controlled Italian witness and the Pater Noster commentary is the stronger new acquisition priority.",
            "editorial",
            "source gaps",
            "Pico writings queue",
            "Pass 018 audit",
            "high",
            "DRAFT",
            "Derived from passes 014-017.",
        ),
        (
            "claim_audit_018_002",
            "audit_pico_writing_update_pass018",
            PUGLIESE_DOC_ID,
            "The Ficino dispute essay should add a Pugliese-Allen synthesis because Benivieni's mediation and softening of the Commento confirms that Pico-Ficino conflict was partly reshaped in transmission.",
            "editorial",
            "Ficino",
            "Ficino dispute essay",
            "Pass 018 audit",
            "high",
            "DRAFT",
            "Derived from Allen and Pugliese artifacts.",
        ),
        (
            "claim_audit_018_003",
            "audit_pico_writing_update_pass018",
            PUGLIESE_DOC_ID,
            "Benivieni must be added to the biography as collaborator, posthumous mediator, vernacular translator, and reception agent rather than only as the poet whose canzone Pico commented on.",
            "editorial",
            "biography",
            "Pico biography",
            "Pass 018 audit",
            "high",
            "DRAFT",
            "Derived from Pugliese pass 017.",
        ),
        (
            "claim_profile_pugliese_018_001",
            "profile_olga_zorzi_pugliese_pass018",
            PUGLIESE_DOC_ID,
            "Pugliese's main PicoDB value is transmission-centered: she makes Benivieni visible as collaborator, translator, mediator, and possible reviser of Pico-related texts.",
            "historiographical",
            "scholar profile",
            "Pugliese",
            "Pass 018 profile",
            "high",
            "DRAFT",
            "Profile synthesis from pass 017.",
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
                "audit-pico-writing-update-pass018",
                "editorial_audit",
                "PicoDB Writing Audit",
                "What the latest passes add",
                "An actionable audit maps Commento, Jayne, translation, and Pugliese findings onto every major essay, summary, profile, and source gap.",
                "DRAFT",
                "audit_pico_writing_update_pass018",
            ),
            (
                "profile-olga-zorzi-pugliese-pass018",
                "scholar_profile",
                "Olga Zorzi Pugliese",
                "Benivieni and transmission",
                "Pugliese becomes the guide scholar for Benivieni as collaborator, translator, Commento mediator, and Pater Noster source-gap witness.",
                "DRAFT",
                "profile_olga_zorzi_pugliese_pass018",
            ),
        ],
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                "page-audit-pico-writing-update-pass018",
                "editorial_audit",
                "Writing Audit After Commento, Jayne, Translation, and Pugliese Passes",
                "artifacts/audits/pico_writing_update_audit_pass018.md",
                "DRAFT",
                "audit_pico_writing_update_pass018",
            ),
            (
                "page-profile-olga-zorzi-pugliese-pass018",
                "scholar_profile",
                "Olga Zorzi Pugliese",
                "artifacts/scholar_profiles/olga_zorzi_pugliese_profile_pass018.md",
                "DRAFT",
                "profile_olga_zorzi_pugliese_pass018",
            ),
        ],
    )


def refresh(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
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
    print("Study pass 018 writing audit complete.")


if __name__ == "__main__":
    main()
