const vscode = require("vscode");
const { monitorConfigChanges } = require("./lib/change-listener");
const { syncOriginal } = require("./lib/theme");
const { log } = require("./lib/log");
/**
 * @param {vscode.ExtensionContext} context
 */
async function activate(context) {
	log.info("Carbon Candy activated");
	await syncOriginal();
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
