"""Ingest one PDF/EPUB source into PicoDB without rerunning the full bootstrap."""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "db" / "pico.db"


def load_init_module():
    spec = importlib.util.spec_from_file_location("init_pico_portal", ROOT / "scripts" / "init_pico_portal.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load init_pico_portal.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_seed_module():
    spec = importlib.util.spec_from_file_location("seed_research_artifacts", ROOT / "scripts" / "seed_research_artifacts.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load seed_research_artifacts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/ingest_single_source.py <source-file>")
    source = Path(sys.argv[1]).resolve()
    if not source.exists():
        raise SystemExit(f"Source not found: {source}")

    init = load_init_module()
    if source.suffix.lower() not in init.SOURCE_EXTS:
        raise SystemExit(f"Unsupported extension: {source.suffix}")

    conn = sqlite3.connect(DB)
    init.init_db(conn)
    digest = init.sha256(source)
    ext = source.suffix.lower().lstrip(".")
    doc_id = f"{init.slugify(source.stem, max_len=96)}_{ext}_{digest[:8]}"
    markdown_path = init.MARKDOWN_DIR / f"{doc_id}.md"

    if source.suffix.lower() == ".pdf":
        pages, toc_rows, meta = init.extract_pdf(source)
    else:
        pages, toc_rows, meta = init.extract_epub(source)
    full_text = "\n\n".join(p["text"] for p in pages)
    doc_type, works, themes = init.classify_doc(source, full_text)
    md = init.markdown_for(source, doc_id, doc_type, themes, works, pages, meta)
    init.MARKDOWN_DIR.mkdir(exist_ok=True)
    markdown_path.write_text(md, encoding="utf-8", errors="replace")
    word_count = init.count_words(full_text)
    duplicate = conn.execute(
        "SELECT id FROM documents WHERE sha256=? AND id<>? ORDER BY created_at LIMIT 1",
        (digest, doc_id),
    ).fetchone()
    duplicate_of = duplicate[0] if duplicate else None

    conn.execute(
        """
        INSERT OR REPLACE INTO documents
        (id,title,source_file,source_path,markdown_path,extension,sha256,duplicate_of,document_type,
         themes_json,pico_works_json,page_count,word_count,extraction_status,metadata_json,source_method,review_status,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            doc_id,
            meta.get("title") or source.stem,
            source.name,
            str(source),
            str(markdown_path.resolve()),
            source.suffix.lower(),
            digest,
            duplicate_of,
            doc_type,
            json.dumps(themes, ensure_ascii=False),
            json.dumps(works, ensure_ascii=False),
            len(pages),
            word_count,
            "OK",
            json.dumps(meta, ensure_ascii=False, default=str),
            "deterministic_single_source_extraction",
            "UNREVIEWED",
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    for table in ["pages", "sections", "document_fts", "reading_tasks"]:
        conn.execute(f"DELETE FROM {table} WHERE document_id=?", (doc_id,))
    conn.executemany(
        "INSERT INTO pages(document_id,page_number,heading,text,word_count) VALUES (?,?,?,?,?)",
        [(doc_id, p["page"], p["title"], p["text"], init.count_words(p["text"])) for p in pages],
    )
    if toc_rows:
        conn.executemany(
            "INSERT INTO sections(document_id,level,title,start_page) VALUES (?,?,?,?)",
            [(doc_id, r["level"], r["title"], r["page"]) for r in toc_rows],
        )
    else:
        for p in pages:
            if p["page"] == 1 or (p["page"] - 1) % 10 == 0:
                conn.execute(
                    "INSERT INTO sections(document_id,level,title,start_page,notes) VALUES (?,?,?,?,?)",
                    (doc_id, 1, f"Generated reading unit starting page {p['page']}", p["page"], "No bookmarks found."),
                )
    conn.execute(
        "INSERT INTO document_fts(document_id,title,source_file,text,themes) VALUES (?,?,?,?,?)",
        (doc_id, meta.get("title") or source.stem, source.name, full_text, " ".join(themes + works)),
    )
    for name in init.detect_scholars(source.name, full_text):
        conn.execute(
            "INSERT OR REPLACE INTO scholars(id,name,source_count,notes) VALUES (?,?,COALESCE((SELECT source_count FROM scholars WHERE id=?),0)+1,?)",
            (init.slugify(name).lower(), name, init.slugify(name).lower(), "Updated by single-source ingest; biography pending corpus-based pass."),
        )
    for work in works:
        conn.execute(
            "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
            (doc_id, "pico_text_close_reading", work, 1, "Summarize every section and extract doctrinal claims."),
        )
    conn.execute(
        "INSERT INTO reading_tasks(document_id,task_type,target,priority,notes) VALUES (?,?,?,?,?)",
        (doc_id, "document_section_summary", source.stem, 2, "Create exhaustive section-by-section summary with claims and citations."),
    )
    conn.commit()

    seed = load_seed_module()
    seed.export_data(conn)
    seed.build_site(conn)
    conn.close()
    print(f"Ingested {source.name} as {doc_id}")
    print(f"Markdown: {markdown_path}")


if __name__ == "__main__":
    main()
