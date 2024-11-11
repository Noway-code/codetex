/* eslint-disable no-unused-vars */
const vscode = require('vscode');

/**
 * Reverses a given string.
 * @param {string} text The text to reverse.
 * @returns {string} The reversed text.
 */

async function passCodeToPython(code) {
    try {
        const response = await fetch('http://127.0.0.1:5000/passPython', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result);
    } catch (error) {
        console.error('Error passing code to Python:', error);
    }
}


function provideHover(document, position, token) {
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
    hoverContent.appendMarkdown('\n\n**Pasing Python Code**');
    passCodeToPython(document.lineAt(currentLine).text);

    return new vscode.Hover(hoverContent);
}

function registerHoverProvider() {
    return vscode.languages.registerHoverProvider('plaintext', {
        provideHover
    });
}

module.exports = {
    registerHoverProvider
};
