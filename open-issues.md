# FD SOGs — Open Issues

Running tracker for outstanding work on `FD SOGs.md`. Two kinds of items live here:

1. **Content bugs** — defects in the *source material* (the original Word doc). Fixing these actually changes what the SOG says. Needs sign-off from the SOG author or Chief.
2. **Formatting cleanup** — leftovers from the `.doc` → `.docx` → Markdown conversion pipeline. Fixing these does not change what the SOG says; they're pure cosmetics/structure and can be done anytime.

Each entry cites its location by section anchor (e.g. `## Foo` → `### Bar`) rather than line numbers, since line numbers drift as edits accumulate.

## Status legend

- **Open** — issue identified, no action taken.
- **Verified** — confirmed as a real defect (not a false positive) and awaiting fix.
- **Deferred** — real issue, intentionally not fixing this pass.
- **Fixed** — corrected in `FD SOGs.md`.

---

# Part 1 — Content bugs (source material)

## C1 · State-of-Washington agency block references Wisconsin

- **Status:** Verified · deferred
- **Location:** `## Equal Opportunity, Discrimination, and Harassment` → `### COMPLAINT PROCEDURES`, in the "State of Washington Equal Rights Agency" block.
- **Symptoms:** The section names the *State of Washington Equal Rights Agency* but the address, phone, and web link all point to a **Wisconsin** state agency (`Madison, WI 53703`, area code 608, `dwd.wisconsin.gov`). Later in the same section, `RETALIATION` cites "Section 111.322 (2m), Washington Statutes" but the hyperlink target is `folio.legis.state.wi.us` (Wisconsin state legislature).
- **Likely cause:** The template was copied from a Wisconsin fire department SOG and only partially re-branded to Washington.
- **What needs to change:** Replace with the correct Washington state agency (probably the Washington State Human Rights Commission — `hum.wa.gov`, Olympia address) and the correct Washington statute citation for retaliation under RCW 49.60.
- **Owner:** SOG author / Chief.

## C2 · Stray "HF" fragment in Rehab section

- **Status:** Verified · deferred
- **Location:** `## Incident Guidelines` → `### Rehab`, between the `#### Establishment of Rehab` paragraph and the `#### Staffing of Rehab` heading. The current line reads simply `**HF**`.
- **Symptoms:** An unexplained two-letter bold fragment appears mid-section with no context, no preceding sentence, and no following expansion.
- **Likely cause:** An aborted edit in the Word source — possibly a placeholder for "Heat/Fire" or "Heat-related Factors" or the start of a paragraph that was never finished.
- **What needs to change:** Either delete the line or complete the intended content.
- **Owner:** SOG author.

## C3 · Appendix D fit-testing table is missing its Quantitative (QNFT) column

- **Status:** Verified · deferred
- **Location:** `## Appendix D: Fit Testing Record`. The pandoc HTML table that follows the four fill-in-blank fields (`Date of test`, `Employee Fit Tested`, `Make Style`, `Model Size`).
- **Symptoms:** The table on-page has a single column labeled **Qualitative (QLFT)** with substances listed (Isoamyl Acetate, Saccharin Solution Aerosol, Bitrex, Irritant smoke) followed by `Pass Fail`, `Exercises Performed:`, `Comments:`. OSHA-compliant fit-testing forms have a *second* column headed **Quantitative (QNFT)** with its own substance list, pass/fail, and exercises fields. That column is not present in the source.
- **Likely cause:** The Word source's original two-column layout collapsed during the `.doc` → `.docx` → Markdown pandoc conversion (pandoc's HTML-table emitter can drop empty or complex cells), or the original template only ever had QLFT.
- **What needs to change:** Restore the QNFT column so both fit-testing methods have their own fields. Suggested structure: two side-by-side columns, each with substance list, pass/fail, exercises, and comments. Convert the whole table to a GFM pipe table while we're in there (see **F2** below — this is one of the three raw HTML tables to migrate anyway).
- **Owner:** SOG author (needs the source Word doc to confirm what the original template contained).

---

# Part 2 — Formatting cleanup (conversion leftovers)

## F1 · Pandoc `<!-- -->` list separators (29 instances)

- **Status:** Verified · deferred
- **Symptoms:** Scattered across the doc are stray HTML comments (`<!-- -->`) that appear on their own line between list items. They render as nothing in most Markdown viewers, but they exist because pandoc had to inject them to prevent adjacent list items from being merged into one paragraph. This happens when the Word source used indented "sub-points" that were formatted as continuation paragraphs of a list item rather than as a proper nested list.
- **Detection:** `rg -c "<!-- -->" "FD SOGs.md"` → 29.
- **What needs to change:** Case-by-case, replace each `<!-- -->` with proper Markdown nested-list structure. In most cases the pattern is:
  ```
  1. Main item
  <!-- -->
      Continuation text that was originally a sub-point.
  ```
  → should become:
  ```
  1. Main item
     - Sub-point (nested list, 3-space indent for ordered-list continuation)
  ```
  or, if it's genuinely a continuation paragraph of the same item:
  ```
  1. Main item

     Continuation paragraph.
  ```
- **Effort:** Medium. Programmatic replacement is risky because the correct nesting depends on the surrounding context; needs a manual pass.
- **Owner:** Whoever does the next formatting pass.

## F2 · Three pandoc-generated HTML `<table>` blocks

- **Status:** Verified · deferred
- **Location & purpose:**
  - **Line 31** (approx.) — the officers/roster table in the front matter of the doc (the "who's who" of the department at time of publication).
  - **Line 2851** (approx.) — the fit-testing pass/fail grid in `## Appendix D: Fit Testing Record`.
  - **Line 2918** (approx.) — the "Cause of injury" checkbox grid in `## Appendix E: Injury/Incident Reporting Form`.
- **Symptoms:** These three tables came through as raw HTML (`<table><colgroup><tr><td>…</td></tr></table>`) rather than as GitHub-Flavored-Markdown pipe tables. HTML tables render fine in most Markdown viewers, but they break down in some pipelines (email clients, some static site generators, PDF exporters), and they're much harder to diff or edit.
- **Detection:** `rg -n "^<table" "FD SOGs.md"` → 3 hits.
- **What needs to change:** Convert each of the three to GFM pipe-table syntax (`| col1 | col2 |` with `|:---|:---|` separator row). The Appendix D fit-testing grid may need multiple sub-tables similar to the Appendix C treatment.
- **Effort:** Small–medium. One-shot conversion per table.
- **Owner:** Whoever does the next formatting pass.

## F3 · Escaped-underscore fill-in-the-blank lines (~67 instances)

- **Status:** Open · not necessarily worth fixing
- **Symptoms:** Fill-in-the-blank lines in the appendices render as long runs of escaped underscores, e.g. `Date\_\_\_\_\_\_\_\_\_\_\_`. This is functionally correct — pandoc escaped the underscores so they don't get interpreted as emphasis — and it renders as a visible blank line in every viewer we care about.
- **Detection:** `rg -c '\\_\\_\\_' "FD SOGs.md"` → 67.
- **What could change:** For an online HTML render, we could replace these with real underline styling (`<span style="border-bottom:1px solid #000;">&nbsp;&nbsp;&nbsp;…</span>`) or with actual empty form fields. For a print PDF, the current runs work fine.
- **Recommendation:** **Leave as-is unless publishing target changes.** Cosmetics only; no semantic loss.

## F4 · Escaped period on ordered-list markers (3 instances)

- **Status:** Open · low-priority cosmetic
- **Symptoms:** A handful of ordered-list items begin with `1\.` / `2\.` / `3\.` (escaped period) instead of `1.` / `2.` / `3.`. This is a pandoc safety escape to prevent the number-plus-period from being *unintentionally* interpreted as an ordered-list start in a context where the paragraph was NOT actually a list item in Word.
- **Detection:** `rg -c '^[0-9]+\\\.' "FD SOGs.md"` → 3.
- **What could change:** Unescape the ones that *should* be list items (converts to real Markdown ordered lists) and leave the ones that are just "the number one, followed by a period" as literal text.
- **Effort:** Trivial — three spots, all easy to eyeball.

---

## Housekeeping

Add new entries at the bottom of the relevant Part (1 or 2). Cite the section anchor (e.g. `## Foo` → `### Bar`) rather than raw line numbers so the tracker stays useful as the SOG evolves.
