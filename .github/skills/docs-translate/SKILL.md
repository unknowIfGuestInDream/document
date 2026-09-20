---
name: docs-translate
description: Translate Docsify documentation while preserving links, code blocks, commands, configuration, and repository navigation structure.
---

## Instructions

Use this skill when asked to translate a document.

1. Read the source document and identify whether the translation should replace the existing page or create a parallel page.
2. Preserve code blocks, commands, file paths, API names, class names, method names, version numbers, and configuration keys.
3. Translate prose accurately and keep the result concise and technical.
4. Do not invent missing terminology or unsupported product/version details.
5. Keep Markdown structure, headings, lists, tables, and links intact unless the task explicitly requires a structural change.
6. If a translated page is added to navigation, update the nearest `_sidebar.md` in the existing style.
7. Run `python .github/scripts/check_docs_links.py <translated-file> <related-sidebar>` on the affected files.
8. Report the translation scope, any preserved source-language terms, and any phrases that still need subject-matter confirmation.
