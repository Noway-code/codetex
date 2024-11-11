import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

def python_to_latex(code_str):
    # Define the allowed functions and constants
    allowed_symbols = {
        'pi': sp.pi,
        'oo': sp.oo,
        'I': sp.I
    }
    allowed_functions = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'integrate', 'limit', 'diff']

    # Add allowed functions to the namespace
    for func in allowed_functions:
        allowed_symbols[func] = getattr(sp, func)
    
    # Extract variable names
    import re
    var_names = set(re.findall(r'[a-zA-Z_]\w*', code_str))
    # Remove any function names from variables
    var_names -= set(allowed_functions)
    
    # Define symbols dynamically for variables in the expression
    for var in var_names:
        allowed_symbols[var] = sp.Symbol(var)
    
    # Parse and convert expression
    try:
        expr = parse_expr(code_str, evaluate=False, local_dict=allowed_symbols)
        latex_expr = sp.latex(expr)
        return latex_expr
    except Exception as e:
        return f"Error parsing expression: {e}"

def main():
    print("Enter a Python expression to convert to LaTeX (type 'exit' to quit):")
    while True:
        code_str = input('> ')
        if code_str.lower() == 'exit':
            break
        latex_output = python_to_latex(code_str)
        print(f"LaTeX Output: {latex_output}\n")

if __name__ == '__main__':
    main()
