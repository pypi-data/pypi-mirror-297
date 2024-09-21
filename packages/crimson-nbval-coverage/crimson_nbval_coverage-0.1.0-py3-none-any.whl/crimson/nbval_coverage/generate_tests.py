import json
import ast
import os
from typing import List, Optional
from pathlib import Path

import shutil

from crimson.ast_dev_tool.node_info import extend_positions
from crimson.ast_dev_tool import collect_nodes
from crimson.templator import format_indent, format_insert
import tokenize
import io


def get_code(notebook_path: str) -> str:
    """
    Extract code from a Jupyter notebook file.

    Args:
        notebook_path (str): Path to the notebook file.

    Returns:
        str: Concatenated code from all code cells in the notebook.
    """
    code_cells = get_code_cells(notebook_path)

    filtered_cells = []

    for code_cell in code_cells:
        comments = extract_comments(code_cell)
        if all([comment.find("nbval.ignore") == -1 for comment in comments]):
            filtered_cells.append(code_cell)

    return "\n".join(filtered_cells)


def get_code_cells(notebook_path: str) -> List[str]:
    notebook_contents = json.loads(open(os.path.abspath(notebook_path)).read())
    code_cells = [
        "\n".join(cell["source"])
        for cell in notebook_contents["cells"]
        if cell["cell_type"] == "code"
    ]

    return code_cells


def extract_comments(code: str) -> List[str]:
    comments = []
    try:
        for tok in tokenize.tokenize(io.BytesIO(code.encode("utf-8")).readline):
            if tok.type == tokenize.COMMENT:
                comments.append(tok.string)
    except tokenize.TokenError:
        # 불완전한 코드에 대한 예외 처리
        pass
    return comments


def modify_is_notebook(code: str, value: bool):
    assigns: List[ast.Assign] = collect_nodes(code, ast.Assign)

    code_lines = code.splitlines()

    for assign in assigns:
        if ast.unparse(assign.targets) == "Config.is_notebook":
            if hasattr(assign.value, "value"):
                if assign.lineno != assign.end_lineno:
                    raise Exception(
                        "Unexpected line numbers. Write `Config.is_notebook = True` in one line."
                    )
                code_lines[assign.lineno - 1] = f"Config.is_notebook = {value}"

    return "\n".join(code_lines)


def remove_nodes_with_lines(source_code: str, nodes_to_remove: List[ast.AST]) -> str:
    """
    Remove specified AST nodes from the source code.

    Args:
        source_code (str): Original source code.
        nodes_to_remove (List[ast.AST]): List of AST nodes to remove.

    Returns:
        str: Source code with specified nodes removed.
    """
    nodes_data = extend_positions(nodes_to_remove)
    code_lines = source_code.splitlines()
    lines_to_remove = {
        i
        for node_data in nodes_data
        for i in range(
            node_data["position"]["lineno"], node_data["position"]["end_lineno"] + 1
        )
    }
    return "\n".join(
        line for i, line in enumerate(code_lines, start=1) if i not in lines_to_remove
    )


def unparse_nodes(nodes: List[ast.AST]) -> str:
    """
    Convert a list of AST nodes back into source code.

    Args:
        nodes (List[ast.AST]): List of AST nodes.

    Returns:
        str: Unparsed source code.
    """
    return "\n".join(ast.unparse(node) for node in nodes)


def generate_pytest_path(
    notebook_path: str,
    notebook_root: str,
    pytest_root: str = "__pytest__",
    file_name_prefix: str = "test_ipynb_",
) -> str:

    path = Path(os.path.abspath(notebook_path))
    notebook_root = os.path.abspath(notebook_root)
    new_file_name = f"{file_name_prefix}{path.stem}.py"

    return Path(pytest_root) / path.parent.relative_to(notebook_root) / new_file_name


def generate_test_function_name(notebook_path: str) -> str:
    """
    Generate a test function name based on the notebook file name.

    Args:
        notebook_path (str): Path to the notebook file.

    Returns:
        str: Generated test function name.
    """
    return f"test_example_{Path(notebook_path).stem}"


def generate_test_function_code(function_name: str, code_in_test_function: str) -> str:
    """
    Generate the code for the test function.

    Args:
        function_name (str): Name of the test function.
        code_in_test_function (str): Code to be included in the test function.

    Returns:
        str: Generated test function code.
    """
    template = r"""
def \[function_name\]():
    \{code_in_test_function\}
"""
    return format_insert(
        template=format_indent(template, code_in_test_function=code_in_test_function),
        function_name=function_name,
    )


def sort_code(code: str) -> str:
    """
    Sort the given code by parsing and unparsing it.

    Args:
        code (str): Source code to sort.

    Returns:
        str: Sorted source code.
    """
    return ast.unparse(ast.parse(code))


def generate_import_code(code: str) -> str:
    """
    Generate import statements from the given code.

    Args:
        code (str): Source code to extract imports from.

    Returns:
        str: Generated import statements.
    """
    all_import_nodes = get_all_import_nodes(code)
    return unparse_nodes(all_import_nodes)


def get_all_import_nodes(code: str) -> List[ast.AST]:
    """
    Get all import nodes from the given code.

    Args:
        code (str): Source code to extract import nodes from.

    Returns:
        List[ast.AST]: List of import nodes.
    """
    import_nodes = collect_nodes(code, ast.Import)
    from_import_nodes = collect_nodes(code, ast.ImportFrom)
    return import_nodes + from_import_nodes


def process_notebook(
    notebook_path: str,
    notebook_root: str,
    pytest_root: Optional[str] = None,
    file_name_prefix: str = "test_ipynb_",
) -> None:
    """
    Process a Jupyter notebook and generate a corresponding test file.

    Args:
        notebook_path (str): Path to the Jupyter notebook file.
    """
    if pytest_root is None:
        pytest_root = Path(notebook_root) / "__pytest__"

    test_path = generate_pytest_path(
        notebook_path, notebook_root, pytest_root, file_name_prefix
    )
    function_name = generate_test_function_name(notebook_path)
    source_code = get_code(notebook_path)
    source_code = modify_is_notebook(source_code, value=False)
    import_nodes = get_all_import_nodes(source_code)
    import_code = generate_import_code(source_code)
    code_in_test_function = remove_nodes_with_lines(source_code, import_nodes)
    test_function_code = generate_test_function_code(
        function_name, code_in_test_function
    )
    test_code = import_code + test_function_code

    os.makedirs(Path(test_path).parent, exist_ok=True)
    with open(test_path, "w") as f:
        f.write(sort_code(test_code))

    print(f"Generated test file: {test_path}")


def process_notebooks_recursively(
    notebook_root: str,
    pytest_root: Optional[str] = None,
    file_name_prefix: str = "test_ipynb_",
) -> None:
    """
    Recursively process all Jupyter notebooks in the given root directory and its subdirectories.

    Args:
        notebook_root (str): Root directory containing notebooks.
        pytest_root (str): Root directory for pytest files.
        file_name_prefix (str): Prefix for generated test files.
    """
    notebook_root_path = Path(notebook_root).resolve()

    for notebook_path in notebook_root_path.rglob("*.ipynb"):
        if not any(
            part.startswith(".") for part in notebook_path.parts
        ):  # 숨김 폴더 제외
            relative_path = notebook_path.relative_to(notebook_root_path)
            print(f"Processing notebook: {relative_path}")
            process_notebook(
                str(notebook_path),
                str(notebook_root_path),
                pytest_root,
                file_name_prefix,
            )


def delete_dir(dir: str):
    shutil.rmtree(dir)


class Config:
    is_notebook = True
    ignore = True
