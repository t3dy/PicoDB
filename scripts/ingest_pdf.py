"""
ingest_pdf.py — PicoDB PDF ingestion script

Creates a SourceMetadataArtifact for a PDF or article dropped into the corpus.

Usage:
    python scripts/ingest_pdf.py /path/to/file.pdf
    python scripts/ingest_pdf.py /path/to/file.pdf --title "..." --authors "Author One, Author Two" --year 2009
    python scripts/ingest_pdf.py /path/to/file.pdf --source-type article --dry-run

Options:
    --source-id    Override auto-generated source_id
    --title        Source title (required if not in PDF metadata)
    --authors      Comma-separated list of authors
    --year         Publication year (integer)
    --source-type  pdf|book|article|podcast_episode|youtube_video|webpage|manuscript
                   (default: article)
    --journal      Journal name (for articles)
    --volume       Volume number
    --issue        Issue number
    --pages        Page range (e.g. "444-479")
    --doi          DOI string
    --dry-run      Print the artifact JSON without writing to disk

Creates:
    artifacts/generated/{source_id}/source_metadata.json

Notes:
    - source_id is generated as: {first_author_lastname}_{first_title_word}_{year}
      e.g. copenhaver_ten_arguments_2009
    - Use --source-id to override this if the auto-generated id is ambiguous
    - After ingestion, run an extraction agent to produce raw_extraction artifacts
"""

import json
import sys
import os
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GENERATED_DIR = REPO_ROOT / "artifacts" / "generated"

KNOWN_SOURCE_TYPES = {
    "pdf", "book", "article", "podcast_episode",
    "youtube_video", "webpage", "manuscript", "database_record", "other"
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "_", text)
    text = re.sub(r"-+", "_", text)
    return text[:40].strip("_")


def make_source_id(authors: list[str], title: str, year: int | None) -> str:
    lastname = slugify(authors[0].split()[-1]) if authors else "unknown"
    first_word = slugify(title.split()[0]) if title else "untitled"
    second_word = slugify(title.split()[1]) if title and len(title.split()) > 1 else ""
    year_str = str(year) if year else "0000"
    parts = [lastname, first_word]
    if second_word and second_word not in {"a", "an", "the", "of", "in", "on"}:
        parts.append(second_word)
    parts.append(year_str)
    return "_".join(parts)


def try_read_pdf_metadata(pdf_path: Path) -> dict:
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(pdf_path))
        meta = doc.metadata
        doc.close()
        return {
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "page_count": doc.page_count,
        }
    except ImportError:
        return {}
    except Exception:
        return {}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="PicoDB PDF ingestion script")
    p.add_argument("pdf_path", help="Path to the PDF file")
    p.add_argument("--source-id", default=None)
    p.add_argument("--title", default=None)
    p.add_argument("--authors", default=None, help="Comma-separated author names")
    p.add_argument("--year", type=int, default=None)
    p.add_argument("--source-type", default="article", choices=sorted(KNOWN_SOURCE_TYPES))
    p.add_argument("--journal", default=None)
    p.add_argument("--volume", default=None)
    p.add_argument("--issue", default=None)
    p.add_argument("--pages", default=None, help="Page range e.g. 444-479")
    p.add_argument("--doi", default=None)
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    pdf_path = Path(args.pdf_path).resolve()
    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)

    # Try to pull metadata from the PDF itself
    pdf_meta = try_read_pdf_metadata(pdf_path)

    title = args.title or pdf_meta.get("title") or pdf_path.stem
    raw_authors = args.authors or pdf_meta.get("author") or ""
    authors = [a.strip() for a in raw_authors.split(",") if a.strip()]

    if not authors:
        print("WARNING: No authors specified. Use --authors to set them.")
        authors = ["Unknown"]

    year = args.year

    source_id = args.source_id or make_source_id(authors, title, year)
    # Sanitize
    source_id = re.sub(r"[^a-z0-9_]", "_", source_id.lower())

    now = datetime.now(timezone.utc).isoformat()

    artifact: dict = {
        "artifact_id": f"sm_{source_id}_001",
        "artifact_type": "source_metadata",
        "schema_version": "1.0.0",
        "source_id": source_id,
        "generated_at": now,
        "generating_agent": "ingest_pdf.py",
        "source_title": title,
        "source_type": args.source_type,
        "authors": authors,
        "local_path": str(pdf_path),
        "raw_text_available": True,
    }

    if year:
        artifact["publication_date"] = str(year)
    if args.journal:
        artifact["journal"] = args.journal
    if args.volume:
        artifact["volume"] = args.volume
    if args.issue:
        artifact["issue"] = args.issue
    if args.pages:
        artifact["page_range"] = args.pages
    if args.doi:
        artifact["isbn_or_doi"] = args.doi

    out_json = json.dumps(artifact, indent=2, ensure_ascii=False)

    if args.dry_run:
        print(out_json)
        print(f"\n# Would write to: artifacts/generated/{source_id}/source_metadata.json")
        return

    out_dir = GENERATED_DIR / source_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "source_metadata.json"

    if out_file.exists():
        print(f"WARNING: {out_file} already exists. Overwrite? [y/N] ", end="")
        answer = input().strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out_json)
        f.write("\n")

    print(f"Created: {out_file.relative_to(REPO_ROOT)}")
    print(f"source_id: {source_id}")
    print(f"Next step: run an extraction agent on {pdf_path.name}")
    print(f"  Artifact storage: artifacts/generated/{source_id}/")


if __name__ == "__main__":
    main()
