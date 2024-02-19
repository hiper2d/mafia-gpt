from enum import Enum

from pydantic import BaseModel


class MafiaRole(Enum):
    MAFIA = 'Mafia'  # A regular Mafia member
    DOCTOR = 'Doctor'  # Has the ability to protect players from being eliminated
    DETECTIVE = 'Detective'  # Can investigate players to determine their alignment
    ESCORT = 'Escort'  # Can block a player from performing their role's action
    VILLAGER = 'Villager'  # A regular townsperson without a special role


role_order_map = {
    MafiaRole.MAFIA: 2,
    MafiaRole.DOCTOR: 4,
    MafiaRole.DETECTIVE: 3,
    MafiaRole.ESCORT: 1,
}


role_motivations = {
    MafiaRole.MAFIA: "Seeks to control the town from the shadows, operating with cunning and secrecy. \
    Their goal is to eliminate non-Mafia players while protecting their own. They must act covertly, executing their \
    plans under the cover of night and misleading others during the day to conceal their true identity.",

    MafiaRole.DOCTOR: "Dedicated to saving lives, the Doctor works to protect those in danger from Mafia attacks. \
    Their main goal is to identify and eliminate the Mafia threat, using their night actions to safeguard potential \
    targets. All non-Mafia players are allies in the quest for peace.",

    MafiaRole.DETECTIVE: "With a keen eye for deceit, the Detective investigates players to uncover their true \
    alignments. Their mission is to use this knowledge to guide the town in rooting out the Mafia menace, employing \
    their night actions to gather crucial intelligence.",

    MafiaRole.ESCORT: "Utilizing their unique skills, the Escort can block players from performing their night actions,\
    potentially thwarting Mafia plans. Their primary objective is to protect the town and help eliminate the Mafia, \
    using their abilities to disrupt enemy strategies.",

    MafiaRole.VILLAGER: "As a regular townsperson, the Villager lacks special actions but plays a critical role in \
    discussions and votes to eliminate the Mafia threat. Vigilance and collaboration with fellow non-Mafia players \
    are their main weapons in the quest for safety and order."
}


class Temperament(Enum):
    CHOLERIC = 'Choleric'
    MELANCHOLIC = 'Melancholic'
    PHLEGMATIC = 'Phlegmatic'
    SANGUINE = 'Sanguine'


class HumanPlayer(BaseModel):
    name: str
    role: MafiaRole


class BotPlayer(BaseModel):
    name: str
    assistant_id: str
    thread_id: str
    role: MafiaRole
    backstory: str
    role_motivation: str
    temperament: str
    is_alive: bool = True
    current_offset: int = -1


class Game(BaseModel):
    id: str
    story: str
    arbiter_assistant_id: str
    arbiter_thread_id: str
    bot_players: dict[str, BotPlayer]
    human_player: HumanPlayer
    current_offset: int = 0
    current_day: int = 1
    user_moves_day_counter: int = 0
    user_moves_total_counter: int = 0
    is_active: bool = True


class ArbiterReply(BaseModel):
    players_to_reply: list[str]


class VotingResponse(BaseModel):
    name: str
    reason: str
