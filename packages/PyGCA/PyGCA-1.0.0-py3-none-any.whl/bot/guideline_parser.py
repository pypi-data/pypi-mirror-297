import os

class GuidelineParser:
    def __init__(self, readme_file='README.md', contributing_file='CONTRIBUTING.md'):
        self.readme_file = readme_file
        self.contributing_file = contributing_file

    def parse_guidelines(self):
        guidelines = {}

        # Parse README.md
        if os.path.exists(self.readme_file):
            with open(self.readme_file, 'r') as file:
                content = file.read().lower()
                if 'use is instead of ==' in content:
                    guidelines['comparison'] = 'Use is for comparison with None'

        # Parse CONTRIBUTING.md
        if os.path.exists(self.contributing_file):
            with open(self.contributing_file, 'r') as file:
                content = file.read().lower()
                if 'avoid bitwise operators' in content:
                    guidelines['bitwise'] = 'Bitwise operators are discouraged'

        return guidelines