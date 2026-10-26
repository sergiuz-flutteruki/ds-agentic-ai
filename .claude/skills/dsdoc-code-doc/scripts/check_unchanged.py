"""Check that adding documentation did not change a file's logic.

Usage:
    python check_unchanged.py <original> <edited>
    python check_unchanged.py --git <file>        # compare against git HEAD

Python (.py): compares the AST with docstrings removed (comments are not in the AST).
SQL (.sql):   compares the code with comments removed and whitespace normalized.

Exit code 0 = logic unchanged, 1 = logic changed.
"""
import ast
import subprocess
import sys


def normalize_python(code):
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    return ast.dump(tree)


def normalize_sql(code):
    """Remove -- and /* */ comments (not inside quotes), collapse whitespace."""
    out, i, n = [], 0, len(code)
    while i < n:
        ch = code[i]
        if ch in ("'", '"'):                      # quoted string or identifier
            j = i + 1
            while j < n:
                if code[j] == ch:
                    if j + 1 < n and code[j + 1] == ch:   # escaped quote
                        j += 2
                        continue
                    break
                j += 1
            out.append(code[i:j + 1])
            i = j + 1
        elif code.startswith("--", i):
            j = code.find("\n", i)
            i = n if j == -1 else j
        elif code.startswith("/*", i):
            j = code.find("*/", i + 2)
            i = n if j == -1 else j + 2
            out.append(" ")
        else:
            out.append(ch)
            i += 1
    return " ".join("".join(out).split())


def main():
    if sys.argv[1] == "--git":
        path = sys.argv[2]
        original = subprocess.run(["git", "show", f"HEAD:{path}"],
                                  capture_output=True, text=True, check=True).stdout
    else:
        path = sys.argv[2]
        original = open(sys.argv[1], encoding="utf-8").read()
    edited = open(path, encoding="utf-8").read()

    normalize = normalize_sql if path.endswith(".sql") else normalize_python
    if normalize(original) == normalize(edited):
        print(f"OK: logic unchanged in {path}")
        sys.exit(0)
    print(f"ERROR: logic changed in {path}")
    sys.exit(1)


if __name__ == "__main__":
    main()
