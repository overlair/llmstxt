import ast
import pathlib
import re

from gitignore_parser import parse_gitignore  # type: ignore


def compress_python_code(content):
    """Compress Python code while preserving docstrings."""
    try:
        parsed_ast = ast.parse(content)
    except SyntaxError:
        # If the code cannot be parsed, return it unmodified
        return content

    class RemoveCommentsAndDocstrings(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)
            return node

        def visit_ClassDef(self, node):
            self.generic_visit(node)
            return node

        def visit_AsyncFunctionDef(self, node):
            self.generic_visit(node)
            return node

        def visit_Module(self, node):
            self.generic_visit(node)
            return node

        def visit_Expr(self, node):
            if not isinstance(node.value, ast.Constant):
                # Remove expressions that are not docstrings
                return None
            return node

        def visit_Str(self, node):
            # Keep docstrings, remove other strings
            return node

        def visit_Constant(self, node):
            # For Python 3.8 and above (ast.Constant replaces ast.Str)
            if isinstance(node.value, str):
                # Keep docstrings
                return node
            return None

        def visit_Import(self, node):
            return node

        def visit_ImportFrom(self, node):
            return node

        def visit_Pass(self, node):
            return node

    transformer = RemoveCommentsAndDocstrings()
    cleaned_ast = transformer.visit(parsed_ast)
    ast.fix_missing_locations(cleaned_ast)
    compressed_code = ast.unparse(cleaned_ast)
    return compressed_code


def compress_code_content(content, file_extension):
    """Compress code content based on the file extension."""
    if file_extension == ".py":
        return compress_python_code(content)
    else:
        # For other languages, basic comment and blank line removal
        return basic_compress(content, file_extension)


def basic_compress(content, file_extension):
    """Basic compression: remove comments and multiple blank lines."""
    if file_extension in [".js", ".java", ".c", ".cpp", ".h", ".hpp", ".sh"]:
        # Remove single-line comments starting with //
        content = re.sub(r"//.*", "", content)
        # Remove multi-line comments /* ... */
        content = re.sub(r"/\*[\s\S]*?\*/", "", content)
        # Remove shell script comments starting with #
        if file_extension == ".sh":
            content = re.sub(r"#.*", "", content)
    # Remove multiple blank lines
    content = re.sub(r"\n\s*\n", "\n", content)
    return content.strip()


def compress_text_content(content):
    """Removes multiple blank lines from text files."""
    content = re.sub(r"\n\s*\n", "\n", content)
    return content.strip()


def compress_markdown_content(content):
    """Extracts code blocks from Markdown and compresses them."""
    code_blocks = re.findall(r"```.*?\n(.*?)```", content, re.DOTALL)
    compressed_blocks = []
    for block in code_blocks:
        compressed_block = basic_compress(block, "")
        compressed_blocks.append(compressed_block)
    return "\n".join(compressed_blocks)


def generate_llms_txt(
    output_file="llms.txt",
    allowed_extensions=(
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
    max_file_size=100 * 1024,  # 100 KB
):
    """
    Generates a compressed llms.txt file.
    """
    current_dir = pathlib.Path(".")
    gitignore_path = current_dir / ".gitignore"
    matches = parse_gitignore(gitignore_path) if gitignore_path.exists() else None

    with open(output_file, "w", encoding="utf-8") as outfile:
        # Include README.md and LICENSE at the beginning if they exist
        for special_file in ["README.md", "LICENSE", "LICENSE.txt"]:
            special_path = current_dir / special_file
            if special_path.exists():
                outfile.write(f"# {special_file}\n\n")
                with open(
                    special_path, "r", encoding="utf-8", errors="replace"
                ) as infile:
                    content = infile.read()
                    outfile.write(content + "\n\n")

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

                relative_path = file.relative_to(current_dir)
                outfile.write(f"## File: {relative_path}\n\n")

                try:
                    with open(file, "r", encoding="utf-8", errors="replace") as infile:
                        content = infile.read()
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
                            compressed_content = compress_code_content(
                                content, file.suffix.lower()
                            )
                            language = file.suffix.lstrip(".")
                            outfile.write(
                                f"```{language}\n{compressed_content}\n```\n\n"
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
                            compressed_content = compress_text_content(content)
                            outfile.write(f"```\n{compressed_content}\n```\n\n")
                        elif file.suffix.lower() == ".md":
                            compressed_content = compress_markdown_content(content)
                            outfile.write(f"```md\n{compressed_content}\n```\n\n")
                        else:
                            # For other files like .html, include as-is
                            outfile.write(
                                f"```{file.suffix.lstrip('.')}\n{content}\n```\n\n"
                            )
                except Exception as e:
                    outfile.write(f"Error processing {relative_path}: {e}\n\n")


if __name__ == "__main__":
    output_filename = "llms.txt"
    generate_llms_txt(output_filename)
    print(f"{output_filename} generated successfully in the current directory!")
