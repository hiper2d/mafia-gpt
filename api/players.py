from langchain.schema import SystemMessage

from api.prompts import AI_PLAYER_SYS_PROMPT


class Player:
    def __init__(self, name: str, number_of_players: int):
        self.name = name
        self.system_message = SystemMessage(
            content=AI_PLAYER_SYS_PROMPT.format(name=name, number_of_players=number_of_players)
        )
