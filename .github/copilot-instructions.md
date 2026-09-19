# GitHub Copilot instructions for this repository

This repository is a Docsify-based documentation project. Most user-facing content lives under `/docs` and is maintained as Markdown.

## Repository structure

- Keep Docsify content under `/docs`.
- The Docsify entry file is `/docs/index.html`.
- Root navigation lives in `/docs/_navbar.md` and `/docs/_sidebar.md`.
- Most top-level sections also have their own `README.md`, `_sidebar.md`, and `_navbar.md` files such as `/docs/java`, `/docs/linux`, `/docs/database`, and `/docs/springCloud`.
- `window.$docsify` in `/docs/index.html` enables `loadSidebar`, `loadNavbar`, `coverpage`, `notFoundPage`, Docsify search, Mermaid, tabs, count, and alias fallbacks for nested `_sidebar.md` and `_navbar.md` files. Do not break these conventions.

## Markdown rules

- Use UTF-8.
- Use standard Markdown / GitHub Flavored Markdown.
- Keep heading levels valid. Each document should normally have only one `#` heading.
- Do not skip heading levels.
- Use Chinese punctuation in Chinese prose.
- Keep technical terms, API names, class names, method names, commands, and configuration keys in their original English form.
- Wrap file names, class names, method names, commands, config keys, and literal values in backticks when they are referenced inline.
- Use the correct fenced code block language for shell, Java, JSON, YAML, SQL, Mermaid, and similar content.
- Do not change commands, code, or configuration inside code blocks unless the task explicitly requires it.
- Avoid empty headings, empty links, and placeholder text.

## Documentation style

- Write for technical knowledge recording, not for marketing.
- Keep content direct, accurate, and specific.
- Avoid AI-style filler, repeated summaries, and generic introductions.
- Prefer concrete examples, commands, versions, paths, and configuration snippets when they are known.
- If information cannot be confirmed from the repository or the request, say that it needs confirmation instead of guessing.
- Do not rewrite large sections only for tone. Preserve the author's intent unless there is a clear problem to fix.

## Docsify rules

- Preserve Docsify-specific syntax, including existing HTML snippets, target attributes, tabs, Mermaid blocks, and absolute section links such as `/java/` in navbars.
- For section sidebars, keep the current nested bullet-list style and relative link style.
- When adding a new document to an existing section, update the nearest section `_sidebar.md` when the page should appear in navigation.
- Only update `/docs/_navbar.md` when a new top-level section is added or an existing top-level entry becomes invalid.
- Keep link targets relative to `/docs` behavior. Sidebar links should resolve from the sidebar file location, and navbar links should keep the current Docsify absolute route style.

## Working rules for Copilot

- Before creating a new document, inspect nearby directories and search for similar pages to avoid duplicates.
- When reviewing or updating a document, change only clear problems or confirmed outdated facts.
- When translating a document, preserve code blocks, commands, links, file names, and configuration values.
- Validate changed documentation links with `python .github/scripts/check_docs_links.py <paths...>`.
- If a task touches navigation, check the related `_sidebar.md` or `_navbar.md` file before and after editing.
