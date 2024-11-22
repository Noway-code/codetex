// components/hoverProvider.js

const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');
const which = require('which');

let lastLineContent = '';  // Cache to store last line's content

/**
 * Finds the Python executable on the user's system.
 * @returns {string|null} The path to the Python executable or null if not found.
 */
function findPythonExecutable() {
    const possibleExecutables = ['python3', 'python'];
    for (const execName of possibleExecutables) {
        try {
            const pythonPath = which.sync(execName);
            console.log(`Found Python executable: ${pythonPath}`);
            return pythonPath;
        } catch (err) {
            continue;
        }
    }
    console.error('Python executable not found.');
    return null;
}

/**
 * Executes the Python script with the given code and returns the result.
 * @param {string} scriptPath - The path to the Python script.
 * @param {string} code - The code string to convert.
 * @returns {Promise<object>} The JSON result from the Python script.
 */
function executePythonScript(scriptPath, code) {
    return new Promise((resolve, reject) => {
        const pythonPath = findPythonExecutable();
        if (!pythonPath) {
            return reject('Python is not installed or not found in PATH.');
        }

        console.log(`Executing Python script: ${scriptPath} with code: "${code}"`);

        const process = spawn(pythonPath, [scriptPath, code]);

        let stdout = '';
        let stderr = '';

        process.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        process.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        process.on('close', (code) => {
            console.log(`Python script exited with code ${code}`);
            if (code !== 0) {
                console.error(`Python stderr: ${stderr}`);
                return reject(`Python script exited with code ${code}: ${stderr}`);
            }
            try {
                const result = JSON.parse(stdout);
                console.log('Python script output:', result);
                resolve(result);
            } catch (parseError) {
                console.error(`Failed to parse Python output: ${parseError.message}`);
                reject(`Failed to parse Python output: ${parseError.message}`);
            }
        });

        process.on('error', (err) => {
            console.error(`Failed to start Python process: ${err.message}`);
            reject(`Failed to start Python process: ${err.message}`);
        });
    });
}

/**
 * Creates a webview panel to display LaTeX using KaTeX.
 * @param {string} latexCode - The LaTeX code to render.
 */
function showLaTeXInWebview(latexCode) {
    const panel = vscode.window.createWebviewPanel(
        'latexPreview',
        'LaTeX Preview',
        vscode.ViewColumn.Beside,
        {
            enableScripts: true
        }
    );

    panel.webview.html = getWebviewContent(latexCode);
}

/**
 * Generates the HTML content for the webview with KaTeX.
 * @param {string} latex - The LaTeX code to render.
 * @returns {string} HTML content.
 */
function getWebviewContent(latex) {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src https://cdn.jsdelivr.net; style-src https://cdn.jsdelivr.net 'unsafe-inline';">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css">
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.js"></script>
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/contrib/auto-render.min.js"
            onload="renderMath()"></script>
        <script>
            function renderMath() {
                renderMathInElement(document.body, {
                    delimiters: [
                        {left: "$$", right: "$$", display: true},
                        {left: "$", right: "$", display: false}
                    ]
                });
            }
        </script>
        <style>
            body {
                background-color: transparent;
                font-family: Arial, sans-serif;
                padding: 10px;
            }
        </style>
    </head>
    <body>
        <p>$$${latex}$$</p>
    </body>
    </html>`;
}

/**
 * Provides hover information by converting code to LaTeX.
 * @param {vscode.TextDocument} document
 * @param {vscode.Position} position
 * @param {vscode.CancellationToken} token
 * @returns {Promise<vscode.Hover|null>}
 */
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

    // Path to the Python processing script
    const scriptPath = path.join(__dirname, '..', 'backend', 'process_expression.py');

    console.log(`Hover triggered on line: "${currentLineText}"`);
    console.log(`Resolved script path: ${scriptPath}`);

    try {
        const result = await executePythonScript(scriptPath, currentLineText);

        if (result.error) {
            console.error('Error from Python script:', result.error);
            // Display the error as plaintext in the hover
            const hoverContent = new vscode.MarkdownString(`**Error:** ${result.error}`);
            hoverContent.isTrusted = true;
            return new vscode.Hover(hoverContent);
        }

        const { latex_code, image } = result;

        if (!image) {
            // If there's an error or no image, display the LaTeX code as plaintext
            const hoverContent = new vscode.MarkdownString(`**Converted LaTeX Code:**\n\`\`\`plaintext\n${latex_code}\n\`\`\``);
            hoverContent.isTrusted = true;
            return new vscode.Hover(hoverContent);
        }

        // Create a Markdown string for the hover, embedding the image
        // Use data URI scheme for the image
        const imageUri = `data:image/png;base64,${image}`;
        const hoverContent = new vscode.MarkdownString(`**Converted LaTeX Code:**\n![LaTeX](${imageUri})`);

        // Enable trusted content to allow images to be rendered
        hoverContent.isTrusted = true;

        return new vscode.Hover(hoverContent);
    } catch (error) {
        console.error('Error processing hover:', error);
        const hoverContent = new vscode.MarkdownString(`**Error:** ${error}`);
        hoverContent.isTrusted = true;
        return new vscode.Hover(hoverContent);
    }
}

function registerHoverProvider() {
    return vscode.languages.registerHoverProvider(['plaintext', 'python'], {
        provideHover
    });
}

module.exports = {
    registerHoverProvider
};
