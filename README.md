# Joint Fire 3 & 8 SOGs

This repository contains the Standard Operating Guidelines (SOGs) for Joint Fire Protection District 3 & 8, a rural fire department in Washington.

The Markdown master (`sog-1st-pass.md`) is built into a PDF and an editable DOCX by the pipeline under `pipeline/`.

The published site is https://johnspeare.github.io/joint-38/.

## Project

The project is in a **maintenance and output-polish phase**, plus editorial passes. A second editorial pass (modal-term standardization, WAC corrections, new respirator procedures, Review Notes) was applied and published in November 2026 per `38_STYLE_GUIDE.md`.

## Current scope

The substantive SOG formatting/porting work is complete.

Remaining work is limited to:

1. Improving display and formatting of existing assets.
2. Fixing or documenting remaining presentation issues.
3. Improving the manual Git workflow so the user can reliably build/deploy from a terminal or Git console.

### Explicitly out of scope

* Do **not** build a web application.
* Do **not** create new application features or assets.
* Further editorial changes to SOG content, and applying `38_STYLE_GUIDE.md`, only when explicitly asked. Policy decisions stay with the Chief (see `sog-review-decisions.md`).
* Do not redesign the project architecture unless the user explicitly requests it.

The goal is to **improve the existing project, not expand its scope**.

---

## Source of truth

* `sog-1st-pass.md` — Markdown master and source of truth. The filename is kept because the pipeline reads it; it now holds the edited draft.
* `sog-review-decisions.md` — the Chief's decision log.
* `open-issues.md` — current outstanding issues and deferred work.
* `pipeline/` — current production output pipeline.
* `FD-SOGs-assets/` — existing source and generated assets.
* `38_STYLE_GUIDE.md` — editorial guidance used for the November 2026 pass. Apply it only when explicitly asked.

**This file (`README.md`) defines the current scope.**

---

## Working rules

### Minimize scope

Make the smallest change that solves the requested problem.

Do not refactor working code merely for style.

Do not modify unrelated files.

Do not introduce new dependencies or tools unless necessary and approved.

### Protect SOG content

Do not change SOG wording during formatting or output-only work. `38_STYLE_GUIDE.md` §19 governs that limit, substantive content problems, uncertainty about content or formatting, Chief policy decisions, leadership items, and cite-checks of regulatory and standards references.

### Investigate before modifying

For non-trivial problems:

1. Identify the relevant source, pipeline code, and generated output.
2. Determine the likely cause.
3. Explain the proposed change briefly.
4. Make the smallest appropriate change.
5. Rebuild the affected output.
6. Verify the result.

Prefer a small trial change followed by verification over a large speculative redesign.

### Generated files

Do not manually edit generated PDF, DOCX, or other build artifacts to fix a problem that belongs in the source or build pipeline.

Modify the source or pipeline and regenerate the artifact.

---

## Production pipeline

The current production pipeline is under:

```text
pipeline/
```

Typical builds:

```bash
.venv/bin/python pipeline/build_sog_docx.py
.venv/bin/python pipeline/build_sog_pdf.py
```

The old root-level:

```text
build_sog_pdf.py
```

is retained for local formatting experiments/comparisons. It is **not** the production pipeline.

The published site is deployed through GitHub Actions/GitHub Pages from `main`.

Cover revision text is `TITLE_PAGE_REVISION` in `pipeline/common.py`. Update it when issuing a new revision.

Footer text is `FOOTER_NOTICE` in `pipeline/build_reference.py`. Changing it requires regenerating `pipeline/reference.docx`:

```bash
.venv/bin/python pipeline/build_reference.py
```

A push to `main` that touches `sog-1st-pass.md`, `FD-SOGs-assets/**`, `pipeline/**`, or `.github/workflows/publish.yml` triggers the GitHub Actions build and deploy. The jobs have timeouts. If the apt install step hangs, cancel the run and re-run it.

Do not replace the existing pipeline or introduce a new deployment architecture unless explicitly requested.

---

## Output verification

When changing output formatting, verify the actual generated artifact.

For PDF inspection:

```bash
pdftotext -layout <file>.pdf /tmp/preview.txt
```

For visual inspection of selected pages:

```bash
pdftoppm -png -r 100 -f <start> -l <end> <file>.pdf /tmp/pg
```

Use visual inspection when the issue involves:

* page breaks
* pagination
* tables
* nested lists
* images
* spacing
* headers or footers
* TOC
* typography
* page numbering

Do not assume a successful build means the output is correct.

---

## Existing technical constraints

Several technical problems have already been investigated and have intentional workarounds.

Important examples include:

* Mermaid SVG output has compatibility issues with the PDF renderer; the existing SVG/PNG workaround is intentional.
* Tall images require the existing image sizing constraints.
* Long tables require appropriate table-header handling for page continuation.
* The project uses a local `.venv`; do not install project Python dependencies globally.
* The generated SVG and PNG versions of the chain-of-command diagram must remain synchronized when that source is changed.

Do not remove an existing workaround simply because it appears unusual. Determine why it exists first.

---

## Git and deployment

Git/deployment improvements are currently in scope.

The desired workflow is **simple manual deployment from a terminal/Git console**, not a new automation system.

When working on Git:

* Do not commit changes unless explicitly asked.
* Do not push changes unless explicitly asked.
* Do not reset, rebase, force-push, or rewrite history without explicit approval.
* Be especially cautious with commands that discard working-tree changes.
* Prefer simple, reversible commands.
* Explain potentially destructive commands before running them.

The user wants a workflow that makes it easy to manually build, commit, and deploy the existing project.

---

## Open issues

`open-issues.md` is the authoritative tracker for known outstanding issues.

Before beginning work on an issue:

1. Read the relevant entry.
2. Determine whether it is still applicable.
3. Make the smallest appropriate change.

When discovering a new problem that is intentionally deferred, record it in `open-issues.md`.

Do not silently accumulate known problems outside the issue tracker.

---

## Interaction style

The user prefers:

* direct, concise explanations
* practical recommendations
* minimal filler
* copy/paste-ready commands
* one recommended approach rather than a long list of alternatives
* explicit warnings for destructive operations

When there are multiple viable approaches:

1. Briefly identify the tradeoff.
2. Recommend one.
3. Proceed with the recommended approach unless the decision requires user approval.

Do not over-explain routine operations.

---

## Change discipline

Before making changes, consider whether the requested result can be achieved without modifying code.

Prefer, in order:

1. Existing configuration.
2. Existing pipeline behavior.
3. Small targeted code changes.
4. Larger architectural changes only when necessary.

Do not turn a presentation problem into an architectural project.

---

## Before finishing a task

Confirm:

1. Only relevant files were changed.
2. No unintended SOG content changes were introduced.
3. Required generated outputs were rebuilt.
4. The generated output was actually checked when applicable.
5. Deferred problems were recorded in `open-issues.md`.
6. No unnecessary dependencies or tools were introduced.
7. Git history was not modified unless explicitly requested.
8. The requested task is actually complete before proposing unrelated improvements.
