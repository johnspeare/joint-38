#!/usr/bin/env python3
"""Emit a minimal landing page linking to the built PDF/DOCX, for GitHub Pages.

Not the offline web app (see WEB_APP_NOTES.md) — that's a separate,
later deliverable. This is just enough HTML for the Pages root to serve
something useful instead of a 404.
"""

from __future__ import annotations

from urllib.parse import quote

from common import DOC_BASENAME

PDF_NAME = f"{DOC_BASENAME}.pdf"
DOCX_NAME = f"{DOC_BASENAME}.docx"
SOURCE_URL = "https://github.com/johnspeare/joint-38/blob/main/sog-1st-pass.md"

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Joint Fire Protection District 3 &amp; 8 — SOGs</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; max-width: 40rem; margin: 3rem auto; padding: 0 1rem; color: #111; }}
  h1 {{ color: #8B0000; font-size: 1.4rem; }}
  a {{ color: #8B0000; }}
  ul {{ line-height: 2; }}
  .soon {{ color: #555; font-style: italic; }}
</style>
</head>
<body>
<h1>Joint Fire Protection District 3 &amp; 8 — Standard Operating Guidelines</h1>
<ul>
  <li><a href="{quote(PDF_NAME)}">{PDF_NAME}</a> — print-ready</li>
  <li><a href="{quote(DOCX_NAME)}">{DOCX_NAME}</a> — editable</li>
  <li><a href="{SOURCE_URL}">Markdown source</a></li>
</ul>
</body>
</html>
"""

if __name__ == "__main__":
    print(HTML)
