---
agent: 'agent'
description: 'Plan and execute one or more Docsify documentation maintenance tasks in this repository'
---

You are maintaining the Docsify documentation in this repository.

Task summary: ${input:task:Describe the documentation work to perform}
Target files or directories: ${input:scope:List the files or directories to inspect, or write auto if unknown}
Need translation: ${input:translation:yes/no}
Need navigation updates: ${input:navigation:yes/no}

Workflow:

1. Read `.github/copilot-instructions.md` and `AGENTS.md` before editing.
2. Inspect the related files under `/docs` and look for duplicate or conflicting content.
3. Use these skills when helpful: `/docs-create`, `/docs-review`, `/docs-update`, `/docs-translate`, `/docs-link-check`, `/docs-sidebar-maintain`.
4. Make only the smallest edits needed to complete the request.
5. If you add or move pages, update the nearest `_sidebar.md` and keep the existing order/style.
6. Validate affected documentation with `python .github/scripts/check_docs_links.py <paths...>`.
7. Summarize the files changed, navigation updates, checks run, and any information that still needs confirmation.
