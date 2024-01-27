import os
from typing import Optional

from redis import Redis

from api.models import Game


def connect_to_redis() -> Redis:
    try:
        r = Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)
        print("Connected to Redis: ", r.ping())
        return r
    except ConnectionError:
        print("Failed to connect to Redis")


def save_game_to_redis(r: Redis, game: Game):
    game_json = game.model_dump_json()
    r.set(game.id, game_json)


def load_game_from_redis(r: Redis, game_id: str) -> Game:
    game_json = r.get(game_id)
    if game_json:
        return Game.model_validate_json(game_json.decode('utf-8'))
    else:
        return None
