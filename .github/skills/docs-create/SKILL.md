---
name: docs-create
description: Create a new Docsify Markdown page in the correct section, avoid duplicate pages, update sidebar navigation when needed, and validate the result.
---

## Instructions

Use this skill when asked to create a new document for this repository.

1. Inspect the target topic area under `/docs` and read the nearest `README.md`, `_sidebar.md`, and related pages.
2. Search for existing pages on the same topic before creating a new file. If a duplicate or near-duplicate already exists, extend or update that page instead of creating another one.
3. Choose the closest existing section directory. Reuse the naming style of nearby files.
4. Create a Markdown file with one clear `#` heading, concise technical content, and correctly labeled fenced code blocks.
5. Preserve technical terms, commands, API names, file names, and configuration keys in English, and wrap inline literals in backticks.
6. If the new page should appear in navigation, add exactly one matching entry to the nearest `_sidebar.md` without changing unrelated order or hierarchy.
7. Run `python .github/scripts/check_docs_links.py <new-file> <related-sidebar>` on the affected files.
8. Report what was created, why that location was chosen, and whether navigation was updated.
