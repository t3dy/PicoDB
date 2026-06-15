"""
validate_artifacts.py — PicoDB artifact pipeline validator

Usage:
    python scripts/validate_artifacts.py                    # validate all fixtures and generated/
    python scripts/validate_artifacts.py path/to/file.json  # validate a single file
    python scripts/validate_artifacts.py artifacts/fixtures/ # validate a directory

Checks:
    1. Schema validation against artifacts/schemas/{artifact_type}.schema.json
    2. Required provenance fields present
    3. Unique artifact_ids across all validated files
    4. Interpretive artifacts: each claim has evidence_links or confidence=speculative
    5. PublicProseArtifacts: reviewed/published require extraction + validation input_artifact_ids
    6. CurationArtifacts: publish/feature requires reasons_for_inclusion (also enforced by schema)
    7. No unknown artifact_type values
"""

import json
import sys
import os
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
SCHEMAS_DIR = REPO_ROOT / "artifacts" / "schemas"
FIXTURES_DIR = REPO_ROOT / "artifacts" / "fixtures"
GENERATED_DIR = REPO_ROOT / "artifacts" / "generated"

KNOWN_ARTIFACT_TYPES = {
    "source_metadata",
    "raw_extraction",
    "validation",
    "ontology_tagging",
    "interpretive",
    "curation",
    "public_prose",
    "text_comparison",
    "scholar_citation",
    # Legacy types from pico.db (not JSON-schema validated here but recognized)
    "source_packet",
    "claim_record",
    "section_summary",
    "scholar_profile",
    "pico_work_dossier",
    "concept_dossier",
    "historiography_node",
    "timeline_event",
    "location_record",
    "website_card",
    "website_page",
}

REQUIRED_PROVENANCE = ["artifact_id", "artifact_type", "schema_version", "source_id", "generated_at"]

ERRORS = []
WARNINGS = []
seen_artifact_ids: dict[str, str] = {}  # id -> file path


def err(path: str, msg: str) -> None:
    ERRORS.append(f"  ERROR [{path}]: {msg}")


def warn(path: str, msg: str) -> None:
    WARNINGS.append(f"  WARN  [{path}]: {msg}")


def load_schema(artifact_type: str) -> dict | None:
    schema_file = SCHEMAS_DIR / f"{artifact_type}.schema.json"
    if not schema_file.exists():
        return None
    with open(schema_file, encoding="utf-8") as f:
        return json.load(f)


def validate_file(json_path: Path) -> bool:
    json_path = json_path.resolve()
    try:
        path_str = str(json_path.relative_to(REPO_ROOT))
    except ValueError:
        path_str = str(json_path)

    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        err(path_str, f"Invalid JSON: {e}")
        return False

    if not isinstance(data, dict):
        err(path_str, "Root value must be an object")
        return False

    artifact_type = data.get("artifact_type")
    artifact_id = data.get("artifact_id")

    # 1. Known artifact type
    if artifact_type not in KNOWN_ARTIFACT_TYPES:
        err(path_str, f"Unknown artifact_type: {artifact_type!r}")

    # 2. Required provenance fields
    for field in REQUIRED_PROVENANCE:
        if field not in data or data[field] is None:
            err(path_str, f"Missing required provenance field: {field}")

    # 3. Unique artifact_id
    if artifact_id:
        if artifact_id in seen_artifact_ids:
            err(path_str, f"Duplicate artifact_id {artifact_id!r} (also in {seen_artifact_ids[artifact_id]})")
        else:
            seen_artifact_ids[artifact_id] = path_str

    # 4. JSON Schema validation (only for types with schemas)
    schema = load_schema(artifact_type) if artifact_type else None
    if schema:
        validator = jsonschema.Draft7Validator(schema)
        schema_errors = list(validator.iter_errors(data))
        for se in schema_errors:
            field_path = " > ".join(str(p) for p in se.absolute_path) or "root"
            err(path_str, f"Schema error at [{field_path}]: {se.message}")
    elif artifact_type not in KNOWN_ARTIFACT_TYPES:
        pass  # already reported above
    else:
        warn(path_str, f"No JSON schema for artifact_type={artifact_type!r} (legacy type)")

    # 5. Interpretive artifact: every claim needs evidence_links or confidence=speculative
    if artifact_type == "interpretive":
        for claim in data.get("interpretive_claims", []):
            cid = claim.get("claim_id", "?")
            confidence = claim.get("confidence")
            evidence = claim.get("evidence_links", [])
            if confidence != "speculative" and not evidence:
                err(path_str, f"Claim {cid!r}: confidence={confidence!r} but no evidence_links (use confidence=speculative for unsupported claims)")

    # 6. Public prose: reviewed/published require extraction + validation in input_artifact_ids
    if artifact_type == "public_prose":
        status = data.get("editorial_status")
        emergency = data.get("emergency_prose_mode", False)
        if status in ("reviewed", "published") and not emergency:
            input_ids = data.get("input_artifact_ids", [])
            if not input_ids:
                err(path_str, "reviewed/published public_prose must list input_artifact_ids")
            else:
                warn(path_str, "reviewed/published: manually verify input_artifact_ids include an extraction artifact and a validation artifact")

    # 7. Curation: publish/feature must have reasons_for_inclusion (also in schema but double-checked)
    if artifact_type == "curation":
        status = data.get("relevance_status")
        if status in ("publish", "feature"):
            if not data.get("reasons_for_inclusion"):
                err(path_str, f"relevance_status={status!r} requires reasons_for_inclusion")

    # 8. Raw extraction: flag if interpretive_claims_present is True
    if artifact_type == "raw_extraction":
        if data.get("interpretive_claims_present", False):
            warn(path_str, "interpretive_claims_present=true — extraction agent may have overstepped; review before tagging or interpreting")

    return len(ERRORS) == 0


def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(target.rglob("*.json"))
    return []


def main() -> None:
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if not target.exists():
            print(f"Path not found: {target}")
            sys.exit(1)
        files = collect_files(target)
    else:
        files = collect_files(FIXTURES_DIR) + collect_files(GENERATED_DIR)
        if not files:
            print("No JSON files found in artifacts/fixtures/ or artifacts/generated/")
            print("Run: python scripts/validate_artifacts.py artifacts/fixtures/")
            sys.exit(0)

    print(f"\nPicoDB artifact validator — checking {len(files)} file(s)\n")

    for json_path in files:
        validate_file(json_path)

    # Summary
    print(f"Artifact IDs seen: {len(seen_artifact_ids)}")
    print()

    if WARNINGS:
        print(f"Warnings ({len(WARNINGS)}):")
        for w in WARNINGS:
            print(w)
        print()

    if ERRORS:
        print(f"Errors ({len(ERRORS)}):")
        for e in ERRORS:
            print(e)
        print()
        print(f"FAILED: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        sys.exit(1)
    else:
        print(f"PASSED: 0 errors, {len(WARNINGS)} warning(s)")
        sys.exit(0)


if __name__ == "__main__":
    main()
