const vscode = require("vscode");
const { log } = require("./log");
const defaultConfig = require("../icons/carbon-candy-icon-theme.json");
const pkgConfig = require("../package.json");
const { getThemeFile, writeThemeFile, applyModifiedToDefault } = require("./theme");
const { PKG_PROP_MAP } = require("./constants");
const { updateThemeJSONHandlers } = require("./theme-json-handlers");

// get the configuration definition from the package.json
// and also the default state of the theme to act as fallback
// values for the configs
const configDef = pkgConfig.contributes.configuration;
const configKeys = Object.keys(configDef.properties);

/**
 * @description will get the current **workspace** configuration
 */
function getWorkspaceConfiguration() {
	const config = {};
	const workspaceConfig = vscode.workspace.getConfiguration("carbonCandy")
	// read the current theme file to obtain up-to-date default values
	const currentThemeState = themeJSONToConfig(getThemeFile());
	for (const key of configKeys) {
		if (!PKG_PROP_MAP[key]) {
			continue;
		}

		const valueGroup = workspaceConfig.inspect(PKG_PROP_MAP[key]);
		const effective = workspaceConfig.get(PKG_PROP_MAP[key]);
		log.info(`inspect for ${PKG_PROP_MAP[key]} -> workspace:${JSON.stringify(valueGroup.workspaceValue)} global:${JSON.stringify(valueGroup.globalValue)} default:${JSON.stringify(valueGroup.defaultValue)} effective:${JSON.stringify(effective)}`);

		// prefer the effective value from workspace settings (includes global/workspace scopes)
		// fallback to the current theme state only if get() returns undefined
		config[PKG_PROP_MAP[key]] = typeof effective !== 'undefined' ? effective : currentThemeState[PKG_PROP_MAP[key]];
	}

	return config;
}

/**
 * @description normalize a theme definition json to only have
 * keys that are defined in the configuration section of the package.json
 */
function themeJSONToConfig(themeDef) {
	const result = {};

	for (const key of configKeys) {
		if (!PKG_PROP_MAP[key]) {
			continue;
		}
		result[PKG_PROP_MAP[key]] = themeDef[PKG_PROP_MAP[key]];
	}

	return result;
}

/**
 * @description update the changed property in the global settings and
 * in the theme definition file
 */
function updateConfig(config, immediate = false, userInitiated = false) {
	const themeJSON = getThemeFile();
	// pending reload debounce state (module-level)
	if (typeof updateConfig._reloadTimer === 'undefined') {
		updateConfig._reloadTimer = null;
		updateConfig._pendingThemeSnapshot = null;
		updateConfig._pendingConfigSnapshot = null;
		updateConfig._pendingKeys = null;
	}

	// prepare a snapshot with the new values applied
	const updatedTheme = JSON.parse(JSON.stringify(themeJSON));
	const changedKeys = [];
	
	for (const key in config) {
		const newValue = config[key];
		const oldValue = themeJSON[key];
		if (JSON.stringify(oldValue) !== JSON.stringify(newValue)) {
			changedKeys.push(key);
			updatedTheme[key] = newValue;
			log.info(`${key} changed, updating to ${JSON.stringify(newValue)}`);
		}
	}

	if (changedKeys.length === 0) {
		log.info('No configuration changes to apply');
		return;
	}

	// if immediate (activation), apply once and ask user to reload
	if (immediate) {
		if (updateConfig._appliedOnActivation) {
			log.info('Skipping activation apply: already applied once this session');
			return;
		}
		updateConfig._appliedOnActivation = true;
		try {
			// write modified file but do not copy into active theme until user confirms reload
			writeThemeFile(updatedTheme);
			log.info('Theme written on activation. Prompting user for reload.');
			vscode.window.showInformationMessage('Carbon Candy: icon theme updated (activation)', 'Reload').then((choice) => {
				if (choice === 'Reload') {
					try {
						applyModifiedToDefault();
					} catch (e) {
						log.error('Failed to apply modified theme to default file', e);
					}
					vscode.commands.executeCommand('workbench.action.reloadWindow');
				}
			});
		} catch (e) {
			log.error('Failed to apply theme immediately on activation', e);
		}
		return;
	}

	// for user-initiated changes: prepare pending snapshot and debounce
	updateConfig._pendingThemeSnapshot = updatedTheme;
	updateConfig._pendingConfigSnapshot = {};
	updateConfig._pendingKeys = changedKeys;
	for (const k of changedKeys) {
		updateConfig._pendingConfigSnapshot[k] = config[k];
	}

	if (updateConfig._reloadTimer) {
		clearTimeout(updateConfig._reloadTimer);
	}

	log.info('Debouncing pending update for keys: ' + changedKeys.join(', '));

	updateConfig._reloadTimer = setTimeout(() => {
		try {
			const workspaceConfig = vscode.workspace.getConfiguration('carbonCandy');
			let stable = true;
			for (const key of updateConfig._pendingKeys) {
				const effective = workspaceConfig.get(key);
				const intended = updateConfig._pendingConfigSnapshot[key];
				if (JSON.stringify(effective) !== JSON.stringify(intended)) {
					stable = false;
					log.info(`Stability check failed for ${key}: effective=${JSON.stringify(effective)} vs intended=${JSON.stringify(intended)}`);
					break;
				}
			}

			if (stable) {
				log.info('Settings stable. Writing theme and prompting reload.');
				// write the modified theme and prompt the user to reload; apply on confirmation
				writeThemeFile(updateConfig._pendingThemeSnapshot);
				try {
					vscode.window.showInformationMessage('Carbon Candy: icon theme updated', 'Reload').then((choice) => {
						if (choice === 'Reload') {
							try {
								applyModifiedToDefault();
							} catch (e) {
								log.error('Failed to apply modified theme to default file', e);
							}
							vscode.commands.executeCommand('workbench.action.reloadWindow');
						}
					});
				} catch (e) {
					log.error('Failed to show reload prompt', e);
				}
			} else {
				log.info('Pending theme update aborted: settings not stable yet');
			}
		} finally {
			updateConfig._reloadTimer = null;
			updateConfig._pendingThemeSnapshot = null;
			updateConfig._pendingConfigSnapshot = null;
			updateConfig._pendingKeys = null;
		}
	}, 600);
}

module.exports = {
	getWorkspaceConfiguration,
	themeJSONToConfig,
	updateConfig,
};
