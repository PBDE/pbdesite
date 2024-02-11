from portfolio.functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By
from unittest import skip

from .constants import *

class HomePageTest(FunctionalTest):

    def test_home_page(self):

        # the user goes to the home page
        self.browser.get(self.live_server_url)

        # the user sees the title
        self.assertIn(BROWSER_TITLE_TEXT, self.browser.title)

        # the user sees the header text
        header_text = self.browser.find_element(By.CLASS_NAME, CLS_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT.upper(), header_text.upper())

    @skip
    def test_user_can_register(self):

        # the user goes to the register page
        self.browser.get(self.live_server_url + "/register")

        # the user enters their username, password, password confirmation, and email address
        username = self.random_user_details(self.UserDetails.USERNAME)
        password = self.random_user_details(self.UserDetails.PASSWORD)
        email = self.random_user_details(self.UserDetails.EMAIL)
        self.browser.find_element(By.ID, ID_USERNAME_INPUT).send_keys(username)
        self.browser.find_element(By.ID, ID_CREATE_PASSWORD_INPUT).send_keys(password)
        self.browser.find_element(By.ID, ID_PASSWORD_CONFIRM_INPUT).send_keys(password)
        self.browser.find_element(By.ID, ID_EMAIL_INPUT).send_keys(email)
        self.browser.find_element(By.ID, ID_REGISTER_BTN).click()

        # the registered user is redirected to their user page
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_USER_GREETING_TEXT))

        # the user sees the greeting
        greeting_text = self.browser.find_element(By.ID, ID_USER_GREETING_TEXT).text
        self.assertIn(USER_GREETING_TEXT + username, greeting_text)

    @skip
    def test_user_can_login(self):

        username, _, _ = self.login_temporary_user()

        # the user sees the greeting
        greeting_text = self.browser.find_element(By.ID, ID_USER_GREETING_TEXT).text
        self.assertIn(USER_GREETING_TEXT + username, greeting_text)

    @skip
    def test_user_can_logout(self):

        self.login_temporary_user()

        # on their account page, the user clicks the option to logout
        self.browser.find_element(By.LINK_TEXT, LOGOUT_LINK_TEXT).click()
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_HEADER_TEXT))

        # the user is redirected to the home page
        header_text = self.browser.find_element(By.ID, ID_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT, header_text.title())

    @skip
    def test_user_can_delete_account(self):
        
        self.login_temporary_user()

        # on their account page, the user clicks the option to delete their account
        self.browser.find_element(By.LINK_TEXT, DELETE_ACCOUNT_LINK_TEXT).click()
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_CONFIRMATION_TEXT))

        # the user is asked to confirm the deletion
        confimation_question = self.browser.find_element(By.ID, ID_CONFIRMATION_TEXT).text
        self.assertEqual(confimation_question, CONFIRM_DELETE_ACCOUNT_MSG)

        # the user clicks confirm
        self.browser.find_element(By.ID, ID_CONFIRM_DELETE_BTN).click()
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_DELETED_CONFIRM_TEXT))

        # the user gets confirmation that the account has been deleted
        confirmation_message = self.browser.find_element(By.ID, ID_DELETED_CONFIRM_TEXT).text
        self.assertEqual(confirmation_message, DELETED_ACCOUNT_CONFIRM_MSG)

        # the user sees the option to return to the home page
        html_body = self.browser.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        self.assertInHTML(HOME_PAGE_LINK, html_body)

    @skip
    def test_only_valid_registration_details(self):

        # the user goes to the register page
        self.browser.get(self.live_server_url + "/register")

        # the user clicks register without providing any details
        self.browser.find_element(By.ID, ID_REGISTER_BTN).click()

        # the user sees the error message
        username_input = self.browser.find_element(By.ID, ID_USERNAME_INPUT)
        self.assertTrue(username_input.get_attribute("validationMessage"))

        username = self.random_user_details(self.UserDetails.USERNAME)
        password1 = self.random_user_details(self.UserDetails.PASSWORD)
        password2 = self.random_user_details(self.UserDetails.PASSWORD)
        while password1 == password2:
            password2 = self.random_user_details(self.UserDetails.PASSWORD)

        # the user enters passwords that don't match
        email = self.random_user_details(self.UserDetails.EMAIL)
        self.browser.find_element(By.ID, ID_USERNAME_INPUT).send_keys(username)
        self.browser.find_element(By.ID, ID_CREATE_PASSWORD_INPUT).send_keys(password1)
        self.browser.find_element(By.ID, ID_PASSWORD_CONFIRM_INPUT).send_keys(password2)
        self.browser.find_element(By.ID, ID_EMAIL_INPUT).send_keys(email)
        self.browser.find_element(By.ID, ID_REGISTER_BTN).click()

        # wait for the page to load
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_CREATE_USER_FROM))

        # the user sees the error message
        self.assertTrue(self.browser.find_element(By.CLASS_NAME, CLS_ERROR_LIST))

    @skip
    def test_only_valid_login_details(self):

        username, _, password = self.create_temporary_user()
        wrong_username = self.random_user_details(self.UserDetails.USERNAME)
        wrong_password = self.random_user_details(self.UserDetails.PASSWORD)

        while wrong_username == username:
            wrong_username = self.random_user_details(self.UserDetails.USERNAME)

        while wrong_password == password:
            wrong_password = self.random_user_details(self.UserDetails.PASSWORD)
        
        # the user goes to the login page
        self.browser.get(self.live_server_url + "/login")

        # the user tries to login without providing login details
        self.browser.find_element(By.ID, ID_LOGIN_BTN).click()

        # the user sees the error message
        username_input = self.browser.find_element(By.ID, ID_USERNAME_INPUT)
        self.assertTrue(username_input.get_attribute("validationMessage"))

        # the user then enters their details, but incorrectly
        self.browser.find_element(By.ID, ID_USERNAME_INPUT).send_keys(wrong_username)
        self.browser.find_element(By.ID, ID_PASSWORD_INPUT).send_keys(wrong_password)
        self.browser.find_element(By.ID, ID_LOGIN_BTN).click()

        # the page loads
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_LOGIN_FORM))

        # the user sees the error message
        error_message = self.browser.find_element(By.ID, ID_ERROR_TEXT)
        self.assertIn(USER_DETAILS_ERROR_MSG, error_message.text)

    def test_nav_menu_on_small_screen_size(self):
        self.fail("Implement")
