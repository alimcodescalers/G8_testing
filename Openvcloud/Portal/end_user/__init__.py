import logging
import os

# Initiate testsuite logger
logger = logging.getLogger('portal_testsuite')
if not os.path.exists('logs/portal_testsuite.log'):
    os.mkdir('logs')
handler = logging.FileHandler('logs/portal_testsuite.log')
formatter = logging.Formatter('%(asctime)s [%(testid)s] [%(levelname)s] %(message)s',
                              '%d-%m-%Y %H:%M:%S %Z')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
