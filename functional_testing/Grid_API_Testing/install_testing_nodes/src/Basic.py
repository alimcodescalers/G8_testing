import time, requests, os, uuid, logging, configparser
from subprocess import Popen, PIPE
from src.client import Client
from random import randint


class Basic(object):
    def __init__(self):
        self.clone = False
        self.account = ''
        self.account_id = ''
        self.logging = logging
        self.log('TestingEnvironment.log')
        self.values = {'environment': '',
                       'username': '',
                       'password': '',
                       'location': ''
                       }
        self.client_header = {'Content-Type': 'application/x-www-form-urlencoded',
                              'Accept': 'application/json'}
        self.requests = requests
        self.setup()

    def setup(self):
        self.get_config_values()
        if not self.values['password']:
            self.values['password'] = str(input("Please, Enter %s's password : " % self.values['username']))

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
            self.values[option] = value

    def run_cmd_via_subprocess(self, cmd):
        sub = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
        out, err = sub.communicate()
        if sub.returncode == 0:
            return out.decode('utf-8')
        else:
            error_output = err.decode('utf-8')
            raise RuntimeError("Failed to execute command.\n\ncommand:\n{}\n\n".format(cmd, error_output))

    def log(self, log_file_name='log.log'):
        self.logging.basicConfig(filename=log_file_name, filemode='w', level=logging.INFO,
                                 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        '''
        How to use:
            self.logging.debug("This is a debug message")
            self.logging.info("Informational message")
            self.logging.error("An error has happened!")
        '''

    def get_client(self):
        for _ in range(30):
            try:
                self.client = Client('https://' + self.values['environment'], self.values['username'],
                                     self.values['password'])
                break
            except:
                time.sleep(1)
        else:
            self.client = Client('https://' + self.values['environment'], self.values['username'],
                                 self.values['password'])

    @staticmethod
    def random_string():
        return str(uuid.uuid4()).replace("-", "")[:10]

    @staticmethod
    def random_integer(min_val, max_val):
        return randint(int(min_val), int(max_val))
