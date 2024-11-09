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

	const HelloLaTeXCommand = vscode.commands.registerCommand('codetex.hellolatexcommand', function () {
		// The code you place here will be executed every time your command is executed

		// Display a message box to the user
		vscode.window.showInformationMessage('Hello LaTeX from CodeTeX!');
	});

	context.subscriptions.push(disposable);
	context.subscriptions.push(HelloLaTeXCommand);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
