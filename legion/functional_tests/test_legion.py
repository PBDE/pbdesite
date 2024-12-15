from portfolio.functional_tests.base import FunctionalTest
from unittest import skip

class LegionTest(FunctionalTest):

    def test_legion_index(self):
        
        self.browser.get(self.live_server_url + "/legion")

        # check the user sees the correct information on the legion page
        
        self.fail("Implement")

    def test_select_solo(self):

        # check the game ui becomes visible
        # check the game select buttons are no longer visible

        self.fail("Implement")

    def test_select_pass_and_play(self):

        # check the game ui becomes visible
        # check the game select buttons are no longer visible

        self.fail("Implement")

    def test_select_verses_ai(self):

        # check the game ui becomes visible
        # check the game select buttons are no longer visible

        self.fail("Implement")

    def test_user_can_roll(self):

        self.fail("Implement")

    def test_user_can_keep_dice(self):

        self.fail("Implement")

    def test_user_can_end_turn(self):

        self.fail("Implement")
