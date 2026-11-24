#!/usr/bin/env python3
"""Add VS Code 1.147 "Modern UI" color tokens to every Carbon Candy theme.

VS Code 1.147 ships the Modern UI (``workbench.experimental.modernUI``, on by
default). It introduces a new set of color ids for the floating shell, the
modern activity bar, the connected editor tabs, inline chat, markdown alerts
and the chat surfaces. A theme that does not define them falls back to the
built-in palette, which ignores the Carbon Candy colors and makes the
workbench look foreign (dark pills on the activity bar, missing accent on the
active tab, untinted chat list, ...).

This script derives those tokens from each theme's own palette so every
variant keeps its identity under the Modern UI as well.

The script is idempotent: keys already present in a theme are never touched.
"""

import json
import re
from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent.parent / "themes"


def parse_hex(value):
    """Return the 8-digit hex body of a color, or None if it is not a color."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text.startswith("#"):
        return None
    body = text[1:]
    if len(body) in (3, 4):
        body = "".join(char * 2 for char in body)
    if len(body) not in (6, 8):
        return None
    try:
        int(body, 16)
    except ValueError:
        return None
    return body


def with_alpha(value, alpha):
    """Replace the alpha channel of a hex color, leaving other values alone."""
    body = parse_hex(value)
    if body is None:
        return value
    return "#" + body[:6] + alpha


def alpha_of(value):
    body = parse_hex(value)
    return body[6:8] if body else None


def is_light_theme(colors):
    body = parse_hex(colors.get("editor.background", "#000000"))
    if body is None:
        return False
    red, green, blue = (int(body[index:index + 2], 16) for index in (0, 2, 4))
    return 0.299 * red + 0.587 * green + 0.114 * blue > 140


def pick(colors, *keys, default=None):
    for key in keys:
        value = colors.get(key)
        if isinstance(value, str) and parse_hex(value) is not None:
            return value
    return default


def pick_visible(colors, background, *keys, default=None):
    """Pick the first color that is actually distinguishable from `background`.

    Several Carbon Candy variants set ``list.hoverBackground`` to the same value
    as the editor background, which would make the Modern UI hover states
    invisible.
    """
    base = parse_hex(background)
    for key in keys:
        value = colors.get(key)
        body = parse_hex(value)
        if body is None:
            continue
        if base is not None and body[:6] == base[:6] and body[6:8] in ("", "ff"):
            continue
        return value
    return default


def build_tokens(colors, thin_border):
    background = pick(colors, "editor.background", default="#000000")
    foreground = pick(colors, "foreground", "editor.foreground", default="#D9D9D9")
    side_bar = pick(colors, "sideBar.background", "editor.background", default=background)
    side_bar_foreground = pick(colors, "sideBar.foreground", "foreground", default=foreground)

    accent = pick(
        colors,
        "button.background",
        "progressBar.background",
        "activityBarBadge.background",
        "textLink.foreground",
        default=foreground,
    )
    # `focusBorder` is intentionally transparent in most variants (the theme
    # hides focus rings), so it cannot be used as the accent source.
    focus = pick(colors, "focusBorder", default=accent)
    if alpha_of(focus) == "00":
        focus = accent

    title_bar = pick(colors, "titleBar.activeBackground", "editor.background", default=background)
    title_bar_inactive = pick(colors, "titleBar.inactiveBackground", default=title_bar)

    widget_background = pick(colors, "editorWidget.background", "editor.background", default=background)
    widget_border = pick(colors, "editorWidget.border", default=with_alpha(foreground, "1a"))
    surface_border = pick(
        colors,
        "editorGroup.border",
        "widget.border",
        "panel.border",
        default=with_alpha(foreground, "26"),
    )
    panel_border = pick(colors, "panel.border", default=surface_border)

    input_background = pick(colors, "input.background", "editorWidget.background", default=background)
    input_foreground = pick(colors, "input.foreground", "foreground", default=foreground)
    input_border = pick(colors, "input.border", default=with_alpha(foreground, "1a"))
    input_placeholder = pick(
        colors, "input.placeholderForeground", default=with_alpha(foreground, "99")
    )

    tab_active_background = pick(colors, "tab.activeBackground", "editor.background", default=background)
    tab_active_foreground = pick(colors, "tab.activeForeground", "foreground", default=foreground)
    tab_hover_background = pick_visible(
        colors,
        background,
        "tab.hoverBackground",
        "list.hoverBackground",
        "toolbar.hoverBackground",
        default=with_alpha(foreground, "0f"),
    )
    tabs_background = pick(
        colors, "editorGroupHeader.tabsBackground", "editor.background", default=background
    )

    activity_bar_background = pick(colors, "activityBar.background", "editor.background", default=background)
    activity_bar_foreground = pick(colors, "activityBar.foreground", "foreground", default=foreground)
    activity_bar_hover = pick_visible(
        colors,
        background,
        "list.hoverBackground",
        "toolbar.hoverBackground",
        default=with_alpha(foreground, "1a"),
    )

    added = pick(
        colors,
        "gitDecoration.addedResourceForeground",
        "editorGutter.addedBackground",
        "terminal.ansiGreen",
        default="#C3E88D",
    )
    modified = pick(
        colors,
        "gitDecoration.modifiedResourceForeground",
        "editorGutter.modifiedBackground",
        "terminal.ansiBlue",
        default="#82AAFF",
    )
    deleted = pick(
        colors,
        "gitDecoration.deletedResourceForeground",
        "editorGutter.deletedBackground",
        "terminal.ansiRed",
        default="#f07178",
    )

    blue = pick(colors, "charts.blue", "terminal.ansiBlue", default=modified)
    green = pick(colors, "charts.green", "terminal.ansiGreen", default=added)
    yellow = pick(colors, "charts.yellow", "terminal.ansiYellow", default="#FFCB6B")
    red = pick(colors, "charts.red", "terminal.ansiRed", default=deleted)
    purple = pick(colors, "charts.purple", "terminal.ansiMagenta", default="#C792EA")
    orange = pick(colors, "charts.orange", "terminal.ansiBrightYellow", "terminal.ansiYellow", default=yellow)

    line_highlight = pick(colors, "editor.lineHighlightBackground", default=with_alpha(foreground, "0a"))
    whitespace = pick(colors, "editorWhitespace.foreground", default=with_alpha(foreground, "26"))
    bracket_match = pick(colors, "editorBracketMatch.border", default=accent)
    status_bar = pick(colors, "statusBar.background", "editor.background", default=background)
    checkbox_background = pick(colors, "checkbox.background", "input.background", default=input_background)
    checkbox_foreground = pick(colors, "checkbox.foreground", "input.foreground", default=input_foreground)
    extension_button = pick(colors, "extensionButton.background", default=with_alpha(accent, "14"))
    peek_gutter = pick(colors, "peekViewEditorGutter.background", "editorWidget.background", default=widget_background)
    comment_glyph = pick(
        colors, "editorGutter.commentGlyphForeground", "editorGutter.commentRangeForeground", default=accent
    )
    comment_ruler = pick(
        colors, "editorOverviewRuler.commentForeground", "editorGutter.commentGlyphForeground", default=accent
    )
    comment_range = pick(colors, "editorCommentsWidget.unresolvedBorder", default=with_alpha(accent, "4d"))

    # Thin-border variants already expose a light-gray divider; reuse it so the
    # floating cards keep the bordered look of the rest of the workbench.
    card_border = panel_border if thin_border else surface_border

    return {
        # Floating shell and surfaces
        "modernUI.shellBackground": title_bar,
        "modernUI.inactiveShellBackground": title_bar_inactive,
        "surface.background": side_bar,
        "surface.foreground": side_bar_foreground,
        "surface.border": surface_border,
        "editor.border": surface_border,
        "modernPanel.border": card_border,
        "modernSash.gripForeground": with_alpha(foreground, "66"),
        # Modern activity bar
        "modernActivityBar.background": activity_bar_background,
        "modernActivityBar.border": card_border,
        "modernActivityBar.inactiveBackground": activity_bar_background,
        "modernActivityBarItem.activeBackground": with_alpha(accent, "1f"),
        "modernActivityBarItem.activeForeground": accent,
        "modernActivityBarItem.hoverBackground": activity_bar_hover,
        "modernActivityBarItem.hoverForeground": activity_bar_foreground,
        # Modern tabs (settings, model picker, ...)
        "modernTab.activeBackground": with_alpha(accent, "1f"),
        "modernTab.activeForeground": accent,
        "modernTab.hoverBackground": tab_hover_background,
        "modernTab.hoverForeground": foreground,
        # Connected editor tabs
        "editorGroupHeader.connectedTabsBackground": tabs_background,
        "tab.divider": surface_border,
        "tab.selectedBorderTop": accent,
        "modernEditorTab.activeBackground": tab_active_background,
        "modernEditorTab.activeForeground": tab_active_foreground,
        "modernEditorTab.inactiveBackground": "#00000000",
        "modernEditorTab.hoverBackground": tab_hover_background,
        "modernEditorTab.hoverForeground": tab_active_foreground,
        "modernEditorTab.activeActionBackground": with_alpha(accent, "1a"),
        "modernEditorTab.hoverActionBackground": with_alpha(foreground, "1a"),
        "modernEditorTab.activeHoverBackground": tab_hover_background,
        "modernEditorTab.activeHoverActionBackground": with_alpha(accent, "26"),
        "modernEditorTab.selectedActionBackground": with_alpha(accent, "1a"),
        # Inline chat
        "inlineChat.background": widget_background,
        "inlineChat.border": widget_border,
        "inlineChat.foreground": foreground,
        "inlineChat.shadow": pick(colors, "widget.shadow", default=with_alpha("#000000", "4d")),
        "inlineChatDiff.inserted": with_alpha(added, "33"),
        "inlineChatDiff.removed": with_alpha(deleted, "33"),
        "inlineChatInput.background": input_background,
        "inlineChatInput.border": input_border,
        "inlineChatInput.focusBorder": accent,
        "inlineChatInput.placeholderForeground": input_placeholder,
        # Chat surfaces
        "chat.fusionBadgeGradientStart": accent,
        "chat.fusionBadgeGradientEnd": purple,
        "chat.inputWorkingBorderColor2": with_alpha(accent, "80"),
        "chat.inputWorkingBorderColor3": with_alpha(accent, "4d"),
        "chat.voiceListeningGlow": accent,
        "chat.voiceSpeakingGlow": accent,
        "chat.workingProgressStableIconForeground": accent,
        "chat.workingProgressInsidersIconForeground": accent,
        # Markdown alerts
        "markdownAlert.note.foreground": blue,
        "markdownAlert.tip.foreground": green,
        "markdownAlert.important.foreground": purple,
        "markdownAlert.warning.foreground": yellow,
        "markdownAlert.caution.foreground": red,
        # Editor decorations
        "editor.inactiveLineHighlightBackground": line_highlight,
        "editorBracketMatch.foreground": bracket_match,
        "editorWordWrapIndicator.foreground": whitespace,
        "editorSuggestWidget.focusOutline": accent,
        "quickInputList.focusHighlightForeground": accent,
        "editorStickyScrollGutter.background": background,
        "editorCommentsWidget.rangeBorder": comment_range,
        "editorGutter.addedSecondaryBackground": added,
        "editorGutter.deletedSecondaryBackground": deleted,
        "editorGutter.modifiedSecondaryBackground": modified,
        "editorGutter.commentDraftGlyphForeground": comment_glyph,
        "editorOverviewRuler.commentDraftForeground": comment_ruler,
        "editorOverviewRuler.inlineChatInserted": added,
        "editorOverviewRuler.inlineChatRemoved": deleted,
        "editorMinimap.inlineChatInserted": added,
        "minimap.chatEditHighlight": with_alpha(background, "99"),
        "peekViewEditorStickyScrollGutter.background": peek_gutter,
        # Status bar
        "statusBar.inactiveBackground": status_bar,
        # Buttons and widgets
        "button.secondaryBorder": with_alpha(foreground, "26"),
        "extensionButton.border": extension_button,
        "textPreformat.border": widget_border,
        "checkbox.disabled.background": with_alpha(checkbox_background, "33"),
        "checkbox.disabled.foreground": with_alpha(checkbox_foreground, "33"),
        "browser.border": surface_border,
        "walkThrough.embeddedEditorBackground": with_alpha(background, "66"),
        # Testing
        "testing.coveredMinimapBackground": with_alpha(added, "99"),
        "testing.uncoveredMinimapBackground": with_alpha(deleted, "99"),
        # Confetti (welcome / release notes)
        "confetti.color1": red,
        "confetti.color2": orange,
        "confetti.color3": yellow,
        "confetti.color4": green,
        "confetti.color5": blue,
        "confetti.color6": purple,
        # Terminal symbol icons
        "terminalSymbolIcon.branchForeground": pick(colors, "terminal.ansiBlue", default=blue),
        "terminalSymbolIcon.commitForeground": pick(colors, "terminal.ansiYellow", default=yellow),
        "terminalSymbolIcon.pullRequestForeground": pick(colors, "terminal.ansiMagenta", default=purple),
        "terminalSymbolIcon.pullRequestDoneForeground": pick(colors, "terminal.ansiGreen", default=green),
        "terminalSymbolIcon.remoteForeground": pick(colors, "terminal.ansiCyan", default=blue),
        "terminalSymbolIcon.stashForeground": pick(colors, "terminal.ansiRed", default=red),
        "terminalSymbolIcon.tagForeground": pick(colors, "terminal.ansiYellow", default=yellow),
        "terminalSymbolIcon.symbolText": foreground,
        "terminalSymbolIcon.symbolicLinkFileForeground": pick(colors, "terminal.ansiCyan", default=blue),
        "terminalSymbolIcon.symbolicLinkFolderForeground": pick(colors, "terminal.ansiCyan", default=blue),
        # Agents window extras
        "agentsVoice.speakingBackground": with_alpha(accent, "14"),
        "agentsVoice.speakingForeground": accent,
        "agentsWindowGraphic.orange": orange,
        "mcpIcon.starForeground": orange,
        "strongForeground": foreground,
    }


def detect_indent(raw):
    match = re.search(r"\n( +)\"", raw)
    return len(match.group(1)) if match else 4


def main():
    for path in sorted(THEMES_DIR.glob("*.json")):
        raw = path.read_text(encoding="utf-8")
        theme = json.loads(raw)
        colors = theme.setdefault("colors", {})
        tokens = build_tokens(colors, path.name.endswith("-thin-border.json"))

        added = {key: value for key, value in tokens.items() if key not in colors}
        if not added:
            print(f"{path.name}: already up to date")
            continue

        colors.update(added)
        path.write_text(
            json.dumps(theme, ensure_ascii=False, indent=detect_indent(raw)) + "\n",
            encoding="utf-8",
        )
        print(f"{path.name}: added {len(added)} Modern UI colors")


if __name__ == "__main__":
    main()
