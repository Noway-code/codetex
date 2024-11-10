import re

python_to_latex = {
    # Keywords
    'def': r'\textbf{def} ',
    'return': r'\textbf{return} ',
    'if': r'\textbf{if} ',
    'else': r'\textbf{else} ',
    'elif': r'\textbf{elif} ',
    'for': r'\textbf{for} ',
    'while': r'\textbf{while} ',
    'in': r'\textbf{in} ',
    'and': r'\textbf{and} ',
    'or': r'\textbf{or} ',
    'not': r'\textbf{not} ',
    'True': r'\textbf{True}',
    'False': r'\textbf{False}',
    'None': r'\textbf{None}',
    'import': r'\textbf{import} ',
    'from': r'\textbf{from} ',
    'as': r'\textbf{as} ',
    'class': r'\textbf{class} ',
    'try': r'\textbf{try} ',
    'except': r'\textbf{except} ',
    'raise': r'\textbf{raise} ',
    'with': r'\textbf{with} ',
    'lambda': r'\textbf{lambda} ',
    'global': r'\textbf{global} ',
    'nonlocal': r'\textbf{nonlocal} ',

    # Built-in functions
    'print': r'\textbf{print} ',
    'input': r'\textbf{input} ',
    'len': r'\textbf{len} ',
    'sum': r'\textbf{sum} ',
    'min': r'\textbf{min} ',
    'max': r'\textbf{max} ',
    'range': r'\textbf{range} ',
    'type': r'\textbf{type} ',
    'int': r'\textbf{int} ',
    'float': r'\textbf{float} ',
    'str': r'\textbf{str} ',
    'list': r'\textbf{list} ',
    'dict': r'\textbf{dict} ',
    'set': r'\textbf{set} ',
    'tuple': r'\textbf{tuple} ',
    'zip': r'\textbf{zip} ',
    'map': r'\textbf{map} ',
    'filter': r'\textbf{filter} ',
    'open': r'\textbf{open} ',

    # Operators
    '=': r' \mathrel{=} ',
    '==': r' \mathrel{==} ',
    '!=': r' \mathrel{\neq} ',
    '<': r' \mathrel{<} ',
    '>': r' \mathrel{>} ',
    '<=': r' \mathrel{\leq} ',
    '>=': r' \mathrel{\geq} ',
    '+': r' \mathbin{+} ',
    '-': r' \mathbin{-} ',
    '*': r' \mathbin{\times} ',
    '/': r' \mathbin{\div} ',
    '**': r' \mathbin{**} ',
    '//': r' \mathbin{//} ',
    '%': r' \mathbin{\%} ',
    '(': r'\left( ',
    ')': r'\right) ',
    '[': r'\left[ ',
    ']': r'\right] ',
    '{': r'\left\{ ',
    '}': r'\right\} ',
    '#': r'\#',
    '\n': r'\\',

    # Math module functions
    'math': r'\textbf{math} ',
    'math.sqrt': r'\sqrt ',
    'math.pi': r'\pi ',
    'math.e': r'e ',
    'math.sin': r'\sin ',
    'math.cos': r'\cos ',
    'math.tan': r'\tan ',
    'math.log': r'\log ',
    'math.exp': r'e^{',
    'math.pow': r'^{',  # assumes usage like math.pow(x, 2) --> x^{2}
    'math.factorial': r'! ',
    'math.radians': r'\textbf{radians} ',
    'math.degrees': r'\textbf{degrees} ',

    # Numpy module functions
    'np': r'\textbf{np} ',
    'np.array': r'\textbf{array} ',
    'np.arange': r'\textbf{arange} ',
    'np.zeros': r'\textbf{zeros} ',
    'np.ones': r'\textbf{ones} ',
    'np.linspace': r'\textbf{linspace} ',
    'np.dot': r'\cdot ',
    'np.cross': r'\times ',
    'np.mean': r'\textbf{mean} ',
    'np.std': r'\textbf{std} ',
    'np.var': r'\textbf{var} ',
    'np.sum': r'\sum ',
    'np.min': r'\min ',
    'np.max': r'\max ',
    'np.sqrt': r'\sqrt ',
    'np.log': r'\log ',
    'np.exp': r'e^{',
    'np.sin': r'\sin ',
    'np.cos': r'\cos ',
    'np.tan': r'\tan ',
    'np.pi': r'\pi ',
    'np.e': r'e ',

    # Scipy module functions
    'scipy': r'\textbf{scipy} ',
    'scipy.integrate': r'\textbf{integrate} ',
    'scipy.optimize': r'\textbf{optimize} ',
    'scipy.fftpack': r'\textbf{fftpack} ',
    'scipy.linalg': r'\textbf{linalg} ',
    'scipy.stats': r'\textbf{stats} ',
    'scipy.spatial': r'\textbf{spatial} ',
    'scipy.constants': r'\textbf{constants} ',

    # Scipy.stats functions
    'scipy.stats.norm': r'\mathcal{N} ',
    'scipy.stats.t': r't ',
    'scipy.stats.chi2': r'\chi^2 ',
    'scipy.stats.f': r'F ',
    'scipy.stats.expon': r'\textbf{expon} ',
    'scipy.stats.poisson': r'\textbf{poisson} ',
    'scipy.stats.binom': r'\textbf{binom} ',
}
import re

python_to_latex = {
    'def': r'\textbf{\text{def}} ',
    'return': r'\textbf{\text{return}} ',
    'if': r'\textbf{\text{if}} ',
    'else': r'\textbf{\text{else}} ',
    'elif': r'\textbf{\text{elif}} ',
    'for': r'\textbf{\text{for}} ',
    'while': r'\textbf{\text{while}} ',
    'in': r'\textbf{\text{in}} ',
    'and': r'\textbf{\text{and}} ',
    'or': r'\textbf{\text{or}} ',
    'not': r'\textbf{\text{not}} ',
    'True': r'\textbf{\text{True}}',
    'False': r'\textbf{\text{False}}',
    'None': r'\textbf{\text{None}}',
    'print': r'\textbf{\text{print}} ',
    'input': r'\textbf{\text{input}} ',
    'math.sqrt': r'\sqrt ',
    'abs': r'\textbf{\text{abs}} ',
}

def escape_latex_special_chars(text):
    """Escape special characters in LaTeX."""
    special_chars = {'%': r'\%', '_': r'\_', '$': r'\$', '#': r'\#', '{': r'\{', '}': r'\}', 
                     '&': r'\&', '^': r'\^{}', '\\': r'\\textbackslash ', '~': r'\~{}'}
    return ''.join(special_chars.get(char, char) for char in text)

def print_tokens(long_string):
    lines = long_string.splitlines()
    in_multiline_string = False
    
    for line in lines:
        if in_multiline_string:
            if '"""' in line or "'''" in line:
                in_multiline_string = False
                line = escape_latex_special_chars(line).replace('"""', '').replace("'''", '')
                print(r'& \texttt{' + line + r'} \\')
                continue
            print(r'& \texttt{' + escape_latex_special_chars(line) + r'} \\')
            continue

        # Check for multi-line string start
        if line.strip().startswith(('"""', "'''")):
            in_multiline_string = True
            line = escape_latex_special_chars(line).replace('"""', '').replace("'''", '')
            print(r'& \texttt{' + line + r'} \\')
            continue

        # Determine indentation level for alignment
        indentation_level = len(line) - len(line.lstrip())
        print(' ' * indentation_level + '& ' * (indentation_level // 4), end='')

        # Tokenize the line, including comments and commas
        tokens = re.findall(r'[A-Za-z_]\w*(?:\.\w+)*|\d+|==|!=|<=|>=|[{}()\[\]<>!=+\-*/%,]|".*?"|\'.*?\'|#.*|\.', line)

        for i, token in enumerate(tokens):
            if token.startswith('#'):
                # Handle comments by wrapping them in \text{}
                comment = escape_latex_special_chars(token[1:].strip())
                print(r'\text{' + comment + r'} ', end='')
                break  # Comments should end the line
            elif token.startswith('"') or token.startswith("'"):
                # Handle string literals
                print(r'\texttt{' + escape_latex_special_chars(token[1:-1]) + r'} ', end='')
            elif token in python_to_latex:
                # Check if it's a function definition and bold both def and the function name
                if token == 'def' and i < len(tokens) - 1:
                    func_name = tokens[i + 1]
                    func_name = escape_latex_special_chars(func_name)
                    print(r'\textbf{def ' + func_name + r'} ', end='')
                    next(i for _ in range(i + 2))  # Skip the function name token
                else:
                    print(python_to_latex[token], end='')
            elif token == '.':
                print(r'.', end='')
            elif i > 0 and tokens[i-1] == '.':
                # Attributes or methods after a dot are italicized
                print(r'\textit{' + escape_latex_special_chars(token) + '} ', end='')
            elif re.match(r'^\d+$', token):
                print(token, end=' ')
            elif token in ('+', '-', '*', '/', '**', '//', '%', '=', '==', '!=', '<', '>', '<=', '>='):
                print(escape_latex_special_chars(token) + ' ', end='')
            elif token == ',':
                # Preserve commas without additional formatting
                print(token, end=' ')
            else:
                # Default behavior for variable names
                token = escape_latex_special_chars(token)
                if i < len(tokens) - 1 and tokens[i + 1] == '(':
                    # Format function calls
                    print(r'\textbf{' + token + '} ', end='')
                else:
                    print(token, end=' ')
        print(r'\\')  # Newline for LaTeX

# Test case
long_string = """
def foo(x, y):
     # calculating discriminant using formula
    dis = b * b - 4 * a * c 
    sqrt_val = math.sqrt(abs(dis)) 
    
    # checking condition for discriminant
    if dis > 0: 
        print("real and different roots") 
        print((-b + sqrt_val)/(2 * a)) 
        print((-b - sqrt_val)/(2 * a)) 
    
    elif dis == 0: 
        print("real and same roots") 
        print(-b / (2 * a)) 
    
    # when discriminant is less than 0
    else:
        print("Complex Roots") 
        print(- b / (2 * a), + i, sqrt_val / (2 * a)) 
        print(- b / (2 * a), - i, sqrt_val / (2 * a)) 
"""
print_tokens(long_string)
