from portfolio.functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By
from unittest import skip
from django.core import mail
import re

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
        self.wait_for(lambda: self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT))

        # the user sees the greeting
        greeting_text = self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT).text
        self.assertIn((USER_GREETING_TEXT + username).lower(), greeting_text.lower())

    def test_user_can_login(self):

        username, _, _ = self.login_temporary_user()

        # the user sees the greeting
        greeting_text = self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT).text
        self.assertIn(USER_GREETING_TEXT + username, greeting_text)

    def test_user_can_logout(self):

        self.login_temporary_user()

        # on their account page, the user clicks the option to logout
        self.browser.find_element(By.CLASS_NAME, "logout-link").click()
        self.wait_for(lambda: self.browser.find_element(By.CLASS_NAME, ID_HEADER_TEXT))

        # the user is redirected to the home page
        header_text = self.browser.find_element(By.CLASS_NAME, ID_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT.lower(), header_text.lower())

    def test_user_can_delete_account(self):
        
        self.login_temporary_user()

        # on their account page, the user clicks the option to delete their account
        self.browser.find_element(By.CLASS_NAME, "delete-account-link").click()
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_CONFIRMATION_TEXT))

        # the user is asked to confirm the deletion
        confimation_question = self.browser.find_element(By.ID, ID_CONFIRMATION_TEXT).text
        self.assertEqual(confimation_question, CONFIRM_DELETE_ACCOUNT_MSG)

        # the user clicks confirm
        self.browser.find_element(By.CLASS_NAME, ID_CONFIRM_DELETE_BTN).click()
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_DELETED_CONFIRM_TEXT))

        # the user gets confirmation that the account has been deleted
        confirmation_message = self.browser.find_element(By.ID, ID_DELETED_CONFIRM_TEXT).text
        self.assertEqual(confirmation_message, DELETED_ACCOUNT_CONFIRM_MSG)

        # the user sees the option to return to the home page
        html_body = self.browser.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        self.assertInHTML(HOME_PAGE_LINK, html_body)

    def test_user_can_change_password(self):

        _, _, old_password = self.login_temporary_user()

        # on their account page the user clicks the option to change their password
        self.browser.find_element(By.CLASS_NAME, "change-password-link").click()
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_CHANGE_PASSWORD_FORM))

        # the user is asked to enter their old password
        self.browser.find_element(By.ID, ID_OLD_PASSWORD_INPUT).send_keys(old_password)

        # the user is asked to enter their new password twice
        password = self.random_user_details(self.UserDetails.PASSWORD)
        self.browser.find_element(By.ID, ID_NEW_PASSWORD_INPUT).send_keys(password)
        self.browser.find_element(By.ID, ID_CONFIRM_PASSWORD_INPUT).send_keys(password)

        # the user clicks confirm
        self.browser.find_element(By.ID, ID_CHANGE_PASSWORD_BTN).click()

        # the user gets confirmation that the password has been changed
        self.wait_for(lambda: self.browser.find_element(By.ID
        , ID_PASSWORD_CHANGED_CONFIRM_MSG))

        confirmation_text = self.browser.find_element(By.ID, ID_PASSWORD_CHANGED_CONFIRM_MSG).text
        self.assertIn(PASSWORD_CHANGE_CONFIRMATION_MSG.lower(), confirmation_text.lower())

    def test_user_can_request_new_password_link(self):

        username, email, _ = self.create_temporary_user()

        # the user goes to the login page
        self.browser.get(self.live_server_url + "/login")

        # on the login page the user clicks the forgotten password option
        self.browser.find_element(By.CLASS_NAME, "forgotten-password-link").click()

        # the user is then directed to the forgotten password page
        self.wait_for(lambda: self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT))

        forgotten_password_text = self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT).text

        self.assertEqual(forgotten_password_text, FORGOTTEN_PASSWORD_TEXT)

        # the user enters their email address
        self.browser.find_element(By.ID, ID_EMAIL_INPUT).send_keys(email)
        self.browser.find_element(By.ID, ID_REQUEST_PASSWORD_BTN).click()

        # the user then sees a message advising that an email has been sent to their account with instructions
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_PASSWORD_EMAIL_SENT_TEXT))

        # check the dummy email has been created
        reset_email = mail.outbox[0]
        # self.assertIn(email, reset_email)
        url_search = re.search(r'http://.+/.+$', reset_email.body)
        url = url_search.group(0)

        # the user clicks the link and is directed to create new password page
        self.browser.get(url)
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_NEW_PASSWORD_INPUT))

        # the user enters a new password
        new_password = self.random_user_details(self.UserDetails.PASSWORD)
        self.browser.find_element(By.ID, ID_NEW_PASSWORD_INPUT).send_keys(new_password)
        self.browser.find_element(By.ID, ID_CONFIRM_PASSWORD_INPUT).send_keys(new_password)
        self.browser.find_element(By.ID, ID_RESET_PASSWORD_BTN).click()

        # the user gets confirmation that the password has been changed
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_PASSWORD_CHANGED_CONFIRM_MSG))

        confirmation_text = self.browser.find_element(By.ID, ID_PASSWORD_CHANGED_CONFIRM_MSG).text
        self.assertIn(PASSWORD_CHANGE_CONFIRMATION_MSG.lower(), confirmation_text.lower())

        # the user is redirected to the login page
        self.browser.find_element(By.ID, ID_RETURN_TO_LOGIN_LINK).click()

        # the user logs in with the new details
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_USERNAME_INPUT))

        self.browser.find_element(By.ID, ID_USERNAME_INPUT).send_keys(username)
        self.browser.find_element(By.ID, ID_PASSWORD_INPUT).send_keys(new_password)
        self.browser.find_element(By.ID, ID_LOGIN_BTN).click()

        self.wait_for(lambda: self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT))

        greeting_text = self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT).text
        self.assertIn(USER_GREETING_TEXT + username, greeting_text)

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
        error_message = self.browser.find_element(By.CLASS_NAME, CLS_ERROR_TEXT)
        self.assertIn(USER_DETAILS_ERROR_MSG, error_message.text)

    def test_user_can_view_privacy_statement(self):

        # go to the register page
        self.browser.get(self.live_server_url + "/register")

        # click on the privacy page link
        self.browser.find_element(By.CLASS_NAME, CLS_PRIVACY_STATEMENT_LINK).click() # here

        # check for the expected header
        self.wait_for(lambda: self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT))

        privacy_header = self.browser.find_element(By.CLASS_NAME, CLS_SUB_PAGE_HEADER_TEXT).text
        self.assertEqual(privacy_header.lower(), PRIVACY_STATEMENT_TEXT.lower())

    
    @skip
    def test_nav_menu_on_small_screen_size(self):
        # go to the page
        # reduce the window size
        # check for button
        # check nav gone
        # get side menu appears
        self.fail("Implement")
