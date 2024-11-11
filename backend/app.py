from flask import Flask, request, jsonify
from python_to_latex import python_to_latex
from code_interpreter import code_interpreter

app = Flask(__name__)

@app.route('/passPython', methods=['POST'])
def receive_python():
    # Retrieve the code from the request
    code = request.json.get("code")
    # Convert the code to LaTeX
    print(code)
    latex_code = code_interpreter(code)
    print (latex_code)
    return jsonify({"latex_code": latex_code}), 200

if __name__ == '__main__':
    app.run(debug=True)

