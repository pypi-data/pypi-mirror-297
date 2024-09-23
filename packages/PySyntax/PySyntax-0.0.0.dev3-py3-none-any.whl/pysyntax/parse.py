from typing import Any as _Any
import ast as _ast


def function_call(code: str) -> tuple[str, dict[str, _Any]]:
    """
    Parse a Python function call from a string.

    Parameters
    ----------
    code : str
        The code to parse.

    Returns
    -------
    tuple[str, dict[str, Any]]
        A tuple containing the function name and a dictionary of keyword arguments.
    """

    class CallVisitor(_ast.NodeVisitor):

        def visit_Call(self, node):
            # Function name
            self.func_name = getattr(node.func, 'id', None)
            # Keyword arguments
            self.args = {arg.arg: self._arg_value(arg.value) for arg in node.keywords}

        def _arg_value(self, node):
            if isinstance(node, _ast.Constant):
                return node.value
            elif isinstance(node, (_ast.List, _ast.Tuple, _ast.Dict)):
                return _ast.literal_eval(node)
            return "Complex value"  # Placeholder for complex expressions

    tree = _ast.parse(code)
    visitor = CallVisitor()
    visitor.visit(tree)
    return visitor.func_name, visitor.args


def docstring(code: str) -> str | None:
    """Extract docstring from a Python module, class, or function content.

    Parameters
    ----------
    code : str
        The code to parse.

    Returns
    -------
    str or None
        The module docstring or None if not found.
    """
    tree = _ast.parse(code)
    return _ast.get_docstring(tree, clean=False)


def imports(code: str) -> list[str]:
    """Extract import statements from a Python module content.

    Parameters
    ----------
    code
        The code to parse.

    Returns
    -------
    A list of imported module names.
    """
    tree = _ast.parse(code, filename='<string>')
    imported_modules = []
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Import):
            for alias in node.names:
                imported_modules.append(alias.name)
        elif isinstance(node, _ast.ImportFrom):
            if node.module:  # Sometimes this can be None (for relative imports)
                imported_modules.append(node.module)
    return imported_modules
