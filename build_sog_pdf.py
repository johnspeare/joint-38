#!/usr/bin/env python3
"""
Build a print-ready PDF from the FD SOGs Markdown source.

Usage
-----
    python build_sog_pdf.py                     # defaults below
    python build_sog_pdf.py INPUT.md OUTPUT.pdf

Defaults: input=``FD SOGs.md`` (in cwd), output=``FD-SOGs.pdf`` (in cwd).

Runtime requirements
--------------------
Python packages (pip): ``markdown``, ``weasyprint``.
System libraries (Homebrew on macOS): ``pango``, ``cairo``, ``gdk-pixbuf``,
``glib``, ``harfbuzz``. Install with::

    brew install pango cairo gdk-pixbuf glib harfbuzz

On Apple Silicon, if the Python interpreter can't find the libraries, run
the script with::

    DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 build_sog_pdf.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import markdown
from weasyprint import HTML, CSS


DOC_TITLE = "Standard Operating Guidelines"
FOOTER_LEFT = "STANDARD OPERATING GUIDELINES — UNCONTROLLED WHEN PRINTED"


# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------
CSS_STYLES = r"""
/* =========================================================
   Page geometry + running headers/footers
   ========================================================= */
@page {
    size: letter portrait;
    margin: 0.9in 0.75in 1.0in 0.75in;

    @bottom-left {
        content: "STANDARD OPERATING GUIDELINES — UNCONTROLLED WHEN PRINTED";
        font-family: "Arial", "Helvetica Neue", Helvetica, sans-serif;
        font-size: 8pt;
        font-weight: bold;
        color: #777;
    }
    @bottom-right {
        content: "Page " counter(page) " of " counter(pages);
        font-family: "Arial", "Helvetica Neue", Helvetica, sans-serif;
        font-size: 9pt;
        color: #555;
    }
}

/* Title page: no footer clutter */
@page :first {
    @bottom-left  { content: none; }
    @bottom-right { content: none; }
}

/* =========================================================
   Base typography
   ========================================================= */
body {
    font-family: "Arial", "Helvetica Neue", Helvetica, sans-serif;
    font-size: 11pt;
    line-height: 1.45;
    color: #111;
}

p {
    orphans: 3;
    widows: 3;
    margin: 0.5em 0;
}

a { color: #8B0000; text-decoration: none; }

/* =========================================================
   Headings
   ========================================================= */
h1, h2, h3, h4, h5, h6 {
    color: #8B0000;
    font-weight: bold;
    break-after: avoid;
    page-break-after: avoid;
}
h1 {
    font-size: 24pt;
    text-align: center;
    border-bottom: 2px solid #8B0000;
    padding-bottom: 8px;
    margin: 2.5in 0 0.5em 0;   /* pushes title down on the title page */
}
h2 {
    font-size: 16pt;
    border-bottom: 1px solid #ccc;
    padding-bottom: 3px;
    margin-top: 1.5em;
}
h3 { font-size: 12.5pt; margin-top: 1.2em; }
h4 { font-size: 11.5pt; margin-top: 1.0em; }

/* =========================================================
   Table of Contents
   =========================================================
   Rendered by python-markdown's `toc` extension. Wrapped in
   <div class="toc"> with a <span class="toctitle">. Entries
   are <a href="#anchor"> — WeasyPrint's target-counter() lets
   us add real page numbers with leader dots.
*/
.toc {
    break-before: page;
    break-after: page;
    page-break-before: always;
    page-break-after: always;
}
.toc .toctitle {
    display: block;
    font-size: 22pt;
    font-weight: bold;
    color: #8B0000;
    border-bottom: 2px solid #8B0000;
    padding-bottom: 6px;
    margin: 0 0 1em 0;
}
.toc ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
}
.toc > ul > li { margin-top: 0.35em; }
.toc ul ul { padding-left: 1.4em; font-size: 10.5pt; }
.toc li { break-inside: avoid; margin: 0.15em 0; }
.toc a {
    color: #111;
    text-decoration: none;
}
.toc a::after {
    content: leader('.') " " target-counter(attr(href), page);
    color: #555;
    font-variant-numeric: tabular-nums;
}

/* =========================================================
   Tables
   =========================================================
   Allow long tables (Appendix C) to split across pages while
   repeating <thead> on each continuation page.
*/
table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.8em 0;
    font-size: 10.5pt;
}
th, td {
    border: 1px solid #ddd;
    padding: 6px 8px;
    text-align: left;
    vertical-align: top;
}
th { background: #f2f2f2; }
thead { display: table-header-group; }
tfoot { display: table-footer-group; }

/* =========================================================
   Images, figures, captions
   =========================================================
   Constrain both dimensions so tall/portrait figures (e.g. the
   chain-of-command chart) fit on a single page. `width: auto`
   plus `height: auto` combined with the two max-* rules gives
   proportional scaling to fit within the box.
*/
img, svg {
    display: block;
    margin: 0.5em auto;
    max-width: 100%;
    max-height: 6.5in;
    width: auto;
    height: auto;
}
figure {
    break-inside: avoid;
    margin: 1em 0;
    text-align: center;
}
figcaption, sub {
    color: #555;
    font-size: 9pt;
}

/* =========================================================
   Lists
   ========================================================= */
ul, ol { margin: 0.4em 0 0.4em 1.2em; padding-left: 0.6em; }
li { margin: 0.15em 0; }

/* =========================================================
   Blockquotes & code
   ========================================================= */
blockquote {
    margin: 0.8em 0 0.8em 1em;
    padding: 0.4em 0.9em;
    border-left: 3px solid #8B0000;
    color: #333;
    break-inside: avoid;
}
code, pre {
    font-family: "SF Mono", Menlo, Consolas, monospace;
    font-size: 10pt;
}
pre {
    background: #f6f6f6;
    padding: 0.6em 0.9em;
    border-radius: 4px;
    break-inside: avoid;
}
"""


# ---------------------------------------------------------------------------
# Markdown → HTML
# ---------------------------------------------------------------------------
_TOC_PLACEHOLDER_RE = re.compile(
    r"<!--\s*Table of contents:.*?-->",
    flags=re.DOTALL,
)

_IMG_SVG_RE = re.compile(
    r'(<img[^>]*\bsrc=")([^"]+)\.svg("[^>]*>)',
    flags=re.IGNORECASE,
)


def _swap_svgs_for_pngs(html: str, base_dir: Path) -> str:
    """Replace ``<img src="foo.svg">`` with ``<img src="foo.png">`` when a
    PNG file with the same stem exists on disk next to the SVG.

    This is a WeasyPrint workaround: its SVG rasterizer doesn't render
    ``<foreignObject>`` content (used by mermaid-cli for flowchart labels),
    so we fall back to a pre-rendered PNG for the print pipeline.
    """
    def _sub(m: re.Match[str]) -> str:
        prefix, stem, suffix = m.groups()
        png_rel = f"{stem}.png"
        if (base_dir / png_rel).is_file():
            return f"{prefix}{png_rel}{suffix}"
        return m.group(0)

    return _IMG_SVG_RE.sub(_sub, html)


def render_html(md_path: Path) -> str:
    """Load ``md_path``, splice in a [TOC] marker, and convert to HTML."""
    md_text = md_path.read_text(encoding="utf-8")

    # Replace the front-matter HTML comment (the TOC placeholder) with an
    # actual [TOC] marker that python-markdown's toc extension consumes.
    # If the placeholder isn't found, drop [TOC] right after the H1 instead.
    if _TOC_PLACEHOLDER_RE.search(md_text):
        md_text = _TOC_PLACEHOLDER_RE.sub("[TOC]", md_text, count=1)
    else:
        md_text = re.sub(
            r"(^# .*$)",
            r"\1\n\n[TOC]",
            md_text,
            count=1,
            flags=re.MULTILINE,
        )

    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "sane_lists",
            "attr_list",
            "toc",
        ],
        extension_configs={
            "toc": {
                "title": "Table of Contents",
                "toc_depth": "2-2",
                "anchorlink": False,
                "permalink": False,
            },
        },
    )
    body_html = md.convert(md_text)

    # WeasyPrint's SVG engine can't render <foreignObject> content, which
    # is what mermaid-cli emits for node labels in flowcharts. If a PNG
    # counterpart of any referenced SVG exists next to the SVG, swap the
    # reference at PDF-build time so the print pipeline uses the raster
    # (HTML/web keeps using the crisp SVG).
    body_html = _swap_svgs_for_pngs(body_html, md_path.parent)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{DOC_TITLE}</title>
</head>
<body>
{body_html}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Build the FD SOGs PDF from Markdown.")
    ap.add_argument(
        "input",
        nargs="?",
        default="FD SOGs.md",
        help="Path to the source Markdown file (default: 'FD SOGs.md').",
    )
    ap.add_argument(
        "output",
        nargs="?",
        default="FD-SOGs.pdf",
        help="Path for the output PDF (default: 'FD-SOGs.pdf').",
    )
    args = ap.parse_args()

    md_path = Path(args.input).resolve()
    out_path = Path(args.output).resolve()

    if not md_path.exists():
        sys.exit(f"error: input file not found: {md_path}")

    print(f"Reading   {md_path}")
    html = render_html(md_path)

    print(f"Rendering {out_path}")
    HTML(string=html, base_url=str(md_path.parent)).write_pdf(
        target=str(out_path),
        stylesheets=[CSS(string=CSS_STYLES)],
    )
    print(f"Done → {out_path}")


if __name__ == "__main__":
    main()
