# test_game.py

import unittest

from api.lambda_functions import init_game


class TestGameFunctions(unittest.TestCase):
    def test_init_game(self):
        init_game()
        pass

    def test_talk_to_all(self):
        # Simulate inputs to the talk_to_all function
        # and assert the expected outcomes
        pass


if __name__ == '__main__':
    unittest.main()