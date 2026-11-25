#!/usr/bin/env python3
"""Build ad.png: a poster-style advert for the news-image entry.

The poster frames the finished front page inside a navy masthead, a thin
gold rule, and a footer strip carrying the story count and referral code.
Everything is drawn from entry.png with Pillow; the result is fully
deterministic — no clock, no network, no randomness.
"""

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# Palette for the poster.
DEEP_NAVY = (16, 36, 68)
BRIGHT_GOLD = (250, 205, 21)
WARM_PAPER = (247, 241, 222)
DARK_INK = (20, 26, 42)
SOFT_CREAM = (245, 242, 234)

CANVAS_W, CANVAS_H = 1024, 768
MASTHEAD_H = 70
FOOTER_Y = 724


def load_font(filename, size):
    """Load a DejaVu face from the system font directory."""
    return ImageFont.truetype(FONT_DIR + filename, size)


def draw_masthead(canvas, pen):
    """Navy band across the top with the title and the date line."""
    pen.rectangle([0, 0, CANVAS_W, MASTHEAD_H], fill=DEEP_NAVY)
    title_font = load_font("DejaVuSerif-Bold.ttf", 36)
    date_font = load_font("DejaVuSans-Bold.ttf", 14)
    pen.text(
        (CANVAS_W // 2, 8),
        "THE WORLD IN ONE PAGE",
        font=title_font,
        fill=SOFT_CREAM,
        anchor="ma",
    )
    pen.text(
        (CANVAS_W // 2, 48),
        "WEDNESDAY, 25 NOVEMBER 2026  ·  43 STORIES  ·  ONE IMAGE",
        font=date_font,
        fill=BRIGHT_GOLD,
        anchor="ma",
    )
    # A gold rule under the masthead.
    pen.rectangle([0, MASTHEAD_H, CANVAS_W, MASTHEAD_H + 3], fill=BRIGHT_GOLD)


def draw_footer(canvas, pen):
    """Two centred lines at the bottom: what the page holds, and the referral."""
    body_font = load_font("DejaVuSans.ttf", 13)
    bold_font = load_font("DejaVuSans-Bold.ttf", 13)
    pen.text(
        (CANVAS_W // 2, FOOTER_Y),
        "43 stories reported on 25 November 2026 — headlines, cards, map and timeline.",
        font=body_font,
        fill=DARK_INK,
        anchor="ma",
    )
    pen.text(
        (CANVAS_W // 2, FOOTER_Y + 20),
        "Referral: trfjt22d  ·  make.fun",
        font=bold_font,
        fill=DEEP_NAVY,
        anchor="ma",
    )


def build_poster():
    """Compose the poster and write it to ad.png next to this script."""
    front_page = Image.open("entry.png").convert("RGB")
    poster = Image.new("RGB", (CANVAS_W, CANVAS_H), WARM_PAPER)
    pen = ImageDraw.Draw(poster)

    draw_masthead(poster, pen)

    # The front page, scaled down, centred between masthead and footer.
    thumb = front_page.resize((620, 620), Image.LANCZOS)
    poster.paste(thumb, ((CANVAS_W - 620) // 2, MASTHEAD_H + 14))

    draw_footer(poster, pen)

    poster.save("ad.png", optimize=True)
    print("saved ad.png")


if __name__ == "__main__":
    build_poster()
