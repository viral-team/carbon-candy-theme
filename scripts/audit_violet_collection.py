#!/usr/bin/env python3
"""Contrast and color-vision audit for the Carbon Candy Violet Collection.

Checks every generated violet theme against WCAG 2.2 AA thresholds and
simulates protanopia, deuteranopia and tritanopia (Brettel/Viénot matrices)
to make sure syntax categories stay distinguishable without relying on hue
alone.

    python3 scripts/audit_violet_collection.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"
FILES = [
    "carbon-candy-nocturne.json",
    "carbon-candy-synthwave.json",
    "carbon-candy-amethyst.json",
]


def rgb(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 8:
        h = h[:6]
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    r, g, b = rgb(hex_color)
    return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def blend(fg, bg, alpha):
    f, b = rgb(fg), rgb(bg)
    out = [f[i] * alpha + b[i] * (1 - alpha) for i in range(3)]
    return "#%02X%02X%02X" % tuple(round(c * 255) for c in out)


# Viénot/Brettel-style simulation matrices (linear RGB)
CVD = {
    "protanopia": ((0.152286, 1.052583, -0.204868),
                   (0.114503, 0.786281, 0.099216),
                   (-0.003882, -0.048116, 1.051998)),
    "deuteranopia": ((0.367322, 0.860646, -0.227968),
                     (0.280085, 0.672501, 0.047413),
                     (-0.011820, 0.042940, 0.968881)),
    "tritanopia": ((1.255528, -0.076749, -0.178779),
                   (-0.078411, 0.930809, 0.147602),
                   (0.004733, 0.691367, 0.303900)),
}


def simulate(hex_color, kind):
    r, g, b = (linear(c) for c in rgb(hex_color))
    m = CVD[kind]
    out = [m[i][0] * r + m[i][1] * g + m[i][2] * b for i in range(3)]
    out = [min(1.0, max(0.0, c)) for c in out]
    srgb = [12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055 for c in out]
    return "#%02X%02X%02X" % tuple(round(c * 255) for c in srgb)


def delta_e(a, b):
    """CIE76 distance on sRGB (good enough to flag near-identical colors)."""
    def lab(h):
        r, g, bl = (linear(c) for c in rgb(h))
        x = (0.4124 * r + 0.3576 * g + 0.1805 * bl) / 0.95047
        y = (0.2126 * r + 0.7152 * g + 0.0722 * bl)
        z = (0.0193 * r + 0.1192 * g + 0.9505 * bl) / 1.08883

        def f(t):
            return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

        fx, fy, fz = f(x), f(y), f(z)
        return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

    la, lb = lab(a), lab(b)
    return sum((la[i] - lb[i]) ** 2 for i in range(3)) ** 0.5


# (label, color key, background key, minimum ratio)
TEXT_CHECKS = [
    ("editor foreground", "editor.foreground", "editor.background", 7.0),
    ("side bar foreground", "sideBar.foreground", "sideBar.background", 4.5),
    ("status bar foreground", "statusBar.foreground", "statusBar.background", 4.5),
    ("tab inactive foreground", "tab.inactiveForeground", "tab.inactiveBackground", 4.5),
    ("tab active foreground", "tab.activeForeground", "tab.activeBackground", 7.0),
    ("breadcrumb foreground", "breadcrumb.foreground", "breadcrumb.background", 4.5),
    ("line number", "editorLineNumber.foreground", "editor.background", 2.0),
    ("line number active", "editorLineNumber.activeForeground", "editor.background", 4.5),
    ("input placeholder", "input.placeholderForeground", "input.background", 4.5),
    ("description foreground", "descriptionForeground", "editor.background", 4.5),
    ("disabled foreground", "disabledForeground", "editor.background", 3.0),
    ("list highlight", "list.highlightForeground", "sideBar.background", 4.5),
    ("panel title inactive", "panelTitle.inactiveForeground", "panel.background", 4.5),
    ("terminal foreground", "terminal.foreground", "terminal.background", 7.0),
    ("button foreground", "button.foreground", "button.background", 4.5),
    ("badge foreground", "badge.foreground", "badge.background", 4.5),
    ("activity badge", "activityBarBadge.foreground", "activityBarBadge.background", 4.5),
    ("error foreground", "errorForeground", "editor.background", 4.5),
    ("git added", "gitDecoration.addedResourceForeground", "sideBar.background", 4.5),
    ("git modified", "gitDecoration.modifiedResourceForeground", "sideBar.background", 4.5),
    ("git deleted", "gitDecoration.deletedResourceForeground", "sideBar.background", 4.5),
    ("git conflict", "gitDecoration.conflictingResourceForeground", "sideBar.background", 4.5),
    ("git untracked", "gitDecoration.untrackedResourceForeground", "sideBar.background", 4.5),
    ("editor error", "editorError.foreground", "editor.background", 4.5),
    ("editor warning", "editorWarning.foreground", "editor.background", 4.5),
    ("editor info", "editorInfo.foreground", "editor.background", 4.5),
    ("selection foreground", "editor.selectionForeground", "editor.selectionBackground", 4.5),
    ("find match foreground", "editor.findMatchForeground", "editor.findMatchBackground", 4.5),
    ("cursor", "editorCursor.foreground", "editor.background", 3.0),
    ("ansi red", "terminal.ansiRed", "terminal.background", 4.5),
    ("ansi green", "terminal.ansiGreen", "terminal.background", 4.5),
    ("ansi yellow", "terminal.ansiYellow", "terminal.background", 4.5),
    ("ansi blue", "terminal.ansiBlue", "terminal.background", 4.5),
    ("ansi magenta", "terminal.ansiMagenta", "terminal.background", 4.5),
    ("ansi cyan", "terminal.ansiCyan", "terminal.background", 4.5),
    ("ansi bright black", "terminal.ansiBrightBlack", "terminal.background", 3.0),
]

# Syntax roles resolved from the theme's own token rules.
SYNTAX_ROLES = {
    "keyword": "Keyword",
    "function": "Function definition",
    "type": "Type",
    "class": "Class",
    "interface": "Interface",
    "enum": "Enum",
    "string": "String",
    "number": "Number",
    "variable": "Variable",
    "property": "Variable property",
    "operator": "Operator",
    "comment": "Comment",
    "decorator": "Decorator",
    "import": "Import / export",
    "parameter": "Variable parameter",
}


def token_color(theme, name):
    for rule in theme["tokenColors"]:
        if rule.get("name") == name:
            return rule["settings"].get("foreground")
    return None


def audit(path):
    theme = json.loads(path.read_text(encoding="utf-8"))
    colors = theme["colors"]
    editor_bg = colors["editor.background"]
    failures = []
    rows = []

    for label, fg_key, bg_key, minimum in TEXT_CHECKS:
        fg, bg = colors.get(fg_key), colors.get(bg_key)
        if not fg or not bg:
            failures.append(f"{label}: missing color")
            continue
        ratio = contrast(fg, bg)
        rows.append((label, fg, bg, ratio, minimum))
        if ratio < minimum:
            failures.append(f"{label}: {ratio:.2f} < {minimum}")

    syntax = {}
    for role, rule_name in SYNTAX_ROLES.items():
        color = token_color(theme, rule_name)
        if not color:
            failures.append(f"syntax {role}: rule '{rule_name}' missing")
            continue
        ratio = contrast(color, editor_bg)
        syntax[role] = color
        rows.append((f"syntax {role}", color, editor_bg, ratio, 4.5))
        if ratio < 4.5:
            failures.append(f"syntax {role}: {ratio:.2f} < 4.5")

    # color-vision separation between syntax roles
    cvd_report = {}
    for kind in CVD:
        sims = {role: simulate(color, kind) for role, color in syntax.items()}
        pairs = []
        roles = list(sims)
        for i, a in enumerate(roles):
            for b in roles[i + 1:]:
                d = delta_e(sims[a], sims[b])
                pairs.append((d, a, b))
        pairs.sort()
        cvd_report[kind] = pairs[:3]

    return theme, rows, failures, cvd_report


def main():
    ok = True
    for name in FILES:
        path = THEMES / name
        theme, rows, failures, cvd = audit(path)
        print(f"\n=== {theme['name']} ===")
        worst = sorted(rows, key=lambda r: r[3] / r[4])[:6]
        for label, fg, bg, ratio, minimum in worst:
            print(f"  tightest: {label:28s} {fg} on {bg} = {ratio:5.2f} (min {minimum})")
        for kind, pairs in cvd.items():
            shown = ", ".join(f"{a}/{b} ΔE={d:.1f}" for d, a, b in pairs)
            print(f"  {kind:13s} closest: {shown}")
        if failures:
            ok = False
            print("  FAILURES:")
            for f in failures:
                print(f"    - {f}")
        else:
            print("  all checks passed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
