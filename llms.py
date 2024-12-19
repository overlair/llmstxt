import ast
import pathlib
import re
from typing import Optional, Sequence, cast

import astroid  # type: ignore
from gitignore_parser import parse_gitignore  # type: ignore


def compress_python_code(content: str) -> str:
    """Compress Python code while preserving docstrings."""
    try:
        parsed_ast = ast.parse(content)
    except SyntaxError:
        return content

    class RemoveCommentsAndDocstrings(ast.NodeTransformer):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> Optional[ast.FunctionDef]:
            if (
                ast.get_docstring(node) is not None
                and node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            ):
                docstring = node.body[0]
                node.body = [docstring] + [
                    n for n in map(self.visit, node.body[1:]) if n is not None
                ]
                return node
            node.body = [n for n in map(self.visit, node.body) if n is not None]
            return node

        def visit_ClassDef(self, node: ast.ClassDef) -> Optional[ast.ClassDef]:
            if (
                ast.get_docstring(node) is not None
                and node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            ):
                docstring = node.body[0]
                node.body = [docstring] + [
                    n for n in map(self.visit, node.body[1:]) if n is not None
                ]
                return node
            node.body = [n for n in map(self.visit, node.body) if n is not None]
            return node

        def visit_Module(self, node: ast.Module) -> Optional[ast.Module]:
            if (
                ast.get_docstring(node) is not None
                and node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            ):
                docstring = node.body[0]
                node.body = [docstring] + [
                    n for n in map(self.visit, node.body[1:]) if n is not None
                ]
                return node
            node.body = [n for n in map(self.visit, node.body) if n is not None]
            return node

        def generic_visit(self, node: ast.AST) -> ast.AST:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                return ast.Pass()
            return super().generic_visit(node)

    try:
        transformer = RemoveCommentsAndDocstrings()
        cleaned_ast = transformer.visit(parsed_ast)
        ast.fix_missing_locations(cleaned_ast)
        # Use astroid to handle AST to source code conversion
        astroid_module = astroid.parse(ast.dump(cleaned_ast))
        compressed_code = cast(str, astroid_module.as_string())
        # Remove multiple blank lines
        compressed_code = re.sub(r"\n\s*\n\s*\n", "\n\n", compressed_code)
        return compressed_code
    except Exception as e:
        print(f"Warning: Error compressing Python code: {e}")
        return content


def compress_code_content(content: str, file_extension: str) -> str:
    """Compress code content based on the file extension."""
    if file_extension in (".py", ".pyi"):
        return compress_python_code(content)
    return basic_compress(content, file_extension)


def basic_compress(content: str, file_extension: str) -> str:
    """Basic compression: remove comments and multiple blank lines."""
    lines = content.split("\n")
    cleaned_lines = []
    for line in lines:
        if file_extension in (".py", ".sh"):
            line = re.sub(r"#.*$", "", line)
        elif file_extension in (".js", ".java", ".c", ".cpp", ".h", ".hpp"):
            line = re.sub(r"//.*$", "", line)
        cleaned_lines.append(line)

    content = "\n".join(cleaned_lines)
    return re.sub(r"\n\s*\n\s*\n", "\n\n", content)


def compress_text_content(content: str) -> str:
    """Removes multiple blank lines from text files."""
    return re.sub(r"\n\s*\n\s*\n", "\n\n", content)


def compress_markdown_content(content: str) -> str:
    """Extracts code blocks from Markdown and compresses them."""
    parts = re.split(r"(```\w*\n.*?\n```)", content, flags=re.DOTALL)
    compressed_parts = []
    for part in parts:
        if part.startswith("```"):
            lang_match = re.match(r"```(\w*)\n", part)
            lang = lang_match.group(1) if lang_match else ""
            code = re.sub(r"```\w*\n(.*)\n```", r"\1", part, flags=re.DOTALL)
            if lang in ("python", "py"):
                code = compress_python_code(code)
            else:
                code = compress_text_content(code)
            compressed_parts.append(f"```{lang}\n{code}\n```")
        else:
            compressed_parts.append(compress_text_content(part))
    return "".join(compressed_parts)


def generate_llms_txt(
    output_file: str = "llms.txt",
    allowed_extensions: Sequence[str] = (
        ".py",
        ".js",
        ".html",
        ".css",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".sh",
        ".txt",
        ".md",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
    ),
    max_file_size: int = 100 * 1024,  # 100 KB
) -> None:
    """
    Generates a compressed llms.txt file optimized for LLM/AI consumption.

    Args:
        output_file: Name of the output file
        allowed_extensions: Tuple of file extensions to process
        max_file_size: Maximum file size in bytes to process
    """
    current_dir: pathlib.Path = pathlib.Path(".")
    gitignore_path: pathlib.Path = current_dir / ".gitignore"
    matches = parse_gitignore(gitignore_path) if gitignore_path.exists() else None

    with open(output_file, "w", encoding="utf-8") as outfile:
        # Project metadata
        outfile.write("# Project: llmstxt\n\n")
        outfile.write("## Project Structure\n")
        outfile.write(
            "This file contains the compressed and processed contents of the project.\n\n"
        )
        outfile.write("### File Types\n")
        outfile.write("The following file types are included:\n")
        outfile.write("".join([f"- {ext}\n" for ext in allowed_extensions]))
        outfile.write("\n### Special Files\n")

        # Include README and LICENSE with metadata
        for special_file in ["README.md", "LICENSE", "LICENSE.txt"]:
            special_path: pathlib.Path = current_dir / special_file
            if special_path.exists():
                outfile.write(f"<file>{special_file}</file>\n")
                outfile.write("<metadata>\n")
                outfile.write(f"path: {special_file}\n")
                outfile.write(f"size: {special_path.stat().st_size} bytes\n")
                outfile.write("</metadata>\n\n")
                with open(
                    special_path, "r", encoding="utf-8", errors="replace"
                ) as infile:
                    special_content: str = infile.read()
                    outfile.write(special_content + "\n\n")

        # Process all other files
        for file in current_dir.rglob("*"):
            if (
                file.is_file()
                and file.suffix.lower() in allowed_extensions
                and not (matches and matches(str(file.relative_to(current_dir))))
                and file.name
                not in ["README.md", "LICENSE", "LICENSE.txt", output_file]
            ):
                if file.stat().st_size > max_file_size:
                    print(f"Skipping {file} as it exceeds the maximum file size.")
                    continue

                relative_path: pathlib.Path = file.relative_to(current_dir)
                outfile.write(f"<file>{relative_path}</file>\n")
                outfile.write("<metadata>\n")
                outfile.write(f"path: {relative_path}\n")
                outfile.write(f"type: {file.suffix.lstrip('.')}\n")
                outfile.write(f"size: {file.stat().st_size} bytes\n")
                outfile.write("</metadata>\n\n")

                try:
                    with open(file, "r", encoding="utf-8", errors="replace") as infile:
                        raw_content: str = infile.read()

                        # Add semantic markers based on file type
                        if file.suffix.lower() in (".py", ".js", ".java"):
                            outfile.write("<imports>\n")
                            # Extract and write imports
                            import_lines = [
                                line
                                for line in raw_content.split("\n")
                                if any(
                                    imp in line.lower()
                                    for imp in [
                                        "import ",
                                        "from ",
                                        "require",
                                        "include",
                                    ]
                                )
                            ]
                            if import_lines:
                                outfile.write("\n".join(import_lines) + "\n")
                            outfile.write("</imports>\n\n")

                        if file.suffix.lower() in (
                            ".py",
                            ".js",
                            ".java",
                            ".c",
                            ".cpp",
                            ".h",
                            ".hpp",
                            ".sh",
                        ):
                            code_content: str = compress_code_content(
                                raw_content, file.suffix.lower()
                            )
                            language: str = file.suffix.lstrip(".")
                            outfile.write(
                                f"<code lang='{language}'>\n{code_content}\n</code>\n\n"
                            )
                        elif file.suffix.lower() in (
                            ".txt",
                            ".json",
                            ".xml",
                            ".yaml",
                            ".yml",
                            ".toml",
                            ".ini",
                        ):
                            text_content: str = compress_text_content(raw_content)
                            outfile.write(
                                f"<content type='{file.suffix.lstrip('.')}'>\n"
                            )
                            outfile.write(f"{text_content}\n")
                            outfile.write("</content>\n\n")
                        elif file.suffix.lower() == ".md":
                            md_content: str = compress_markdown_content(raw_content)
                            outfile.write("<markdown>\n")
                            outfile.write(f"{md_content}\n")
                            outfile.write("</markdown>\n\n")
                        else:
                            outfile.write(
                                f"<content type='{file.suffix.lstrip('.')}'>\n"
                            )
                            outfile.write(f"{raw_content}\n")
                            outfile.write("</content>\n\n")
                except Exception as e:
                    outfile.write(
                        f"<error>Error processing {relative_path}: {e}</error>\n\n"
                    )


if __name__ == "__main__":
    output_filename: str = "llms.txt"
    generate_llms_txt(output_filename)
    print(f"{output_filename} generated successfully in the current directory!")
