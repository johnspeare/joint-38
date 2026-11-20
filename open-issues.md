# FD SOGs — Open Issues

Running tracker for outstanding work on `sog-1st-pass.md`. Two kinds of items live here:

1. **Content bugs** — defects in the *source material* (the original Word doc, plus later editorial decisions still awaiting the Chief). Fixing these actually changes what the SOG says. Needs sign-off from the SOG author or Chief.
2. **Formatting cleanup** — leftovers from the `.doc` → `.docx` → Markdown conversion pipeline, plus later output nits. Fixing these does not change what the SOG says; they're pure cosmetics/structure and can be done anytime.

Each entry cites its location by section anchor (e.g. `## Foo` → `### Bar`) rather than line numbers, since line numbers drift as edits accumulate.

## Status legend

- **Open** — issue identified, no action taken.
- **Verified** — confirmed as a real defect (not a false positive) and awaiting fix.
- **Deferred** — real issue, intentionally not fixing this pass.
- **Fixed** — corrected in `sog-1st-pass.md`.

---

# Part 1 — Content bugs (source material)

## C1 · State-of-Washington agency block references Wisconsin

- **Status:** Fixed
- **Evidence (2026-11-20):** No Wisconsin, Madison, 608, `dwd.wisconsin`, or `folio.legis` hits in `sog-1st-pass.md`. `## Equal Opportunity, Discrimination, and Harassment` → `### Complaint Procedures` names the Washington State Human Rights Commission (`hum.wa.gov`, Olympia and Spokane); `### Retaliation` cites RCW 49.60.210 on `app.leg.wa.gov`. Chapter 49.60 RCW / RCW 49.60.180 is also cited in the section intro.
- **Location:** `## Equal Opportunity, Discrimination, and Harassment` → `### COMPLAINT PROCEDURES`, in the "State of Washington Equal Rights Agency" block.
- **Symptoms:** The section names the *State of Washington Equal Rights Agency* but the address, phone, and web link all point to a **Wisconsin** state agency (`Madison, WI 53703`, area code 608, `dwd.wisconsin.gov`). Later in the same section, `RETALIATION` cites "Section 111.322 (2m), Washington Statutes" but the hyperlink target is `folio.legis.state.wi.us` (Wisconsin state legislature).
- **Likely cause:** The template was copied from a Wisconsin fire department SOG and only partially re-branded to Washington.
- **What needs to change:** Replace with the correct Washington state agency (probably the Washington State Human Rights Commission — `hum.wa.gov`, Olympia address) and the correct Washington statute citation for retaliation under RCW 49.60.
- **Owner:** SOG author / Chief.

## C2 · Stray "HF" fragment in Rehab section

- **Status:** Fixed
- **Evidence (2026-11-20):** No `**HF**` hit in `sog-1st-pass.md`. Text between `#### Establishment of Rehab` and `#### Staffing of Rehab` is the rehab-factors list and the Rehab Manager sentence; the fragment is gone.
- **Location:** `## Incident Guidelines` → `### Rehab`, between the `#### Establishment of Rehab` paragraph and the `#### Staffing of Rehab` heading. The current line reads simply `**HF**`.
- **Symptoms:** An unexplained two-letter bold fragment appears mid-section with no context, no preceding sentence, and no following expansion.
- **Likely cause:** An aborted edit in the Word source — possibly a placeholder for "Heat/Fire" or "Heat-related Factors" or the start of a paragraph that was never finished.
- **What needs to change:** Either delete the line or complete the intended content.
- **Owner:** SOG author.

## C3 · Appendix D fit-testing table is missing its Quantitative (QNFT) column

- **Status:** Deferred
- **Evidence (2026-11-20):** Still absent. `## Appendix D: Fit Testing Record` has only a **Qualitative (QLFT)** heading, substance list (Isoamyl Acetate, Saccharin Solution Aerosol, Bitrex, Irritant smoke), then `Pass Fail`, `Exercises Performed:`, and `Comments:`. No `QNFT` or `Quantitative` text anywhere in `sog-1st-pass.md`. The old HTML `<table>` is gone (see F2); the missing column was not restored.
- **Location:** `## Appendix D: Fit Testing Record`. The pandoc HTML table that follows the four fill-in-blank fields (`Date of test`, `Employee Fit Tested`, `Make Style`, `Model Size`).
- **Symptoms:** The table on-page has a single column labeled **Qualitative (QLFT)** with substances listed (Isoamyl Acetate, Saccharin Solution Aerosol, Bitrex, Irritant smoke) followed by `Pass Fail`, `Exercises Performed:`, `Comments:`. OSHA-compliant fit-testing forms have a *second* column headed **Quantitative (QNFT)** with its own substance list, pass/fail, and exercises fields. That column is not present in the source.
- **Likely cause:** The Word source's original two-column layout collapsed during the `.doc` → `.docx` → Markdown pandoc conversion (pandoc's HTML-table emitter can drop empty or complex cells), or the original template only ever had QLFT.
- **What needs to change:** Restore the QNFT column so both fit-testing methods have their own fields. Suggested structure: two side-by-side columns, each with substance list, pass/fail, exercises, and comments. Convert the whole table to a GFM pipe table while we're in there (see **F2** below — this is one of the three raw HTML tables to migrate anyway).
- **Owner:** SOG author (needs the source Word doc to confirm what the original template contained).

## C4 · Member assistance referral phone number

- **Status:** Open
- **Location:** `## Member Assistance Referral Program`
- **Summary:** The section gives Stevens County public health as the referral and the phone number 509-684-2262. Verify the number is current and the referral relationship still exists. Removed from the published Review Notes; still unresolved.
- **Owner:** Chief/SOG author.

## C5 · Communications radio system and dispatch

- **Status:** Open
- **Location:** `## Communications`
- **Summary:** Verify the Stevens County VHF system statement ("Stevens County currently runs on a VHF radio system that has repeated channels") and the Colville dispatch statement ("Stevens County Fire Dispatch is located in Colville") are current. Removed from the published Review Notes; still unresolved.
- **Owner:** Chief.

## C6 · Wildland incident-actions item 8 wording

- **Status:** Open
- **Location:** `## Incident Guidelines` → `### Wildland Fires` → `#### Incident Actions`, item 8
- **Summary:** The sentence formerly ended "...specialists/technicians as." It now reads "Collaborate with the DNR, Forest Service Officials, and specialists/technicians as needed." to match the parallel Hazmat incident-actions item. Confirm the wording.
- **Owner:** Chief.

## C7 · Rescue entry before a full team assembles

- **Status:** Open
- **Location:** `## Respiratory Protection` → `### Two-In/Two-Out`, and the `***NOTE:***` under `### Rapid Intervention Team (RIT)`
- **Summary:** The Two-In/Two-Out paragraph allows an Incident Commander to start rescue operations (entering) before the stated four-member crew is in place, and the RIT note allows emergency rescue activities before an entire team has assembled. WAC 296-305-05002(4) allows that only with at least three personnel (2-in/1-out) present and equipped, and only for a known rescue where immediate action could prevent loss of life or serious injury. Not changed, because it alters a safety requirement.
- **Owner:** Chief.

## C8 · Respiratory protection PLHCP blanks

- **Status:** Open
- **Location:** `## Respiratory Protection` → `### Medical Evaluation of Firefighters Required to Use Respirators`
- **Summary:** Providence Medical Center is named as the PLHCP for medical evaluations without contact information, and the two PLHCP blanks (questionnaire administration; follow-up exams) are empty. Still listed in published Review Notes item 1.
- **Owner:** Chief/department.

## C9 · Breathing-air standard and moisture criterion

- **Status:** Open
- **Location:** `## Respiratory Protection` → `### Quality and Quantity of Breathing Air`
- **Summary:** The section cites Compressed Gas Association G-7.1-1989 (minimum Grade D) and a dew point of -50 degrees F. WAC 296-305-04001(6) requires the 2003 edition of NFPA 1989 or the 1997 edition of ANSI/CGA G7-1 (minimum Grade D) and a water vapor level of 24 ppm or less. Still listed in published Review Notes item 2. Not changed.
- **Owner:** Chief.

## C10 · Stage B modal classification and permissive-as-mandatory rewrites

- **Status:** Open
- **Location:** Document-wide modal wording. Pending decisions are Punch List B and Punch List C in `sog-review-decisions.md` (also summarized under `## Review Notes` → `### Additional items observed but not changed (flagged for leadership review)`, item 3, Stage B).
- **Summary:** Stage B modal classification (`should` → `shall` where a recommendation is actually mandatory) and the permissive-as-mandatory rewrites (`may only`, `no ... may`, and similar) are pending the Chief's decisions on Punch Lists B and C. Not applied.
- **Owner:** Chief.

---

# Part 2 — Formatting cleanup (conversion leftovers)

## F1 · Pandoc `<!-- -->` list separators (29 instances)

- **Status:** Fixed
- **Evidence (2026-11-20):** `rg -c "<!-- -->" sog-1st-pass.md` returns no matches (no `<!--` comments remain). Was 29 in `FD SOGs.md`.
- **Symptoms:** Scattered across the doc are stray HTML comments (`<!-- -->`) that appear on their own line between list items. They render as nothing in most Markdown viewers, but they exist because pandoc had to inject them to prevent adjacent list items from being merged into one paragraph. This happens when the Word source used indented "sub-points" that were formatted as continuation paragraphs of a list item rather than as a proper nested list.
- **Detection:** `rg -c "<!-- -->" "FD SOGs.md"` → 29. Rechecked 2026-11-20 against `sog-1st-pass.md`: no matches.
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

- **Status:** Fixed
- **Evidence (2026-11-20):** `rg -c "^<table" sog-1st-pass.md` and a search for `<table` return no matches. Appendix D is a Markdown heading and list; Appendix E's cause-of-injury block is a pipe table.
- **Location & purpose:**
  - **Line 31** (approx.) — the officers/roster table in the front matter of the doc (the "who's who" of the department at time of publication).
  - **Line 2851** (approx.) — the fit-testing pass/fail grid in `## Appendix D: Fit Testing Record`.
  - **Line 2918** (approx.) — the "Cause of injury" checkbox grid in `## Appendix E: Injury/Incident Reporting Form`.
- **Symptoms:** These three tables came through as raw HTML (`<table><colgroup><tr><td>…</td></tr></table>`) rather than as GitHub-Flavored-Markdown pipe tables. HTML tables render fine in most Markdown viewers, but they break down in some pipelines (email clients, some static site generators, PDF exporters), and they're much harder to diff or edit.
- **Detection:** `rg -n "^<table" "FD SOGs.md"` → 3 hits. Rechecked 2026-11-20 against `sog-1st-pass.md`: no `<table` hits.
- **What needs to change:** Convert each of the three to GFM pipe-table syntax (`| col1 | col2 |` with `|:---|:---|` separator row). The Appendix D fit-testing grid may need multiple sub-tables similar to the Appendix C treatment.
- **Effort:** Small–medium. One-shot conversion per table.
- **Owner:** Whoever does the next formatting pass.

## F3 · Escaped-underscore fill-in-the-blank lines (~67 instances)

- **Status:** Open
- **Evidence (2026-11-20):** `rg -c '\\_\\_\\_' sog-1st-pass.md` → 69 (was 67 in `FD SOGs.md`). Still present in the appendix blanks.
- **Symptoms:** Fill-in-the-blank lines in the appendices render as long runs of escaped underscores, e.g. `Date\_\_\_\_\_\_\_\_\_\_\_`. This is functionally correct — pandoc escaped the underscores so they don't get interpreted as emphasis — and it renders as a visible blank line in every viewer we care about.
- **Detection:** `rg -c '\\_\\_\\_' "FD SOGs.md"` → 67. Rechecked 2026-11-20 against `sog-1st-pass.md`: 69.
- **What could change:** For an online HTML render, we could replace these with real underline styling (`<span style="border-bottom:1px solid #000;">&nbsp;&nbsp;&nbsp;…</span>`) or with actual empty form fields. For a print PDF, the current runs work fine.
- **Recommendation:** **Leave as-is unless publishing target changes.** Cosmetics only; no semantic loss.

## F4 · Escaped period on ordered-list markers (3 instances)

- **Status:** Open
- **Evidence (2026-11-20):** `rg -c '^[0-9]+\\\.' sog-1st-pass.md` → 3. The three lines are `4\.`, `5\.`, and `6\.` under `## Appendix C: Respiratory Protection — Medical Evaluation Questionnaire` → `### Part B.` (fill-in prompts, not a restored ordered list).
- **Symptoms:** A handful of ordered-list items begin with `1\.` / `2\.` / `3\.` (escaped period) instead of `1.` / `2.` / `3.`. This is a pandoc safety escape to prevent the number-plus-period from being *unintentionally* interpreted as an ordered-list start in a context where the paragraph was NOT actually a list item in Word.
- **Detection:** `rg -c '^[0-9]+\\\.' "FD SOGs.md"` → 3. Rechecked 2026-11-20 against `sog-1st-pass.md`: still 3 (now `4\.` / `5\.` / `6\.` in Appendix C Part B).
- **What could change:** Unescape the ones that *should* be list items (converts to real Markdown ordered lists) and leave the ones that are just "the number one, followed by a period" as literal text.
- **Effort:** Trivial — three spots, all easy to eyeball.

## F5 · Review Notes starts mid-page

- **Status:** Deferred
- **Location:** `## Review Notes`, immediately after `## Appendix E: Injury/Incident Reporting Form`
- **Summary:** In the November 2026 published PDF, Review Notes starts mid-page after the Appendix E form (no page break). The Markdown source has no page-break marker before `## Review Notes`. PDF pages were not re-rendered in the 2026-11-20 tracker pass.
- **Owner:** next formatting pass

## F6 · PDF has no Title/Author metadata

- **Status:** Deferred
- **Location:** Published PDF (built by `pipeline/build_sog_pdf.py` via LibreOffice). No Title or Author is set in that script.
- **Summary:** The November 2026 published PDF has no Title/Author metadata. Not re-checked with `pdfinfo` in the 2026-11-20 tracker pass.
- **Owner:** next formatting pass

## F7 · Appendix C Yes/No columns are wide

- **Status:** Deferred
- **Location:** `## Appendix C: Respiratory Protection — Medical Evaluation Questionnaire` (pipe tables headed `# | Question | Yes | No`, including `### Part A.` and `### Part B.`)
- **Summary:** In the November 2026 published PDF, the Appendix C questionnaire tables have a narrow Question column and wide Yes/No columns. Source tables were confirmed; column widths in the PDF were not re-measured in the 2026-11-20 tracker pass.
- **Owner:** next formatting pass

## F8 · Yes/No and Male/Female have no checkboxes

- **Status:** Deferred
- **Location:** `## Appendix C: Respiratory Protection — Medical Evaluation Questionnaire`, the header fields above `### Part A.` ("Yes No", "Male Female", and the later "Yes No" prompts)
- **Summary:** In the November 2026 published PDF, page ~70 "Yes No" / "Male Female" have no checkboxes. The source lines are plain text with no checkbox characters. The PDF page was not re-rendered in the 2026-11-20 tracker pass.
- **Owner:** next formatting pass

## F9 · "Qualitative (QLFT)" heading can strand

- **Status:** Deferred
- **Location:** `## Appendix D: Fit Testing Record`, the `**Qualitative (QLFT)**` heading
- **Summary:** In the November 2026 published PDF, the "Qualitative (QLFT)" heading can strand at the bottom of a page (p83). The heading is present in the source. Page placement was not re-rendered in the 2026-11-20 tracker pass.
- **Owner:** next formatting pass

## F10 · Cover revision line is small and gray

- **Status:** Deferred
- **Location:** Cover page. The line is `TITLE_PAGE_REVISION` in `pipeline/common.py` (`restyle_title_page`), set to 10 pt and RGB `0x55, 0x55, 0x55`.
- **Summary:** In the November 2026 published PDF, the cover revision line is small and gray. The pipeline sets that size and color; the PDF page was not re-rendered in the 2026-11-20 tracker pass.
- **Owner:** next formatting pass

---

## Housekeeping

Add new entries at the bottom of the relevant Part (1 or 2). Cite the section anchor (e.g. `## Foo` → `### Bar`) rather than raw line numbers so the tracker stays useful as the SOG evolves.
