import os, re, requests, uuid, logging, time, configparser
from subprocess import Popen, PIPE
from xml.etree.ElementTree import Element, SubElement, tostring
from bs4 import BeautifulSoup
from random import randint
from unittest import TestCase

class BaseTest(TestCase):
    def __init__(self):
        super(BaseTest, self).__init__()

    def setUp(self):
        pass

    def tearDown(self):
        pass
