from flask import Flask, request, jsonify
from code_interpreter import code_interpreter_generic, render_latex_to_png

app = Flask(__name__)

@app.route('/passPython', methods=['POST'])
def receive_python():
    # Retrieve the code from the request
    code = request.json.get("code")
    # Convert the code to LaTeX
    print(f"Received code: {code}")
    latex_code = code_interpreter_generic(code)
    print(f"Generated LaTeX: {latex_code}")

    # Render LaTeX to PNG image
    if not latex_code.startswith("Error"):
        try:
            image_base64 = render_latex_to_png(latex_code)
            return jsonify({"latex_code": latex_code, "image": image_base64}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to render LaTeX: {str(e)}"}), 500
    else:
        return jsonify({"error": latex_code}), 400

if __name__ == '__main__':
    app.run(debug=True)
