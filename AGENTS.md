# Agent instructions for documentation maintenance

Use these rules when working in this repository with agent mode:

1. Start by locating the affected documentation area under `/docs` and reading the nearest `README.md`, `_sidebar.md`, and `_navbar.md` files when navigation may be affected.
2. Prefer the repository skills `/docs-create`, `/docs-review`, `/docs-update`, `/docs-translate`, `/docs-link-check`, and `/docs-sidebar-maintain` when they match the task.
3. For multi-step maintenance requests, work in this order: inspect related files, check for duplicates or conflicts, make the smallest useful edits, validate links/navigation, then summarize what changed.
4. Do not mass-rewrite documents for style alone. Keep existing terminology, examples, and valid historical notes unless the task requires broader edits.
5. Preserve Docsify-specific syntax and existing navigation structure.
6. When you change Markdown or navigation files, validate the affected files with `python .github/scripts/check_docs_links.py <paths...>` before you finish.
