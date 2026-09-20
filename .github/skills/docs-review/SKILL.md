---
name: docs-review
description: Review existing Docsify documentation for clear Markdown, content, and navigation problems while avoiding unnecessary rewrites.
---

## Instructions

Use this skill when asked to review or lightly repair existing documentation.

1. Read the target Markdown file and any related `_sidebar.md` or `_navbar.md` files.
2. Check for heading hierarchy problems, empty headings, empty links, malformed fenced code blocks, and obvious formatting errors.
3. Check for duplicated passages, obvious typos, mixed Chinese and English punctuation in Chinese prose, inconsistent inline formatting for technical terms, conflicting version statements, and clearly outdated content.
4. Check Docsify-specific navigation and local links, including image paths and `_sidebar.md` references.
5. Only edit confirmed problems. Do not refactor or rewrite large sections just to change tone.
6. After changes, run `python .github/scripts/check_docs_links.py <paths...>` for the edited documentation files.
7. Summarize the problems found, the minimal fixes applied, and any items that still need human confirmation.
