import ast

def get_ast_structure(code):
    # Returns AST structure, ignoring variable names, function names, and argument names. 
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            # Ignore function name
            if isinstance(node, ast.FunctionDef):
                node.name = "FUNC"
                for arg in node.args.args:
                    arg.arg = "VAR"  # Replace argument names with VAR
            # Ignore variable names
            if isinstance(node, ast.Name):
                node.id = "VAR"
            # Ignore constant values
            elif isinstance(node, ast.Constant):
                node.value = "CONST"

        return ast.dump(tree)

    except Exception as e:
        return f"Error in AST Parsing: {str(e)}"

