import ast

class ComparisonOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_Compare(self, node):
        for op in node.ops:
            if isinstance(op, ast.Eq):
                self.issues.append(f"Use of '==' at line {node.lineno}")
            elif isinstance(op, ast.NotEq):
                self.issues.append(f"Use of '!=' at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues