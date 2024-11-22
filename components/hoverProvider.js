// components/hoverProvider.js

const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');
const which = require('which');

// Initialize an in-memory cache using Map
const expressionCache = new Map();

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

    // Get the entire line text
    const currentLineText = document.lineAt(position.line).text.trim();

    // Check if the current line's result is already cached
    if (expressionCache.has(currentLineText)) {
        const cachedResult = expressionCache.get(currentLineText);
        console.log(`Cache hit for line: "${currentLineText}"`);

        if (cachedResult.error) {
            // If there was an error previously, do not show a hover
            return null;
        }

        const { latex_code, image } = cachedResult;

        if (!image) {
            // If image is missing, do not display any hover
            return null;
        }

        // Create a Markdown string for the hover, embedding the image
        const imageUri = `data:image/png;base64,${image}`;
        const hoverContent = new vscode.MarkdownString(`**Converted LaTeX Code:**\n![LaTeX](${imageUri})`);

        // Enable trusted content to allow images to be rendered
        hoverContent.isTrusted = true;

        return new vscode.Hover(hoverContent);
    }

    // Proceed with processing if not cached
    // Path to the Python processing script
    const scriptPath = path.join(__dirname, '..', 'backend', 'process_expression.py');

    console.log(`Hover triggered on line: "${currentLineText}"`);
    console.log(`Resolved script path: ${scriptPath}`);

    try {
        const result = await executePythonScript(scriptPath, currentLineText);

        // Cache the result for future use
        expressionCache.set(currentLineText, result);

        if (result.error) {
            console.error('Error from Python script:', result.error);
            // Do not display any hover if there's an error (i.e., non-expression line)
            return null;
        }

        const { latex_code, image } = result;

        if (!image) {
            // If image is missing, do not display any hover
            return null;
        }

        // Create a Markdown string for the hover, embedding the image
        const imageUri = `data:image/png;base64,${image}`;
        const hoverContent = new vscode.MarkdownString(`**Converted LaTeX Code:**\n![LaTeX](${imageUri})`);

        // Enable trusted content to allow images to be rendered
        hoverContent.isTrusted = true;

        return new vscode.Hover(hoverContent);
    } catch (error) {
        console.error('Error processing hover:', error);
        // Optionally, cache the error to prevent re-processing
        expressionCache.set(currentLineText, { error: error.toString() });
        // Do not display any hover if there's an error
        return null;
    }
}

/**
 * Registers the hover provider for specified languages.
 * @returns {vscode.Disposable} The hover provider disposable.
 */
function registerHoverProvider() {
    return vscode.languages.registerHoverProvider(['plaintext', 'python'], {
        provideHover
    });
}

/**
 * Clears the expression cache.
 */
function clearCache() {
    expressionCache.clear();
    console.log('Expression cache has been cleared.');
}

module.exports = {
    registerHoverProvider,
    clearCache
};
