# test_game.py

import unittest

from api.lambda_functions import init_game, delete_assistants_from_openai, \
    get_welcome_messages_from_all_players_async, talk_to_all


CURRENT_GAME_ID = '02eea83f-f531-482a-80ad-d0014a4a41c4'


class TestGameFunctions(unittest.TestCase):
    def test_init_game(self):
        init_game()
        pass

    def test_get_welcome_messages_from_all_players(self):
        get_welcome_messages_from_all_players_async(game_id=CURRENT_GAME_ID)
        pass

    def test_talk_to_all(self):
        talk_to_all(user_message="Hi folks, my name is Bob. I'm just a traveler.", game_id=CURRENT_GAME_ID)
        pass

    def test_delete(self):
        delete_assistants_from_openai(CURRENT_GAME_ID)
        pass


if __name__ == '__main__':
    unittest.main()