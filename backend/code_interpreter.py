# backend/code_interpreter.py

import matplotlib.pyplot as plt
import io
import base64
import ast
import textwrap
from generic_mappings import GENERIC_MATH_TO_SYMPY_DYNAMIC
from sympy import Symbol, sympify, latex
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import sympy as sp

# Error Handler
import logging
import sys  # Ensure sys is imported

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

def handle_errors(e):
    """
    Handles errors that occur during the conversion process.

    Parameters:
        e (Exception): The exception that was raised.

    Returns:
        str: An error message.
    """
    if isinstance(e, ValueError):
        logging.error(f"Syntax Error: {e}")
        return f"Syntax Error: {e}"
    elif isinstance(e, KeyError):
        logging.error(f"Unsupported Function: {e}")
        return f"Unsupported Function: {e}"
    else:
        logging.error(f"Error: {e}")
        return f"Error: {e}"

class MathToSymPyTransformer(ast.NodeTransformer):
    """
    Transforms Python math expressions and assignment statements in the AST to their SymPy equivalents using a generic mapping.
    """

    def __init__(self, mapping):
        self.mapping = mapping

    def visit_Call(self, node):
        self.generic_visit(node)  # Recursively visit child nodes
        func = node.func

        if isinstance(func, ast.Attribute):
            func_name = func.attr
            if func_name in self.mapping:
                sympy_func = self.mapping[func_name]

                # Handle special cases
                if func_name == 'log2':
                    # Replace log2(x) with log(x, 2)
                    if len(node.args) == 1:
                        new_func = ast.Name(id='log', ctx=ast.Load())
                        new_args = [node.args[0], ast.Constant(value=2) if hasattr(ast, 'Constant') else ast.Num(n=2)]
                        new_call = ast.Call(func=new_func, args=new_args, keywords=[])
                        return ast.copy_location(new_call, node)

                elif func_name == 'polar':
                    # Replace polar(z) with (Abs(z), arg(z))
                    if len(node.args) == 1:
                        new_args = [
                            ast.Call(func=ast.Name(id='Abs', ctx=ast.Load()), args=[node.args[0]], keywords=[]),
                            ast.Call(func=ast.Name(id='arg', ctx=ast.Load()), args=[node.args[0]], keywords=[])
                        ]
                        return ast.copy_location(ast.Tuple(elts=new_args, ctx=ast.Load()), node)

                elif func_name == 'pow':
                    # Replace pow(x, y) with x ** y
                    if len(node.args) == 2:
                        left = node.args[0]
                        right = node.args[1]
                        new_node = ast.BinOp(left=left, op=ast.Pow(), right=right)
                        return ast.copy_location(new_node, node)

                else:
                    # Replace function name with SymPy's function
                    node.func = ast.Name(id=sympy_func, ctx=ast.Load())

        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)  # Recursively visit child nodes

        if isinstance(node.value, ast.Name):
            func_name = node.attr
            if func_name in self.mapping:
                sympy_attr = self.mapping[func_name]
                return ast.copy_location(ast.Name(id=sympy_attr, ctx=ast.Load()), node)

        return node

    def visit_Assign(self, node):
        """
        Handle assignment statements by transforming the value.
        """
        self.generic_visit(node)  # Transform the value

        # Assuming single target assignments like 'a = ...'
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            # The value has already been transformed
            return node
        else:
            logging.error("Multiple assignment targets or unsupported assignment.")
            return node

class SymbolExtractor(ast.NodeVisitor):
    """
    Extracts all unique variable names (symbols) from the AST of a mathematical expression or statement.
    """

    def __init__(self):
        self.symbols = set()

    def visit_Name(self, node):
        self.symbols.add(node.id)

def convert_math_to_sympy_ast(math_expr, mapping):
    """
    Converts a Python math expression or assignment statement string to a SymPy-compatible string using AST transformations.

    Parameters:
        math_expr (str): The Python math expression or assignment statement to convert.
        mapping (dict): The mapping dictionary from function names to SymPy function names.

    Returns:
        str: The transformed SymPy-compatible expression string or assignment.
    """
    try:
        # Dedent the input to ignore indentation
        math_expr = textwrap.dedent(math_expr)

        # Parse the expression into an AST in 'exec' mode to handle statements
        tree = ast.parse(math_expr, mode='exec')
    except SyntaxError as se:
        raise ValueError(f"Invalid syntax: {se}")

    # Transform the AST
    transformer = MathToSymPyTransformer(mapping)
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    try:
        # For Python 3.9 and above, use ast.unparse
        sympy_string = ast.unparse(transformed_tree)
    except AttributeError:
        # For older Python versions, use astor
        import astor
        sympy_string = astor.to_source(transformed_tree).strip()

    print(f"SymPy String: {sympy_string}", file=sys.stderr)  # Redirected to stderr

    return sympy_string

def extract_symbols(math_expr):
    """
    Extracts variable symbols from the math expression or assignment statement.

    Parameters:
        math_expr (str): The Python math expression or assignment statement.

    Returns:
        set: A set of variable names used in the expression.
    """
    # Dedent the input to ignore indentation
    math_expr = textwrap.dedent(math_expr)

    tree = ast.parse(math_expr, mode='exec')
    extractor = SymbolExtractor()
    extractor.visit(tree)
    # Exclude known modules to prevent treating them as symbols
    known_modules = set(['math', 'numpy', 'scipy', 'cmath'])
    return {symbol for symbol in extractor.symbols if symbol not in known_modules}

def code_interpreter_generic(long_string):
    """
    Converts a Python math expression or assignment statement to LaTeX using SymPy.

    Parameters:
        long_string (str): The Python math expression or assignment statement.
    Returns:
        str: The corresponding LaTeX expression or an error message.
    """
    try:
        # Step 1: Transform the Python expression or statement to a SymPy-compatible string
        sympy_string = convert_math_to_sympy_ast(long_string, GENERIC_MATH_TO_SYMPY_DYNAMIC)
        # print("SymPy String:", sympy_string)  # Already handled in convert_math_to_sympy_ast

        # Step 2: Extract symbols (variables) from the original expression or statement
        symbols_in_expr = extract_symbols(long_string)
        custom_locals = {name: Symbol(name) for name in symbols_in_expr}

        # Step 3: Add all math functions from GENERIC_MATH_TO_SYMPY_DYNAMIC to locals
        for func_name, sympy_func_name in GENERIC_MATH_TO_SYMPY_DYNAMIC.items():
            if hasattr(sp, sympy_func_name):
                custom_locals[func_name] = getattr(sp, sympy_func_name)
            else:
                # Fallback: Attempt to use the function name directly as a SymPy function
                custom_locals[func_name] = sp.Function(func_name)

        # Step 4: Define transformations for SymPy parser
        transformations = (standard_transformations + (implicit_multiplication_application,))

        # Step 5: Parse the transformed string into a SymPy expression or statement
        tree = ast.parse(sympy_string, mode='exec')

        if len(tree.body) == 1 and isinstance(tree.body[0], ast.Assign):
            # Handle assignment statement
            assign_node = tree.body[0]
            if len(assign_node.targets) == 1 and isinstance(assign_node.targets[0], ast.Name):
                var_name = assign_node.targets[0].id
                value_expr = assign_node.value

                # Convert the value expression back to string
                value_str = ast.unparse(value_expr)
                # Parse the value expression
                sympy_expr = parse_expr(value_str, local_dict=custom_locals, transformations=transformations)

                # Convert to LaTeX
                latex_expression = latex(sympy_expr)

                # Combine with variable assignment
                latex_assignment = f"{var_name} = {latex_expression}"
                return latex_assignment
        else:
            # Handle single expression
            sympy_expr = parse_expr(sympy_string, local_dict=custom_locals, transformations=transformations)
            latex_expression = latex(sympy_expr)
            return latex_expression

    except Exception as e:
        return handle_errors(e)

def render_latex_to_png(latex_code):
    """
    Renders LaTeX code to a PNG image and returns it as a base64 string.

    Parameters:
        latex_code (str): The LaTeX code to render.
    Returns:
        str: The base64-encoded PNG image.
    """
    # Create a figure with no axes
    fig, ax = plt.subplots(figsize=(0.01, 0.01))
    ax.axis('off')  # Hide axes

    # Add LaTeX text
    text = ax.text(0.5, 0.5, f"${latex_code}$", fontsize=12, ha='center', va='center', color='white')

    # Adjust figure size based on text
    fig.canvas.draw()
    bbox = text.get_window_extent()
    width, height = bbox.size / fig.dpi + 0.1  # Add padding
    fig.set_size_inches(width, height)

    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close(fig)
    buf.seek(0)

    # Encode the image in base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64

# Example Usage for Testing
if __name__ == "__main__":
    expressions = [
        "math.sin(math.pi / 2)",
        "math.exp(math.log(x))",
        "numpy.sqrt(math.pow(x, 2) + scipy.special.gamma(y))",
        "math.unknown_func(x)",
        "math.sin(math.pi / 2",             # Syntax Error
        "math.log2(x) + y * math.cos(z)",
        "cmath.polar(z)",
        "a = sin(theta) + cos(phi)",        # Assignment Statement
    ]

    for expr in expressions:
        print(f"Expression: {expr}", file=sys.stderr)
        latex_output = code_interpreter_generic(expr)
        print(f"LaTeX: {latex_output}\n", file=sys.stderr)
