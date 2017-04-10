import os, re, requests, uuid, logging, time, configparser
from subprocess import Popen, PIPE
from xml.etree.ElementTree import Element, SubElement, tostring
from bs4 import BeautifulSoup
from random import randint
from unittest import TestCase
from api_testing.utiles.utiles import Utiles


class TestcasesBase(TestCase):
    def __init__(self):
        super(TestcasesBase, self).__init__()
        self.config = Utiles().get_config_values()

    def setUp(self):
        pass

    def tearDown(self):
        pass
