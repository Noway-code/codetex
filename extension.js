// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "codetex" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	// Snippet from package.json:
		// 	"contributes": {
		//     "commands": [{
		//       "command": "codetex.helloWorld",
		//       "title": "Hello World"
		//     }]
		//   },
	const disposable = vscode.commands.registerCommand('codetex.helloWorld', function () {
		// The code you place here will be executed every time your command is executed

		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from CodeTeX!');
	});

	const countdownCommand = vscode.commands.registerCommand('codetex.countdown', function () {
		// The code you place here will be executed every time your command is executed
		const now = new Date();
		const dayOfWeek = now.getDay();
		const daysUntilMonday = (8 - dayOfWeek) % 7;
		const targetDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() + daysUntilMonday, 23, 59, 0);
		const diffMs = targetDate - now;
		const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
		const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

		// Display a message box to the user
		vscode.window.showInformationMessage(`You have ${diffHrs} hours and ${diffMins} minutes to complete this project!`);

	});

	context.subscriptions.push(disposable);
	context.subscriptions.push(countdownCommand);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
