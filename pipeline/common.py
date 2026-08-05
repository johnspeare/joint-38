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

DOC_BASENAME = "Joint Fire 3&8 Standard Operating Guide DRAFT"

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
