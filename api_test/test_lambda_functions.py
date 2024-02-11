# test_game.py
import unittest

from api.lambda_functions import init_game, delete_assistants_from_openai_and_game_from_redis, \
    get_welcome_messages_from_all_players_async, talk_to_all, delete_assistants_from_openai_by_name, get_latest_game


class TestGameFunctions(unittest.TestCase):
    def test_init_game_and_welcome(self):
        game_id = init_game(reply_language_instruction='Reply in russian to me. Отвечай на русском.')
        get_welcome_messages_from_all_players_async(game_id=game_id)

    def test_talk_to_all(self):
        game_id = get_latest_game().id
        res = talk_to_all(user_message='Ребят, не вмешивайтесь. Это между мной и Клинтом', game_id=game_id)
        print(res)

    def test_delete_assistants_and_game(self):
        game_id = get_latest_game().id
        delete_assistants_from_openai_and_game_from_redis(game_id=game_id)

    def test_all_delete(self):
        name = 'Math Tutor'
        delete_assistants_from_openai_by_name(name)


if __name__ == '__main__':
    unittest.main()