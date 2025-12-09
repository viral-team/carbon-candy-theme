const { themeJSONToConfig, getWorkspaceConfiguration, updateConfig } = require("./config");
const { getThemeFile } = require("./theme");
const { log } = require("./log");

function monitorConfigChanges(immediate = false, userInitiated = false) {
	try {
		log.info('monitorConfigChanges invoked');
		const themeJSON = getThemeFile();
		const currentState = themeJSONToConfig(themeJSON);
		const workspaceState = getWorkspaceConfiguration();

		log.info('currentState', JSON.stringify(currentState));
		log.info('workspaceState', JSON.stringify(workspaceState));

		// find keys that actually changed between workspace settings and theme JSON
		const changedKeys = {};
		let hasChanges = false;

		for (const key in workspaceState) {
			// if workspace value differs from current theme value, it changed
			if (JSON.stringify(workspaceState[key]) !== JSON.stringify(currentState[key])) {
				changedKeys[key] = workspaceState[key];
				hasChanges = true;
				log.info(`detected change: ${key} workspace=${JSON.stringify(workspaceState[key])} vs current=${JSON.stringify(currentState[key])}`);
			}
		}

		log.info('changedKeys', JSON.stringify(changedKeys));

		// only update if there are actual changes to apply
		if (hasChanges) {
			updateConfig(changedKeys, immediate, userInitiated);
		} else {
			log.info('no changes detected between workspace and theme');
		}
	} catch (e) {
		log.error('monitorConfigChanges error', e && e.message ? e.message : e);
	}
}

module.exports = {
	monitorConfigChanges,
};
