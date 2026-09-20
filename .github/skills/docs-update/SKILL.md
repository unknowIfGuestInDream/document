---
name: docs-update
description: Update an existing Docsify document using confirmed repository information without guessing or unrelated refactoring.
---

## Instructions

Use this skill when asked to update an existing documentation page.

1. Read the target file completely before editing.
2. Search the repository for related configuration, commands, examples, and other documents that can confirm the new information.
3. Identify statements that are outdated, inconsistent, or missing based on confirmed evidence.
4. Update only the necessary lines. Preserve valid history, working examples, and unrelated content.
5. If the requested information cannot be confirmed, do not guess. Mark it as needing confirmation or explain the missing source.
6. If the update changes file names, section names, or page locations, update the nearest `_sidebar.md` entry too.
7. Run `python .github/scripts/check_docs_links.py <updated-file> <related-sidebar>` when links or navigation may be affected.
8. Provide a short summary of the confirmed sources you used and the exact changes made.
