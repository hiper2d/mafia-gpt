from typing import List


class Player:
    def __init__(self, name: str, role: str, backstory: str):
        self.name = name
        self.role = role
        self.backstory = backstory


class Mafia:
    def __init__(self, players: List[Player]):
        self.game_name = 'Mafia'
        self.game_rules = ''
        self.players_names = [player.name for player in players]