import ast

class BitwiseOperatorChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.BitOr, ast.BitAnd)):
            parent = getattr(node, 'parent', None)
            if isinstance(parent, ast.If):
                operator_name = 'bitwise OR' if isinstance(node.op, ast.BitOr) else 'bitwise AND'
                self.issues.append(f"Potential misuse of {operator_name} at line {node.lineno}")
        self.generic_visit(node)

    def get_issues(self):
        return self.issues