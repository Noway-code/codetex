import math
import numpy
import scipy.special
import cmath

def get_all_math_functions(*modules):
    """
    Extracts all callable mathematical functions from the given modules and maps them to SymPy equivalents.

    Parameters:
        *modules: Variable length argument list of modules to inspect.

    Returns:
        dict: A dictionary mapping function names to SymPy function names.
    """
    function_mapping = {}
    for module in modules:
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and not attr_name.startswith('_'):
                # Assume SymPy function has the same name
                # If SymPy doesn't have this function, it will be handled later
                function_mapping[attr_name] = attr_name
    return function_mapping

# Initialize the generic mapping by inspecting desired modules
GENERIC_MATH_TO_SYMPY_DYNAMIC = get_all_math_functions(math, numpy, scipy.special, cmath)

# Weird edge cases
GENERIC_MATH_TO_SYMPY_DYNAMIC['pow'] = 'Pow'
