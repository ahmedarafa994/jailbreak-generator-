import ast
import argparse
import os

def get_top_level_module_name(name: str) -> str:
    """Extracts the top-level module name (e.g., 'os' from 'os.path')."""
    return name.split('.')[0]

def identify_imports(file_path: str) -> set[str]:
    """
    Identifies top-level imported modules in a given Python file.

    Args:
        file_path: The path to the Python file.

    Returns:
        A set of unique top-level module names imported in the file.
    """
    imported_modules = set()

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return imported_modules

    if not file_path.endswith(".py"):
        print(f"Error: Provided file '{file_path}' is not a Python file.")
        return imported_modules

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()

        tree = ast.parse(source_code, filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.add(get_top_level_module_name(alias.name))
            elif isinstance(node, ast.ImportFrom):
                # If node.module is None, it's a relative import like 'from . import foo'
                # For this PoC, we are interested in the module name itself.
                # If level > 0, it's a relative import. node.module might be None.
                # e.g. from . import sibling -> module=None, level=1
                # e.g. from .subpackage import item -> module='subpackage', level=1
                # e.g. from package import item -> module='package', level=0
                if node.module:
                    imported_modules.add(get_top_level_module_name(node.module))
                # If node.module is None and level > 0, it means something like 'from . import x'
                # For this PoC, we won't try to resolve these relative imports further,
                # as it requires package context. We are primarily interested in external
                # or standard library dependencies named explicitly.
                # We also don't add the imported names (alias.name) from ImportFrom
                # as individual modules if a base module is specified,
                # e.g., for 'from collections import Counter', 'collections' is the dependency.

    except SyntaxError as e:
        print(f"SyntaxError parsing {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

    return imported_modules

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Identify top-level imported modules in a Python file.")
    parser.add_argument(
        "file_path",
        nargs='?',
        default="sample_module.py",
        help="Path to the Python file to analyze (default: sample_module.py)"
    )
    args = parser.parse_args()

    print(f"Analyzing imports for: {args.file_path}")

    # Ensure sample_module.py exists if it's the default and not found in current dir
    # This is more for robust execution if the script is called from elsewhere.
    # For this subtask, we assume it's in the same directory.
    # if args.file_path == "sample_module.py" and not os.path.exists("sample_module.py"):
    #     print("Error: Default sample_module.py not found. Please create it or provide a file path.")
    # else:

    modules = identify_imports(args.file_path)

    if modules:
        print("\nIdentified top-level imported modules:")
        for module_name in sorted(list(modules)):
            print(f"- {module_name}")
    elif os.path.exists(args.file_path) and args.file_path.endswith(".py"): # Only print if file was valid
        print("No top-level imports found or an error occurred during parsing.")
