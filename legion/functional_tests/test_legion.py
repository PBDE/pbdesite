from portfolio.functional_tests.base import FunctionalTest
from unittest import skip

class LegionTest(FunctionalTest):

    def test_legion_index(self):
        
        self.browser.get(self.live_server_url + "/legion")
        
        self.fail("Implement")

    def test_user_can_roll(self):

        self.fail("Implement")

    def test_user_can_keep_dice(self):

        self.fail("Implement")

    def test_user_can_keep_score(self):

        self.fail("Implement")
