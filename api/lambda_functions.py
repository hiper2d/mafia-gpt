import json
import os
import textwrap
import redis
from typing import List

from dotenv import load_dotenv, find_dotenv

from api.ai.assistants import ArbiterAssistant
from api.models import Player
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
    _connect_to_redis()

    # todo: generate game id, save a new game object with this id to Redis
    players: List[Player] = generate_players()
    for player in players:
        print(player)
        # todo: create an assistant for each player, add it to the game object

    # create Arbiter assistant, add it to the game object
    # save the game object to Redis, return the game id


def talk_to_all(user_message, game_id):
    load_dotenv(find_dotenv())
    # todo: load the game object from Redis

    # todo: load Arbiter by assistant and thread ids, throw an error if not found
    arbiter = ArbiterAssistant(assistant_id='asst_s1xiaYU5DJXaxNrzapQMRvId')  # todo: update it since prompt has changed
    arbiter.ask(user_message)


def _connect_to_redis():
    try:
        r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)
        print("Connected to Redis: ", r.ping())
    except ConnectionError:
        print("Failed to connect to Redis")


if __name__ == '__main__':
    messages = [
        {"user_id": 1, "message": "I want to eat sushi"},
        {"user_id": 2, "message": "Sushi? No, you should each taco"},
        {"user_id": 1, "message": "Taco? No, I want to eat sushi"},
        {"user_id": 3, "message": "I want him hungry. Don't let hem to eat anything!"},
    ]
    messages_str = json.dumps(messages, indent=4)
    talk_to_all(messages_str)