import ast

class CommentRemover(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Remove the function`s docstring
        if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Str)):
            node.body = node.body[1:]
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        # Remove the documentation strings of a class
        if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Str)):
            node.body = node.body[1:]
        self.generic_visit(node)
        return node

    def visit_Module(self, node):
        # Remove the module`s docstrings
        if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Str)):
            node.body = node.body[1:]
        self.generic_visit(node)
        return node
    

def remove_python_comments(source_code):
    # Parse source code into AST
    tree = ast.parse(source_code)
    # Remove comments
    transformer = CommentRemover()
    tree = transformer.visit(tree)
    # Convert the processed AST back to source code
    return ast.unparse(tree)

# Example usage
if __name__ == "__main__":
    with open("source.py", "r", encoding="utf-8") as f:
        source_code = f.read()

    cleaned_code = remove_python_comments(source_code)

    with open("cleaned_source.py", "w", encoding="utf-8") as f:
        f.write(cleaned_code)