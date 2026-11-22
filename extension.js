const vscode = require("vscode");
const { monitorConfigChanges } = require("./lib/change-listener");
const { syncOriginal } = require("./lib/theme");
const { log } = require("./lib/log");

function isAgentsWindow() {
	// VS Code exposes "agents" as the app host of the Agents window
	return vscode.env.appHost === "agents";
}

/**
 * @param {vscode.ExtensionContext} context
 */
async function activate(context) {
	log.info("Carbon Candy activated");
	// The Agents window only allows static contributions: its file system is
	// not guaranteed to be writable and settings are managed in the editor window.
	if (context.extensionMode !== vscode.ExtensionMode.Production || isAgentsWindow()) {
		log.info("Static-only context (Agents window or development), skipping icon theme sync");
		return;
	}
	try {
		await syncOriginal();
	} catch (e) {
		// e.g. read-only installation: the contributed themes still work
		log.error("Failed to sync icon theme", e && e.message ? e.message : e);
		return;
	}
	// on activation, apply theme settings immediately (once per session)
	monitorConfigChanges(true, false);

	// debounce configuration changes to avoid racing with settings persistence
	let configChangeTimeout = null;
	vscode.workspace.onDidChangeConfiguration((e) => {
		if (!e.affectsConfiguration || !e.affectsConfiguration('carbonCandy')) {
			return;
		}
		if (configChangeTimeout) {
			clearTimeout(configChangeTimeout);
		}
		configChangeTimeout = setTimeout(() => {
			// user changed a setting; this is user-initiated
			monitorConfigChanges(false, true);
			configChangeTimeout = null;
		}, 300);
	});

	vscode.window.onDidChangeWindowState((state) => {
		// Avoid monitoring on every window focus change to prevent repeated checks
		// (can cause loops if file writes trigger focus/config events).
		// If you want to re-check on focus, enable below with caution.
		/*
		if (state.focused) {
			monitorConfigChanges();
		}
		*/
	});
}

function deactivate() {}

// eslint-disable-next-line no-undef
module.exports = {
	activate,
	deactivate,
};
