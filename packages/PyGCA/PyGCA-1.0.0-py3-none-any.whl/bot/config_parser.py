import configparser
import os

class ConfigLoader:
    def __init__(self, config_file='.pygcconfig'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
            return self.config
        else:
            print(f"Config file '{self.config_file}' not found.")
            return None

    def get_excluded_files(self):
        return self.config.get('operators', 'exclude_files', fallback='').split(',')

    def get_excluded_operators(self):
        return self.config.get('operators', 'exclude_operators', fallback='').split(',')

    def should_read_readme(self):
        return self.config.getboolean('guidelines', 'read_readme', fallback=False)

    def should_read_contributing(self):
        return self.config.getboolean('guidelines', 'read_contributing', fallback=False)

    def get_custom_message(self, operator):
        return self.config.get(f'{operator}', 'custom_message', fallback=None)