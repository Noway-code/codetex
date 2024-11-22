# backend/process_expression.py

import sys
import json
from code_interpreter import code_interpreter_generic, render_latex_to_png

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No expression provided."}))
        sys.exit(1)
    
    # Retrieve the code from command-line arguments
    code = sys.argv[1]
    
    # Convert the code to LaTeX
    print(f"Received code: {code}", file=sys.stderr)
    latex_code = code_interpreter_generic(code)
    print(f"Generated LaTeX: {latex_code}", file=sys.stderr)
    
    # Render LaTeX to PNG image
    if not latex_code.startswith("Error"):
        try:
            image_base64 = render_latex_to_png(latex_code)
            output = {"latex_code": latex_code, "image": image_base64}
            print(json.dumps(output))  # Only JSON to stdout
            sys.exit(0)
        except Exception as e:
            error_message = f"Failed to render LaTeX: {str(e)}"
            print(json.dumps({"error": error_message}))
            sys.exit(1)
    else:
        print(json.dumps({"error": latex_code}))
        sys.exit(1)

if __name__ == '__main__':
    main()
