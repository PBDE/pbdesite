from home_page.functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By
from unittest import skip

from .constants import *

class LegionTest(FunctionalTest):

    def test_legion_index(self):
        
        self.browser.get(self.live_server_url + "/legion")

        # the user sees the title
        self.assertIn(BROWSER_TITLE_TEXT, self.browser.title)

        # the user sees the header text
        header_text = self.browser.find_element(By.CLASS_NAME, CLS_HEADER_TEXT).text
        self.assertIn(HEADER_TEXT.lower(), header_text.lower())

        # confirm roll and end turn buttons are hidden
        turn_btns_container_class = self.browser.find_element(By.ID, ID_TURN_BTN_CONTAINER).get_attribute("class")
        self.assertIn("hidden", turn_btns_container_class)

        # confirm mode buttons are not hidden
        mode_btns_container_class = self.browser.find_element(By.ID, ID_MODE_BTN_CONTAINER).get_attribute("class")
        self.assertNotIn("hidden", mode_btns_container_class)

    def test_select_solo(self):

        self.browser.get(self.live_server_url + "/legion")

        # press the solo button
        self.browser.find_element(By.ID, ID_SOLO_BTN).click()

        # confirm roll and end turn buttons are no longer hidden
        turn_btns_container_class = self.browser.find_element(By.ID, ID_TURN_BTN_CONTAINER).get_attribute("class")
        self.assertNotIn("hidden", turn_btns_container_class)

        # confirm mode buttons are now hidden
        mode_btns_container_class = self.browser.find_element(By.ID, ID_MODE_BTN_CONTAINER).get_attribute("class")
        self.assertIn("hidden", mode_btns_container_class)

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

    def test_user_roll(self):

        self.browser.get(self.live_server_url + "/legion")

        # press the solo button
        self.browser.find_element(By.ID, ID_SOLO_BTN).click()

        # click roll button
        self.browser.find_element(By.ID, ID_ROLL_BTN).click()
        roll_score = self.browser.find_element(By.ID, ID_ROLL_SCORE).text
        roll_message = self.browser.find_element(By.CLASS_NAME, CLS_ROLL_MESSAGE).text

        # check the score increases or a no score message is displayed
        self.assertTrue((roll_message != "" and int(roll_score) > 0 and "no score" not in roll_message.lower()) or (int(roll_score) == 0 and "no score" in roll_message.lower()))

        # check that roll button is disabled
        roll_btn_disabled = self.browser.find_element(By.ID, ID_ROLL_BTN).get_property("disabled")
        self.assertTrue(roll_btn_disabled)

    @skip
    def test_user_can_keep_dice(self):

        self.fail("Implement")

    def test_user_can_end_turn(self):

        self.browser.get(self.live_server_url + "/legion")

        # press the solo button
        self.browser.find_element(By.ID, ID_SOLO_BTN).click()

        # check that end turn button is disabled
        end_turn_btn_disabled = self.browser.find_element(By.ID, ID_END_TURN_BTN).get_property("disabled")
        self.assertTrue(end_turn_btn_disabled)

        # click roll button
        self.browser.find_element(By.ID, ID_ROLL_BTN).click()

        # check that end turn button is no longer disabled
        end_turn_btn_disabled = self.browser.find_element(By.ID, ID_END_TURN_BTN).get_property("disabled")
        self.assertFalse(end_turn_btn_disabled)

        total_score_before = int(self.browser.find_element(By.ID, ID_TOTAL_SCORE).text)
        roll_score = int(self.browser.find_element(By.ID, ID_ROLL_SCORE).text)

        # click end turn button
        self.browser.find_element(By.ID, ID_END_TURN_BTN).click()

        # check the total score has been updated
        total_score_after = int(self.browser.find_element(By.ID, ID_TOTAL_SCORE).text)
        self.assertEqual(total_score_after, total_score_before + roll_score)
