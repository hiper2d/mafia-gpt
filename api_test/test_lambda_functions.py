# test_game.py

import unittest

from api.lambda_functions import init_game, talk_to_all, delete_assistants_from_openai


class TestGameFunctions(unittest.TestCase):
    def test_init_game(self):
        init_game()
        pass

    def test_talk_to_all(self):
        talk_to_all(user_message='', game_id='0a908031-bd88-4194-b995-3b3190c3b3f6')
        pass

    def test_delete(self):
        delete_assistants_from_openai('1ae71e30-6ac3-40e6-b8bf-7e9c6387f8d1')
        pass


if __name__ == '__main__':
    unittest.main()