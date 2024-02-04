import os
import time
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
    timestamp = time.time()

    # Add to sorted set and check if added successfully
    added_to_zset = r.zadd('games', {game.id: timestamp})
    if added_to_zset:
        print(f"Game ID {game.id} added to sorted set with timestamp {timestamp}")
    else:
        print(f"Failed to add Game ID {game.id} to sorted set")

    # Set the value and check response
    set_response = r.set(game.id, game_json)
    if set_response:
        print(f"Game data for ID {game.id} saved successfully to string")
    else:
        print(f"Failed to save game data for ID {game.id}")


def load_game_from_redis(r: Redis, game_id: str) -> Optional[Game]:
    game_json = r.get(game_id)
    if game_json:
        return Game.model_validate_json(game_json.decode('utf-8'))
    else:
        print(f"Game with id {game_id} not found in Redis")
        return None
