from unittest import TestCase
from api_testing.utiles.utiles import Utiles


class TestcasesBase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Utiles().get_config_values()

    def setUp(self):
        pass

    def tearDown(self):
        pass
