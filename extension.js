// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

/**
 * This method is called when your extension is activated.
 * Your extension is activated the very first time the command is executed.
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Congratulations, your extension "codetex" is now active!');

    const disposable = vscode.commands.registerCommand('codetex.helloWorld', function () {
        // Display a message box to the user
        vscode.window.showInformationMessage('Hello World from CodeTeX!');
    });

    const countdownCommand = vscode.commands.registerCommand('codetex.countdown', function () {
        const now = new Date();
        const dayOfWeek = now.getDay();
        const daysUntilMonday = (8 - dayOfWeek) % 7;
        const targetDate = new Date(now.getFullYear(), now.getMonth(), now.getDate() + daysUntilMonday, 23, 59, 0);
        const diffMs = targetDate - now;
        const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
        const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        vscode.window.showInformationMessage(`Hi, you have ${diffHrs} hours and ${diffMins} minutes to complete this project!`);
    });


    // Register the Hover Provider for all languages
    const hoverProvider = vscode.languages.registerHoverProvider('*', {
        provideHover(document, position, token) {
            const range = document.getWordRangeAtPosition(position);
            const word = range ? document.getText(range) : '';

            if (!word) {
                return;
            }

            // Get the current line number
            const currentLine = position.line;

            // Calculate the range for 5 lines above and below
            const startLine = Math.max(currentLine - 5, 0);
            const endLine = Math.min(currentLine + 5, document.lineCount - 1);

            // Retrieve the lines
            const lines = [];
            for (let i = startLine; i <= endLine; i++) {
                lines.push(document.lineAt(i).text);
            }

            const contextText = lines.join('\n');

            // Create a Markdown string for the hover
            const hoverContent = new vscode.MarkdownString(`**Context:**\n\`\`\`plaintext\n${contextText}\n\`\`\``);

            return new vscode.Hover(hoverContent);
        }
	});

    context.subscriptions.push(hoverProvider);
    context.subscriptions.push(disposable);
    context.subscriptions.push(countdownCommand);
}

/**
 * This method is called when your extension is deactivated.
 */
function deactivate() {}

// Export the activate and deactivate functions
module.exports = {
    activate,
    deactivate
};
