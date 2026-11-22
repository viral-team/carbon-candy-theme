# Changelog

## 0.2.19 — 2026-11-22

### Fixed
- **Agents window compatibility**: the manifest now declares `capabilities.agentsWindow.supported`, so the extension is explicitly allowed in the Agents window instead of relying on the implicit "static contributions only" rule.
- **Extension activation crash**: `lib/config.js` and `lib/theme.js` still required `icons/carbon-candy-icon-theme.json`, which was renamed to `carbon-candy-file-icon-theme.json` in 0.2.1. Activation failed with `Cannot find module '../icons/carbon-candy-icon-theme.json'` in every window; the paths now point to the current file.
- The icon theme sync is skipped in the Agents window and in development hosts, and a read-only installation no longer breaks activation.

### Note
- The Agents window uses its own profile and its own `workbench.colorTheme`: select a Carbon Candy variant from the Agents window settings (or the Color Theme picker opened there) to apply it.

## 0.2.18 — 2026-11-21

### Added
- **Agents window support**: every theme variant now ships dedicated color tokens for the VS Code Agents window (agent sessions), so it no longer falls back to the built-in palette.
  - Shell and panels: `agents.background`, `agentsPanel.*`, `agentsDetail.background`, `agentsActivityBar.*`, `agentsCard.border`, `agentsBottomPanel.border`, `agentsGradient.tintColor`
  - Chat input: `agentsChatInput.*` (background, foreground, border, focus border, placeholder)
  - Session list: `agentSessionReadIndicator.foreground`, `agentSessionSelectedBadge.border`, `agentSessionSelectedUnfocusedBadge.border`, `agentSessionNeedsInput.foreground`, `agentStatusIndicator.background`
  - Session views: `activeSessionView.*`, `inactiveSessionView.*`
  - Buttons and badges: `agentsNewSessionButton.*`, `agentsBadge.*`, `agentsUnreadBadge.*`, `agentsUpdateButton.*`
  - Agent feedback widgets: `agentFeedbackEditorWidget.*`, `agentFeedbackInputWidget.border`
  - Mobile changes list: `agentsMobileDiff.addedForeground`, `agentsMobileDiff.modifiedForeground`, `agentsMobileDiff.deletedForeground`
  - Chat surfaces shared with the Agents window: `chat.requestBackground`, `chat.statusBackground`, `chat.sessionStateIndicator.*`, `chat.avatarBackground`, `chat.linesAddedForeground`, `chat.linesRemovedForeground`, `chat.findMatch*`, `chat.thinkingShimmer`, `chat.inputWorkingBorderColor1`, `chat.voiceGlowBaseColor`, `chat.dictationActiveMicGlow`, `chat.mcpCompatibilityWarningForeground`, `chatManagement.sashBorder`, `aiCustomizationManagement.sashBorder`
- Added `scripts/add_agents_colors.py`, which derives the Agents window tokens from each theme's own palette and is safe to re-run (existing keys are never overwritten).

### Changed
- Thin-border variants reuse their light-gray divider color for the Agents window cards, keeping the bordered look consistent across the workbench.
- Updated the README with an Agents window support section.
- **New branding**: the extension icon is now the 1:1 neon "VS Code + candy" logo, and the README opens with the new Carbon Candy hero banner.
- README refreshed: new header with quick links, complete variant tree (thin-border and Bee Lightroom variants included) and updated variant count.

## 0.2.14 — 2026-07-01

### Added
- Added a brand new theme variant: **Matrix**, with luminous neon green highlights and a digital rain-inspired dark base.
- Added the new theme entries to the extension manifest for discoverability in VS Code.

### Changed
- Updated the documentation to reflect the new Matrix theme.

## 0.2.13 — 2026-06-29

### Added
- Added a new Lightroom-based theme variant: **Kawasaki Lightroom** with light green 400 accents.
- Added the new theme entry to the extension manifest for discoverability in VS Code.

### Changed
- Expanded the theme catalog with a new Lightroom-inspired option while keeping the original Lightroom base styling.
- Updated the documentation to reflect the latest theme additions.

## 0.2.4 — 2026-02-07
- Fixed upper border color in thin bordered themes

## 0.2.3 — 2026-02-06

### Added
- Added thin light-gray bordered variants (UI division via thin borders):
  - `carbon-candy-dark (thin-border)`
  - `carbon-candy-carbon (thin-border)`
  - `carbon-candy-graphene (thin-border)`
  - `carbon-candy-aurora (thin-border)`

## 0.2.2 — 2025-12-16

### Changed
- Made debug toolbar more prominent for Graphene and Obsidian themes

## 0.2.1 — 2025-12-16

### Added
- Added **product icons** theme for custom VS Code product icon customization.
- Added **Carbon Candy** product icon theme to the extension.

### Changed
- Updated README with credits to Carbon Product Icons (tweaked) under MIT License.

## 0.1.9 — 2025-12-15

### Changed
- Changed the product logo.

## 0.1.8 — 2025-12-15

### Added
- Added **Bee** theme — bumblebee yellow accents on dark base.
- Added new product logo.

### Fixed
- Optimized logo size.

## 0.1.5 — 2025-12-09

### Added
- Added **Aurora** theme — clean, minimalist variant with crisp contrast and teal accents.
- Added **Palenight** theme — classic purple-tinted dark theme.
- Added **Carbon** theme — deep, focused dark theme.
- Added **Obsidian** theme — ultra-minimalist variant with borderless aesthetic.

### Fixed
- Fixed configuration change detection to prevent false positives and reload loops.
- Fixed settings stability verification before applying configuration changes.
- Improved debounce logic for configuration monitoring.

## 0.1.4 — 2025-12-09

### Added
- Added **configuration** to the extension.

### Changed
- Changed the **configuration** to be **carbonCandy**.

## 0.1.3 — 2025-12-08

### Added
- First release of the **dark theme collection**.
- Introduced **9 dark variants**:
  - **Anthracite**
  - **Dark**
  - **Graphene**
  - **Graphene Gradients**: v1, v2, v3, v4
  - **Graphene Solid Colors**: Pink, Purple
