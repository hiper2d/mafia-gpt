import random
from api.models import MafiaRole, Player

backstories = [
    "Hailing from a distant town, this individual came to the saloon seeking refuge and perhaps a new start, leaving a mysterious past behind.",
    "Once a renowned gambler, this character now lays low, their sharp eyes observing more than they let on.",
    "A charismatic storyteller, this person is always ready with a tale or two, but their true intentions remain hidden beneath their charming facade.",
    "This rugged traveler, carrying tales of distant lands, seems to be running from something—or someone.",
    "A local artisan, known for their exquisite craftsmanship, has many connections but reveals little about their own life."
]

role_motivations = {
    MafiaRole.MAFIA: "Seeks to control the town from the shadows, using cunning and influence to sway others.",
    MafiaRole.DOCTOR: "Dedicated to saving lives, often found pondering the best way to protect those in danger.",
    MafiaRole.VILLAGER: "Aims to maintain peace and order, always vigilant for signs of trouble in their beloved town."
}

names = ["Clint", "Eleanor", "Jedediah", "Rose", "Silas", "Mabel", "Wesley", "Harriet", "Emmett", "Lottie"]


def generate_player_backstory():
    return random.choice(backstories)


def generate_role_motivation(role):
    return role_motivations[role]


def generate_western_name():
    return random.choice(names)


def generate_players():
    player_roles = [MafiaRole.MAFIA, MafiaRole.DOCTOR, MafiaRole.VILLAGER, MafiaRole.VILLAGER, MafiaRole.VILLAGER]
    players = []

    for role in player_roles:
        player = Player(
            name=generate_western_name(),
            role=role,
            backstory=generate_player_backstory(),
            role_motivation=generate_role_motivation(role),
            is_alive=True
        )
        players.append(player)
    return players
