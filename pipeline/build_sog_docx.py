#!/usr/bin/env python3
"""Build the editable .docx from the Markdown source, via Pandoc.

This is the collaboration artifact — people editing the SOG in Word or
LibreOffice work from this file. It does not need publication-grade
pagination polish (that's the PDF's job); a plain `--toc` is enough, even
though its TOC field shows empty until whoever opens it updates fields
(completely normal for an editable Word document).

Usage: python build_sog_docx.py [output.docx]
Requires: pandoc on PATH.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from common import DOC_BASENAME, REFERENCE_DOCX, load_preprocessed_source


def main() -> None:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"{DOC_BASENAME}.docx")

    md_text = load_preprocessed_source()

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(md_text)
        tmp_path = Path(tmp.name)

    try:
        print(f"Building {out_path} ...")
        subprocess.run(
            [
                "pandoc",
                str(tmp_path),
                "--from=gfm+attributes",
                "--to=docx",
                f"--reference-doc={REFERENCE_DOCX}",
                "--toc",
                "--toc-depth=2",
                "--standalone",
                "-o",
                str(out_path),
            ],
            check=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)

    print(f"Done -> {out_path}")


if __name__ == "__main__":
    main()
