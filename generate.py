#!/usr/bin/env python3
"""Render entry.png for the make.fun bounty
"Sum up 24 November's world news in one image" (news-image-20261124).

Local build tool only -- NOT the entrypoint. The entrypoint is main.py,
which only copies the committed entry.png to /output/entry.png, so the
submitted program needs no network, no Pillow and no fonts at run time.

Run:  python3 generate.py   (writes entry.png next to this file)
Requires Pillow + DejaVu/Liberation fonts locally (present on this VM).
Deterministic: fixed text, fixed layout, fixed PNG encoder settings.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

NAVY = (15, 42, 68)
NAVY2 = (23, 64, 100)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
GREY = (88, 88, 88)
LIGHT = (242, 240, 234)
PAPER = (250, 248, 243)
LINE = (200, 196, 188)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width, returning lines."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, leading=None):
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, xy, text, color=RED):
    f = font(SANS_B, 21)
    draw.text(xy, text.upper(), font=f, fill=color)
    return xy[1] + 28


def headline(draw, xy, text, size, width, fill=INK):
    f = font(SERIF, size)
    return para(draw, xy, text, f, width, fill=fill, leading=int(size * 1.08))


def rule(draw, x0, y, x1, w=2, color=LINE):
    draw.line([(x0, y), (x1, y)], fill=color, width=w)


def bullet(draw, x, y, text, fnt, width, fill=INK, dot=RED):
    draw.ellipse([x, y + 8, x + 9, y + 17], fill=dot)
    return para(draw, (x + 18, y), text, fnt, width - 18, fill=fill,
                leading=int(fnt.size * 1.3))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    d.text((36, 22), "THE WORLD IN ONE DAY", font=font(SERIF, 50),
           fill=(255, 255, 255))
    d.text((36, 90), "TUESDAY  24  NOVEMBER  2026", font=font(SANS_B, 28),
           fill=GOLD)
    d.text((772, 30), "ONE IMAGE.", font=font(SANS_B, 22), fill=(255, 255, 255))
    d.text((772, 58), "THE WHOLE DAY.", font=font(SANS_B, 22),
           fill=(255, 255, 255))
    d.text((772, 96), "10 stories · 5 regions",
           font=font(SANS, 20), fill=(200, 210, 220))

    # ---------- lead: Hormuz ----------
    y = 178
    y = kicker(d, (36, y), "Lead story  —  Middle East  ·  Tue 24 Nov")
    y = headline(d, (36, y + 2),
                 "Tankers hit by mines in\nthe Strait of Hormuz",
                 48, 640)
    y = para(d, (36, y + 8),
             "Three oil tankers suffered explosions and fire after hitting "
             "naval mines in the strait on Tuesday, Iran's Revolutionary "
             "Guard said. Tehran vowed to use “all available means” against "
             "the US naval blockade — and said the strait could reopen if "
             "Washington meets its terms.",
             font(SANS, 22), 640)
    # right-hand fact box: the strait, drawn
    d.rectangle([712, 178, 988, 452], outline=NAVY2, width=3)
    d.rectangle([712, 178, 988, 222], fill=NAVY2)
    d.text((730, 186), "THE CHOKEPOINT", font=font(SANS_B, 22),
           fill=(255, 255, 255))
    d.text((730, 240), "Strait of Hormuz", font=font(SERIF, 30), fill=INK)
    para(d, (730, 282),
         "The world's most important\noil chokepoint. Attacks on\nshipping there hit their\nhighest level since the\nIran war began.",
         font(SANS, 20), 240)
    d.text((730, 420), "20+ ships struck in Nov.",
           font=font(SANS_B, 20), fill=RED)

    rule(d, 36, 478, 988)

    # ---------- row 2: COP31 | Gaza ----------
    y = 496
    # COP31 (left)
    y1 = kicker(d, (36, y), "Climate  ·  ended Sun 22 Nov")
    y1 = headline(d, (36, y1 + 2), "COP31 collapses:\nno deal at all", 34, 440)
    y1 = para(d, (36, y1 + 6),
              "The UN climate summit in Antalya ends after 49+ hours of "
              "overtime with no agreement. 90+ nations rejected a draft "
              "that never mentioned fossil fuels — the first failed summit "
              "since Copenhagen 2009.",
              font(SANS, 21), 440)
    # Gaza (right)
    x2 = 528
    y2 = kicker(d, (x2, y), "Gaza  ·  Tue 24 Nov")
    y2 = headline(d, (x2, y2 + 2), "Strikes kill Hamas\nsecurity chief", 34, 440)
    y2 = para(d, (x2, y2 + 6),
              "Israeli strikes kill Naeem Abu Nahel, Hamas's internal-"
              "security director, and six others, including two police "
              "officers. A UN aid-agency worker was killed a day earlier.",
              font(SANS, 21), 440)

    rule(d, 36, 736, 988)
    d.line([(504, 496), (504, 724)], fill=LINE, width=2)

    # ---------- row 3: Ukraine | Also on Tuesday ----------
    y = 752
    y1 = kicker(d, (36, y), "Ukraine  ·  Tue 24 Nov")
    y1 = headline(d, (36, y1 + 2), "Zaporizhzhia hit:\n2 killed, 40 hurt", 34, 440)
    y1 = para(d, (36, y1 + 6),
              "A Russian strike on an apartment block kills 2 and wounds "
              "40, including four children. Kyiv says its drones sank a "
              "Russian corvette off Libya.",
              font(SANS, 20), 440)
    x2 = 528
    y2 = kicker(d, (x2, y), "Also on Tuesday", color=NAVY2)
    yy = y2 + 4
    yy = bullet(d, x2, yy, "Nvidia reinstates Jensen Huang as CEO.",
                font(SANS, 19), 440)
    yy = bullet(d, x2, yy + 6, "US sanctions Iran's shadow banking "
                "networks.", font(SANS, 19), 440)
    yy = bullet(d, x2, yy + 6, "Fighting in Ituri traps Ebola responders "
                "(WHO).", font(SANS, 19), 440)
    yy = bullet(d, x2, yy + 6, "South Korea: $375k rewards to catch AI "
                "exam cheats.", font(SANS, 19), 440)

    # ---------- footer: the weekend that led here + sources ----------
    d.rectangle([0, 948, W, H], fill=NAVY)
    d.text((36, 958), "THE WEEKEND THAT LED HERE  —  Sun 22 Nov:",
           font=font(SANS_B, 20), fill=GOLD)
    d.text((36, 980), "Mercury orbiters arrive after an 8-year cruise  ·  "
           "Indonesia factory fire kills at least 24",
           font=font(SANS, 20), fill=(255, 255, 255))
    d.text((36, 1004), "Sources: Just Security · Reuters · AP · Al Jazeera · "
           "BBC · AFP · Grist — as reported 24 Nov 2026",
           font=font(SANS, 16), fill=(170, 185, 200))

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
