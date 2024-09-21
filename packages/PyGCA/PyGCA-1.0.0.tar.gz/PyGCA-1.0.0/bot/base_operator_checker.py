
class BaseOperatorChecker:
    def __init__(self):
        self.issues = []

    def log_issue(self, message, node):
        self.issues.append(f"{message} at line {node.lineno}")

    def get_issues(self):
        return self.issues

    def generic_visit(self, node):
        """Can be extended for future needs."""
        pass