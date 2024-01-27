import json
import os
import textwrap
import uuid

from api.redis.redis_helper import connect_to_redis, save_game_to_redis, load_game_from_redis
from redis import Redis

import redis
from typing import List

from dotenv import load_dotenv, find_dotenv

from api.ai.assistants import ArbiterAssistant
from api.models import Player, Game
from api.player_generator import generate_players


def init_game():
    load_dotenv(find_dotenv())

    # Here we create a game object and store it in Redis
    # To do so we need generate players with names, roles and backstories
    # Then we can initialize assistants for each player and for an arbiter
    # We also need to generate a welcome message and create a message history Redis list

    game_scene = textwrap.dedent(  # to get rid of indentation in each line
        """\
        In the heart of a bustling mid-west saloon, the air filled with the sound of piano tunes and clinking glasses,
        a diverse group of individuals finds shelter from a howling snowstorm. Each person, a stranger to the next,
        carries a story colored by the trials of the Wild West. As the fire crackles in the hearth and the storm rages on, 
        unseen tensions and hidden tales weave a tapestry of intrigue and suspense.
        """
    )
    print("\nGame Scene:")
    print(game_scene)

    arbiter = ArbiterAssistant.create_arbiter_from_assistant_id(assistant_id='asst_s1xiaYU5DJXaxNrzapQMRvId')  # todo: update it since prompt has changed
    players: List[Player] = generate_players()
    for player in players:
        print(player)
        # todo: create an assistant for each player, add it to the game object

    game = Game(
        id=uuid.uuid4(),
        story=game_scene,
        players=players,
        arbiter_assistant_id=arbiter.assistant.id,
        arbiter_thread_id=arbiter.thread.id
    )

    r = connect_to_redis()
    save_game_to_redis(r, game)
    return game.id


def talk_to_all(game_id: str, user_message: str):
    load_dotenv(find_dotenv())
    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)

    arbiter = ArbiterAssistant.create_arbiter_from_assistant_id_and_thread_id(
        assistant_id=game.arbiter_assistant_id, thread_id=game.arbiter_thread_id
    )
    arbiter.ask(user_message)


if __name__ == '__main__':
    messages = [
        {"user_id": 1, "message": "I want to eat sushi"},
        {"user_id": 2, "message": "Sushi? No, you should each taco"},
        {"user_id": 1, "message": "Taco? No, I want to eat sushi"},
        {"user_id": 3, "message": "I want him hungry. Don't let hem to eat anything!"},
    ]
    messages_str = json.dumps(messages, indent=4)
    talk_to_all(messages_str)