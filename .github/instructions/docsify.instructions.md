---
applyTo: "docs/**/*.md"
---

## Docsify markdown instructions

- Treat `/docs` as the Docsify site root.
- Follow the repository-wide markdown rules in `.github/copilot-instructions.md`.
- Keep one primary `#` heading per document unless the file is intentionally a navigation file.
- Prefer matching the structure and tone of nearby documents in the same directory.
- Preserve special Docsify syntax, inline HTML, Mermaid blocks, and any existing tabs or plugin-specific blocks.
- When adding or moving a page, check whether the nearest `_sidebar.md` needs one new entry. Do not add duplicate links.
- Preserve existing sort order and indentation in `_sidebar.md` files.
- Keep `_navbar.md` links in the current absolute Docsify route style such as `/java/` or `/springCloud/`.
- Check local Markdown links, Docsify page links, image paths, and `_sidebar.md` references after changes.
