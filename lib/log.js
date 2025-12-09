const vscode = require("vscode");

const channel = vscode.window.createOutputChannel("Carbon Candy");
const log = {
	info: (...args) => {
		const time = new Date().toLocaleTimeString();
		channel.appendLine(`[INFO ${time}] ${args.join(" ")}`);
	},
	error: (...args) => {
		const time = new Date().toLocaleTimeString();
		channel.appendLine(`[ERROR ${time}] ${args.join(" ")}`);
	},
};

module.exports = {
	log,
};
