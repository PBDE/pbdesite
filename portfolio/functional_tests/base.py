from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from time import time, sleep
from enum import Enum, auto
from string import ascii_letters, digits, punctuation
from random import randint

from home_page.functional_tests.constants import ID_USERNAME_INPUT, ID_PASSWORD_INPUT, ID_LOGIN_BTN, CLS_SUB_PAGE_HEADER_TEXT

class FunctionalTest(StaticLiveServerTestCase):

    class UserDetails(Enum):
        USERNAME = auto()
        PASSWORD = auto()
        EMAIL = auto()

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

    def random_user_details(self, input_field_type):

        match input_field_type:
            case self.UserDetails.USERNAME:
                characters = ascii_letters + digits + "@.+-_"
            case self.UserDetails.PASSWORD:
                characters = ascii_letters + digits + punctuation
            case self.UserDetails.EMAIL:
                characters = ascii_letters + digits + "._"

        user_detail = ""
        for _ in range(randint(10, 20)):
            user_detail += characters[randint(0, len(characters)-1)]

        if input_field_type == self.UserDetails.EMAIL:
            # if there is a . or _ in the first position, remove it
            if user_detail[0] in [".", "_"]:
                user_detail = user_detail[1:]
            if user_detail[-1] in [".", "_"]:
                user_detail = user_detail[0:-1]
            user_detail += "@example.com"

        return user_detail
    
    def create_temporary_user(self):
                
        username = self.random_user_details(self.UserDetails.USERNAME)
        email = self.random_user_details(self.UserDetails.EMAIL)
        password = self.random_user_details(self.UserDetails.PASSWORD)
        get_user_model().objects.create_user(username, email, password)

        return username, email, password
    
    def login_temporary_user(self):

        username, email, password = self.create_temporary_user()

        # the user goes to the login page
        self.browser.get(self.live_server_url + "/login")

        # the user enters their username and password and clicks login
        self.browser.find_element(By.ID, ID_USERNAME_INPUT).send_keys(username)
        self.browser.find_element(By.ID, ID_PASSWORD_INPUT).send_keys(password)
        self.browser.find_element(By.ID, ID_LOGIN_BTN).click()

        # the registered user is redirected to their user page
        self.wait_for(lambda: self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT))

        return username, email, password
 