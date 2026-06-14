# Pipeline

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
