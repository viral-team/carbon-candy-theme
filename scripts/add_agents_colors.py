#!/usr/bin/env python3
"""Add Agents window color tokens to every Carbon Candy theme.

VS Code's Agents window (agent sessions) is themed through its own color ids
(``agents*``, ``agentsPanel*``, ``agentsChatInput*``, ``agentSession*``, ...).
A theme that does not define them falls back to the built-in defaults, which
ignore the Carbon Candy palette and make the Agents window look foreign.

This script derives those tokens from each theme's existing palette so every
variant keeps its identity in the Agents window as well.

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


def build_tokens(colors, thin_border):
    background = pick(colors, "editor.background", default="#000000")
    side_bar = pick(colors, "sideBar.background", "editor.background", default=background)
    foreground = pick(colors, "foreground", "editor.foreground", default="#D9D9D9")
    # `sideBar.foreground` is intentionally dim in these themes (inactive explorer
    # items), so panel text uses the regular foreground to stay readable.
    panel_foreground = foreground

    accent = pick(
        colors,
        "button.background",
        "progressBar.background",
        "activityBarBadge.background",
        "textLink.foreground",
        default=foreground,
    )
    focus = pick(colors, "focusBorder", default=accent)
    if alpha_of(focus) == "00":
        focus = accent

    input_background = pick(colors, "input.background", "editorWidget.background", default=background)
    input_foreground = pick(colors, "input.foreground", "foreground", default=foreground)
    input_border = pick(colors, "input.border", default=with_alpha(foreground, "1a"))
    input_placeholder = pick(
        colors, "input.placeholderForeground", default=with_alpha(foreground, "99")
    )

    widget_background = pick(colors, "editorWidget.background", "editor.background", default=background)
    widget_border = pick(colors, "editorWidget.border", default=with_alpha(foreground, "1a"))

    badge_background = pick(colors, "activityBarBadge.background", default=accent)
    badge_foreground = pick(colors, "activityBarBadge.foreground", default=background)

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
        "terminal.ansiYellow",
        default="#FFCB6B",
    )
    deleted = pick(
        colors,
        "gitDecoration.deletedResourceForeground",
        "editorGutter.deletedBackground",
        "terminal.ansiRed",
        default="#f07178",
    )
    warning = pick(
        colors, "list.warningForeground", "editorWarning.foreground", "terminal.ansiYellow",
        default=modified,
    )
    error = pick(
        colors, "errorForeground", "editorError.foreground", "terminal.ansiRed", default=deleted
    )

    toolbar_hover = pick(colors, "toolbar.hoverBackground", default=with_alpha(foreground, "1a"))
    secondary_border = pick(
        colors, "button.secondaryBorder", "button.border", default=with_alpha(foreground, "33")
    )
    command_center = pick(
        colors, "commandCenter.background", "titleBar.activeBackground", default=background
    )
    list_selection_foreground = pick(
        colors, "list.activeSelectionForeground", default=accent
    )
    bubble_background = pick(colors, "input.background", "editorWidget.background", default=background)
    bubble_hover = pick(colors, "list.hoverBackground", default=bubble_background)
    separator = pick(
        colors, "editorIndentGuide.background", default=with_alpha(foreground, "26")
    )
    # Chat find matches must stay translucent so they do not hide the transcript.
    find_match = with_alpha(
        pick(colors, "editor.findMatchBackground", default=accent), "80"
    )
    find_match_highlight = with_alpha(
        pick(colors, "editor.findMatchHighlightBackground", default=accent), "4d"
    )

    # Thin-border variants already expose a light-gray divider; reuse it so the
    # Agents window cards match the rest of the workbench.
    if thin_border:
        card_border = pick(colors, "panel.border", "editorGroup.border", default=with_alpha(foreground, "26"))
    else:
        card_border = with_alpha(foreground, "26")

    return {
        # Shell and panels
        "agents.background": background,
        "agentsPanel.background": side_bar,
        "agentsPanel.foreground": panel_foreground,
        "agentsPanel.border": card_border,
        "agentsCard.border": card_border,
        "agentsBottomPanel.border": card_border,
        "agentsDetail.background": background,
        "agentsActivityBar.background": "#00000000",
        "agentsActivityBar.border": card_border if thin_border else "#00000000",
        "agentsGradient.tintColor": accent,
        # Agent feedback widgets
        "agentFeedbackEditorWidget.background": widget_background,
        "agentFeedbackEditorWidget.border": with_alpha(foreground, "59"),
        "agentFeedbackInputWidget.border": widget_border,
        # Update button
        "agentsUpdateButton.downloadingBackground": with_alpha(accent, "66"),
        "agentsUpdateButton.downloadedBackground": with_alpha(accent, "b3"),
        # Chat input
        "agentsChatInput.background": input_background,
        "agentsChatInput.foreground": input_foreground,
        "agentsChatInput.border": input_border,
        "agentsChatInput.focusBorder": focus,
        "agentsChatInput.placeholderForeground": input_placeholder,
        # New session button
        "agentsNewSessionButton.background": "#00000000",
        "agentsNewSessionButton.foreground": panel_foreground,
        "agentsNewSessionButton.border": secondary_border,
        "agentsNewSessionButton.hoverBackground": toolbar_hover,
        # Badges
        "agentsBadge.background": badge_background,
        "agentsBadge.foreground": badge_foreground,
        "agentsUnreadBadge.background": badge_background,
        "agentsUnreadBadge.foreground": badge_foreground,
        # Session views
        "activeSessionView.background": side_bar,
        "inactiveSessionView.background": background,
        "activeSessionView.foreground": panel_foreground,
        "inactiveSessionView.foreground": panel_foreground,
        # Mobile changes list / diff overlay
        "agentsMobileDiff.addedForeground": added,
        "agentsMobileDiff.modifiedForeground": modified,
        "agentsMobileDiff.deletedForeground": deleted,
        # Agent session list
        "agentSessionReadIndicator.foreground": with_alpha(foreground, "33"),
        "agentSessionSelectedBadge.border": with_alpha(list_selection_foreground, "4d"),
        "agentSessionSelectedUnfocusedBadge.border": with_alpha(foreground, "4d"),
        "agentSessionNeedsInput.foreground": warning,
        "agentStatusIndicator.background": command_center,
        # Chat surfaces shared with the Agents window
        "chat.requestBorder": with_alpha(foreground, "1a"),
        "chat.requestBackground": with_alpha(background, "9e"),
        "chat.statusBackground": with_alpha(foreground, "14"),
        "chat.sessionStateIndicator.inProgressBorder": warning,
        "chat.sessionStateIndicator.unvisitedBorder": added,
        "chat.sessionStateIndicator.needsInputBorder": error,
        "chat.avatarBackground": widget_background,
        "chat.avatarForeground": accent,
        "chat.editedFileForeground": modified,
        "chat.linesAddedForeground": added,
        "chat.linesRemovedForeground": deleted,
        "chat.requestCodeBorder": with_alpha(foreground, "26"),
        "chat.requestBubbleBackground": bubble_background,
        "chat.requestBubbleHoverBackground": bubble_hover,
        "chat.checkpointSeparator": separator,
        "chat.findMatchBackground": find_match,
        "chat.findMatchHighlightBackground": find_match_highlight,
        "chat.thinkingShimmer": "#000000" if is_light_theme(colors) else "#ffffff",
        "chat.inputWorkingBorderColor1": accent,
        "chat.voiceGlowBaseColor": focus,
        "chat.dictationActiveMicGlow": accent,
        "chat.mcpCompatibilityWarningForeground": warning,
        "chatManagement.sashBorder": card_border,
        "aiCustomizationManagement.sashBorder": card_border,
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
        print(f"{path.name}: added {len(added)} Agents window colors")


if __name__ == "__main__":
    main()
