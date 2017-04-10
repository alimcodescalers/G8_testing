import os, configparser


class Utiles:
    def __init__(self):
        self.config = {}

    def get_config_values(self):
        script_dir = os.path.dirname(__file__)
        config_file = "../config.ini"
        config_path = os.path.join(script_dir, config_file)
        config = configparser.ConfigParser()
        config.read(config_path)
        section = config.sections()[0]
        options = config.options(section)
        for option in options:
            value = config.get(section, option)
            self.config[option] = value
        return self.config