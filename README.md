# CodeTeX

**CodeTeX** is a VS Code extension that converts code expressions into LaTeX, providing visual hover tooltips for enhanced readability and documentation.

# ⚠️ Warning ⚠️

**I would not recommend using this extension.** A majority of this project was completed in the span of 48 hours. Not much testing has been done to profile the project, optimize, or verify the security. These are not necessarily the priority at the moment as this is purely a personal project. Feel free to fork and use at your own risk though!


## Features

- **Hover-to-LaTeX Conversion:** Hover over any line containing a mathematical expression to view its LaTeX representation.
- **Efficient Caching:** Optimized performance with in-memory caching to ensure quick render times for repeated expressions.
- **Cache Management:** Easily clear the cache using the `CodeTeX: Clear Cache` command.
- **Supports Multiple Languages:** Works with Python and plain text files.

## Installation

1. Open VS Code.
2. Navigate to the Extensions view by clicking on the Extensions icon in the Activity Bar or pressing `Ctrl+Shift+X` (`Cmd+Shift+X` on macOS).
3. Search for `CodeTeX`.
4. Click `Install`.

## Usage

1. Open a Python (`.py`) or plain text (`.txt`) file.
2. Write or open code containing mathematical expressions.
3. Hover over the line containing the expression to see its LaTeX-rendered image.
4. To clear the cache, open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`), type `CodeTeX: Clear Cache`, and press `Enter`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.