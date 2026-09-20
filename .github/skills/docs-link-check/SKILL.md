---
name: docs-link-check
description: Check Docsify Markdown links, sidebar links, image paths, and local file references, then fix obvious local link problems when safe.
---

## Instructions

Use this skill when asked to validate documentation links or Docsify navigation.

1. Run `python .github/scripts/check_docs_links.py <paths...>` on the target Markdown files, `_sidebar.md` files, and `_navbar.md` files.
2. Review each reported problem in this format:
   - `File:`
   - `Line:`
   - `Link:`
   - `Problem:`
   - `Suggested fix:`
3. Automatically fix only obvious local issues, such as a wrong relative path that has a single clear target or a missing sidebar entry caused by a same-task file move.
4. Do not guess at ambiguous targets. If multiple fixes are possible, stop and explain the options.
5. Re-run the checker after each fix and ensure the affected files pass.
6. Summarize the broken links found, which ones were auto-fixed, and which ones still need manual confirmation.
