import concurrent.futures
import json
import logging
import logging.handlers
import textwrap
import uuid
from collections import Counter
from typing import Dict

from dotenv import load_dotenv, find_dotenv

from api.ai.assistants import ArbiterAssistantDecorator, PlayerAssistantDecorator, RawAssistant
from api.ai.prompts import GAME_MASTER_VOTING_COMMAND
from api.models import Player, Game, ArbiterReply, VotingResponse
from api.player_generator import generate_players
from api.redis.redis_helper import connect_to_redis, save_game_to_redis, load_game_from_redis, \
    add_message_to_game_history_redis_list, delete_game_history_redis_list, read_messages_from_game_history_redis_list, \
    delete_game_from_redis, read_newest_game_from_redis


def _setup_logger(log_level=logging.DEBUG):
    logger = logging.getLogger('my_application')
    logger.setLevel(log_level)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create file handler which logs even debug messages
    file_handler = logging.handlers.RotatingFileHandler(
        'my_application.log', maxBytes=20*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = _setup_logger(log_level=logging.DEBUG)


def init_game(reply_language_instruction: str = ''):
    load_dotenv(find_dotenv())

    game_scene = textwrap.dedent(
"""In the heart of a bustling mid-west saloon, the air filled with the sound of piano tunes and clinking, \
glasses a diverse group of individuals finds shelter from a howling snowstorm. Each person, a stranger to the \
next, carries a story colored by the trials of the Wild West. As the fire crackles in the hearth and the storm \
rages on, unseen tensions and hidden tales weave a tapestry of intrigue and suspense."""
    )
    # print("\nGame Scene:")
    # print(game_scene)
    # print()
    logger.info("Game Scene: %s\n", game_scene)

    all_players: Dict[str, Player] = generate_players()
    for current_player_id, current_player in all_players.items():
        #print('Create a player:', current_player_id)
        logger.debug("Create a player: %s", current_player.name)

        players_names_and_stories = "\n\n".join(
            f"Name: {player.name}\nStory: {player.backstory}"
            for player_id, player in all_players.items() if player_id != current_player_id
        )

        new_player_assistant = PlayerAssistantDecorator.create_player(
            player=current_player,
            game_story=game_scene,
            players_names_and_stories=players_names_and_stories,
            reply_language_instruction=reply_language_instruction
        )
        current_player.assistant_id = new_player_assistant.assistant.id
        current_player.thread_id = new_player_assistant.thread.id

    new_arbiter = ArbiterAssistantDecorator.create_arbiter(players=list(all_players.values()), game_story=game_scene)

    game = Game(
        id=str(uuid.uuid4()),
        story=game_scene,
        players=all_players,
        arbiter_assistant_id=new_arbiter.assistant.id,
        arbiter_thread_id=new_arbiter.thread.id
    )

    r = connect_to_redis()
    save_game_to_redis(r, game)
    return game.id


# Sequential execution is super slow
# todo: change the welcoming logic:
# randomly pick the order in which players will introduce themselves
# ask players to introduce themselves in the order, and make them hear what other players said before them
def get_welcome_messages_from_all_players(game_id: str):
    logger.info('Players introduction:')
    load_dotenv(find_dotenv())

    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)
    if not game or not game.players:
        logger.debug(f"Game with id {game_id} not found in Redis")
        return

    all_introductions = []
    for player in game.players.values():
        player_assistant = PlayerAssistantDecorator.load_player_by_assistant_id_with_new_thread(
            assistant_id=player.assistant_id, old_thread_id=player.thread_id
        )
        answer = player_assistant.ask("Please introduce yourself to the other players.")
        all_introductions.append(f"{player.name}: {answer}")

    add_message_to_game_history_redis_list(r, game_id, all_introductions)
    logger.info("*** Day 1 begins! ***")
    return all_introductions


# This function for local testing only. When deployed to AWS Lambda, it should call other lambdas for each player
# rather than using threads
def get_welcome_messages_from_all_players_async(game_id: str):
    logger.info('Players introduction:')
    load_dotenv(find_dotenv())

    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)
    if not game or not game.players:
        logger.debug(f"Game with id {game_id} not found in Redis")
        return

    def get_player_introduction(player):
        player_assistant = PlayerAssistantDecorator.load_player_by_assistant_id_with_new_thread(
            assistant_id=player.assistant_id, old_thread_id=player.thread_id
        )
        answer = player_assistant.ask("Please introduce yourself to the other players.")
        return f"{player.name}: {answer}"

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_player_introduction, player) for player in game.players.values()]
        all_introductions = [future.result() for future in concurrent.futures.as_completed(futures)]

    add_message_to_game_history_redis_list(r, game_id, all_introductions)
    logger.info("*** Day 1 begins! ***")
    return all_introductions


def talk_to_all(game_id: str, user_message: str):
    load_dotenv(find_dotenv())
    logger.info('User: %s', user_message)

    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)

    arbiter = ArbiterAssistantDecorator.load_arbiter_by_assistant_id_and_thread_id(
        assistant_id=game.arbiter_assistant_id, thread_id=game.arbiter_thread_id
    )
    add_message_to_game_history_redis_list(r, game_id, ['User: ' + user_message])  # todo: human player name should be pulled from the game object

    new_messages, new_offset = read_messages_from_game_history_redis_list(r, game_id, game.current_offset + 1)
    new_messages_concatenated = '\n'.join(new_messages)
    arbiter_reply = arbiter.ask(new_messages_concatenated)
    game.current_offset = new_offset
    game.user_moves_total_counter += 1
    game.user_moves_day_counter += 1
    arbiter_reply_json = json.loads(arbiter_reply)
    reply_obj: ArbiterReply = ArbiterReply(players_to_reply=arbiter_reply_json['players_to_reply'])
    return reply_obj.players_to_reply


def talk_to_certain_player(game_id: str, name: str):
    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)
    if name not in game.players:
        return None
    player = game.players[name]

    new_messaged_for_player, new_offset = read_messages_from_game_history_redis_list(r, game_id, player.current_offset + 1)
    new_messaged_for_player_concatenated = '\n'.join(new_messaged_for_player)
    message = f"Reply to these few messages from other players:\n{new_messaged_for_player_concatenated}"
    player_assistant = PlayerAssistantDecorator.load_player_by_assistant_id_and_thread_id(
        assistant_id=player.assistant_id, thread_id=player.thread_id
    )
    player_reply = player_assistant.ask(message)
    player_reply_message = f"{player.name}: {player_reply}"
    add_message_to_game_history_redis_list(r, game_id, [player_reply_message])
    player.current_offset = new_offset
    save_game_to_redis(r, game)
    return player_reply


def start_elimination_vote_round_one(game_id: str, user_vote: str):
    logger.info("*** Time to vote! ***")
    load_dotenv(find_dotenv())
    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)

    names = Counter([user_vote])
    for player in game.players.values():
        new_messaged_for_player, new_offset = read_messages_from_game_history_redis_list(r, game_id, player.current_offset + 1)
        new_messaged_for_player_concatenated = '\n'.join(new_messaged_for_player)
        voting_instruction = GAME_MASTER_VOTING_COMMAND.format( # todo: include the player
            latest_messages=new_messaged_for_player_concatenated
        )
        player_assistant = PlayerAssistantDecorator.load_player_by_assistant_id_with_new_thread(
            assistant_id=player.assistant_id, old_thread_id=player.thread_id
        )
        answer = player_assistant.ask(voting_instruction)
        voting_response_json = json.loads(answer)
        voting_result = VotingResponse(name=voting_response_json['player_to_eliminate'], reason=voting_response_json['reason'])
        names[voting_result.name] += 1
        # todo: increase offsets for all players and save the game state

    leaders = names.most_common(3)
    candidate_1, votes_for_candidate_1 = leaders[0]
    candidate_2, votes_for_candidate_2 = leaders[1]
    candidate_3, votes_for_candidate_3 = leaders[2]
    logger.info(f"Vote results (round one): {candidate_1} - {votes_for_candidate_1}, "
                f"{candidate_2} - {votes_for_candidate_2}, {candidate_3} - {votes_for_candidate_3}")
    if votes_for_candidate_1 == votes_for_candidate_2 or votes_for_candidate_2 == votes_for_candidate_3:
        return [candidate_1, candidate_2, candidate_3]
    else:
        return [candidate_1, candidate_2]


def ask_player_to_speak_for_themself_after_first_round_voting(game_id: str, name: str):
    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)
    if name not in game.players:
        return None
    player = game.players[name]

    new_messaged_for_player, new_offset = read_messages_from_game_history_redis_list(r, game_id, player.current_offset + 1)
    new_messaged_for_player_concatenated = '\n'.join(new_messaged_for_player)
    message = (f"Player have chosen you as a candidate for elimination. Protect yourself. Explain why you should not be "
               f"eliminated. Below are the latest messages:\n{new_messaged_for_player_concatenated}")
    player_assistant = PlayerAssistantDecorator.load_player_by_assistant_id_and_thread_id(
        assistant_id=player.assistant_id, thread_id=player.thread_id
    )
    player_reply = player_assistant.ask(message)
    player_reply_message = f"{player.name}: {player_reply}"
    add_message_to_game_history_redis_list(r, game_id, [player_reply_message])
    player.current_offset = new_offset
    save_game_to_redis(r, game)
    return player_reply


def delete_assistants_from_openai_and_game_from_redis(game_id: str):
    load_dotenv(find_dotenv())
    r = connect_to_redis()
    game: Game = load_game_from_redis(r, game_id)


    arbiter = ArbiterAssistantDecorator.load_arbiter_by_assistant_id_and_thread_id(
        assistant_id=game.arbiter_assistant_id, thread_id=game.arbiter_thread_id
    )
    arbiter.delete()
    for player in game.players.values():
        if player.assistant_id:
            player_assistant = PlayerAssistantDecorator.load_player_by_assistant_id_and_thread_id(
                assistant_id=player.assistant_id, thread_id=player.thread_id
            )
            player_assistant.delete()
            player.assistant_id = ''
            player.thread_id = ''

    delete_game_history_redis_list(r, game_id)
    delete_game_from_redis(r, game)


def delete_assistants_from_openai_by_name(name: str):
    load_dotenv(find_dotenv())
    RawAssistant.delete_all_by_name(name=name)

def get_latest_game():
    load_dotenv(find_dotenv())
    r = connect_to_redis()
    return read_newest_game_from_redis(r)

