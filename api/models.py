from enum import Enum

from pydantic import BaseModel


class MafiaRole(Enum):
    MAFIA = 'Mafia'  # A regular Mafia member
    DOCTOR = 'Doctor'  # Has the ability to protect players from being eliminated
    DETECTIVE = 'Detective'  # Can investigate players to determine their alignment
    ESCORT = 'Escort'  # Can block a player from performing their role's action
    VILLAGER = 'Villager'  # A regular townsperson without a special role


class Temperament(Enum):
    CHOLERIC = 'Choleric'
    MELANCHOLIC = 'Melancholic'
    PHLEGMATIC = 'Phlegmatic'
    SANGUINE = 'Sanguine'


class Player(BaseModel):
    name: str
    assistant_id: str
    thread_id: str
    role: MafiaRole
    backstory: str
    role_motivation: str
    temperament: Temperament
    is_alive: bool = True
    current_offset: int = 1  # 1 message is reserved for the welcome message
    # fixme: init current_offset to 0 and increase on welcome message


class Game(BaseModel):
    id: str
    story: str
    arbiter_assistant_id: str
    arbiter_thread_id: str
    players: dict[str, Player] # todo: rename to bot_players and add human_player
    current_offset: int = 0
    current_day: int = 1
    user_moves_day_counter: int = 0
    user_moves_total_counter: int = 0
    is_active: bool = True


class ArbiterReply(BaseModel):
    players_to_reply: list[str]
