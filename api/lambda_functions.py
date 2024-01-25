import json
import textwrap
from typing import List

from dotenv import load_dotenv, find_dotenv

from api.ai.assistants import ArbiterAssistant
from api.models import Player
from api.player_generator import generate_players


def init_game():
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

    # todo: generate game id and store it in Redis, make the game id the init_game argument, so the current game can be locaded
    players: List[Player] = generate_players()
    for player in players:
        print(player)
        # todo: create an assistant for each player and store it in Redis

    # todo:
    # There should be a general welcome message with the game scene description
    # Each player should generate a welcome message: introduce themselves and tell their stories
    # Then it's time for a user to input something and start the conversation


def talk_to_all(user_message):
    arbiter = ArbiterAssistant(assistant_id='asst_s1xiaYU5DJXaxNrzapQMRvId')  # todo: update it since prompt has changed
    arbiter.ask(user_message)


if __name__ == '__main__':
    load_dotenv(find_dotenv())

    messages = [
        {"user_id": 1, "message": "I want to eat sushi"},
        {"user_id": 2, "message": "Sushi? No, you should each taco"},
        {"user_id": 1, "message": "Taco? No, I want to eat sushi"},
        {"user_id": 3, "message": "I want him hungry. Don't let hem to eat anything!"},
    ]
    messages_str = json.dumps(messages, indent=4)
    talk_to_all(messages_str)