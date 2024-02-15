# test_game.py
import unittest

from api.lambda_functions import init_game, delete_assistants_from_openai_and_game_from_redis, \
    get_welcome_messages_from_all_players_async, talk_to_all, delete_assistants_from_openai_by_name, get_latest_game, \
    start_elimination_vote_round_one, talk_to_certain_player, ask_player_to_speak_for_themself_after_first_round_voting


class TestGameFunctions(unittest.TestCase):
    def test_init_game_and_welcome(self):
        # game_id = init_game(reply_language_instruction='Reply in russian to me but keep original names (in English).
        # Отвечай на русском, но сохрани оригинальные имена.')
        game_id = init_game()
        get_welcome_messages_from_all_players_async(game_id=game_id)

    def test_talk_to_all(self):
        game_id = get_latest_game().id
        players_to_reply = talk_to_all(
            game_id=game_id,
            user_message=
"""Look. There are 2 mafia players among us. If we hang anybody, \
the change we hit Mafia is much higher that if specifically you wi ll be hang. \
Let's do this. This is logical. How about we hang Jedediah?"""
        )
        for player_name in players_to_reply:
            talk_to_certain_player(game_id=game_id, name=player_name)

    def test_start_elimination_vote_round_one(self):
        game_id = get_latest_game().id
        players_to_eliminate = start_elimination_vote_round_one(user_vote="Jedediah", game_id=game_id)
        for player_name in players_to_eliminate:
            ask_player_to_speak_for_themself_after_first_round_voting(game_id=game_id, name=player_name)

    def test_delete_assistants_and_game(self):
        game_id = get_latest_game().id
        delete_assistants_from_openai_and_game_from_redis(game_id=game_id)

    def test_all_delete(self):
        name = 'Math Tutor'
        delete_assistants_from_openai_by_name(name)


if __name__ == '__main__':
    unittest.main()