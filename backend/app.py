from flask import Flask, request, jsonify
from python_to_latex import python_to_latex
from basictry import generate_latex

app = Flask(__name__)

@app.route('/passPython', methods=['POST'])
def receive_python():
    # Retrieve the code from the request
    code = request.json.get("code")
    # Convert the code to LaTeX
    print(code)
    latex_code = generate_latex(code)
    print (latex_code)
    # Return the LaTeX code
    return jsonify({"latex_code": latex_code}), 200

if __name__ == '__main__':
    app.run(debug=True)

