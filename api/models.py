from enum import Enum

from pydantic import BaseModel


class MafiaRole(Enum):
    MAFIA = 'Mafia'  # A regular Mafia member
    DOCTOR = 'Doctor'  # Has the ability to protect players from being eliminated
    DETECTIVE = 'Detective'  # Can investigate players to determine their alignment
    ESCORT = 'Escort'  # Can block a player from performing their role's action
    VILLAGER = 'Villager'  # A regular townsperson without a special role

    def __repr__(self):
        return self.value


class Player(BaseModel):
    name: str
    role: MafiaRole
    backstory: str
    role_motivation: str
    is_alive: bool = True

    def __repr__(self):
        return (f"Player(name={self.name!r}, role={self.role.value!r}, "
                f"backstory={self.backstory!r}, role_motivation={self.role_motivation!r}, "
                f"is_alive={self.is_alive!r})")

