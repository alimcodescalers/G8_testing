import os, configparser, logging


class Utiles:
    def __init__(self):
        self.config = {}
        self.logging = logging
        self.log('api_testing/api_testing.log')

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

    def log(self, log_file_name='log.log'):
        self.logging.basicConfig(filename=log_file_name, filemode='w', level=logging.INFO,
                                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        '''
        How to use:
            self.logging.debug("This is a debug message")
            self.logging.info("Informational message")
            self.logging.error("An error has happened!")
        '''