import sys
import collections
from termcolor import colored

def eprint(obj, indent=0, color=None, on_color=None, attrs=None, _visited=None):
    """
    Custom pretty-print function with color and formatting options.

    Parameters:
        obj: The object to be printed.
        indent: Current indentation level.
        color: Text color.
        on_color: Background color.
        attrs: List of attributes like bold, underline, etc.
        _visited: Internal parameter to track visited objects (for handling recursion).
    """
    if _visited is None:
        _visited = set()

    if id(obj) in _visited:
        print(colored("<Recursive Reference>", color=color, on_color=on_color, attrs=attrs))
        return

    _visited.add(id(obj))

    indent_str = ' ' * indent
    if isinstance(obj, dict):
        print(colored("{", color=color, on_color=on_color, attrs=attrs))
        for k, v in obj.items():
            print(indent_str + ' ' * 2 + colored(repr(k) + ": ", color=color, on_color=on_color, attrs=attrs), end='')
            eprint(v, indent=indent + 4, color=color, on_color=on_color, attrs=attrs, _visited=_visited)
        print(indent_str + colored("}", color=
