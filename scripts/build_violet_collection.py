#!/usr/bin/env python3
"""Generate the Carbon Candy Violet Collection themes.

Three variants share one structural template (the same workbench surface map
used by the rest of the pack) but each one owns a complete, independent
palette: backgrounds, foregrounds, accents, syntax roles, status colors and
Git decorations are all derived from that variant's own tokens.

Run from the repository root:

    python3 scripts/build_violet_collection.py

The script is deterministic and rewrites only the three violet theme files.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"


def a(color, alpha):
    """Append an alpha channel (0-1) to a 6-digit hex color."""
    return f"{color}{round(alpha * 255):02x}"


# ---------------------------------------------------------------------------
# Palettes
# ---------------------------------------------------------------------------
# Every variant defines the same semantic slots so the template below can be
# shared, but the values are chosen per variant (hue, saturation, temperature).

NOCTURNE = {
    "id": "carbon-candy-nocturne",
    "label": "Carbon Candy Nocturne",
    "file": "carbon-candy-nocturne.json",
    "mood": "Deep Violet / Midnight / Amethyst",
    # surfaces
    "bg": "#14121F",          # window / title bar
    "editor": "#191627",      # editor canvas
    "side": "#15121F",        # side bar, activity bar
    "panel": "#17141F",       # panel, terminal
    "raised": "#221E33",      # inputs, widgets, peek view
    "raised2": "#2A2540",     # hover, selected rows
    "border": "#2C2740",
    "borderSoft": "#241F35",
    # text
    "fg": "#E4E0F2",
    "fg2": "#B4AECB",
    "fg3": "#8A83A6",         # comments
    "fgDisabled": "#6B6580",
    "lineNumber": "#544D70",
    "lineNumberActive": "#A79FC4",
    # accents
    "accent": "#A78BFA",      # amethyst - primary
    "accent2": "#7DD3FC",     # cold lavender / ice - secondary
    "accent3": "#E879C7",     # desaturated magenta - occasional
    "accentInk": "#17131F",   # text on accent fills
    # syntax
    "kw": "#B79CFF",
    "kwControl": "#C9B4FF",
    "fn": "#8FB8FF",
    "method": "#A9C4FF",
    "importKw": "#D9C2FF",
    "ty": "#E9C46A",
    "cls": "#D8A0F0",
    "iface": "#DCC27A",
    "enum": "#D9B45E",
    "str": "#9FD8A8",
    "num": "#F2A97E",
    "bool": "#F2A97E",
    "var": "#DCD7EE",
    "prop": "#C9C2E4",
    "param": "#B3A9D2",
    "op": "#9C93B8",
    "punct": "#8E86A8",
    "decorator": "#E879C7",
    "import": "#C9B4FF",
    "escape": "#F2C4A0",
    "tag": "#E879C7",
    "attr": "#B79CFF",
    "mdHeading": "#A78BFA",
    "mdLink": "#7DD3FC",
    "mdCode": "#9FD8A8",
    # status
    "error": "#F07A8A",
    "warning": "#E9C46A",
    "success": "#8FD3A0",
    "info": "#7DD3FC",
    # git
    "gitAdded": "#8FD3A0",
    "gitModified": "#8FB8FF",
    "gitDeleted": "#F07A8A",
    "gitConflict": "#E9C46A",
    "gitUntracked": "#8FD3A0",
    # terminal ANSI
    "ansiBlack": "#2A2540",
    "ansiRed": "#F07A8A",
    "ansiGreen": "#8FD3A0",
    "ansiYellow": "#E9C46A",
    "ansiBlue": "#8FB8FF",
    "ansiMagenta": "#C79BF0",
    "ansiCyan": "#7DD3FC",
    "ansiWhite": "#DCD7EE",
    "ansiBrightBlack": "#6B6580",
    "ansiBrightRed": "#FF9AA8",
    "ansiBrightGreen": "#A8E6B6",
    "ansiBrightYellow": "#F5D98A",
    "ansiBrightBlue": "#A9C4FF",
    "ansiBrightMagenta": "#DDB4FF",
    "ansiBrightCyan": "#A5E4FF",
    "ansiBrightWhite": "#F2EFFA",
    # selection / focus
    "selection": "#3B3363",
    "selectionInactive": "#2E2848",
    "lineHighlight": "#1F1B2E",
    "cursor": "#C4B5FD",
    "findMatch": "#5B4A8C",
    "findMatchBorder": "#A78BFA",
    "wordHighlight": "#3A3358",
    "bracketMatch": "#A78BFA",
}

SYNTHWAVE = {
    "id": "carbon-candy-synthwave",
    "label": "Carbon Candy Synthwave",
    "file": "carbon-candy-synthwave.json",
    "mood": "Cyberpunk / Neon / Digital Future",
    "bg": "#0B0D18",
    "editor": "#111326",
    "side": "#0B0F1B",
    "panel": "#0F1121",
    "raised": "#1B1B35",
    "raised2": "#252446",
    "border": "#302C52",
    "borderSoft": "#211F3B",
    "fg": "#E6E3F5",
    "fg2": "#B0AAC8",
    "fg3": "#8A86A6",
    "fgDisabled": "#6A6585",
    "lineNumber": "#4A4468",
    "lineNumberActive": "#A79FC4",
    "accent": "#B57BFF",
    "accent2": "#4FD8E8",
    "accent3": "#FF6FB5",
    "accentInk": "#120F1E",
    "kw": "#C08BFF",
    "kwControl": "#D3A8FF",
    "fn": "#7FE3F0",
    "method": "#9DEBF5",
    "importKw": "#D3A8FF",
    "ty": "#9EBFFF",
    "cls": "#FF9FC5",
    "iface": "#DCCBFF",
    "enum": "#FFC2A8",
    "str": "#8FD9B6",
    "num": "#FFB86B",
    "bool": "#FFB86B",
    "var": "#DEDAF0",
    "prop": "#B9B2D6",
    "param": "#9C95BA",
    "op": "#C4BEDC",
    "punct": "#7E7899",
    "decorator": "#FF6FB5",
    "import": "#D3A8FF",
    "escape": "#FFC98F",
    "tag": "#FF6FB5",
    "attr": "#C08BFF",
    "mdHeading": "#B57BFF",
    "mdLink": "#4FD8E8",
    "mdCode": "#8FD9B6",
    "error": "#FF6B7A",
    "warning": "#FFB86B",
    "success": "#6FE0A8",
    "info": "#4FD8E8",
    "gitAdded": "#6FE0A8",
    "gitModified": "#7FE3F0",
    "gitDeleted": "#FF6B7A",
    "gitConflict": "#FFB86B",
    "gitUntracked": "#6FE0A8",
    "ansiBlack": "#241F3D",
    "ansiRed": "#FF6B7A",
    "ansiGreen": "#6FE0A8",
    "ansiYellow": "#FFB86B",
    "ansiBlue": "#7FB8FF",
    "ansiMagenta": "#C08BFF",
    "ansiCyan": "#4FD8E8",
    "ansiWhite": "#DEDAF0",
    "ansiBrightBlack": "#6A6585",
    "ansiBrightRed": "#FF8E9A",
    "ansiBrightGreen": "#8FEBC0",
    "ansiBrightYellow": "#FFD08F",
    "ansiBrightBlue": "#A5CCFF",
    "ansiBrightMagenta": "#D9AEFF",
    "ansiBrightCyan": "#8FEBF5",
    "ansiBrightWhite": "#F4F2FB",
    "selection": "#3A2F63",
    "selectionInactive": "#2A2450",
    "lineHighlight": "#181530",
    "cursor": "#4FD8E8",
    "findMatch": "#4A3A7A",
    "findMatchBorder": "#B57BFF",
    "wordHighlight": "#332B55",
    "bracketMatch": "#4FD8E8",
}

AMETHYST = {
    "id": "carbon-candy-amethyst",
    "label": "Carbon Candy Amethyst",
    "file": "carbon-candy-amethyst.json",
    "mood": "Aubergine / Plum / Soft Violet",
    "bg": "#191219",
    "editor": "#211821",
    "side": "#1B141C",
    "panel": "#1E171D",
    "raised": "#30232D",
    "raised2": "#3A2A36",
    "border": "#493543",
    "borderSoft": "#352833",
    "fg": "#E6DFE6",
    "fg2": "#C1B1BF",
    "fg3": "#9D8B9B",
    "fgDisabled": "#6E6370",
    "lineNumber": "#544A57",
    "lineNumberActive": "#B3A7B5",
    "accent": "#B98BD9",
    "accent2": "#A7A0C9",
    "accent3": "#D88FAD",
    "accentInk": "#1B1420",
    "kw": "#D0A6E3",
    "kwControl": "#E1B9EC",
    "fn": "#B8B3DE",
    "method": "#CBC2E8",
    "importKw": "#D9B9E5",
    "ty": "#E8BC8E",
    "cls": "#D99AAE",
    "iface": "#E8D5B0",
    "enum": "#D9A875",
    "str": "#B0C99B",
    "num": "#E9A087",
    "bool": "#E9A087",
    "var": "#E6DDE5",
    "prop": "#D5C2D0",
    "param": "#BBAAB9",
    "op": "#B5A4B4",
    "punct": "#9D8B9B",
    "decorator": "#E6A0BC",
    "import": "#D9B9E5",
    "escape": "#E8BCA0",
    "tag": "#D88FAD",
    "attr": "#D0A6E3",
    "mdHeading": "#C18DD4",
    "mdLink": "#A7A0C9",
    "mdCode": "#B0C99B",
    "error": "#E08A8A",
    "warning": "#E8BC8E",
    "success": "#A8C79C",
    "info": "#A7A0C9",
    "gitAdded": "#A8C79C",
    "gitModified": "#B8B3DE",
    "gitDeleted": "#E08A8A",
    "gitConflict": "#E8BC8E",
    "gitUntracked": "#A8C79C",
    "ansiBlack": "#3A2A36",
    "ansiRed": "#E08A8A",
    "ansiGreen": "#A0C9A0",
    "ansiYellow": "#E8BC8E",
    "ansiBlue": "#B8B3DE",
    "ansiMagenta": "#D0A6E3",
    "ansiCyan": "#9FC4C9",
    "ansiWhite": "#E0D8E2",
    "ansiBrightBlack": "#766574",
    "ansiBrightRed": "#EDA5A5",
    "ansiBrightGreen": "#B8DBB8",
    "ansiBrightYellow": "#F0D0A8",
    "ansiBrightBlue": "#D0CAE9",
    "ansiBrightMagenta": "#E3C2EF",
    "ansiBrightCyan": "#B8D8DC",
    "ansiBrightWhite": "#F2ECF2",
    "selection": "#4A354D",
    "selectionInactive": "#392A3A",
    "lineHighlight": "#2A202B",
    "cursor": "#D9B9E5",
    "findMatch": "#5A3D59",
    "findMatchBorder": "#C18DD4",
    "wordHighlight": "#443246",
    "bracketMatch": "#C18DD4",
}


# ---------------------------------------------------------------------------
# Workbench colors
# ---------------------------------------------------------------------------

def workbench(p):
    """Build the full `colors` map for one variant."""
    c = {}

    # --- base ---------------------------------------------------------------
    c["foreground"] = p["fg"]
    c["descriptionForeground"] = p["fg2"]
    c["disabledForeground"] = p["fgDisabled"]
    c["errorForeground"] = p["error"]
    c["icon.foreground"] = p["fg2"]
    c["focusBorder"] = p["accent"]
    c["contrastBorder"] = "#00000000"
    c["contrastActiveBorder"] = p["accent"]
    c["selection.background"] = p["selection"]
    c["widget.shadow"] = "#00000066"
    c["widget.border"] = p["border"]
    c["sash.hoverBorder"] = p["accent"]
    c["progressBar.background"] = p["accent"]
    c["textLink.foreground"] = p["accent2"]
    c["textLink.activeForeground"] = p["fg"]
    c["textBlockQuote.background"] = p["raised"]
    c["textBlockQuote.border"] = p["accent"]
    c["textCodeBlock.background"] = p["raised"]
    c["textPreformat.foreground"] = p["fg"]
    c["textPreformat.background"] = p["raised"]
    c["textPreformat.border"] = p["border"]
    c["textSeparator.foreground"] = p["border"]
    c["strongForeground"] = p["fg"]
    c["keybindingLabel.foreground"] = p["fg2"]
    c["keybindingLabel.border"] = p["border"]
    c["keybindingLabel.bottomBorder"] = p["border"]
    c["pickerGroup.foreground"] = p["accent"]
    c["pickerGroup.border"] = p["border"]

    # --- title bar ----------------------------------------------------------
    c["titleBar.activeBackground"] = p["bg"]
    c["titleBar.activeForeground"] = p["fg"]
    c["titleBar.inactiveBackground"] = p["bg"]
    c["titleBar.inactiveForeground"] = p["fgDisabled"]
    c["titleBar.border"] = p["borderSoft"]

    # --- activity bar -------------------------------------------------------
    c["activityBar.background"] = p["side"]
    c["activityBar.foreground"] = p["fg"]
    c["activityBar.inactiveForeground"] = p["fgDisabled"]
    c["activityBar.border"] = p["borderSoft"]
    c["activityBar.activeBorder"] = p["accent"]
    c["activityBar.activeBackground"] = a(p["accent"], 0.10)
    c["activityBarBadge.background"] = p["accent"]
    c["activityBarBadge.foreground"] = p["accentInk"]
    c["activityWarningBadge.background"] = p["warning"]
    c["activityWarningBadge.foreground"] = p["accentInk"]
    c["activityErrorBadge.background"] = p["error"]
    c["activityErrorBadge.foreground"] = p["accentInk"]
    c["activityBarTop.background"] = p["side"]
    c["activityBarTop.foreground"] = p["fg"]
    c["activityBarTop.inactiveForeground"] = p["fgDisabled"]
    c["activityBarTop.activeBorder"] = p["accent"]
    c["sideBarActivityBarTop.border"] = p["borderSoft"]

    # --- side bar -----------------------------------------------------------
    c["sideBar.background"] = p["side"]
    c["sideBar.foreground"] = p["fg2"]
    c["sideBar.border"] = p["borderSoft"]
    c["sideBarTitle.foreground"] = p["fg"]
    c["sideBarSectionHeader.background"] = p["side"]
    c["sideBarSectionHeader.foreground"] = p["fg"]
    c["sideBarSectionHeader.border"] = p["borderSoft"]
    c["sideBarStickyScroll.border"] = p["borderSoft"]
    c["tree.indentGuidesStroke"] = p["border"]
    c["tree.inactiveIndentGuidesStroke"] = p["borderSoft"]

    # --- editor -------------------------------------------------------------
    c["editor.background"] = p["editor"]
    c["editor.foreground"] = p["fg"]
    c["editor.border"] = p["borderSoft"]
    c["editorLineNumber.foreground"] = p["lineNumber"]
    c["editorLineNumber.activeForeground"] = p["lineNumberActive"]
    c["editorLineNumber.dimmedForeground"] = a(p["lineNumber"], 0.6)
    c["editorCursor.foreground"] = p["cursor"]
    c["editorCursor.background"] = p["editor"]
    c["editor.selectionBackground"] = p["selection"]
    c["editor.selectionForeground"] = p["fg"]
    c["editor.inactiveSelectionBackground"] = p["selectionInactive"]
    c["editor.selectionHighlightBackground"] = a(p["accent"], 0.18)
    c["editor.selectionHighlightBorder"] = a(p["accent"], 0.35)
    c["editor.wordHighlightBackground"] = p["wordHighlight"]
    c["editor.wordHighlightBorder"] = a(p["accent"], 0.30)
    c["editor.wordHighlightStrongBackground"] = a(p["accent"], 0.22)
    c["editor.wordHighlightStrongBorder"] = a(p["accent"], 0.45)
    c["editor.wordHighlightTextBackground"] = p["wordHighlight"]
    c["editor.wordHighlightTextBorder"] = a(p["accent"], 0.30)
    c["editor.lineHighlightBackground"] = p["lineHighlight"]
    c["editor.lineHighlightBorder"] = "#00000000"
    c["editor.inactiveLineHighlightBackground"] = p["lineHighlight"]
    c["editor.findMatchBackground"] = p["findMatch"]
    c["editor.findMatchForeground"] = p["fg"]
    c["editor.findMatchBorder"] = p["findMatchBorder"]
    c["editor.findMatchHighlightBackground"] = a(p["findMatch"], 0.55)
    c["editor.findMatchHighlightBorder"] = a(p["findMatchBorder"], 0.45)
    c["editor.findRangeHighlightBackground"] = a(p["accent"], 0.12)
    c["editor.findRangeHighlightBorder"] = "#00000000"
    c["editor.rangeHighlightBackground"] = a(p["accent"], 0.10)
    c["editor.rangeHighlightBorder"] = "#00000000"
    c["editor.hoverHighlightBackground"] = a(p["accent"], 0.14)
    c["editor.foldBackground"] = a(p["accent"], 0.10)
    c["editorWhitespace.foreground"] = a(p["border"], 0.9)
    c["editorIndentGuide.background1"] = a(p["border"], 0.75)
    c["editorIndentGuide.background"] = a(p["border"], 0.75)
    c["editorIndentGuide.activeBackground1"] = a(p["accent"], 0.45)
    c["editorIndentGuide.activeBackground"] = a(p["accent"], 0.45)
    c["editorRuler.foreground"] = p["border"]
    c["editorLink.activeForeground"] = p["accent2"]
    c["editorCodeLens.foreground"] = p["fg3"]
    c["editorLightBulb.foreground"] = p["warning"]
    c["editorLightBulbAutoFix.foreground"] = p["accent2"]
    c["editorBracketMatch.background"] = a(p["bracketMatch"], 0.16)
    c["editorBracketMatch.border"] = p["bracketMatch"]
    c["editorBracketMatch.foreground"] = p["bracketMatch"]
    c["editorBracketHighlight.foreground1"] = p["accent"]
    c["editorBracketHighlight.foreground2"] = p["accent2"]
    c["editorBracketHighlight.foreground3"] = p["ty"]
    c["editorBracketHighlight.foreground4"] = p["accent3"]
    c["editorBracketHighlight.foreground5"] = p["str"]
    c["editorBracketHighlight.foreground6"] = p["num"]
    c["editorBracketHighlight.unexpectedBracket.foreground"] = p["error"]
    c["editorBracketPairGuide.background1"] = a(p["accent"], 0.18)
    c["editorBracketPairGuide.background2"] = a(p["accent2"], 0.18)
    c["editorBracketPairGuide.background3"] = a(p["ty"], 0.18)
    c["editorBracketPairGuide.activeBackground1"] = a(p["accent"], 0.45)
    c["editorBracketPairGuide.activeBackground2"] = a(p["accent2"], 0.45)
    c["editorBracketPairGuide.activeBackground3"] = a(p["ty"], 0.45)
    c["editorGutter.background"] = p["editor"]
    c["editorGutter.addedBackground"] = p["gitAdded"]
    c["editorGutter.modifiedBackground"] = p["gitModified"]
    c["editorGutter.deletedBackground"] = p["gitDeleted"]
    c["editorGutter.addedSecondaryBackground"] = a(p["gitAdded"], 0.6)
    c["editorGutter.modifiedSecondaryBackground"] = a(p["gitModified"], 0.6)
    c["editorGutter.deletedSecondaryBackground"] = a(p["gitDeleted"], 0.6)
    c["editorGutter.foldingControlForeground"] = p["fg2"]
    c["editorGutter.commentDraftGlyphForeground"] = p["accent"]
    c["editorStickyScroll.background"] = p["editor"]
    c["editorStickyScrollHover.background"] = p["raised"]
    c["editorStickyScrollGutter.background"] = p["editor"]
    c["editorWidget.background"] = p["raised"]
    c["editorWidget.foreground"] = p["fg"]
    c["editorWidget.border"] = p["border"]
    c["editorWidget.resizeBorder"] = p["accent"]
    c["editorHoverWidget.background"] = p["raised"]
    c["editorHoverWidget.foreground"] = p["fg"]
    c["editorHoverWidget.border"] = p["border"]
    c["editorHoverWidget.statusBarBackground"] = p["raised2"]
    c["editorMarkerNavigation.background"] = p["raised"]
    c["editorMarkerNavigationError.background"] = p["error"]
    c["editorMarkerNavigationError.headerBackground"] = a(p["error"], 0.15)
    c["editorMarkerNavigationWarning.background"] = p["warning"]
    c["editorMarkerNavigationWarning.headerBackground"] = a(p["warning"], 0.15)
    c["editorMarkerNavigationInfo.background"] = p["info"]
    c["editorMarkerNavigationInfo.headerBackground"] = a(p["info"], 0.15)
    c["editorCommentsWidget.rangeBorder"] = a(p["accent"], 0.35)
    c["editorCommentsWidget.replyInputBackground"] = p["raised"]
    c["editorWordWrapIndicator.foreground"] = p["border"]
    c["editorUnicodeHighlight.border"] = p["warning"]
    c["editorUnicodeHighlight.background"] = a(p["warning"], 0.12)

    # --- diagnostics --------------------------------------------------------
    c["editorError.foreground"] = p["error"]
    c["editorWarning.foreground"] = p["warning"]
    c["editorInfo.foreground"] = p["info"]
    c["editorHint.foreground"] = p["fg3"]
    c["problemsErrorIcon.foreground"] = p["error"]
    c["problemsWarningIcon.foreground"] = p["warning"]
    c["problemsInfoIcon.foreground"] = p["info"]
    c["editorOverviewRuler.errorForeground"] = p["error"]
    c["editorOverviewRuler.warningForeground"] = p["warning"]
    c["editorOverviewRuler.infoForeground"] = p["info"]
    c["editorOverviewRuler.border"] = "#00000000"
    c["editorOverviewRuler.findMatchForeground"] = p["findMatchBorder"]
    c["editorOverviewRuler.selectionHighlightForeground"] = a(p["accent"], 0.6)
    c["editorOverviewRuler.wordHighlightForeground"] = a(p["accent"], 0.5)
    c["editorOverviewRuler.wordHighlightStrongForeground"] = a(p["accent"], 0.7)
    c["editorOverviewRuler.modifiedForeground"] = p["gitModified"]
    c["editorOverviewRuler.addedForeground"] = p["gitAdded"]
    c["editorOverviewRuler.deletedForeground"] = p["gitDeleted"]
    c["editorOverviewRuler.commentDraftForeground"] = p["accent"]
    c["editorOverviewRuler.inlineChatInserted"] = p["gitAdded"]
    c["editorOverviewRuler.inlineChatRemoved"] = p["gitDeleted"]

    # --- minimap ------------------------------------------------------------
    c["minimap.background"] = p["editor"]
    c["minimap.findMatchHighlight"] = p["findMatchBorder"]
    c["minimap.selectionHighlight"] = p["selection"]
    c["minimap.selectionOccurrenceHighlight"] = a(p["accent"], 0.35)
    c["minimap.errorHighlight"] = p["error"]
    c["minimap.warningHighlight"] = p["warning"]
    c["minimap.infoHighlight"] = p["info"]
    c["minimapGutter.addedBackground"] = p["gitAdded"]
    c["minimapGutter.modifiedBackground"] = p["gitModified"]
    c["minimapGutter.deletedBackground"] = p["gitDeleted"]
    c["minimapSlider.background"] = a(p["fg"], 0.08)
    c["minimapSlider.hoverBackground"] = a(p["fg"], 0.14)
    c["minimapSlider.activeBackground"] = a(p["accent"], 0.35)
    c["minimap.chatEditHighlight"] = a(p["accent"], 0.25)

    # --- editor groups & tabs ----------------------------------------------
    c["editorGroup.border"] = p["borderSoft"]
    c["editorGroupHeader.tabsBackground"] = p["bg"]
    c["editorGroupHeader.tabsBorder"] = p["borderSoft"]
    c["editorGroupHeader.border"] = p["borderSoft"]
    c["editorGroupHeader.noTabsBackground"] = p["bg"]
    c["editorGroupHeader.connectedTabsBackground"] = p["bg"]
    c["editorGroup.dropBackground"] = a(p["accent"], 0.12)
    c["editorGroup.dropIntoPromptForeground"] = p["fg"]
    c["editorGroup.dropIntoPromptBackground"] = p["raised"]
    c["editorGroup.emptyBackground"] = p["bg"]
    c["editorGroup.focusedEmptyBorder"] = p["accent"]
    c["tab.activeBackground"] = p["editor"]
    c["tab.activeForeground"] = p["fg"]
    c["tab.activeBorder"] = "#00000000"
    c["tab.activeBorderTop"] = p["accent"]
    c["tab.activeModifiedBorder"] = p["accent3"]
    c["tab.inactiveBackground"] = p["bg"]
    c["tab.inactiveForeground"] = p["fg3"]
    c["tab.inactiveModifiedBorder"] = a(p["accent3"], 0.6)
    c["tab.unfocusedActiveBackground"] = p["editor"]
    c["tab.unfocusedActiveForeground"] = p["fg2"]
    c["tab.unfocusedActiveBorder"] = "#00000000"
    c["tab.unfocusedActiveBorderTop"] = a(p["accent"], 0.45)
    c["tab.unfocusedInactiveBackground"] = p["bg"]
    c["tab.unfocusedInactiveForeground"] = p["fgDisabled"]
    c["tab.hoverBackground"] = p["raised"]
    c["tab.hoverForeground"] = p["fg"]
    c["tab.unfocusedHoverBackground"] = p["raised"]
    c["tab.unfocusedHoverForeground"] = p["fg2"]
    c["tab.border"] = p["borderSoft"]
    c["tab.divider"] = p["borderSoft"]
    c["tab.selectedBackground"] = p["editor"]
    c["tab.selectedForeground"] = p["fg"]
    c["tab.selectedBorderTop"] = p["accent"]
    c["tab.lastPinnedBorder"] = p["border"]

    # --- breadcrumbs --------------------------------------------------------
    c["breadcrumb.background"] = p["editor"]
    c["breadcrumb.foreground"] = p["fg3"]
    c["breadcrumb.focusForeground"] = p["fg"]
    c["breadcrumb.activeSelectionForeground"] = p["accent"]
    c["breadcrumbPicker.background"] = p["raised"]

    # --- status bar ---------------------------------------------------------
    c["statusBar.background"] = p["side"]
    c["statusBar.foreground"] = p["fg2"]
    c["statusBar.border"] = p["borderSoft"]
    c["statusBar.focusBorder"] = p["accent"]
    c["statusBar.noFolderBackground"] = p["side"]
    c["statusBar.noFolderForeground"] = p["fg2"]
    c["statusBar.noFolderBorder"] = p["borderSoft"]
    c["statusBar.debuggingBackground"] = p["accent"]
    c["statusBar.debuggingForeground"] = p["accentInk"]
    c["statusBar.debuggingBorder"] = p["accent"]
    c["statusBarItem.hoverBackground"] = a(p["fg"], 0.10)
    c["statusBarItem.activeBackground"] = a(p["fg"], 0.16)
    c["statusBarItem.focusBorder"] = p["accent"]
    c["statusBarItem.prominentBackground"] = a(p["accent"], 0.18)
    c["statusBarItem.prominentForeground"] = p["fg"]
    c["statusBarItem.prominentHoverBackground"] = a(p["accent"], 0.28)
    c["statusBarItem.errorBackground"] = p["error"]
    c["statusBarItem.errorForeground"] = p["accentInk"]
    c["statusBarItem.warningBackground"] = p["warning"]
    c["statusBarItem.warningForeground"] = p["accentInk"]
    c["statusBarItem.remoteBackground"] = a(p["accent"], 0.16)
    c["statusBarItem.remoteForeground"] = p["accent"]
    c["statusBarItem.remoteHoverBackground"] = p["accent"]
    c["statusBarItem.remoteHoverForeground"] = p["accentInk"]

    # --- panel & terminal ---------------------------------------------------
    c["panel.background"] = p["panel"]
    c["panel.border"] = p["borderSoft"]
    c["panel.dropBackground"] = a(p["accent"], 0.12)
    c["panelTitle.activeForeground"] = p["fg"]
    c["panelTitle.inactiveForeground"] = p["fg3"]
    c["panelTitle.activeBorder"] = p["accent"]
    c["panelTitle.border"] = p["borderSoft"]
    c["panelSection.border"] = p["borderSoft"]
    c["panelSectionHeader.background"] = p["panel"]
    c["panelSectionHeader.foreground"] = p["fg2"]
    c["panelInput.border"] = p["border"]
    c["panelStickyScroll.background"] = p["panel"]
    c["panelStickyScroll.border"] = p["borderSoft"]
    c["terminal.background"] = p["panel"]
    c["terminal.foreground"] = p["fg"]
    c["terminal.border"] = p["borderSoft"]
    c["terminal.selectionBackground"] = p["selection"]
    c["terminal.inactiveSelectionBackground"] = p["selectionInactive"]
    c["terminal.findMatchBackground"] = p["findMatch"]
    c["terminal.findMatchBorder"] = p["findMatchBorder"]
    c["terminal.findMatchHighlightBackground"] = a(p["findMatch"], 0.55)
    c["terminalCursor.foreground"] = p["cursor"]
    c["terminalCursor.background"] = p["panel"]
    c["terminal.tab.activeBorder"] = p["accent"]
    c["terminalCommandGuide.foreground"] = p["border"]
    c["terminalCommandDecoration.defaultBackground"] = p["fg3"]
    c["terminalCommandDecoration.successBackground"] = p["success"]
    c["terminalCommandDecoration.errorBackground"] = p["error"]
    c["terminal.ansiBlack"] = p["ansiBlack"]
    c["terminal.ansiRed"] = p["ansiRed"]
    c["terminal.ansiGreen"] = p["ansiGreen"]
    c["terminal.ansiYellow"] = p["ansiYellow"]
    c["terminal.ansiBlue"] = p["ansiBlue"]
    c["terminal.ansiMagenta"] = p["ansiMagenta"]
    c["terminal.ansiCyan"] = p["ansiCyan"]
    c["terminal.ansiWhite"] = p["ansiWhite"]
    c["terminal.ansiBrightBlack"] = p["ansiBrightBlack"]
    c["terminal.ansiBrightRed"] = p["ansiBrightRed"]
    c["terminal.ansiBrightGreen"] = p["ansiBrightGreen"]
    c["terminal.ansiBrightYellow"] = p["ansiBrightYellow"]
    c["terminal.ansiBrightBlue"] = p["ansiBrightBlue"]
    c["terminal.ansiBrightMagenta"] = p["ansiBrightMagenta"]
    c["terminal.ansiBrightCyan"] = p["ansiBrightCyan"]
    c["terminal.ansiBrightWhite"] = p["ansiBrightWhite"]
    c["terminalSymbolIcon.branchForeground"] = p["gitModified"]
    c["terminalSymbolIcon.commitForeground"] = p["warning"]
    c["terminalSymbolIcon.pullRequestDoneForeground"] = p["success"]
    c["terminalSymbolIcon.pullRequestForeground"] = p["accent"]
    c["terminalSymbolIcon.remoteForeground"] = p["info"]
    c["terminalSymbolIcon.stashForeground"] = p["error"]
    c["terminalSymbolIcon.symbolText"] = p["fg"]
    c["terminalSymbolIcon.symbolicLinkFileForeground"] = p["info"]
    c["terminalSymbolIcon.symbolicLinkFolderForeground"] = p["info"]
    c["terminalSymbolIcon.tagForeground"] = p["warning"]

    # --- command palette / quick input -------------------------------------
    c["quickInput.background"] = p["raised"]
    c["quickInput.foreground"] = p["fg"]
    c["quickInputTitle.background"] = p["raised2"]
    c["quickInputList.focusBackground"] = a(p["accent"], 0.20)
    c["quickInputList.focusForeground"] = p["fg"]
    c["quickInputList.focusOutline"] = p["accent"]
    c["quickInputList.focusIconForeground"] = p["accent"]
    c["quickInputList.focusHighlightForeground"] = p["accent"]
    c["commandCenter.foreground"] = p["fg2"]
    c["commandCenter.activeForeground"] = p["fg"]
    c["commandCenter.activeBorder"] = p["accent"]
    c["commandCenter.activeBackground"] = p["raised2"]
    c["commandCenter.inactiveForeground"] = p["fg3"]
    c["commandCenter.inactiveBorder"] = p["borderSoft"]
    c["commandCenter.background"] = p["bg"]
    c["commandCenter.activeBackground"] = p["raised"]
    c["commandCenter.border"] = p["borderSoft"]
    c["commandCenter.debuggingBackground"] = a(p["accent"], 0.18)

    # --- notifications ------------------------------------------------------
    c["notifications.background"] = p["raised"]
    c["notifications.foreground"] = p["fg"]
    c["notifications.border"] = p["border"]
    c["notificationsErrorIcon.foreground"] = p["error"]
    c["notificationsWarningIcon.foreground"] = p["warning"]
    c["notificationsInfoIcon.foreground"] = p["info"]
    c["notificationLink.foreground"] = p["accent2"]
    c["notificationToast.border"] = p["border"]
    c["notificationCenter.border"] = p["border"]
    c["notificationCenterHeader.background"] = p["raised2"]
    c["notificationCenterHeader.foreground"] = p["fg"]

    # --- lists & trees ------------------------------------------------------
    c["list.activeSelectionBackground"] = a(p["accent"], 0.20)
    c["list.activeSelectionForeground"] = p["fg"]
    c["list.activeSelectionIconForeground"] = p["accent"]
    c["list.inactiveSelectionBackground"] = a(p["accent"], 0.10)
    c["list.inactiveSelectionForeground"] = p["fg2"]
    c["list.inactiveSelectionIconForeground"] = p["fg2"]
    c["list.focusBackground"] = a(p["accent"], 0.24)
    c["list.focusForeground"] = p["fg"]
    c["list.focusOutline"] = p["accent"]
    c["list.focusAndSelectionOutline"] = p["accent"]
    c["list.hoverBackground"] = a(p["fg"], 0.06)
    c["list.hoverForeground"] = p["fg"]
    c["list.highlightForeground"] = p["accent"]
    c["list.dropBackground"] = a(p["accent"], 0.14)
    c["list.dropBetweenBackground"] = p["accent"]
    c["list.errorForeground"] = p["error"]
    c["list.warningForeground"] = p["warning"]
    c["list.filterMatchBackground"] = a(p["accent"], 0.22)
    c["list.filterMatchBorder"] = p["accent"]
    c["listFilterWidget.background"] = p["raised"]
    c["listFilterWidget.outline"] = p["accent"]
    c["listFilterWidget.noMatchesOutline"] = p["error"]
    c["listFilterWidget.shadow"] = "#00000066"

    # --- menus --------------------------------------------------------------
    c["menu.background"] = p["raised"]
    c["menu.foreground"] = p["fg"]
    c["menu.border"] = p["border"]
    c["menu.selectionBackground"] = a(p["accent"], 0.20)
    c["menu.selectionForeground"] = p["fg"]
    c["menu.selectionBorder"] = "#00000000"
    c["menu.separatorBackground"] = p["border"]
    c["menubar.selectionBackground"] = a(p["fg"], 0.10)
    c["menubar.selectionForeground"] = p["fg"]
    c["menubar.selectionBorder"] = "#00000000"

    # --- buttons ------------------------------------------------------------
    c["button.background"] = p["accent"]
    c["button.foreground"] = p["accentInk"]
    c["button.hoverBackground"] = a(p["accent"], 0.85)
    c["button.border"] = "#00000000"
    c["button.separator"] = a(p["accentInk"], 0.25)
    c["button.secondaryBackground"] = p["raised2"]
    c["button.secondaryForeground"] = p["fg"]
    c["button.secondaryHoverBackground"] = a(p["fg"], 0.12)
    c["button.secondaryBorder"] = p["border"]
    c["extensionButton.background"] = a(p["accent"], 0.16)
    c["extensionButton.foreground"] = p["accent"]
    c["extensionButton.hoverBackground"] = a(p["accent"], 0.28)
    c["extensionButton.border"] = a(p["accent"], 0.35)
    c["extensionButton.prominentBackground"] = p["accent"]
    c["extensionButton.prominentForeground"] = p["accentInk"]
    c["extensionButton.prominentHoverBackground"] = a(p["accent"], 0.85)
    c["extensionButton.separator"] = a(p["accent"], 0.35)
    c["extensionIcon.verifiedForeground"] = p["success"]
    c["extensionIcon.preReleaseForeground"] = p["warning"]
    c["extensionIcon.starForeground"] = p["warning"]
    c["extensionBadge.remoteForeground"] = p["fg"]
    c["extensionBadge.remoteBackground"] = p["accent"]

    # --- inputs -------------------------------------------------------------
    c["input.background"] = p["raised"]
    c["input.foreground"] = p["fg"]
    c["input.border"] = p["border"]
    c["input.placeholderForeground"] = p["fg3"]
    c["inputOption.activeBackground"] = a(p["accent"], 0.22)
    c["inputOption.activeForeground"] = p["fg"]
    c["inputOption.activeBorder"] = p["accent"]
    c["inputOption.hoverBackground"] = a(p["fg"], 0.08)
    c["inputValidation.errorBackground"] = a(p["error"], 0.12)
    c["inputValidation.errorBorder"] = p["error"]
    c["inputValidation.warningBackground"] = a(p["warning"], 0.12)
    c["inputValidation.warningBorder"] = p["warning"]
    c["inputValidation.infoBackground"] = a(p["info"], 0.12)
    c["inputValidation.infoBorder"] = p["info"]
    c["dropdown.background"] = p["raised"]
    c["dropdown.foreground"] = p["fg"]
    c["dropdown.border"] = p["border"]
    c["dropdown.listBackground"] = p["raised"]
    c["checkbox.background"] = p["raised"]
    c["checkbox.foreground"] = p["fg"]
    c["checkbox.border"] = p["border"]
    c["checkbox.disabled.background"] = a(p["raised"], 0.5)
    c["checkbox.disabled.foreground"] = p["fgDisabled"]

    # --- badges -------------------------------------------------------------
    c["badge.background"] = p["accent"]
    c["badge.foreground"] = p["accentInk"]

    # --- scrollbars ---------------------------------------------------------
    c["scrollbar.shadow"] = "#00000066"
    c["scrollbarSlider.background"] = a(p["fg"], 0.12)
    c["scrollbarSlider.hoverBackground"] = a(p["fg"], 0.20)
    c["scrollbarSlider.activeBackground"] = a(p["accent"], 0.55)

    # --- suggest widget -----------------------------------------------------
    c["editorSuggestWidget.background"] = p["raised"]
    c["editorSuggestWidget.foreground"] = p["fg"]
    c["editorSuggestWidget.border"] = p["border"]
    c["editorSuggestWidget.selectedBackground"] = a(p["accent"], 0.20)
    c["editorSuggestWidget.selectedForeground"] = p["fg"]
    c["editorSuggestWidget.highlightForeground"] = p["accent"]
    c["editorSuggestWidget.focusHighlightForeground"] = p["accent"]
    c["editorSuggestWidget.focusOutline"] = p["accent"]

    # --- peek view ----------------------------------------------------------
    c["peekView.border"] = p["accent"]
    c["peekViewEditor.background"] = p["raised"]
    c["peekViewEditorGutter.background"] = p["raised"]
    c["peekViewEditor.matchHighlightBackground"] = a(p["accent"], 0.30)
    c["peekViewEditor.matchHighlightBorder"] = p["accent"]
    c["peekViewEditorStickyScroll.background"] = p["raised"]
    c["peekViewEditorStickyScrollGutter.background"] = p["raised"]
    c["peekViewResult.background"] = p["panel"]
    c["peekViewResult.fileForeground"] = p["fg"]
    c["peekViewResult.lineForeground"] = p["fg2"]
    c["peekViewResult.matchHighlightBackground"] = a(p["accent"], 0.30)
    c["peekViewResult.selectionBackground"] = a(p["accent"], 0.22)
    c["peekViewResult.selectionForeground"] = p["fg"]
    c["peekViewTitle.background"] = p["raised2"]
    c["peekViewTitleLabel.foreground"] = p["fg"]
    c["peekViewTitleDescription.foreground"] = p["fg2"]

    # --- diff editor --------------------------------------------------------
    c["diffEditor.border"] = p["borderSoft"]
    c["diffEditor.insertedTextBackground"] = a(p["gitAdded"], 0.16)
    c["diffEditor.insertedLineBackground"] = a(p["gitAdded"], 0.10)
    c["diffEditor.removedTextBackground"] = a(p["gitDeleted"], 0.16)
    c["diffEditor.removedLineBackground"] = a(p["gitDeleted"], 0.10)
    c["diffEditorGutter.insertedLineBackground"] = a(p["gitAdded"], 0.20)
    c["diffEditorGutter.removedLineBackground"] = a(p["gitDeleted"], 0.20)
    c["diffEditorOverview.insertedForeground"] = p["gitAdded"]
    c["diffEditorOverview.removedForeground"] = p["gitDeleted"]
    c["diffEditor.unchangedRegionBackground"] = p["panel"]
    c["diffEditor.unchangedRegionForeground"] = p["fg3"]
    c["diffEditor.unchangedCodeBackground"] = a(p["fg"], 0.04)

    # --- merge --------------------------------------------------------------
    c["merge.border"] = "#00000000"
    c["merge.currentHeaderBackground"] = a(p["gitAdded"], 0.30)
    c["merge.currentContentBackground"] = a(p["gitAdded"], 0.12)
    c["merge.incomingHeaderBackground"] = a(p["info"], 0.30)
    c["merge.incomingContentBackground"] = a(p["info"], 0.12)
    c["merge.commonHeaderBackground"] = a(p["fg"], 0.12)
    c["merge.commonContentBackground"] = a(p["fg"], 0.06)

    # --- git decorations ----------------------------------------------------
    c["gitDecoration.addedResourceForeground"] = p["gitAdded"]
    c["gitDecoration.modifiedResourceForeground"] = p["gitModified"]
    c["gitDecoration.deletedResourceForeground"] = p["gitDeleted"]
    c["gitDecoration.renamedResourceForeground"] = p["accent2"]
    c["gitDecoration.untrackedResourceForeground"] = p["gitUntracked"]
    c["gitDecoration.ignoredResourceForeground"] = p["fgDisabled"]
    c["gitDecoration.conflictingResourceForeground"] = p["gitConflict"]
    c["gitDecoration.submoduleResourceForeground"] = p["accent3"]
    c["gitDecoration.stageModifiedResourceForeground"] = p["gitModified"]
    c["gitDecoration.stageDeletedResourceForeground"] = p["gitDeleted"]

    # --- debug --------------------------------------------------------------
    c["debugToolBar.background"] = p["raised"]
    c["debugToolBar.border"] = p["border"]
    c["debugIcon.breakpointForeground"] = p["error"]
    c["debugIcon.breakpointDisabledForeground"] = p["fgDisabled"]
    c["debugIcon.breakpointCurrentStackframeForeground"] = p["warning"]
    c["debugIcon.breakpointStackframeForeground"] = p["success"]
    c["debugIcon.startForeground"] = p["success"]
    c["debugIcon.pauseForeground"] = p["warning"]
    c["debugIcon.stopForeground"] = p["error"]
    c["debugIcon.restartForeground"] = p["success"]
    c["debugIcon.stepOverForeground"] = p["accent"]
    c["debugIcon.stepIntoForeground"] = p["accent"]
    c["debugIcon.stepOutForeground"] = p["accent"]
    c["debugIcon.continueForeground"] = p["success"]
    c["debugIcon.disconnectForeground"] = p["error"]
    c["debugConsole.errorForeground"] = p["error"]
    c["debugConsole.infoForeground"] = p["info"]
    c["debugConsole.warningForeground"] = p["warning"]
    c["debugConsole.sourceForeground"] = p["fg2"]
    c["debugConsoleInputIcon.foreground"] = p["accent"]
    c["debugTokenExpression.name"] = p["prop"]
    c["debugTokenExpression.value"] = p["str"]
    c["debugTokenExpression.string"] = p["str"]
    c["debugTokenExpression.number"] = p["num"]
    c["debugTokenExpression.boolean"] = p["bool"]
    c["debugTokenExpression.error"] = p["error"]
    c["debugTokenExpression.type"] = p["ty"]
    c["debugView.exceptionLabelForeground"] = p["accentInk"]
    c["debugView.exceptionLabelBackground"] = p["error"]
    c["debugView.stateLabelForeground"] = p["fg"]
    c["debugView.stateLabelBackground"] = p["raised2"]
    c["debugView.valueChangedHighlight"] = a(p["accent"], 0.30)
    c["debugView.reversedActiveValueBackground"] = a(p["accent"], 0.20)
    c["debugView.reversedActiveValueForeground"] = p["fg"]

    # --- testing ------------------------------------------------------------
    c["testing.iconPassed"] = p["success"]
    c["testing.iconFailed"] = p["error"]
    c["testing.iconErrored"] = p["error"]
    c["testing.iconQueued"] = p["warning"]
    c["testing.iconSkipped"] = p["fg3"]
    c["testing.iconUnset"] = p["fg3"]
    c["testing.message.error.decorationForeground"] = p["error"]
    c["testing.message.error.lineBackground"] = a(p["error"], 0.12)
    c["testing.message.warning.decorationForeground"] = p["warning"]
    c["testing.message.warning.lineBackground"] = a(p["warning"], 0.12)
    c["testing.message.info.decorationForeground"] = p["info"]
    c["testing.message.info.lineBackground"] = a(p["info"], 0.12)
    c["testing.coveredBackground"] = a(p["success"], 0.20)
    c["testing.coveredBorder"] = a(p["success"], 0.45)
    c["testing.uncoveredBackground"] = a(p["error"], 0.20)
    c["testing.uncoveredBorder"] = a(p["error"], 0.45)
    c["testing.coveredMinimapBackground"] = a(p["success"], 0.55)
    c["testing.uncoveredMinimapBackground"] = a(p["error"], 0.55)

    # --- settings -----------------------------------------------------------
    c["settings.headerForeground"] = p["fg"]
    c["settings.modifiedItemIndicator"] = p["accent"]
    c["settings.dropdownBackground"] = p["raised"]
    c["settings.dropdownForeground"] = p["fg"]
    c["settings.dropdownBorder"] = p["border"]
    c["settings.dropdownListBorder"] = p["border"]
    c["settings.checkboxBackground"] = p["raised"]
    c["settings.checkboxForeground"] = p["fg"]
    c["settings.checkboxBorder"] = p["border"]
    c["settings.textInputBackground"] = p["raised"]
    c["settings.textInputForeground"] = p["fg"]
    c["settings.textInputBorder"] = p["border"]
    c["settings.numberInputBackground"] = p["raised"]
    c["settings.numberInputForeground"] = p["fg"]
    c["settings.numberInputBorder"] = p["border"]
    c["settings.focusedRowBackground"] = a(p["accent"], 0.08)
    c["settings.focusedRowBorder"] = p["accent"]
    c["settings.rowHoverBackground"] = a(p["fg"], 0.05)
    c["settings.sashBorder"] = p["borderSoft"]

    # --- welcome / walkthrough ---------------------------------------------
    c["welcomePage.background"] = p["bg"]
    c["welcomePage.tileBackground"] = p["raised"]
    c["welcomePage.tileHoverBackground"] = p["raised2"]
    c["welcomePage.tileBorder"] = p["border"]
    c["welcomePage.progress.foreground"] = p["accent"]
    c["welcomePage.progress.background"] = p["border"]
    c["walkThrough.embeddedEditorBackground"] = p["editor"]

    # --- notebook -----------------------------------------------------------
    c["notebook.editorBackground"] = p["editor"]
    c["notebook.cellBorderColor"] = p["borderSoft"]
    c["notebook.cellEditorBackground"] = p["editor"]
    c["notebook.focusedCellBorder"] = p["accent"]
    c["notebook.focusedCellBackground"] = a(p["accent"], 0.06)
    c["notebook.inactiveFocusedCellBorder"] = a(p["accent"], 0.45)
    c["notebook.selectedCellBorder"] = p["accent"]
    c["notebook.cellStatusBarItemHoverBackground"] = a(p["fg"], 0.10)
    c["notebook.outputContainerBackgroundColor"] = p["panel"]
    c["notebook.outputContainerBorderColor"] = p["borderSoft"]
    c["notebook.focusedEditorBorder"] = p["accent"]

    # --- chat / agents ------------------------------------------------------
    c["chat.requestBackground"] = a(p["raised"], 0.62)
    c["chat.requestBorder"] = p["border"]
    c["chat.requestBubbleBackground"] = p["raised"]
    c["chat.requestBubbleHoverBackground"] = p["raised2"]
    c["chat.requestCodeBorder"] = p["border"]
    c["chat.avatarBackground"] = p["raised2"]
    c["chat.avatarForeground"] = p["accent"]
    c["chat.slashCommandForeground"] = p["accent"]
    c["chat.slashCommandBackground"] = "#00000000"
    c["chat.checkpointSeparator"] = p["border"]
    c["chat.editedFileForeground"] = p["gitModified"]
    c["chat.linesAddedForeground"] = p["gitAdded"]
    c["chat.linesRemovedForeground"] = p["gitDeleted"]
    c["chat.findMatchBackground"] = p["findMatch"]
    c["chat.findMatchHighlightBackground"] = a(p["findMatch"], 0.55)
    c["chat.thinkingShimmer"] = p["fg"]
    c["chat.statusBackground"] = a(p["fg"], 0.08)
    c["chat.inputWorkingBorderColor1"] = p["accent"]
    c["chat.inputWorkingBorderColor2"] = a(p["accent"], 0.50)
    c["chat.inputWorkingBorderColor3"] = a(p["accent"], 0.30)
    c["chat.voiceGlowBaseColor"] = p["accent"]
    c["chat.voiceListeningGlow"] = p["accent2"]
    c["chat.voiceSpeakingGlow"] = p["accent"]
    c["chat.dictationActiveMicGlow"] = p["accent"]
    c["chat.workingProgressStableIconForeground"] = p["accent"]
    c["chat.workingProgressInsidersIconForeground"] = p["accent3"]
    c["chat.fusionBadgeGradientStart"] = p["accent"]
    c["chat.fusionBadgeGradientEnd"] = p["accent3"]
    c["chat.mcpCompatibilityWarningForeground"] = p["warning"]
    c["chat.sessionStateIndicator.inProgressBorder"] = p["warning"]
    c["chat.sessionStateIndicator.unvisitedBorder"] = p["success"]
    c["chat.sessionStateIndicator.needsInputBorder"] = p["error"]
    c["chatManagement.sashBorder"] = p["borderSoft"]
    c["aiCustomizationManagement.sashBorder"] = p["borderSoft"]
    c["agents.background"] = p["bg"]
    c["agentsPanel.background"] = p["side"]
    c["agentsPanel.foreground"] = p["fg"]
    c["agentsPanel.border"] = p["border"]
    c["agentsCard.border"] = p["border"]
    c["agentsBottomPanel.border"] = p["border"]
    c["agentsDetail.background"] = p["panel"]
    c["agentsActivityBar.background"] = "#00000000"
    c["agentsActivityBar.border"] = "#00000000"
    c["agentsGradient.tintColor"] = p["accent"]
    c["agentsChatInput.background"] = p["raised"]
    c["agentsChatInput.foreground"] = p["fg"]
    c["agentsChatInput.border"] = p["border"]
    c["agentsChatInput.focusBorder"] = p["accent"]
    c["agentsChatInput.placeholderForeground"] = p["fg3"]
    c["agentsNewSessionButton.background"] = "#00000000"
    c["agentsNewSessionButton.foreground"] = p["fg"]
    c["agentsNewSessionButton.border"] = p["border"]
    c["agentsNewSessionButton.hoverBackground"] = a(p["fg"], 0.08)
    c["agentsBadge.background"] = p["accent"]
    c["agentsBadge.foreground"] = p["accentInk"]
    c["agentsUnreadBadge.background"] = p["accent"]
    c["agentsUnreadBadge.foreground"] = p["accentInk"]
    c["agentsUpdateButton.downloadingBackground"] = a(p["accent"], 0.40)
    c["agentsUpdateButton.downloadedBackground"] = a(p["accent"], 0.70)
    c["agentsVoice.speakingBackground"] = a(p["accent"], 0.14)
    c["agentsVoice.speakingForeground"] = p["accent"]
    c["agentsMobileDiff.addedForeground"] = p["gitAdded"]
    c["agentsMobileDiff.modifiedForeground"] = p["gitModified"]
    c["agentsMobileDiff.deletedForeground"] = p["gitDeleted"]
    c["agentsWindowGraphic.orange"] = p["warning"]
    c["agentFeedbackEditorWidget.background"] = p["raised"]
    c["agentFeedbackEditorWidget.border"] = p["border"]
    c["agentFeedbackInputWidget.border"] = p["accent"]
    c["agentSessionReadIndicator.foreground"] = a(p["fg"], 0.25)
    c["agentSessionSelectedBadge.border"] = a(p["accent"], 0.45)
    c["agentSessionSelectedUnfocusedBadge.border"] = a(p["fg"], 0.30)
    c["agentSessionNeedsInput.foreground"] = p["warning"]
    c["agentStatusIndicator.background"] = p["side"]
    c["activeSessionView.background"] = p["side"]
    c["activeSessionView.foreground"] = p["fg"]
    c["inactiveSessionView.background"] = p["bg"]
    c["inactiveSessionView.foreground"] = p["fg2"]
    c["inlineChat.background"] = p["raised"]
    c["inlineChat.foreground"] = p["fg"]
    c["inlineChat.border"] = p["accent"]
    c["inlineChat.shadow"] = "#00000066"
    c["inlineChatDiff.inserted"] = a(p["gitAdded"], 0.20)
    c["inlineChatDiff.removed"] = a(p["gitDeleted"], 0.20)
    c["inlineChatInput.background"] = p["raised2"]
    c["inlineChatInput.border"] = p["border"]
    c["inlineChatInput.focusBorder"] = p["accent"]
    c["inlineChatInput.placeholderForeground"] = p["fg3"]

    # --- markdown alerts ----------------------------------------------------
    c["markdownAlert.note.foreground"] = p["info"]
    c["markdownAlert.tip.foreground"] = p["success"]
    c["markdownAlert.important.foreground"] = p["accent"]
    c["markdownAlert.warning.foreground"] = p["warning"]
    c["markdownAlert.caution.foreground"] = p["error"]

    # --- misc ---------------------------------------------------------------
    c["actionBar.toggledBackground"] = a(p["accent"], 0.18)
    c["toolbar.hoverBackground"] = a(p["fg"], 0.10)
    c["toolbar.activeBackground"] = a(p["accent"], 0.18)
    c["browser.border"] = p["border"]
    c["ports.iconRunningProcessForeground"] = p["success"]
    c["mcpIcon.starForeground"] = p["warning"]
    c["confetti.color1"] = p["accent"]
    c["confetti.color2"] = p["accent2"]
    c["confetti.color3"] = p["accent3"]
    c["confetti.color4"] = p["ty"]
    c["confetti.color5"] = p["str"]
    c["confetti.color6"] = p["num"]

    # --- modern UI (VS Code 1.147+) ----------------------------------------
    c["modernUI.shellBackground"] = p["bg"]
    c["modernUI.inactiveShellBackground"] = p["bg"]
    c["surface.background"] = p["side"]
    c["surface.foreground"] = p["fg2"]
    c["surface.border"] = p["borderSoft"]
    c["modernPanel.border"] = p["borderSoft"]
    c["modernSash.gripForeground"] = p["fg3"]
    c["modernActivityBar.background"] = p["side"]
    c["modernActivityBar.inactiveBackground"] = p["side"]
    c["modernActivityBar.border"] = p["borderSoft"]
    c["modernActivityBarItem.activeBackground"] = a(p["accent"], 0.16)
    c["modernActivityBarItem.activeForeground"] = p["accent"]
    c["modernActivityBarItem.hoverBackground"] = a(p["fg"], 0.08)
    c["modernActivityBarItem.hoverForeground"] = p["fg"]
    c["modernTab.activeBackground"] = a(p["accent"], 0.16)
    c["modernTab.activeForeground"] = p["accent"]
    c["modernTab.hoverBackground"] = a(p["fg"], 0.08)
    c["modernTab.hoverForeground"] = p["fg"]
    c["modernEditorTab.activeBackground"] = p["editor"]
    c["modernEditorTab.activeForeground"] = p["fg"]
    c["modernEditorTab.inactiveBackground"] = "#00000000"
    c["modernEditorTab.hoverBackground"] = p["raised"]
    c["modernEditorTab.hoverForeground"] = p["fg"]
    c["modernEditorTab.activeActionBackground"] = a(p["accent"], 0.16)
    c["modernEditorTab.hoverActionBackground"] = a(p["fg"], 0.10)
    c["modernEditorTab.activeHoverBackground"] = p["raised"]
    c["modernEditorTab.activeHoverActionBackground"] = a(p["accent"], 0.24)
    c["modernEditorTab.selectedActionBackground"] = a(p["accent"], 0.16)

    return c


# ---------------------------------------------------------------------------
# Syntax
# ---------------------------------------------------------------------------

def token_colors(p):
    """TextMate rules. Ordered from generic to specific, like the rest of the pack."""
    t = []

    def rule(name, scope, fg=None, style=None):
        settings = {}
        if fg:
            settings["foreground"] = fg
        if style:
            settings["fontStyle"] = style
        t.append({"name": name, "scope": scope, "settings": settings})

    rule("Global settings", [], p["fg"])
    t[0]["settings"] = {"background": p["editor"], "foreground": p["fg"]}

    # comments
    rule("Comment", "comment", p["fg3"], "italic")
    rule("Comment punctuation", "punctuation.definition.comment", p["fg3"], "italic")
    rule("Comment documentation", "comment.block.documentation", p["fg3"], "italic")
    rule("Comment TODO", "comment.line.keyword", p["accent3"], "italic bold")

    # strings
    rule("String", "string", p["str"])
    rule("String quoted", "string.quoted", p["str"])
    rule("String template", "string.template", p["str"])
    rule("String regexp", "string.regexp", p["escape"])
    rule("String escape", "constant.character.escape, text.html constant.character.entity.named", p["escape"])
    rule("String interpolation", "punctuation.definition.template-expression, punctuation.section.embedded", p["accent2"])
    rule("String interpolation content", "meta.embedded.line, meta.template.expression", p["fg"])

    # numbers / constants
    rule("Number", "constant.numeric", p["num"])
    rule("Boolean", "constant.language.boolean", p["bool"])
    rule("Language constant", "constant.language", p["bool"])
    rule("Other constant", "constant.other", p["num"])
    rule("Placeholder", "constant.other.placeholder", p["accent3"])

    # keywords
    rule("Keyword", "keyword", p["kw"])
    rule("Keyword control", "keyword.control", p["kwControl"], "italic")
    rule("Keyword operator", "keyword.operator", p["op"])
    rule("Keyword other", "keyword.other", p["kw"])
    rule("Storage", "storage.type, storage.modifier, storage.control", p["kw"])
    rule("Modifier", "modifier", p["kw"])
    rule("Import / export", "keyword.control.import, keyword.control.export, keyword.control.from, keyword.control.as", p["importKw"])
    rule("Module", "support.module, support.node", p["import"], "italic")
    rule("This / self", "variable.language.this, variable.language.self, variable.language.super", p["kwControl"], "italic")

    # functions
    rule("Function definition", "entity.name.function, meta.function entity.name.function", p["fn"])
    rule("Function call", "meta.function-call entity.name.function, support.function, entity.name.function.call", p["fn"])
    rule("Method definition", "meta.definition.method entity.name.function, entity.name.function.member", p["method"])
    rule("Method call", "meta.method-call entity.name.function, variable.other.object.property", p["method"])
    rule("Builtin function", "support.function.builtin", p["fn"], "italic")

    # types
    rule("Type", "support.type, entity.name.type, entity.other.inherited-class", p["ty"])
    rule("Class", "entity.name.type.class, support.class, entity.name.class", p["cls"])
    rule("Interface", "entity.name.type.interface, entity.name.type.alias", p["iface"])
    rule("Enum", "entity.name.type.enum, entity.name.type.enummember", p["enum"])
    rule("Type parameter", "entity.name.type.parameter", p["num"], "italic")
    rule("Namespace", "entity.name.type.namespace, entity.name.namespace", p["fg2"])
    rule("Primitive type", "storage.type.primitive, support.type.primitive", p["ty"], "italic")

    # variables
    rule("Variable", "variable, variable.other, support.variable", p["var"])
    rule("Variable parameter", "variable.parameter", p["param"], "italic")
    rule("Variable property", "variable.object.property, variable.other.property, meta.object-literal.key", p["prop"])
    rule("Variable constant", "variable.other.constant, variable.other.enummember", p["num"])
    rule("Variable readonly", "variable.other.readonly, variable.readonly", p["num"])
    rule("Variable default library", "variable.defaultLibrary, support.variable.magic", p["ty"], "italic")

    # operators & punctuation
    rule("Operator", "keyword.operator.assignment, keyword.operator.arithmetic, keyword.operator.logical, keyword.operator.comparison, keyword.operator.bitwise, keyword.operator.ternary", p["op"])
    rule("Punctuation", "punctuation", p["punct"])
    rule("Punctuation separator", "punctuation.separator, punctuation.terminator", p["punct"])
    rule("Punctuation accessor", "punctuation.accessor", p["op"])

    # decorators / annotations
    rule("Decorator", "meta.decorator, entity.name.function.decorator, punctuation.decorator", p["decorator"])
    rule("Annotation", "storage.type.annotation, punctuation.definition.annotation", p["decorator"])

    # JSON / YAML / INI
    rule("JSON key", "support.type.property-name.json, meta.object-literal.key string", p["prop"])
    rule("JSON constant", "constant.language.json", p["bool"])
    rule("YAML key", "entity.name.tag.yaml", p["prop"])
    rule("YAML anchor", "variable.other.anchor.yaml, entity.other.attribute-name.yaml", p["accent3"])
    rule("INI property", "keyword.other.definition.ini", p["prop"])
    rule("INI section", "entity.name.section.group-title.ini", p["accent"])

    # HTML / XML / JSX
    rule("HTML tag", "entity.name.tag, meta.tag entity.name.tag", p["tag"])
    rule("HTML tag punctuation", "punctuation.definition.tag", p["punct"])
    rule("HTML attribute", "entity.other.attribute-name", p["attr"])
    rule("HTML entity", "punctuation.definition.entity.html, constant.character.entity", p["escape"])
    rule("JSX component", "support.class.component", p["cls"])
    rule("JSX text", "meta.jsx.children, SXNested", p["fg"])

    # CSS / SCSS
    rule("CSS property", "support.type.property-name.css, support.type.property-name.scss", p["prop"])
    rule("CSS class", "entity.other.attribute-name.class.css, entity.other.attribute-name.class.scss", p["ty"])
    rule("CSS id", "entity.other.attribute-name.id.css", p["num"])
    rule("CSS pseudo", "entity.other.attribute-name.pseudo-class, entity.other.attribute-name.pseudo-element", p["accent3"])
    rule("CSS unit", "keyword.other.unit", p["num"])
    rule("CSS variable", "variable.css, variable.scss", p["accent2"])
    rule("CSS at-rule", "keyword.control.at-rule", p["kw"])

    # Markdown
    rule("Markdown heading", "markup.heading", p["mdHeading"], "bold")
    rule("Markdown heading punctuation", "punctuation.definition.heading", p["mdHeading"])
    rule("Markdown link", "markup.underline.link, string.other.link", p["mdLink"])
    rule("Markdown link text", "meta.link.inline, meta.link.reference", p["mdLink"])
    rule("Markdown list", "punctuation.definition.list", p["accent"])
    rule("Markdown italic", "markup.italic", p["fg"], "italic")
    rule("Markdown bold", "markup.bold", p["fg"], "bold")
    rule("Markdown quote", "markup.quote", p["fg2"], "italic")
    rule("Markdown inline code", "markup.inline.raw.string.markdown", p["mdCode"])
    rule("Markdown fenced code", "markup.fenced_code.block", p["fg2"])
    rule("Markdown separator", "meta.separator.markdown", p["border"])
    rule("Markup inserted", "markup.inserted", p["gitAdded"])
    rule("Markup deleted", "markup.deleted", p["gitDeleted"])
    rule("Markup changed", "markup.changed", p["gitModified"])

    # SQL
    rule("SQL keyword", "keyword.other.sql, keyword.other.DML.sql, keyword.other.DDL.sql", p["kw"])
    rule("SQL function", "support.function.aggregate.sql, support.function.scalar.sql", p["fn"])
    rule("SQL type", "storage.type.sql", p["ty"])
    rule("SQL table", "entity.name.table.sql", p["cls"])
    rule("SQL column", "entity.name.column.sql, variable.other.column.sql", p["prop"])

    # Shell / Dockerfile / Terraform
    rule("Shell variable", "variable.other.normal.shell, variable.other.special.shell", p["accent2"])
    rule("Shell command", "support.function.builtin.shell, entity.name.command.shell", p["fn"])
    rule("Dockerfile instruction", "keyword.other.special-method.dockerfile", p["kw"])
    rule("Terraform resource", "entity.name.type.terraform, entity.name.type.resource.terraform", p["cls"])
    rule("Terraform attribute", "variable.other.terraform, entity.other.attribute-name.terraform", p["prop"])

    # C / C++ / C# / Java / Go / Rust
    rule("C preprocessor", "meta.preprocessor, keyword.control.directive", p["accent3"])
    rule("C# namespace", "entity.name.type.namespace.cs", p["fg2"])
    rule("Go package", "entity.name.package.go", p["fg2"])
    rule("Rust lifetime", "storage.modifier.lifetime.rust, entity.name.type.lifetime.rust", p["num"], "italic")
    rule("Rust macro", "entity.name.function.macro.rust, support.macro.rust", p["decorator"])
    rule("Python self", "variable.parameter.function.language.special.self.python", p["kwControl"], "italic")
    rule("Python decorator", "entity.name.function.decorator.python", p["decorator"])
    rule("Python format placeholder", "constant.character.format.placeholder.other.python", p["num"])

    return t


def semantic_tokens(p):
    return {
        "namespace": p["fg2"],
        "type": p["ty"],
        "class": p["cls"],
        "enum": p["enum"],
        "interface": p["iface"],
        "struct": p["cls"],
        "typeParameter": p["num"],
        "parameter": p["param"],
        "variable": p["var"],
        "variable.readonly": p["num"],
        "variable.defaultLibrary": p["ty"],
        "property": p["prop"],
        "property.readonly": p["num"],
        "enumMember": p["num"],
        "event": p["accent3"],
        "function": p["fn"],
        "method": p["method"],
        "macro": p["decorator"],
        "keyword": p["kw"],
        "modifier": p["kw"],
        "comment": p["fg3"],
        "string": p["str"],
        "number": p["num"],
        "regexp": p["escape"],
        "operator": p["op"],
        "decorator": p["decorator"],
        "label": p["accent"],
        "*.deprecated": {"foreground": p["fg3"], "strikethrough": True},
        "*.declaration": {"bold": True},
        "*.static": {"italic": True},
        "*.readonly": {"italic": True},
        "*.async": {"italic": True},
        "*.abstract": {"italic": True},
        "*.modification": {"underline": True},
    }


def build(p):
    colors = workbench(p)
    if p["id"] == "carbon-candy-amethyst":
        for key in (
            "focusBorder",
            "contrastActiveBorder",
            "list.focusOutline",
            "list.focusAndSelectionOutline",
            "quickInputList.focusOutline",
            "editorSuggestWidget.focusOutline",
            "commandCenter.activeBorder",
            "commandCenter.inactiveBorder",
            "statusBar.focusBorder",
            "statusBarItem.focusBorder",
            "inputOption.activeBorder",
            "settings.focusedRowBorder",
        ):
            colors[key] = "#00000000"
    return {
        "name": p["id"],
        "type": "dark",
        "semanticHighlighting": True,
        "colors": colors,
        "tokenColors": token_colors(p),
        "semanticTokenColors": semantic_tokens(p),
    }


def main():
    for palette in (NOCTURNE, SYNTHWAVE, AMETHYST):
        theme = build(palette)
        out = THEMES / palette["file"]
        out.write_text(json.dumps(theme, indent=4) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} ({len(theme['colors'])} colors, "
              f"{len(theme['tokenColors'])} token rules)")


if __name__ == "__main__":
    main()
