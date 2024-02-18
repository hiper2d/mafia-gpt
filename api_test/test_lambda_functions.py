# test_game.py
import unittest

from api.lambda_functions import init_game, delete_assistants_from_openai_and_game_from_redis, \
    get_welcome_messages_from_all_players_async, talk_to_all, delete_assistants_from_openai_by_name, get_latest_game, \
    start_elimination_vote_round_one, talk_to_certain_player, \
    ask_bot_player_to_speak_for_themself_after_first_round_voting, start_elimination_vote_round_two


class TestGameFunctions(unittest.TestCase):
    def test_init_game_and_welcome(self):
        game_id = init_game(
            human_player_name='Alex',
            reply_language_instruction='Reply in russian to me but keep original names (in English). Отвечай на русском, но сохрани оригинальные имена на английском.'
        )
        get_welcome_messages_from_all_players_async(game_id=game_id)

    def test_talk_to_all(self):
        game_id = get_latest_game().id
        players_to_reply = talk_to_all(
            game_id=game_id,
            user_message=
"""\
Clayton, что думаешь?
"""
        )
        for player_name in players_to_reply:
            talk_to_certain_player(game_id=game_id, name=player_name)

    def test_start_elimination_vote_round_one(self):
        game_id = get_latest_game().id
        players_to_eliminate = start_elimination_vote_round_one(user_vote="Clayton", game_id=game_id)
        for player_name in players_to_eliminate:
            ask_bot_player_to_speak_for_themself_after_first_round_voting(game_id=game_id, name=player_name)

    def test_ask_bot_player_to_speak_for_themself_after_first_round_voting(self):
        game_id = get_latest_game().id
        ask_bot_player_to_speak_for_themself_after_first_round_voting(game_id=game_id, name='Whisper')

    def test_start_elimination_vote_round_two(self):
        game_id = get_latest_game().id
        start_elimination_vote_round_two(user_vote="Whisper", leaders=["Whisper", "Clayton"], game_id=game_id)

    def test_delete_assistants_and_game(self):
        """Cleanup function. Loads the latest Game from Redis, deletes all assistants from OpenAI
        and deletes the Game from Redis."""

        game_id = get_latest_game().id
        delete_assistants_from_openai_and_game_from_redis(game_id=game_id)

    def test_all_delete(self):
        name = 'Math Tutor'
        delete_assistants_from_openai_by_name(name)


if __name__ == '__main__':
    unittest.main()