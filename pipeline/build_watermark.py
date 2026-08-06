#!/usr/bin/env python3
"""Regenerate pipeline/watermark-draft.png — the "DRAFT" page watermark.

Run this whenever the watermark needs to change (text, color, size). The
output is a checked-in binary, like reference.docx; this script is how you
reproduce or edit it instead of hand-editing an image.

Requires: `pip install Pillow`.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT = Path(__file__).resolve().parent / "watermark-draft.png"
TEXT = "DRAFT"
GRAY = (160, 160, 160)
OPACITY = 90  # out of 255 -- faint enough to read through, not obscure, body text
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def main() -> None:
    font_size = 260
    font = _load_font(font_size)

    # Draw the text horizontally on a generously padded transparent canvas
    # first, then rotate the whole canvas -- simpler than computing rotated
    # text-bbox math by hand, and PIL's rotate(expand=True) auto-sizes the
    # output so nothing gets clipped.
    scratch = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch)
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 40

    canvas = Image.new("RGBA", (text_w + pad * 2, text_h + pad * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.text((pad - bbox[0], pad - bbox[1]), TEXT, font=font, fill=(*GRAY, OPACITY))

    rotated = canvas.rotate(45, expand=True, resample=Image.BICUBIC)
    rotated.save(OUTPUT)
    print(f"Wrote {OUTPUT} ({rotated.width}x{rotated.height}px)")


if __name__ == "__main__":
    sys.exit(main())
