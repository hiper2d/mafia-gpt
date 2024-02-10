import os
import time
from typing import Optional, List, Tuple

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


def delete_game_from_redis(r: Redis, game: Game):
    deleted = r.delete(game.id)
    if deleted:
        print(f"Game ID {game.id} deleted successfully from Redis")
    else:
        print(f"Failed to delete game ID {game.id} from Redis")

    removed_from_zset = r.zrem('games', game.id)
    if removed_from_zset:
        print(f"Game ID {game.id} removed from sorted set successfully")
    else:
        print(f"Failed to remove game ID {game.id} from sorted set")


def load_game_from_redis(r: Redis, game_id: str) -> Optional[Game]:
    game_json = r.get(game_id)
    if game_json:
        return Game.model_validate_json(game_json.decode('utf-8'))
    else:
        print(f"Game with id {game_id} not found in Redis")
        return None


def add_message_to_game_history_redis_list(r: Redis, game_id: str, messages: List[str]):
    if messages:
        pushed = r.rpush(f"{game_id}:history", *messages)
        if pushed:
            print(f"{len(messages)} messages added to game {game_id}")
        else:
            print("Failed to add messages to game {game_id}")
    else:
        print("No messages to add.")


def delete_game_history_redis_list(r: Redis, game_id: str):
    list_key = f"{game_id}:history"
    result = r.delete(list_key)
    if result:
        print(f"List {list_key} deleted successfully.")
    else:
        print(f"List {list_key} does not exist or could not be deleted.")


def read_messages_from_game_history_redis_list(r: Redis, game_id: str, read_from_line: int) -> Tuple[List[str], int]:
    if not r.exists(f"{game_id}:history"):
        print(f"No list found for game ID {game_id}")
        return [], -1

    messages = r.lrange(f"{game_id}:history", read_from_line, -1)
    decoded_messages = [message.decode('utf-8') for message in messages]

    # Get the total length of the list to find the index of the latest record
    total_length = r.llen(f"{game_id}:history")
    latest_index = total_length - 1  # Subtracting 1 because list indices start at 0
    return decoded_messages, latest_index
