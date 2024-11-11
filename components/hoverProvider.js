/* eslint-disable no-unused-vars */
const vscode = require('vscode');

let lastLineContent = '';  // Cache to store last line's content

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
        console.log(result.latex_code);
        return result.latex_code;
    } catch (error) {
        console.error('Error passing code to Python:', error);
        return 'Error retrieving LaTeX code';
    }
}

async function provideHover(document, position, token) {
    const range = document.getWordRangeAtPosition(position);
    const word = range ? document.getText(range) : '';

    if (!word) {
        return;
    }

    // Get the current line text
    const currentLineText = document.lineAt(position.line).text;

    if (currentLineText === lastLineContent) {
        return;  // Skip processing if the content hasn't changed
    }
    lastLineContent = currentLineText;  // Update the cache with the new content


    // Commented out multi-line functionality
    /*
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
    */

    // Asynchronously get the LaTeX output from the Python server
    const oneLineLatex = await passCodeToPython(currentLineText);

    // Create a Markdown string for the hover
    const hoverContent = new vscode.MarkdownString(`**Converted LaTeX Code:**\n\`\`\`plaintext\n${oneLineLatex}\n\`\`\``);

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
