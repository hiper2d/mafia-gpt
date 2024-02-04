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
        delete_assistants_from_openai('02eea83f-f531-482a-80ad-d0014a4a41c4')  # game_id
        pass


if __name__ == '__main__':
    unittest.main()