import ast
from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
from bot.bitwise.bitwise_checker import BitwiseOperatorChecker

class OperatorDetector(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit(self, node):
        # Use both arithmetic and bitwise checkers
        arithmetic_checker = ArithmeticOperatorChecker()
        bitwise_checker = BitwiseOperatorChecker()
        arithmetic_checker.visit(node)
        bitwise_checker.visit(node)

        self.issues.extend(arithmetic_checker.get_issues())
        self.issues.extend(bitwise_checker.get_issues())

    def get_issues(self):
        return self.issues