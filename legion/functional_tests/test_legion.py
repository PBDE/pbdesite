from home_page.functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By
from unittest import skip

from constants import *

class LegionTest(FunctionalTest):

    def test_legion_index(self):
        
        self.browser.get(self.live_server_url + "/legion")

        # the user sees the title
        self.assertIn(BROWSER_TITLE_TEXT, self.browser.title)

        # the user sees the header text
        header_text = self.browser.find_element(By.CLASS_NAME, CLS_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT.lower(), header_text.lower())

    @skip
    def test_select_solo(self):

        # check the game ui becomes visible
        # check the game select buttons are no longer visible

        self.fail("Implement")

    @skip
    def test_select_pass_and_play(self):

        # check the game ui becomes visible
        # check the game select buttons are no longer visible

        self.fail("Implement")

    @skip
    def test_select_verses_ai(self):

        # check the game ui becomes visible
        # check the game select buttons are no longer visible

        self.fail("Implement")

    @skip
    def test_user_can_roll(self):

        self.fail("Implement")

    @skip
    def test_user_can_keep_dice(self):

        self.fail("Implement")

    @skip
    def test_user_can_end_turn(self):

        self.fail("Implement")
