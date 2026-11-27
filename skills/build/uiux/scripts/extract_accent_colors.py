#!/usr/bin/env python3
"""Extract chromatic accent colors from a reference screenshot via HSV filtering.

Why: area-based median-cut quantization on light/document UIs returns mostly
background neutrals. Filtering by saturation/value isolates deliberate accents.
"""
import argparse
import colorsys
from collections import Counter
from pathlib import Path
from PIL import Image


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract chromatic accent colors from an image.")
    ap.add_argument("image", type=Path)
    ap.add_argument("--min-sat", type=float, default=0.18)
    ap.add_argument("--min-val", type=float, default=0.30)
    ap.add_argument("--top", type=int, default=14)
    args = ap.parse_args()

    im = Image.open(args.image).convert("RGB")
    px = list(im.getdata())
    buckets: Counter[tuple[int, int, int]] = Counter()
    for r, g, b in px:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > args.min_sat and v > args.min_val:
            buckets[(round(h * 24), round(s * 4), round(v * 6))] += 1

    for k, n in buckets.most_common(args.top):
        r, g, b = colorsys.hsv_to_rgb(k[0] / 24, k[1] / 4, k[2] / 6)
        print(
            f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}  "
            f"h={k[0]/24*360:5.0f}deg  s={k[1]/4:.2f}  v={k[2]/6:.2f}  {100*n/len(px):5.2f}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
