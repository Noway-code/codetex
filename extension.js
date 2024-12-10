// extension.js
const vscode = require('vscode');
const { registerHoverProvider, clearCache } = require('./components/hoverProvider.js');

/**
 * This method is called when your extension is activated.
 * Your extension is activated the very first time the command is executed.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    
    let disposable = vscode.commands.registerCommand('codetex.clearCache', () => {
        clearCache();
        vscode.window.showInformationMessage('CodeTeX cache cleared.');
    });

    context.subscriptions.push(disposable);

    const hoverProvider = registerHoverProvider();
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
