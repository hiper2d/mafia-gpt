import json
import logging
import random
from typing import List, Dict, Tuple
from openai import OpenAI

from api.ai.text_generator_prompts import GAME_GENERATION_PROMPT
from api.models import BotPlayer, MafiaRole, role_motivations, HumanPlayer

logger = logging.getLogger('my_application')


def generate_scene_and_players(num_players, mafia_count: int, additional_roles: List[MafiaRole],
                               human_player_name: str, theme: str = 'Western') -> Tuple[str, MafiaRole, Dict[str, BotPlayer]]:
    logger.debug(f"Generating {num_players} players for a new game. Theme: {theme}.")
    roles: List[MafiaRole] = _generate_mafia_roles(num_players, mafia_count, additional_roles)
    human_player_role = _pick_and_remove_role(roles)

    instruction = GAME_GENERATION_PROMPT.format(theme=theme, num_players=num_players-1,
                                                human_player_name=human_player_name)
    response = _generate_game_and_players(instruction)
    logger.debug(f"Received response from OpenAI: {response}")

    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Failed to decode JSON from OpenAI response.")

    game_scene = response_json.get('game_scene')
    players_data = response_json.get('players')
    bot_players: Dict[str, BotPlayer] = {}
    for i, player_data in enumerate(players_data):
        name = player_data.get('name')
        backstory = player_data.get('backstory')
        temperament = player_data.get('temperament')

        bot_player = BotPlayer(
            name=name,
            role=roles[i],
            backstory=backstory,
            role_motivation=role_motivations[roles[i]],
            temperament=temperament,
            is_alive=True,
            assistant_id='',
            thread_id=''
        )
        bot_players[name] = bot_player

    return game_scene, human_player_role, bot_players


def _generate_mafia_roles(total_players: int, num_mafia: int, additional_roles: List[MafiaRole]) -> List[MafiaRole]:
    if total_players < num_mafia + len(additional_roles):
        raise ValueError("Total players cannot be less than the sum of Mafia players and additional roles.")

    roles = [MafiaRole.MAFIA for _ in range(num_mafia)]
    roles.extend(additional_roles)
    num_villagers = total_players - len(roles)
    roles.extend([MafiaRole.VILLAGER for _ in range(num_villagers)])
    random.shuffle(roles)
    return roles


def generate_human_player(name: str, role: MafiaRole) -> HumanPlayer:
    return HumanPlayer(name=name, role=role, is_alive=True)


def _generate_game_and_players(instruction):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": instruction}
        ]
    )
    return response.choices[0].message.content


def _pick_and_remove_role(roles_list):
    selected_role = random.choice(roles_list)
    roles_list.remove(selected_role)
    return selected_role


if __name__ == '__main__':
    players = generate_scene_and_players(6, 2, [MafiaRole.DOCTOR, MafiaRole.DETECTIVE])
    for player in players.values():
        print(player)
    print(len(players))
    print(players)
    print("Done.")