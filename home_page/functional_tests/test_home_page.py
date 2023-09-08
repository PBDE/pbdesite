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
        header_text = self.browser.find_element(By.ID, ID_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT, header_text)

    def test_user_can_register(self):

        # on the home page, the user clicks the option to register
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.LINK_TEXT, REGISTER_LINK_TEXT).click()

        # the registration page loads
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_REGISTER_BTN))

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

    def test_user_can_login(self):

        username, _, _ = self.login_temporary_user()

        # the user sees the greeting
        greeting_text = self.browser.find_element(By.ID, ID_USER_GREETING_TEXT).text
        self.assertIn(USER_GREETING_TEXT + username, greeting_text)

    def test_user_can_logout(self):

        self.login_temporary_user()

        # on their account page, the user clicks the option to logout
        self.browser.find_element(By.LINK_TEXT, LOGOUT_LINK_TEXT).click()
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_HEADER_TEXT))

        # the user is redirected to the home page
        header_text = self.browser.find_element(By.ID, ID_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT, header_text)

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
        pass

    @skip
    def test_only_valid_login_details(self):
        pass