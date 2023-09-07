from portfolio.functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By
from django.urls import reverse
from unittest import skip

# page text
BROWSER_TITLE_TEXT = "PBDE"
HEADER_TEXT = "Portfolio"
USER_GREETING_TEXT = "Hi, "

# links
LOGIN_LINK = "<a href='%s'>Login</a>" % reverse("home_page:login")
REGISTER_LINK = "<a href='%s'>Register</a>" % reverse("home_page:register")
HOME_PAGE_LINK = "<a href='%s'>Home</a>" % reverse("home_page:index")

# css ids
ID_HEADER_TEXT = "header-text"
ID_USERNAME_INPUT = "id_username"
ID_PASSWORD_INPUT = "id_password1"
ID_PASSWORD_CONFIRM = "id_password2"
ID_EMAIL_INPUT = "id_email"
ID_REGISTER_BTN = "register-btn"
ID_USER_GREETING_TEXT = "user-greeting"


class HomePageTest(FunctionalTest):

    def test_home_page(self):

        # the user goes to the home page
        self.browser.get(self.live_server_url)

        # the user sees the title
        self.assertIn(BROWSER_TITLE_TEXT, self.browser.title)
        # the user sees the header text
        header_text = self.browser.find_element(By.ID, ID_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT, header_text)

        # the user sees the option to login and to register
        body_html = self.browser.find_element(By.TAG_NAME, "body").get_attribute('innerHTML')
        self.assertInHTML(LOGIN_LINK, body_html)
        self.assertInHTML(REGISTER_LINK, body_html)

    def test_user_can_register(self):

        # on the home page, the user clicks the option to register
        self.browser.get(self.live_server_url)
        register_link = self.browser.find_element(By.LINK_TEXT, REGISTER_LINK)
        register_link.click()

        # the registration page loads
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_REGISTER_BTN))

        # on the register page, the user sees the options to login and to return to the home page
        body_html = self.browser.find_element(By.TAG_NAME, "body").get_attribute('innerHTML')
        self.assertInHTML(LOGIN_LINK, body_html)
        self.assertInHTML(HOME_PAGE_LINK, body_html)

        # the user enters their username, password, password confirmation, and email address
        username = "Username"
        self.browser.find_element(By.ID, ID_USERNAME_INPUT).send_keys(username)
        self.browser.find_element(By.ID, ID_PASSWORD_INPUT).send_keys("NotACommonPassword651489")
        self.browser.find_element(By.ID, ID_PASSWORD_CONFIRM).send_keys("NotACommonPassword651489")
        self.browser.find_element(By.ID, ID_EMAIL_INPUT).send_keys("username@example.com")
        self.browser.find_element(By.ID, ID_REGISTER_BTN).click()

        # the registered user is redirected to their user page
        self.wait_for(lambda: self.browser.find_element(By.ID, ID_USER_GREETING_TEXT))

        # the user sees the greeting
        greeting_text = self.browser.find_element(By.ID, ID_USER_GREETING_TEXT).text
        self.assertIn(USER_GREETING_TEXT + username, greeting_text)

    @skip
    def test_user_can_login(self):
        pass

        # on the home page, the user clicks the option to login

        # on the login page, the user sees the options to register or to return to the home page

        # the user sees enters their username and password and clicks login

        # the user is now successfully logged in

    @skip
    def test_user_can_logout(self):
        pass

    @skip
    def test_user_can_delete_account(self):
        pass

    @skip
    def test_only_valid_registration_details(self):
        pass

    @skip
    def test_only_valid_login_details(self):
        pass