# test_game.py

import unittest

from api.lambda_functions import init_game, delete_assistants_from_openai, \
    get_welcome_messages_from_all_players_async, talk_to_all, delete_assistants_from_openai_by_name

CURRENT_GAME_ID = '02eea83f-f531-482a-80ad-d0014a4a41c4'


class TestGameFunctions(unittest.TestCase):
    def test_init_game(self):
        init_game()

    def test_get_welcome_messages_from_all_players(self):
        get_welcome_messages_from_all_players_async(game_id=CURRENT_GAME_ID)

    def test_talk_to_all(self):
        res = talk_to_all(user_message="I heard there is a mafia among us. Should I be worried?", game_id=CURRENT_GAME_ID)
        print(res)

    def test_delete(self):
        delete_assistants_from_openai(CURRENT_GAME_ID)

    def test_all_delete(self):
        name = 'Math Tutor'
        delete_assistants_from_openai_by_name(name)


if __name__ == '__main__':
    unittest.main()