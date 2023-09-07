from portfolio.functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By

BROWSER_TITLE_TEXT = "PBDE"
HEADER_TEXT = "Portfolio"
LANGUAGE_LINK_TEXT = "Language"

# css class names (CN)
CN_HEADER_TEXT = "header-text"

class HomePageTest(FunctionalTest):

    def test_home_page(self):

        # the user goes to the home page
        self.browser.get(self.live_server_url)

        # the user sees the title and the header text
        self.assertIn(BROWSER_TITLE_TEXT, self.browser.title)

        # the user sees the option to login or register
        header_text = self.browser.find_element(By.CLASS_NAME, CN_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT, header_text)

        # # the user sees the list of apps to explore
        # self.assertTrue(self.browser.find_element(By.LINK_TEXT, LANGUAGE_LINK_TEXT), "The 'Language' link has not been found")

    def test_user_can_login(self):
        pass

        # on the home page, the user clicks the option to login

        # on the login page, the user sees the options to register or to return to the home page

        # the user sees enters their username and password and clicks login
            # test incorrect
            # test correct

        # the user is now successfully logged in

    def test_user_can_logout(self):
        pass

    def test_user_can_register(self):
        pass

        # on the home page, the user clicks the option to register

        # on the register page, the user sees the options to login or to return to the home page

        # the user enters their username, password, password confirmation and email address
            # test incorrect
            # test correct

        # the user is now successfully registered