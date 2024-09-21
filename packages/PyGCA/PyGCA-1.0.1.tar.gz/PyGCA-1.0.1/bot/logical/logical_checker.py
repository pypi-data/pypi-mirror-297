import ast

class LogicalOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_BoolOp(self, node):
        if isinstance(node.op, ast.And):
            self.issues.append(f"Logical AND detected at line {node.lineno}")
        elif isinstance(node.op, ast.Or):
            self.issues.append(f"Logical OR detected at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues