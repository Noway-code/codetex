import ast
import sympy as sp
from sympy import symbols, Symbol, sympify, latex
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# mappings.py
MASTER_MATH_TO_SYMPY = {
    'math': {
        'sqrt': 'sqrt',
        'pow': 'Pow',
        'exp': 'exp',
        'log': 'log',
        'log10': 'log10',
        'log2': 'log',  # Special handling in transformer
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'asin': 'asin',
        'acos': 'acos',
        'atan': 'atan',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        'asinh': 'asinh',
        'acosh': 'acosh',
        'atanh': 'atanh',
        'factorial': 'factorial',
        'gamma': 'gamma',
        'floor': 'floor',
        'ceil': 'ceiling',
        'pi': 'pi',
        'e': 'E',
        'inf': 'oo',
        'nan': 'nan',
    },
    'numpy': {
        'sqrt': 'sqrt',
        'power': 'Pow',
        'exp': 'exp',
        'log': 'log',
        'log10': 'log10',
        'log2': 'log',  # Special handling in transformer
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'arcsin': 'asin',
        'arccos': 'acos',
        'arctan': 'atan',
        'sinh': 'sinh',
        'cosh': 'cosh',
        'tanh': 'tanh',
        'arcsinh': 'asinh',
        'arccosh': 'acosh',
        'arctanh': 'atanh',
        'floor': 'floor',
        'ceil': 'ceiling',
        'pi': 'pi',
        'e': 'E',
        'inf': 'oo',
        'nan': 'nan',
    },
    'scipy.special': {
        'gamma': 'gamma',
        'factorial': 'factorial',
        'erf': 'erf',
        'erfc': 'erfc',
        'digamma': 'digamma',
        'polygamma': 'polygamma',
        'lambertw': 'lambertw',
        'beta': 'beta',
        'zeta': 'zeta',
    },
    'cmath': {
        'sqrt': 'sqrt',
        'exp': 'exp',
        'log': 'log',
        'log10': 'log10',
        'sin': 'sin',
        'cos': 'cos',
        'tan': 'tan',
        'asin': 'asin',
        'acos': 'acos',
        'atan': 'atan',
        'phase': 'arg',
        # 'polar' and 'rect' require special handling
    },
    'scipy.constants': {
        'pi': 'pi',
        'e': 'E',
    },
    # Extend with other modules as needed
}

# parser.py
class MathToSymPyTransformer(ast.NodeTransformer):
    def __init__(self, mapping):
        self.mapping = mapping

    def visit_Call(self, node):
        self.generic_visit(node)
        func = node.func
        if isinstance(func, ast.Attribute):
            module = func.value.id if isinstance(func.value, ast.Name) else None
            func_name = func.attr
            if module and module in self.mapping and func_name in self.mapping[module]:
                sympy_func = self.mapping[module][func_name]
                if module == 'math' and func_name == 'log2':
                    # Replace log2(x) with log(x, 2)
                    if len(node.args) == 1:
                        new_func = ast.Name(id='log', ctx=ast.Load())
                        new_args = [node.args[0], ast.Num(n=2)]
                        new_call = ast.Call(func=new_func, args=new_args, keywords=[])
                        return ast.copy_location(new_call, node)
                elif module == 'cmath' and func_name == 'polar':
                    # Replace polar(z) with (Abs(z), arg(z))
                    if len(node.args) == 1:
                        new_args = [
                            ast.Call(func=ast.Name(id='Abs', ctx=ast.Load()), args=[node.args[0]], keywords=[]),
                            ast.Call(func=ast.Name(id='arg', ctx=ast.Load()), args=[node.args[0]], keywords=[])
                        ]
                        return ast.copy_location(ast.Tuple(elts=new_args, ctx=ast.Load()), node)
                else:
                    node.func = ast.Name(id=sympy_func, ctx=ast.Load())
        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Name):
            module = node.value.id
            attr = node.attr
            if module in self.mapping and attr in self.mapping[module]:
                sympy_attr = self.mapping[module][attr]
                return ast.copy_location(ast.Name(id=sympy_attr, ctx=ast.Load()), node)
        return node

class SymbolExtractor(ast.NodeVisitor):
    def __init__(self):
        self.symbols = set()

    def visit_Name(self, node):
        self.symbols.add(node.id)

def convert_math_to_sympy_ast(math_expr, mapping):
    """
    Convert a math expression string to SymPy-compatible string using AST.
    """
    try:
        tree = ast.parse(math_expr, mode='eval')
    except SyntaxError as se:
        raise ValueError(f"Invalid syntax: {se}")

    transformer = MathToSymPyTransformer(mapping)
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)

    try:
        sympy_string = ast.unparse(transformed_tree)
    except AttributeError:
        import astor
        sympy_string = astor.to_source(transformed_tree).strip()
    return sympy_string

def extract_symbols(math_expr):
    """
    Extract variable symbols from the math expression.
    """
    tree = ast.parse(math_expr, mode='eval')
    extractor = SymbolExtractor()
    extractor.visit(tree)
    # Exclude known modules to prevent treating them as symbols
    known_modules = set(MASTER_MATH_TO_SYMPY.keys())
    return {symbol for symbol in extractor.symbols if symbol not in known_modules}

# error_handler.py
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s:%(message)s')

def handle_errors(e):
    """
    Handle errors during expression conversion.
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

# main.py
def code_interpreter(long_string):
    """
    Convert a Python math expression to LaTeX using SymPy.
    """
    try:
        sympy_string = convert_math_to_sympy_ast(long_string, MASTER_MATH_TO_SYMPY)
        print("SymPy String:", sympy_string)

        symbols_in_expr = extract_symbols(long_string)
        custom_locals = {name: Symbol(name) for name in symbols_in_expr}

        # Define transformations for SymPy parser
        transformations = (standard_transformations + (implicit_multiplication_application,))

        # Parse using SymPy's parser
        sympy_expr = parse_expr(sympy_string, local_dict=custom_locals, transformations=transformations)
        latex_expression = latex(sympy_expr)
        return latex_expression

    except Exception as e:
        return handle_errors(e)

# Example Usage
if __name__ == "__main__":
    expressions = [
        "math.sin(math.pi / 2)",
        "math.exp(math.log(x))",
        "numpy.sqrt(math.pow(x, 2) + scipy.special.gamma(y))",
        "math.unknown_func(x)",
        "math.sin(math.pi / 2",
        "math.log2(x) + y * math.cos(z)",
        "cmath.polar(z)",  # Example of a complex function
    ]

    for expr in expressions:
        print(f"Expression: {expr}")
        latex_output = code_interpreter(expr)
        print(f"LaTeX: {latex_output}\n")
