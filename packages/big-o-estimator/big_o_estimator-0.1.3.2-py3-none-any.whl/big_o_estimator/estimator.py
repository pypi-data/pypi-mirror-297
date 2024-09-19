import ast
import inspect


def estimate_big_o_from_source(source_code):
    """
    Estimate the Big-O complexity of an algorithm based on its source code.

    Args:
    source_code (str): The source code of the algorithm to analyze.

    Returns:
    str: The estimated Big-O complexity.
    """
    # Parse the source code into an Abstract Syntax Tree (AST)
    tree = ast.parse(source_code)

    # Initialize counters for different constructs
    loop_count = 0
    nested_loop_count = 0
    recursion_count = 0

    # Traverse the AST to analyze the code
    for node in ast.walk(tree):
        if isinstance(node, ast.For) or isinstance(node, ast.While):
            loop_count += 1
            # Check for nested loops by examining the body of loops
            for inner_node in ast.walk(node):
                if isinstance(inner_node, ast.For) or isinstance(inner_node, ast.While):
                    nested_loop_count += 1
        elif isinstance(node, ast.FunctionDef):
            # Check for recursive calls within the function definition
            if any(
                isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id == node.name
                for n in ast.walk(node)
                if isinstance(n, ast.Call)
            ):
                recursion_count += 1

    # Determine the Big-O complexity based on the counts
    if recursion_count > 0:
        return "O(2^n) or O(n!) (recursive)"
    elif nested_loop_count > loop_count:
        return "O(n^2) or higher (nested loops)"
    elif loop_count > 0:
        return "O(n) (single loop)"
    else:
        return "O(1) (constant time)"


def get_big_o_of_function(func):
    """
    Get the Big-O complexity of a provided function.

    Args:
    func (function): The function to analyze.

    Returns:
    str: The estimated Big-O complexity.
    """
    source_code = inspect.getsource(func)
    return estimate_big_o_from_source(source_code)
