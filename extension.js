// extension.js
const vscode = require('vscode');
const { registerHoverProvider } = require('./components/hoverProvider.js');

/**
 * This method is called when your extension is activated.
 * Your extension is activated the very first time the command is executed.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Congratulations, your extension "codetex" is now active!');

    const helloWorldCommand = vscode.commands.registerCommand('codetex.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from CodeTeX!');
    });

    const countdownCommand = vscode.commands.registerCommand('codetex.countdown', () => {
        const now = new Date();
        const dayOfWeek = now.getDay();
        const daysUntilMonday = (8 - dayOfWeek) % 7;
        const targetDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() + daysUntilMonday, 23, 59, 0);
        const diffMs = targetDate - now;
        const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
        const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        vscode.window.showInformationMessage(`Hi, you have ${diffHrs} hours and ${diffMins} minutes to complete this project!`);
    });

    const hoverProvider = registerHoverProvider();

    context.subscriptions.push(helloWorldCommand);
    context.subscriptions.push(countdownCommand);
    context.subscriptions.push(hoverProvider);
}

/**
 * This method is called when your extension is deactivated.
 */
function deactivate() {}

module.exports = {
    activate,
    deactivate
};
