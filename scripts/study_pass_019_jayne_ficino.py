"""Study pass 019: Sears Jayne materials and the Pico-Ficino relationship."""

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

JAYNE_ARTICLE_ID = "Comparative_Literature_vol._4_iss._3_Ficino_and_the_Platonism_of_the_English_RenaissanceJayne_Se_pdf_0d8e1dd1"
CRAVEN_ID = "Bibliothèque_d_and__039_Humanisme_et_Renaissance_vol._49_iss._2_Giovanni_Commentary_on_a_canzone_pdf_31ae00a5"
BENSON_ID = "Bibliothèque_d_and__039_Humanisme_et_Renaissance_vol._49_iss._3_Commentary_on_Plato_and__039_s_S_pdf_8e8d68a9"
NELSON_ID = "Italica_vol._65_iss._2_Commentary_on_Plato_and__039_s_Symposium_on_Loveby_Marsilio_Ficino__Sears_pdf_f6669030"
MILES_ID = "Comparative_Literature_vol._16_iss._3_John_Colet_and_Marsilio_FicinoMiles_Leland__Jayne_Sears196_pdf_7007834e"


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
    payload["version"] = "0.18.0"
    payload["ficino_relationship_fields"] = sorted(set(payload.get("ficino_relationship_fields", []) + [
        "direct_ficino_influence",
        "mediated_ficino_influence",
        "ficinian_love_platonism",
        "commentary_as_original_treatise",
        "literary_popularization",
        "reader_marginalia",
        "selective_reception",
        "anti_ficinian_correction",
        "pico_as_mediator",
    ]))
    payload["commento_comparison_fields"] = sorted(set(payload.get("commento_comparison_fields", []) + [
        "ficino_de_amore_as_comparator",
        "pico_commento_as_rival_commentary",
        "methodology_dispute",
        "mythology_dispute",
        "love_theory_dispute",
        "poetic_theology_project",
    ]))
    write_json(path, payload)


def update_docs() -> None:
    append_once(
        DOCS / "FICINO_PICO_READING_PROTOCOL.md",
        "## Pass 019 Jayne Reception Overlay",
        """## Pass 019 Jayne Reception Overlay

Add Sears Jayne as a secondary guide for mediated Ficinian influence, love Platonism, and reception. Jayne's rule for PicoDB: Ficino's influence is often strongest when transformed by mediators. Do not equate reading, praise, marginalia, or shared sources with discipleship.

When comparing Ficino's *De amore* and Pico's *Commento*, mark both works as commentaries that exceed their occasions. Ficino uses Plato's *Symposium* to construct a doctrine of cosmic and personal love; Pico uses Benivieni's canzone to construct poetic theology, love metaphysics, and anti-Ficinian correction.
""",
    )


def db_rows(conn: sqlite3.Connection) -> None:
    now = now_utc()
    artifacts = [
        (
            "source_jayne_ficino_pico_pass019",
            "source_packet",
            "Sears Jayne, Ficino Reception, and the Pico-Ficino Problem",
            "artifacts/source_packets/jayne_ficino_pico_pass019.md",
            JAYNE_ARTICLE_ID,
            "Pico-Ficino relationship",
            "SOURCE_ANCHORED",
            "high",
        ),
        (
            "concept_jayne_ficino_love_platonism_pass019",
            "concept_dossier",
            "Jayne on Ficino, Love Platonism, and Pico's Mediation",
            "artifacts/concepts/pico_ficino_jayne_love_platonism_overlay_pass019.md",
            JAYNE_ARTICLE_ID,
            "Ficinian love Platonism",
            "SOURCE_ANCHORED_DRAFT",
            "high",
        ),
        (
            "profile_sears_jayne_pass019",
            "scholar_profile",
            "Sears Jayne",
            "artifacts/scholar_profiles/sears_jayne_profile_pass019.md",
            JAYNE_ARTICLE_ID,
            "Sears Jayne",
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
            "claim_jayne_019_001",
            "source_jayne_ficino_pico_pass019",
            JAYNE_ARTICLE_ID,
            "Jayne argues that Ficino's influence on English Renaissance Platonism was often indirect and most specific in the doctrine of love and beauty.",
            "historiographical",
            "Ficino",
            "Ficinian love Platonism",
            "Jayne 1952 conclusion",
            "high",
            "DRAFT",
            "Pass 019.",
        ),
        (
            "claim_jayne_019_002",
            "source_jayne_ficino_pico_pass019",
            JAYNE_ARTICLE_ID,
            "Jayne treats Pico as a key mediator through whom Ficinian Christian Platonism affected Colet and More more strongly than through Ficino's own works.",
            "reception",
            "Pico-Ficino",
            "Pico as mediator",
            "Jayne 1952 prose section",
            "high",
            "DRAFT",
            "Pass 019.",
        ),
        (
            "claim_jayne_019_003",
            "source_jayne_ficino_pico_pass019",
            CRAVEN_ID,
            "Craven credits Jayne with clarifying the Commento as a composite work and a direct attack on Ficino's methodology, mythology, and theory of love.",
            "interpretive",
            "Commento",
            "Pico-Ficino dispute",
            "Craven review pp. 471-473",
            "high",
            "DRAFT",
            "Pass 019.",
        ),
        (
            "claim_jayne_019_004",
            "concept_jayne_ficino_love_platonism_pass019",
            BENSON_ID,
            "Reviews of Jayne's Ficino translation support treating De amore as Ficino's own love doctrine rather than only a continuous commentary on Plato's Symposium.",
            "interpretive",
            "Ficino",
            "De amore",
            "Benson/Nelson reviews",
            "high",
            "DRAFT",
            "Pass 019.",
        ),
        (
            "claim_jayne_019_005",
            "source_jayne_ficino_pico_pass019",
            MILES_ID,
            "The Colet reviews show that reading, admiration, marginalia, rejection, and selective use can coexist, giving PicoDB a method rule for influence claims.",
            "methodological",
            "reception",
            "Influence is not discipleship",
            "Miles/Rice/Rouse reviews",
            "high",
            "DRAFT",
            "Pass 019.",
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
                "source-jayne-ficino-pico-pass019",
                "source_packet",
                "Jayne on Ficino and Pico",
                "Mediated influence and love Platonism",
                "A new source packet uses Jayne and reviewers to sharpen Ficino's mediated influence, Pico's Commento, and rival love commentaries.",
                "DRAFT",
                "source_jayne_ficino_pico_pass019",
            ),
            (
                "concept-jayne-ficino-love-platonism-pass019",
                "concept",
                "Ficinian Love Platonism",
                "Direct, mediated, and contested",
                "Jayne helps PicoDB distinguish Ficino as translator, Ficino as source of love Platonism, and Pico as a mediator/corrector.",
                "DRAFT",
                "concept_jayne_ficino_love_platonism_pass019",
            ),
            (
                "profile-sears-jayne-pass019",
                "scholar_profile",
                "Sears Jayne",
                "Ficino, Pico, and reception",
                "Jayne is now a guide for Ficino's De amore, Pico's Commento translation history, Colet marginalia, and mediated Platonist influence.",
                "DRAFT",
                "profile_sears_jayne_pass019",
            ),
        ],
    )
    conn.executemany(
        "INSERT OR REPLACE INTO website_pages(id, entity_type, title, markdown_path, status, source_artifact_id) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                "page-jayne-ficino-pico-pass019",
                "source_packet",
                "Sears Jayne, Ficino Reception, and the Pico-Ficino Problem",
                "artifacts/source_packets/jayne_ficino_pico_pass019.md",
                "DRAFT",
                "source_jayne_ficino_pico_pass019",
            ),
            (
                "page-concept-jayne-ficino-love-platonism-pass019",
                "concept",
                "Jayne on Ficino, Love Platonism, and Pico's Mediation",
                "artifacts/concepts/pico_ficino_jayne_love_platonism_overlay_pass019.md",
                "DRAFT",
                "concept_jayne_ficino_love_platonism_pass019",
            ),
            (
                "page-profile-sears-jayne-pass019",
                "scholar_profile",
                "Sears Jayne",
                "artifacts/scholar_profiles/sears_jayne_profile_pass019.md",
                "DRAFT",
                "profile_sears_jayne_pass019",
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
    print("Study pass 019 Jayne/Ficino complete.")


if __name__ == "__main__":
    main()
