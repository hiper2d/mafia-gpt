from abc import abstractmethod, ABC
from typing import List

from api.ai.assistant_prompts import GAME_MASTER_NIGHT_MAFIA_COMMAND, GAME_MASTER_NIGHT_DETECTIVE_COMMAND, \
    GAME_MASTER_NIGHT_DOCTOR_COMMAND
from api.models import MafiaRole


class RoleDto(ABC):
    role: MafiaRole
    order: int
    # response_for_bot_player: str = None
    game_message_to_everybody: str = None
    eliminated_bot_player_name: str = None
    elimination_story: str = None

    @abstractmethod
    def get_command(self) -> str:
        pass

    @abstractmethod
    def process_response(self, response_str: str) -> str:
        pass


class DoctorDto(RoleDto):
    def process_response(self, response_str: str) -> str:
        response_json = {
            "player_to_save": "John",
            "reason": "I believe this player is not a mafia. I believe Mafia might try to eliminate the player tonight"
        }
        # todo: create this json from response_str
        # log the response with DEBUG

        self.game_message_to_everybody = f"Doctor saved {response_json['player_to_save']}"

        # todo: hmm... it is bit more complicated than I expected
        # I need to collect role results as a role to name mapping
        # Based on this mapping I need to generate a message for everybody based on what happened
        # I should also know who has been eliminated and update assistant instructions
        return self.game_message_to_everybody

    def get_command(self) -> str:
        return GAME_MASTER_NIGHT_DOCTOR_COMMAND  # ask to return a name and a reason (for debugging)


class MafiaDto(RoleDto):
    def get_command(self) -> str:
        return GAME_MASTER_NIGHT_MAFIA_COMMAND  # ask to return a name


class DetectiveDto(RoleDto):

    def get_command(self) -> str:
        return GAME_MASTER_NIGHT_DETECTIVE_COMMAND  # ask to return a name


ROLE_DICTIONARY: List[MafiaDto] = [
    DoctorDto(role=MafiaRole.DOCTOR, order=1),
    MafiaDto(role=MafiaRole.MAFIA, order=2),
    DetectiveDto(role=MafiaRole.DETECTIVE, order=3)
]