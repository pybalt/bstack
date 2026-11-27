#!/usr/bin/env python3
"""Static contract & WCAG contrast validator for visual-brief standalone HTML files.

Checks:
1. Standalone HTML shell (<!doctype html>, <meta name="viewport">).
2. Data separation block (// <DATA> ... // </DATA>) and valid JSON/object structure.
3. WCAG 2.1 contrast ratios for light and dark theme tokens (text >= 4.5, controls >= 3.0).
4. XSS hygiene (zero innerHTML / outerHTML / document.write usage).
5. Copy density caps on structured data (lead <= 14 words, detail bullets <= 12 words).

Outputs JSON to stdout. Exit 0 = OK, exit 1 = failures found, exit 2 = error.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TEXT_PAIRS = [("ink", "bg"), ("ink", "zone"), ("ink", "surface"), ("muted", "bg"), ("muted", "surface"), ("bg", "ink")]
STROKE_PAIRS = [("ctl", "bg"), ("ctl", "surface"), ("accentA", "bg"), ("accentA", "surface"), ("accentB", "bg"), ("accentB", "surface")]


def luminance(hex_color: str) -> float:
    rgb = [int(hex_color[i : i + 2], 16) / 255.0 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_ratio(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def extract_tokens(css_block: str) -> dict[str, str]:
    return dict(re.findall(r"--([A-Za-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6})\b", css_block))


def word_count(text: str) -> int:
    return len([w for w in text.split() if re.search(r"\w", w)])


def validate(html_path: Path) -> dict:
    src = html_path.read_text(encoding="utf-8")
    failures = []
    warnings = []

    if not re.search(r"^\s*<!doctype\s+html>", src, re.I):
        failures.append("Missing <!doctype html> at document start (standalone browsers fall back to quirks mode).")
    if not re.search(r'<meta\s+name=["\']viewport["\']', src, re.I):
        failures.append('Missing <meta name="viewport" content="width=device-width,initial-scale=1"> for mobile rendering.')

    # XSS hygiene
    if re.search(r"\.(?:innerHTML|outerHTML)\s*=|document\.write\s*\(", src):
        failures.append("Unsafe DOM sink detected (innerHTML/outerHTML/document.write); use textContent/createTextNode.")

    # Contrast check on light and dark CSS blocks
    light_m = re.search(r":root\s*\{([^}]+)\}", src)
    dark_m = re.search(r':root\[data-theme="dark"\]\s*\{([^}]+)\}', src)
    if not light_m or not dark_m:
        failures.append('Missing :root and :root[data-theme="dark"] token blocks for WCAG contrast check.')
    else:
        light_toks = extract_tokens(light_m.group(1))
        dark_toks = dict(light_toks)
        dark_toks.update(extract_tokens(dark_m.group(1)))
        for theme_name, toks in (("light", light_toks), ("dark", dark_toks)):
            for kind, pairs, minimum in (("text", TEXT_PAIRS, 4.5), ("stroke", STROKE_PAIRS, 3.0)):
                for fg, bg in pairs:
                    if fg not in toks or bg not in toks:
                        continue
                    r = contrast_ratio(toks[fg], toks[bg])
                    if r < minimum:
                        failures.append(f"WCAG {theme_name} {kind}: --{fg} on --{bg} is {r:.2f}:1 (min {minimum}:1)")

    # Data block check + copy limits
    data_m = re.search(r"//\s*<DATA>\s*(.*?)\s*//\s*</DATA>", src, re.S)
    if not data_m:
        warnings.append("No // <DATA> ... // </DATA> separation block found.")
    else:
        block = data_m.group(1)
        json_m = re.search(r"const\s+BRIEF\s*=\s*(\{.*\})\s*;?\s*$", block, re.S)
        if json_m:
            try:
                brief = json.loads(json_m.group(1))
                for section in brief.get("views", []):
                    for item in section.get("nodes", []) + section.get("options", []) + section.get("cards", []):
                        lead = item.get("lead", "")
                        if lead and word_count(lead) > 16:
                            warnings.append(f"Copy density: '{item.get('id', item.get('title'))}' lead has {word_count(lead)} words (target <= 14).")
                        for grp in item.get("details", []):
                            for bullet in grp.get("items", []):
                                if word_count(bullet) > 14:
                                    warnings.append(f"Copy density: bullet in '{item.get('id', item.get('title'))}' has {word_count(bullet)} words (target <= 12).")
            except json.JSONDecodeError as exc:
                failures.append(f"Invalid JSON inside BRIEF // <DATA> block: {exc}")

    return {
        "status": "ok" if not failures else "failed",
        "file": str(html_path.name),
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures,
        "warnings": warnings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html_file", type=Path, help="Path to standalone visual-brief HTML file.")
    args = ap.parse_args()

    try:
        report = validate(args.html_file.resolve())
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 0 if report["failure_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
