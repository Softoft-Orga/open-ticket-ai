"""
A script to generate structured JSON documentation from Python source code.

This script uses Python's `ast` module and dataclasses to create a typed,
structured representation of the source code. The final output is a JSON file
ready for consumption by front-end frameworks like VitePress/Vue.
"""
import ast
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Optional, Union

from docstring_parser import Docstring, DocstringParam, DocstringRaises, parse


# --- Data Models (using Dataclasses) ---

@dataclass
class ParameterData:
    """Represents a single parameter from a docstring."""
    name: Optional[str] = None
    type: Optional[str] = None
    default: Optional[str] = None
    is_optional: Optional[bool] = None
    description: Optional[str] = None


@dataclass
class ReturnsData:
    """Represents the returns section of a docstring."""
    type: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None


@dataclass
class DocstringData:
    """Represents a parsed docstring."""
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    params: list[ParameterData] = field(default_factory=list)
    raises: list[ParameterData] = field(default_factory=list)
    returns: Optional[ReturnsData] = None


@dataclass
class FunctionData:
    """Represents a parsed function or method."""
    name: str
    signature: str
    is_async: bool
    docstring: DocstringData


@dataclass
class ClassData:
    """Represents a parsed class."""
    name: str
    docstring: DocstringData
    methods: list[FunctionData] = field(default_factory=list)


@dataclass
class ModuleData:
    """Represents a single parsed Python file."""
    module_path: str
    module_docstring: DocstringData
    classes: list[ClassData] = field(default_factory=list)
    functions: list[FunctionData] = field(default_factory=list)


# --- Custom JSON Encoder for Dataclasses ---

class DataClassJSONEncoder(json.JSONEncoder):
    """A JSON encoder that can handle dataclasses."""

    def default(self, o):
        if isinstance(o, Path):
            return str(o)
        if hasattr(o, '__dict__'):
            return o.__dict__
        try:
            return super().default(o)
        except TypeError:
            return str(o)


# --- AST Visitor ---

class JsonVisitor(ast.NodeVisitor):
    """
    An AST visitor that traverses a Python file and builds a collection
    of dataclass objects representing the documentation structure.
    """

    def __init__(self):
        self.classes: list[ClassData] = []
        self.functions: list[FunctionData] = []
        self.current_class_context: Optional[ClassData] = None

    def _format_signature(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> str:
        """Formats a function/method signature into a readable string."""
        # This implementation remains the same
        args_list = []
        for arg in node.args.posonlyargs + node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args_list.append(arg_str)
        if node.args.vararg:
            args_list.append(f"*{node.args.vararg.arg}")
        if node.args.kwonlyargs:
            if not node.args.vararg:
                args_list.append('*')
            for kw_arg in node.args.kwonlyargs:
                kw_arg_str = kw_arg.arg
                if kw_arg.annotation:
                    kw_arg_str += f": {ast.unparse(kw_arg.annotation)}"
                args_list.append(kw_arg_str)
        if node.args.kwarg:
            args_list.append(f"**{node.args.kwarg.arg}")
        signature = f"({', '.join(args_list)})"
        if node.returns:
            signature += f" -> {ast.unparse(node.returns)}"
        return signature

    def _process_docstring(self, docstring_raw: Optional[str]) -> DocstringData:
        """Parses a docstring and returns a DocstringData instance."""
        if not docstring_raw:
            return DocstringData()

        docstring: Docstring = parse(docstring_raw)

        def param_to_dataclass(p: Union[DocstringParam, DocstringRaises]) -> ParameterData:
            # --- START OF FIX ---
            # Check if we are processing a 'Raises' entry instead of a 'Param' entry
            if isinstance(p, DocstringRaises):
                return ParameterData(
                    name=p.type_name,  # The "name" of a raise is its type (e.g., ValueError)
                    type=p.type_name,
                    description=p.description,
                )
            # --- END OF FIX ---

            # This is the original logic for regular parameters, which is correct.
            return ParameterData(
                name=p.arg_name,
                type=p.type_name,
                default=p.default,
                is_optional=p.is_optional,
                description=p.description,
            )

        returns_data = None
        if docstring.returns:
            returns_data = ReturnsData(
                type=docstring.returns.type_name,
                description=docstring.returns.description,
                name=docstring.returns.return_name,
            )

        return DocstringData(
            short_description=docstring.short_description,
            long_description=docstring.long_description,
            params=[param_to_dataclass(p) for p in docstring.params],
            raises=[param_to_dataclass(p) for p in docstring.raises],  # This now works correctly
            returns=returns_data,
        )

    def visit_ClassDef(self, node: ast.ClassDef):
        """Processes a class definition."""
        class_info = ClassData(
            name=node.name,
            docstring=self._process_docstring(ast.get_docstring(node)),
        )
        self.classes.append(class_info)
        self.current_class_context = class_info
        self.generic_visit(node)
        self.current_class_context = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Processes a function or method definition."""
        self._process_function_node(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Processes an async function or method definition."""
        self._process_function_node(node, is_async=True)

    def _process_function_node(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], is_async: bool = False
    ):
        """Processes a function/method node into a FunctionData instance."""
        func_name = node.name
        if func_name.startswith("_") and not func_name.startswith("__"):
            return  # Skip private methods/functions

        function_info = FunctionData(
            name=func_name,
            signature=self._format_signature(node),
            is_async=is_async,
            docstring=self._process_docstring(ast.get_docstring(node)),
        )

        if self.current_class_context:
            self.current_class_context.methods.append(function_info)
        else:
            self.functions.append(function_info)


# --- Main Orchestration Logic ---

def parse_python_file(file_path: Path) -> tuple[DocstringData, list[ClassData], list[FunctionData]]:
    """Parses a Python file and returns its documentation components."""
    source_code = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source_code)

    module_docstring_raw = ast.get_docstring(tree)
    visitor = JsonVisitor()
    visitor.visit(tree)

    module_docstring = visitor._process_docstring(module_docstring_raw)

    return module_docstring, visitor.classes, visitor.functions


def generate_documentation(
    src_path: Path,
    output_path: Path,
    exclude_patterns: Optional[list[str]] = None,
) -> None:
    """
    Generates structured JSON documentation for an entire Python project.

    Args:
        src_path: The root directory of the Python source code.
        output_path: The file path to save the generated JSON file.
        exclude_patterns: A list of glob patterns to exclude from parsing.
    """
    if not src_path.is_dir():
        raise ValueError(f"Source path `{src_path}` is not a directory.")
    if exclude_patterns is None:
        exclude_patterns = []

    all_python_files = list(src_path.rglob("*.py"))

    # Filter out excluded files
    filtered_files = [
        py_file for py_file in all_python_files
        if not any(py_file.match(pattern) for pattern in exclude_patterns)
    ]

    all_module_data = []
    for py_file in sorted(filtered_files):
        try:
            relative_path = py_file.relative_to(src_path)

            print(f"📄 Processing: {relative_path}")

            module_doc, classes, functions = parse_python_file(py_file)
            relative_path = relative_path.with_suffix("")  # Remove .py suffix for cleaner paths
            relative_path = str(relative_path).replace("/", ".")  # Normalize path for JSON output
            relative_path = str(relative_path).replace("\\", ".")  # Normalize path for JSON output
            module_data = ModuleData(
                module_path=str(relative_path),
                module_docstring=module_doc,
                classes=classes,
                functions=functions,
            )
            all_module_data.append(asdict(module_data))
        except Exception as e:
            print(f"❌ Error parsing `{py_file}`: {e}")

    # Ensure the output directory exists and write the JSON file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_module_data, f, indent=2, cls=DataClassJSONEncoder)

    print(f"\n✅ JSON documentation successfully generated at: {output_path.resolve()}")

# --- Example Usage ---
