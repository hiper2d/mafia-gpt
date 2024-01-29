import json
import textwrap
import uuid
from typing import List, Tuple

from dotenv import load_dotenv, find_dotenv

from api.ai.assistants import ArbiterAssistant
from api.models import Player, Game, MafiaRole
from api.player_generator import generate_players
from api.redis.redis_helper import connect_to_redis, save_game_to_redis, load_game_from_redis


def init_game():
    load_dotenv(find_dotenv())

    # Here we create a game object and store it in Redis
    # To do so we need generate players with names, roles and backstories
    # Then we can initialize assistants for each player and for an arbiter
    # We also need to generate a welcome message and create a message history Redis list

    game_scene = textwrap.dedent(  # todo: get rid of indentation in each line
        """\
        In the heart of a bustling mid-west saloon, the air filled with the sound of piano tunes and clinking glasses,
        a diverse group of individuals finds shelter from a howling snowstorm. Each person, a stranger to the next,
        carries a story colored by the trials of the Wild West. As the fire crackles in the hearth and the storm rages on, 
        unseen tensions and hidden tales weave a tapestry of intrigue and suspense."""
    )
    print("\nGame Scene:")
    print(game_scene)

    players: List[Player] = generate_players()
    # fixme: temporary disabled for Redis save/load testing
    # player_names = [p.name for p in players]
    # for player in players:
    #     print(player)
    #     new_player_assistant = PlayerAssistant.create_player(
    #         name=player.name, backstory=player.backstory, role=player.role, player_names=player_names
    #     )
    #     player.assistant_id = new_player_assistant.assistant.id
    #     player.thread_id = new_player_assistant.thread.id

    # new_arbiter = ArbiterAssistant.load_arbiter_by_assistant_id_with_new_thread(assistant_id='asst_s1xiaYU5DJXaxNrzapQMRvId')
    new_arbiter = ArbiterAssistant.create_arbiter(players=players, game_story=game_scene)

    game = Game(
        id=str(uuid.uuid4()),
        story=game_scene,
        players=players,
        # fixme: temporary disabled for Redis save/load testing
        #arbiter_assistant_id=new_arbiter.assistant.id,
        #arbiter_thread_id=new_arbiter.thread.id
        arbiter_assistant_id="",
        arbiter_thread_id=""
    )

    r = connect_to_redis()
    save_game_to_redis(r, game)
    return game.id


def talk_to_all(game_id: str, user_message: str):
    load_dotenv(find_dotenv())
    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)

    # fixme: temporary disabled for Redis save/load testing
    # arbiter = ArbiterAssistant.load_arbiter_by_assistant_id_and_thread_id(
    #     assistant_id=game.arbiter_assistant_id, thread_id=game.arbiter_thread_id
    # )
    # arbiter.ask(user_message)


if __name__ == '__main__':
    messages = [
        {"user_id": 1, "message": "I want to eat sushi"},
        {"user_id": 2, "message": "Sushi? No, you should each taco"},
        {"user_id": 1, "message": "Taco? No, I want to eat sushi"},
        {"user_id": 3, "message": "I want him hungry. Don't let hem to eat anything!"},
    ]
    messages_str = json.dumps(messages, indent=4)
    talk_to_all(messages_str)