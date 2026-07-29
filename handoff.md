# FD SOGs — Session Handoff

You're picking up a project that converts a rural fire department's **Standard Operating Guidelines** from a Microsoft Word `.doc` file into a clean Markdown master and a print-ready PDF. This doc gets you productive fast.

Everything below assumes you have shell + file access to `/Users/jspeare/38/` (rename the path if the workspace is elsewhere on the new machine).

---

## 1. What this project is

- **Client:** Joint Fire Protection District 3 & 8 (rural, Washington State).
- **Deliverables:**
  1. `FD SOGs.md` — the Markdown master of the SOG manual. Single source of truth.
  2. `FD-SOGs.pdf` — a print-ready PDF built from that markdown via `build_sog_pdf.py`.
  3. Eventually: a web version (HTML site) too, though not yet wired up.
- **Phase we're in:** **format porting**, not content editing. The user is very clear about this — see [§8 Working conventions](#8-working-conventions) below.

---

## 2. Current state

- **`FD SOGs.md`** — 2,949 lines. Structure: 1 H1 (title) · 32 H2 (major sections) · 86 H3 (subsections) · 41 H4 (sub-subsections, all inside `## Incident Guidelines`).
- **`FD-SOGs.pdf`** — 87 pages, letter portrait, ~340 KB. Auto-generated title page → 2-page TOC → body → 5 appendices. Chain-of-command org chart renders correctly (see [§9](#9-key-gotchas-and-workarounds) about the SVG→PNG workaround).
- **`open-issues.md`** — has 3 content-bug entries (**C1**–**C3**) and 4 formatting-cleanup entries (**F1**–**F4**). Each entry is deferred, not blocking. Read this first when planning the next work session.

The doc is publication-ready except for the items in `open-issues.md`. Format-porting is essentially done; the remaining work is either **content review** (SOG-author decisions) or **optional cleanup** (F1–F4).

---

## 3. File inventory

```
/Users/jspeare/38/
├── FD SOGs.doc              Original Word source. DO NOT edit. Reference only.
├── FD SOGs.md               Markdown master. This is the source of truth going forward.
├── FD-SOGs.pdf              Latest PDF build output. Rebuild anytime; not hand-edited.
├── FD-SOGs-assets/          Referenced by FD SOGs.md.
│   ├── chain-of-command.mmd   Mermaid source for the org chart (editable).
│   ├── chain-of-command.svg   Generated SVG. Used by HTML/web renders.
│   └── chain-of-command.png   Generated PNG. Used by the PDF pipeline (see §9).
├── build_sog_pdf.py         Python script that renders FD SOGs.md → FD-SOGs.pdf.
├── open-issues.md           Outstanding work tracker (content bugs + formatting cleanup).
├── 38_STYLE_GUIDE.md        Style guide for a future *content-editing* phase.
│                            NOT relevant to the current format-porting phase.
├── handoff.md               This file.
└── .venv/                   Local Python env with `markdown` + `weasyprint`.
                             Rebuild on new machine (see §4).
```

---

## 4. Environment setup on a new machine

This project uses macOS-specific paths (Homebrew on Apple Silicon). For Linux, substitute your distro's package manager and adjust paths.

### macOS (Apple Silicon)

```bash
# 1. System libraries WeasyPrint depends on.
brew install pango cairo gdk-pixbuf glib harfbuzz

# 2. A non-SIP Python (system /usr/bin/python3 has DYLD env vars stripped
#    and fails to load the Homebrew libraries above — see §9).
brew install python@3.14

# 3. Optional but recommended: tooling for regenerating assets.
brew install poppler          # provides pdfinfo, pdftoppm, pdftotext for previewing PDFs
brew install mermaid-cli      # mmdc; used to regenerate the chain-of-command diagram

# 4. Project venv.
cd /path/to/38
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/pip install markdown weasyprint
```

### Linux (Debian/Ubuntu, for reference)

```bash
sudo apt install libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libgdk-pixbuf2.0-0 libharfbuzz0b
sudo apt install python3-venv poppler-utils
# npm i -g @mermaid-js/mermaid-cli   # only if you need to regenerate the org chart
cd /path/to/38
python3 -m venv .venv
.venv/bin/pip install markdown weasyprint
```

### Verifying the setup

```bash
cd /path/to/38
.venv/bin/python -c "import markdown, weasyprint; print(markdown.__version__, weasyprint.__version__)"
# Expected on a fresh install today: 3.10.2  69.0
```

---

## 5. Build pipeline

Rebuild the PDF anytime with:

```bash
cd /path/to/38
.venv/bin/python build_sog_pdf.py
# → writes FD-SOGs.pdf in the same directory
```

Custom I/O:

```bash
.venv/bin/python build_sog_pdf.py "FD SOGs.md" some-output.pdf
```

Regenerating the chain-of-command chart (only if the `.mmd` changes):

```bash
cd FD-SOGs-assets
mmdc -i chain-of-command.mmd -o chain-of-command.svg -b white
mmdc -i chain-of-command.mmd -o chain-of-command.png -b white --width 800 --scale 3
```

**Both SVG and PNG must be regenerated together.** SVG is for HTML/web consumers; PNG is what the PDF pipeline actually uses (see [§9](#9-key-gotchas-and-workarounds)).

Previewing PDF pages during iteration:

```bash
# Extract text of the full PDF for grep-based location:
pdftotext -layout FD-SOGs.pdf preview.txt

# Rasterize specific pages as PNG for visual review:
pdftoppm -png -r 100 -f 8 -l 8 FD-SOGs.pdf /tmp/pg   # renders page 8 → /tmp/pg-08.png
```

---

## 6. What's been done (chronological)

1. **`.doc` → `.md` port.** `soffice` converted `.doc` → `.docx`, then `pandoc` converted `.docx` → GFM. Strict format-only port, no content changes.
2. **Chain-of-Command flowchart re-created.** Pandoc dropped the Word SmartArt drawing during conversion. Rebuilt as a Mermaid diagram (`FD-SOGs-assets/chain-of-command.mmd`) from the Job Descriptions section of the SOG, and generated SVG + PNG artifacts.
3. **Front matter cleaned.** Doc title normalized to a single H1. Inline TOC removed from the source (replaced with an HTML comment placeholder that the PDF build script substitutes for `[TOC]` at build time). TOC now generates at publication time — not persisted in the .md.
4. **Heading hierarchy standardized.** 32 top-level sections converted from bold text to `##`. 86 subsection heads converted from bold to `###`. 41 sub-subsections inside `## Incident Guidelines` demoted to `####` for correct hierarchy.
5. **Reverts / cleanup on the heading pass.**
   - 3 italic instruction paragraphs (`***text***`) that got incorrectly promoted to `### *text*` were reverted.
   - 2 multi-sentence policy paragraphs that got promoted to `###` were reverted to bold body paragraphs.
   - 6 body sentences that ended with `:` and got over-promoted to `###` were reverted (Fire apparatus operator list intro, sexual harassment list intros, Part B extended heading, "This is documenting an:", etc.).
6. **Pandoc blockquote artifacts fixed.** 9 mis-converted blockquotes (Word's indented paragraphs → pandoc `>` blockquotes) were converted to proper Markdown list continuations or nested sub-lists.
7. **Address block de-blockquoted.** The State-of-Washington Equal Rights Agency address (in the harassment section) was extracted from a blockquote and formatted with explicit line breaks.
8. **Appendix C questionnaire tabelized.** The multi-page OSHA `29 CFR 1910.134 Appendix C` questionnaire was converted from prose "Yes / No" bullets into GFM pipe tables — 2 tables in Part A (Q1–Q9, Q10–Q15) and 4 tables in Part B, interspersed with plain paragraphs for the multi-select / fill-in questions.
9. **Appendix headings normalized (Option B).** All five appendix H2s merged their descriptive subtitle into the heading itself: e.g. `## APPENDIX A` + `**PERSONAL PROTECTIVE EQUIPMENT**` + `**EMPLOYEE TRAINING CERTIFICATION**` collapsed into `## Appendix A: Personal Protective Equipment Training Certification`. Appendix B kept its `Section 1910.1030` regulatory citation as an italic subtitle.
10. **`open-issues.md` created.** Populated with 3 content bugs + 4 formatting cleanups. See [§7](#7-whats-still-open) below.
11. **PDF build pipeline created (`build_sog_pdf.py`).** WeasyPrint-based, python-markdown for HTML conversion. Includes auto-generated TOC via `target-counter()` for real page numbers with leader dots, styled title page, per-page footer with "UNCONTROLLED WHEN PRINTED" + page X of Y, dark-red heading accent (fire-dept convention). H1 pushed down 2.5in on the title page; TOC on new page(s); body flows naturally without forced page breaks between sections.
12. **TOC scoped to H2-only.** `toc_depth: "2-2"` — clean 30-entry list of top-level sections. TOC fits in 2 pages.

---

## 7. What's still open

Everything is in **`open-issues.md`** — read that file directly for full context. Summary:

| ID | Kind | Summary | Blocking? |
|---|---|---|---|
| C1 | Content bug | State-of-Washington agency block references Wisconsin (address, phone, statute URL all point to WI). Template origin. | No (deferred) |
| C2 | Content bug | Stray `**HF**` fragment in the Rehab section — aborted edit in Word source. | No (deferred) |
| C3 | Content bug | Appendix D fit-testing table is missing its Quantitative (QNFT) column — pandoc dropped it, or template only had QLFT. | No (deferred) |
| F1 | Formatting | 29 pandoc `<!-- -->` list separators to convert into proper Markdown nested lists. | No |
| F2 | Formatting | 3 raw HTML `<table>` blocks (mission-statement SERVICE grid, Appendix D fit-testing, Appendix E injury-cause) to convert to GFM pipe tables. | No |
| F3 | Formatting | 67 escaped-underscore fill-in blanks (`\_\_\_`). Working as intended; recommended to leave. | No |
| F4 | Formatting | 3 escaped-period ordered-list markers (`1\.`). Trivial cosmetic. | No |

All are non-blocking for a first publication. C1–C3 need the SOG author or Chief; F1–F2 are agent-executable.

---

## 8. Working conventions

The user's operating style — read this before your first change.

- **Minimize content changes.** The prime directive during this phase. Format-only edits are default; anything that alters what the SOG *says* needs justification and usually goes in `open-issues.md` for the SOG author to decide. When in doubt, log it, don't fix it.
- **Be honest about tradeoffs.** Present options with pros/cons, then make a recommendation. Don't wall-of-text the user with alternatives — pick a default, explain briefly, and offer to change.
- **Prefer "trial-run + iterate" over "one perfect design pass."** The user opened the PDF build script as a "trial run at building a pdf" — they want to see something working quickly, then critique. Ship, then polish.
- **Tone: dry, direct, concise.** Match what the user's messages sound like: short, imperative, no filler. Don't over-explain. No emojis.
- **Bias against side effects.** Don't proactively install things, run destructive commands, or commit to git without an explicit ask. Read + edit + local run = OK; anything that touches the network or shared state = ask first.
- **Track everything you defer.** If you notice a problem and don't fix it in this pass, put it in `open-issues.md`. The user relies on that file to be complete.

---

## 9. Key gotchas and workarounds

Things that will burn hours if you don't know them:

### macOS SIP strips `DYLD_*` env vars from the system Python

`/usr/bin/python3` on Apple Silicon is SIP-protected. That means:
- `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 ...` **does not work** — the env var is silently stripped before Python starts, and WeasyPrint fails with `cannot load library 'libgobject-2.0-0'` even though the library is installed via Homebrew.
- **Workaround:** use the Homebrew Python (`/opt/homebrew/bin/python3` on Apple Silicon), which is NOT SIP-protected. This project's `.venv` is built from that interpreter. If you rebuild the venv, use the Homebrew Python.

### PEP 668 blocks `pip install` on Homebrew Python

- `/opt/homebrew/bin/python3 -m pip install --user X` will error out with "externally-managed-environment".
- **Workaround:** use the project venv (`.venv`). Never do global installs.

### Mermaid CLI v11 always emits `<foreignObject>` labels

Mermaid renders flowchart node labels inside `<foreignObject>` tags with embedded HTML. That's fine in browsers, but **WeasyPrint's SVG rasterizer silently drops `<foreignObject>` content**, leaving the SVG shell with invisible labels.
- The `flowchart.htmlLabels: false` config option and the `%%{init: ...}%%` directive both **do not fix this in Mermaid 11** — foreignObjects are always emitted. We tried; skip re-trying.
- **Workaround:** the build script (`build_sog_pdf.py`) scans the generated HTML for `<img src="foo.svg">` and, if a `foo.png` file exists next to the SVG on disk, rewrites the `src` to `.png` before feeding HTML to WeasyPrint. HTML/web consumers still get the crisp SVG. See `_swap_svgs_for_pngs()` in the script.
- **When you edit the `.mmd`, regenerate BOTH the SVG and the PNG** (both commands listed in the header comment of `chain-of-command.mmd` and in [§5](#5-build-pipeline) above).

### Tall images blow up the PDF page count

WeasyPrint respects `max-width: 100%` on images, so a portrait-oriented image (like the chain-of-command tree) will scale to full column width and can then span multiple pages vertically.
- **Fix already applied:** in `build_sog_pdf.py` CSS, `img` has both `max-width: 100%` and `max-height: 6.5in`, plus `width: auto; height: auto` for proportional scaling. Don't remove.

### Long HTML tables need explicit `thead { display: table-header-group }`

Pandoc's HTML tables from the docx source use `<tr><td>` for headers (no `<thead>`), so header rows don't repeat when a table splits across pages. Some of our tables don't have header rows at all (they're layout grids). The current CSS handles this, but if you convert an HTML table to GFM (F2 item), make sure the header row is preserved with `|:---|:---|` separator syntax so WeasyPrint recognizes it as `<thead>` and repeats it on continuation pages.

---

## 10. Recommended next steps

In priority order:

1. **Nothing, if the user wants to ship as-is.** The PDF is publication-ready.
2. **Get sign-off on `open-issues.md` C1–C3 from the SOG author or Chief.** These need domain input.
3. **Do F1 (pandoc list separators) and F2 (HTML tables → GFM).** Both are agent-executable, one-time cleanup, and improve diff-ability of the source going forward. Do F1 before F2 because F2's Appendix D work will get simpler if list nesting is already correct.
4. **If a web version is needed**, evaluate MkDocs Material or Docusaurus. The current `.md` is portable — main things to plan for are (a) how to render `[TOC]` in the chosen pipeline, (b) whether the SVG chain-of-command renders correctly (it should — foreignObjects work fine in browsers), and (c) publishing pipeline.
5. **Content-editing phase.** Only after the format phase is fully signed off. The user has `38_STYLE_GUIDE.md` prepared for this — it's an editor persona / rulebook for making the SOG language authoritative, imperative, and rural-context-aware. Treat that as a separate project phase.

---

## Handy one-liners for a fresh session

```bash
# See the shape of the doc:
rg -c "^# |^## |^### |^#### " "FD SOGs.md"

# List all H2 sections:
rg -n "^## " "FD SOGs.md"

# Full-doc word count:
wc -w "FD SOGs.md"

# Detect pandoc leftover patterns (F1, F2, F4):
rg -c "<!-- -->" "FD SOGs.md"          # F1: list separators
rg -n "^<table" "FD SOGs.md"           # F2: HTML tables
rg -n '^[0-9]+\\\.' "FD SOGs.md"       # F4: escaped ordered-list markers

# Rebuild PDF:
.venv/bin/python build_sog_pdf.py

# Preview a page range:
pdftoppm -png -r 100 -f 2 -l 4 FD-SOGs.pdf /tmp/pg && open /tmp/pg-02.png
```
