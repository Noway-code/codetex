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

        if (result.error) {
            console.error('Error from Python server:', result.error);
            return { latex_code: 'Error retrieving LaTeX code', image: null };
        }

        console.log('Received LaTeX Code:', result.latex_code);
        return { latex_code: result.latex_code, image: result.image };
    } catch (error) {
        console.error('Error passing code to Python:', error);
        return { latex_code: 'Error retrieving LaTeX code', image: null };
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

    // Asynchronously get the LaTeX output from the Python server
    const { latex_code, image } = await passCodeToPython(currentLineText);

    if (!image) {
        // If there's an error or no image, display the LaTeX code as plaintext
        const hoverContent = new vscode.MarkdownString(`**Converted LaTeX Code:**\n\`\`\`plaintext\n${latex_code}\n\`\`\``);
        return new vscode.Hover(hoverContent);
    }

    // Create a Markdown string for the hover, embedding the image
    // Use data URI scheme for the image
    const imageUri = `data:image/png;base64,${image}`;
    const hoverContent = new vscode.MarkdownString(`**Converted LaTeX Code:**\n![LaTeX](${imageUri})`);

    // Enable trusted content to allow images to be rendered
    hoverContent.isTrusted = true;

    return new vscode.Hover(hoverContent);
}

function registerHoverProvider() {
    return vscode.languages.registerHoverProvider(['plaintext', 'python'], {
        provideHover
    });
}

module.exports = {
    registerHoverProvider
};
