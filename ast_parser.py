import ast

def get_ast_structure(code):
    """ Returns AST structure, ignoring variable names, function names, and argument names. """
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


# import ast
# import os
# from tree_sitter import Language, Parser

# # Define paths for tree-sitter parsers
# TREE_SITTER_DIR = os.path.join(os.getcwd(), "tree-sitter-languages")

# # Build and load languages
# LIB_PATH = os.path.join(TREE_SITTER_DIR, "my-languages.so")
# if not os.path.exists(LIB_PATH):
#     Language.build_library(
#         LIB_PATH,
#         [
#             os.path.join(TREE_SITTER_DIR, "tree-sitter-python"),
#             os.path.join(TREE_SITTER_DIR, "tree-sitter-java"),
#             os.path.join(TREE_SITTER_DIR, "tree-sitter-c"),
#             os.path.join(TREE_SITTER_DIR, "tree-sitter-cpp"),
#         ],
#     )

# # Load supported languages
# PY_LANGUAGE = Language(LIB_PATH, "python")
# JAVA_LANGUAGE = Language(LIB_PATH, "java")
# C_LANGUAGE = Language(LIB_PATH, "c")
# CPP_LANGUAGE = Language(LIB_PATH, "cpp")

# # Create parsers for different languages
# parsers = {
#     "python": Parser(),
#     "java": Parser(),
#     "c": Parser(),
#     "cpp": Parser(),
# }

# parsers["python"].set_language(PY_LANGUAGE)
# parsers["java"].set_language(JAVA_LANGUAGE)
# parsers["c"].set_language(C_LANGUAGE)
# parsers["cpp"].set_language(CPP_LANGUAGE)


# def get_ast_structure(code, language="python"):
#     """Returns AST structure, ignoring variable names, function names, and argument names."""
    
#     # Use built-in AST for Python
#     if language == "python":
#         try:
#             tree = ast.parse(code)
            
#             for node in ast.walk(tree):
#                 # Replace function names with FUNC
#                 if isinstance(node, ast.FunctionDef):
#                     node.name = "FUNC"
#                     for arg in node.args.args:
#                         arg.arg = "VAR"  # Replace argument names with VAR
                
#                 # Replace variable names with VAR
#                 elif isinstance(node, ast.Name):
#                     node.id = "VAR"
                
#                 # Replace constant values with CONST
#                 elif isinstance(node, ast.Constant):
#                     node.value = "CONST"

#             return ast.dump(tree)

#         except Exception as e:
#             return f"Error in Python AST Parsing: {str(e)}"

#     # Use Tree-Sitter for Java, C, and C++
#     elif language in ["java", "c", "cpp"]:
#         if language not in parsers:
#             raise ValueError(f"Unsupported language: {language}")

#         try:
#             # Parse the code with Tree-Sitter
#             tree = parsers[language].parse(bytes(code, "utf8"))
#             return tree.root_node.sexp()

#         except Exception as e:
#             return f"Error in {language.upper()} AST Parsing: {str(e)}"

#     else:
#         return f"Unsupported language: {language}"
