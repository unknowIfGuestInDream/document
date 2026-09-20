---
name: docs-sidebar-maintain
description: Maintain Docsify `_sidebar.md` files when pages are added, renamed, moved, or removed, while preserving the current hierarchy and ordering.
---

## Instructions

Use this skill when asked to update Docsify sidebar navigation.

1. Read the nearest section `_sidebar.md` and inspect sibling documents in the same directory tree.
2. Preserve the existing indentation, hierarchy, and ordering style.
3. Add new entries only when the page should be discoverable from navigation.
4. Do not add duplicate links, and do not remove valid entries unrelated to the task.
5. Use correct relative link paths from the `_sidebar.md` file location.
6. If a page moved or was renamed, update the existing entry instead of adding a second one.
7. Validate the sidebar and the affected page with `python .github/scripts/check_docs_links.py <sidebar> <page>`.
8. Report exactly which sidebar entries were added, updated, or left unchanged.
