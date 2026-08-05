"""Shared constants and Markdown preprocessing for the docx/PDF build pipeline.

Both build_sog_docx.py and build_sog_pdf.py start from the same Markdown
source and need the same two fixups before handing it to Pandoc:

1. Swap the chain-of-command SVG for its PNG counterpart. Word/LibreOffice's
   SVG support can't render mermaid-cli's <foreignObject> node labels any
   more reliably than WeasyPrint could (see handoff.md §9) — same
   workaround, same PNG asset, new consumer.
2. Cap that image's height. Pandoc places images at native pixel size with
   no default max-height, so the chain-of-command PNG (546x1986px) gets
   inserted at ~21 inches tall and spills across several pages. A single
   `{height=...}` attribute (needs the `attributes` Pandoc extension) fixes
   it, matching the `max-height: 6.5in` rule already in the old WeasyPrint
   CSS.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

DOC_BASENAME = "Joint Fire 3&8 Standard Operating Guide DRAFT"
TITLE_PAGE_LINE_1 = "Joint Fire Protection 3 & 8"
TITLE_PAGE_LINE_2 = "Standard Operating Guidelines"
TITLE_PAGE_REVISION = "Revised Summer 2026"
TITLE_LOGO_SIZE = Inches(3.25)

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "FD-SOGs-assets"
SOURCE_MD = REPO_ROOT / "sog-1st-pass.md"
REFERENCE_DOCX = Path(__file__).resolve().parent / "reference.docx"

_CHAIN_OF_COMMAND_RE = re.compile(
    r"!\[([^\]]*)\]\(FD-SOGs-assets/chain-of-command\.svg\)"
)


def preprocess_markdown(md_text: str) -> str:
    """Apply the docx/PDF-only fixups described above to Markdown source text."""
    png_path = (ASSETS_DIR / "chain-of-command.png").as_posix()

    def _swap(m: re.Match[str]) -> str:
        alt = m.group(1)
        return f"![{alt}]({png_path}){{height=6in}}"

    return _CHAIN_OF_COMMAND_RE.sub(_swap, md_text)


def load_preprocessed_source() -> str:
    md_text = SOURCE_MD.read_text(encoding="utf-8")
    return preprocess_markdown(md_text)


def restyle_title_page(docx_path: Path) -> None:
    """Post-process a Pandoc-generated docx's title page (shared by both builds).

    Pandoc has no concept of "the cover page" — the H1 and the logo that
    follows it are just the first two paragraphs of the body. This finds
    them structurally (the H1 is unique in this document) and rewrites:
    the title to a short, centered, two-line form; the logo, centered and
    enlarged; and adds a centered "Revised ..." line pushed down near the
    bottom of the page via paragraph spacing (no true frame/anchor needed
    since it's the only content on the page other than the title/logo).
    """
    doc = Document(str(docx_path))

    paragraphs = doc.paragraphs
    h1 = next(p for p in paragraphs if p.style.name == "Heading 1")
    h1_index = paragraphs.index(h1)
    image_paragraph = paragraphs[h1_index + 1]

    for run in list(h1.runs):
        run._r.getparent().remove(run._r)
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.add_run(TITLE_PAGE_LINE_1)
    h1.add_run().add_break()
    h1.add_run(TITLE_PAGE_LINE_2)

    image_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_shape = doc.inline_shapes[0]
    logo_shape.width = TITLE_LOGO_SIZE
    logo_shape.height = TITLE_LOGO_SIZE

    revision_p = doc.add_paragraph()
    revision_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    revision_p.paragraph_format.space_before = Inches(3.3)
    run = revision_p.add_run(TITLE_PAGE_REVISION)
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    image_paragraph._p.addnext(revision_p._p)

    doc.save(str(docx_path))
