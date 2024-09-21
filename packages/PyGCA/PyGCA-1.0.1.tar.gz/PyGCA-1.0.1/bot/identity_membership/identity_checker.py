import ast

class IdentityOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Compare(self, node):
        for op in node.ops:
            if isinstance(op, ast.Is):
                self.issues.append(f"Potential misuse of 'is' at line {node.lineno}")
            elif isinstance(op, ast.IsNot):
                self.issues.append(f"Potential misuse of 'is not' at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues