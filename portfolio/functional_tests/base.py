from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from time import time, sleep

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn):

        MAX_WAIT = 10
        start_time = time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as errors:
                if time() - start_time > MAX_WAIT:
                    raise errors
                sleep(0.5)
