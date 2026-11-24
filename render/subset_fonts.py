#!/usr/bin/env python3
"""Subset the system Noto CJK SC fonts to only the glyphs used in the 8 beats,
emit woff2 files + a @font-face CSS snippet for HyperFrames.

Why: HyperFrames lint errors on font-family without @font-face; the renderer
cannot auto-supply system CJK fonts. Subsetting keeps each woff2 tiny
(only ~100 unique chars are used on screen) and everything stays local/free.
"""
import glob
import os
import re
import unicodedata

from fontTools import subset
from fontTools.ttLib import TTCollection

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.path.join(ROOT, "render", "project")
FONTS_DIR = os.path.join(PROJECT, "assets", "fonts")

FACES = [
    ("NotoSansCJK-Regular.ttc", "Noto Sans CJK SC", 400, "sans-regular.woff2"),
    ("NotoSansCJK-Bold.ttc", "Noto Sans CJK SC", 700, "sans-bold.woff2"),
    ("NotoSerifCJK-Regular.ttc", "Noto Serif CJK SC", 400, "serif-regular.woff2"),
    ("NotoSerifCJK-Bold.ttc", "Noto Serif CJK SC", 700, "serif-bold.woff2"),
]


def collect_text():
    chars = set()
    for p in glob.glob(os.path.join(PROJECT, "b*.html")):
        html = open(p, encoding="utf-8").read()
        # strip tags/scripts/styles, keep visible text
        html = re.sub(r"<script.*?</script>", "", html, flags=re.S)
        html = re.sub(r"<style.*?</style>", "", html, flags=re.S)
        text = re.sub(r"<[^>]+>", "", html)
        chars.update(text)
    # drop whitespace/control; keep printable incl. CJK, latin, punctuation, ≠
    chars = {c for c in chars if c.strip() and unicodedata.category(c)[0] != "C"}
    return "".join(sorted(chars))


def sc_font_number(ttc_path):
    coll = TTCollection(ttc_path)
    for i, font in enumerate(coll.fonts):
        names = {r.toUnicode() for r in font["name"].names
                 if r.nameID in (1, 4, 16) and r.platformID == 3}
        if any("SC" in n for n in names):
            return i
    raise RuntimeError(f"no SC face in {ttc_path}")


def main():
    text = collect_text()
    print(f"unique chars on screen: {len(text)}")
    os.makedirs(FONTS_DIR, exist_ok=True)
    css = []
    for ttc, family, weight, out in FACES:
        path = f"/usr/share/fonts/opentype/noto/{ttc}"
        num = sc_font_number(path)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        opts.recalc_bounds = True
        coll = TTCollection(path)
        font = coll.fonts[num]
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
        out_path = os.path.join(FONTS_DIR, out)
        font.save(out_path)
        size = os.path.getsize(out_path)
        print(f"{out}: {size} bytes (from {ttc} face {num})")
        css.append(
            f"@font-face {{ font-family:'{family}'; font-weight:{weight}; "
            f"font-style:normal; font-display:swap; "
            f"src:url('assets/fonts/{out}') format('woff2'); }}")
    with open(os.path.join(PROJECT, "fonts.css"), "w", encoding="utf-8") as f:
        f.write("\n".join(css) + "\n")
    print("wrote", os.path.join(PROJECT, "fonts.css"))


if __name__ == "__main__":
    main()
