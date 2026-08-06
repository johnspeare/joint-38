#!/usr/bin/env python3
"""Build the print-ready PDF from the Markdown source, via Pandoc + LibreOffice.

Pipeline: Markdown -> (preprocessed) -> Pandoc -> intermediate .docx ->
LibreOffice headless (with a field-update macro) -> .pdf.

Two things this script does that build_sog_docx.py doesn't need to:

1. Places the title page, then the TOC, then the body — in that order, each
   on its own page. Pandoc's `--toc` flag always inserts the TOC before all
   body content, which is wrong here (it would put a page break-less title
   block after the TOC, bleeding into "Introduction"). Fixed by NOT using
   `--toc` and instead hand-inserting the identical TOC field as a raw
   OOXML block at the exact spot wanted, bracketed by explicit page breaks.
2. Runs the intermediate .docx through a LibreOffice Basic macro that
   forces every index/field (the TOC, the Page-of-Page footer) to
   recompute before export. LibreOffice's headless `--convert-to pdf` does
   NOT do this on its own — confirmed by spike testing; the TOC renders
   completely empty without this step (a documented upstream limitation:
   https://github.com/jgm/pandoc/issues/458).

Usage: python build_sog_pdf.py [output.pdf]
Requires: pandoc and soffice (LibreOffice) on PATH, `pip install python-docx`.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from common import (
    DOC_BASENAME,
    REFERENCE_DOCX,
    load_preprocessed_source,
    restyle_title_page,
    split_after_title_logo,
    use_letters_for_nested_lists,
)

PAGE_BREAK = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'

TOC_FIELD = '''
```{=openxml}
<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents" /><w:docPartUnique /></w:docPartObj></w:sdtPr><w:sdtContent><w:p><w:pPr><w:pStyle w:val="TOCHeading" /></w:pPr><w:r><w:t xml:space="preserve">Table of Contents</w:t></w:r></w:p><w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true" /><w:instrText xml:space="preserve">TOC \\o "1-2" \\h \\z \\u</w:instrText><w:fldChar w:fldCharType="separate" /><w:fldChar w:fldCharType="end" /></w:r></w:p></w:sdtContent></w:sdt>
```
'''

LO_MACRO_XBA = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">REM  *****  BASIC  *****

Sub ConvertDocxToPdfWithFieldUpdate(inPath As String, outPath As String)
    Dim oDesktop As Object
    Dim oDoc As Object
    Dim oArgs(0) As New com.sun.star.beans.PropertyValue
    Dim oExportArgs(0) As New com.sun.star.beans.PropertyValue

    oDesktop = createUnoService("com.sun.star.frame.Desktop")
    oArgs(0).Name = "Hidden"
    oArgs(0).Value = True
    oDoc = oDesktop.loadComponentFromURL(ConvertToURL(inPath), "_blank", 0, oArgs())

    Dim oIndexes As Object
    Dim i As Integer
    oIndexes = oDoc.getDocumentIndexes()
    For i = 0 To oIndexes.getCount() - 1
        oIndexes.getByIndex(i).update()
    Next i
    oDoc.getTextFields().refresh()

    oExportArgs(0).Name = "FilterName"
    oExportArgs(0).Value = "writer_pdf_Export"
    oDoc.storeToURL(ConvertToURL(outPath), oExportArgs())
    oDoc.close(False)
End Sub

Sub Run
    ConvertDocxToPdfWithFieldUpdate("{IN_PATH}", "{OUT_PATH}")
End Sub</script:module>
"""


def build_pdf_markdown(md_text: str) -> str:
    """Insert page-break -> TOC -> page-break right after the title+logo block
    that load_preprocessed_source() already inserted (see module docstring)."""
    head, rest = split_after_title_logo(md_text)
    return head + PAGE_BREAK + TOC_FIELD + PAGE_BREAK + rest


def run_pandoc_to_docx(md_text: str, out_docx: Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tmp:
        tmp.write(md_text)
        tmp_path = Path(tmp.name)
    try:
        subprocess.run(
            [
                "pandoc",
                str(tmp_path),
                "--from=gfm+attributes+raw_attribute",
                "--to=docx",
                f"--reference-doc={REFERENCE_DOCX}",
                "--standalone",
                "-o",
                str(out_docx),
            ],
            check=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


def convert_docx_to_pdf(in_docx: Path, out_pdf: Path) -> None:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        sys.exit("error: soffice (LibreOffice) not found on PATH")

    with tempfile.TemporaryDirectory() as profile_dir, tempfile.TemporaryDirectory() as macro_home:
        # Isolated, disposable LibreOffice profile — safe for CI, doesn't
        # touch (or depend on) the machine's real LibreOffice profile.
        user_installation = f"file://{profile_dir}"

        # Cold-start once so LibreOffice creates the Standard Basic library
        # skeleton (script.xlb, dialog.xlb, etc.) that our macro needs to
        # slot into.
        subprocess.run(
            [soffice, "--headless", f"-env:UserInstallation={user_installation}", "--terminate_after_init"],
            check=True,
            timeout=60,
        )

        module_path = Path(profile_dir) / "user" / "basic" / "Standard" / "Module1.xba"
        macro = LO_MACRO_XBA.replace("{IN_PATH}", xml_escape(str(in_docx))).replace(
            "{OUT_PATH}", xml_escape(str(out_pdf))
        )
        module_path.write_text(macro, encoding="utf-8")

        script_uri = "vnd.sun.star.script:Standard.Module1.Run?language=Basic&location=application"
        subprocess.run(
            [soffice, "--headless", "--invisible", f"-env:UserInstallation={user_installation}", script_uri],
            check=True,
            timeout=120,
        )

    if not out_pdf.is_file():
        sys.exit(
            f"error: {out_pdf} was not created — the LibreOffice macro likely failed silently "
            "(soffice exits 0 even when the invoked Basic macro errors out)"
        )


def main() -> None:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"{DOC_BASENAME}.pdf")

    md_text = build_pdf_markdown(load_preprocessed_source())

    with tempfile.TemporaryDirectory() as tmp_dir:
        intermediate_docx = Path(tmp_dir) / "intermediate.docx"
        print("Building intermediate .docx ...")
        run_pandoc_to_docx(md_text, intermediate_docx)
        restyle_title_page(intermediate_docx)
        use_letters_for_nested_lists(intermediate_docx)

        print(f"Converting to {out_path} (LibreOffice headless + field-update macro) ...")
        convert_docx_to_pdf(intermediate_docx, out_path.resolve())

    print(f"Done -> {out_path}")


if __name__ == "__main__":
    main()
