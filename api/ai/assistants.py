import time
from typing import Optional, List

from openai import OpenAI
from openai.types.beta import Assistant, Thread

from api.ai.prompts import PLAYER_PROMPT, ARBITER_PROMPT
from api.models import Player, MafiaRole


class RawAssistant:
    def __init__(self, assistant: Assistant, thread: Thread):
        self.client = OpenAI()
        self.assistant = assistant
        self.thread = thread

    @staticmethod
    def create_with_new_assistant(assistant_name: str, prompt: str,
                                  model: str = "gpt-4-0125-preview") -> 'RawAssistant':
        client = OpenAI()
        assistant = client.beta.assistants.create(
            name=assistant_name,
            instructions=prompt,
            model=model
        )
        print(f"Created assistant {assistant.id}")
        thread = client.beta.threads.create()
        print(f"Created thread {thread.id}")
        return RawAssistant(assistant, thread)

    @staticmethod
    def create_with_existing_assistant(assistant_id: str, new_thread_id: Optional[str] = None,
                                       old_thread_id: Optional[str] = None) -> 'RawAssistant':
        client = OpenAI()
        assistant = client.beta.assistants.retrieve(assistant_id)
        print(f"Retrieved assistant {assistant.name} ({assistant.id})")
        if new_thread_id:
            thread = client.beta.threads.retrieve(new_thread_id)
            print(f"Retrieved thread {thread.id} from assistant {assistant.id}")
            if old_thread_id:
                client.beta.threads.delete(thread_id=old_thread_id)
                print(f"Deleted thread {old_thread_id} from assistant {assistant.id}")
        else:
            thread = client.beta.threads.create()
            print(f"Created thread {thread.id} for assistant {assistant.name} ({assistant.id})")
        return RawAssistant(assistant, thread)

    @staticmethod
    def delete_all_by_name(name: str):
        client = OpenAI()
        all_assistants = client.beta.assistants.list(limit=100)
        for assistant in all_assistants.data:
            if assistant.name == name:
                client.beta.assistants.delete(assistant_id=assistant.id)
                print(f"Deleted assistant {assistant.name} ({assistant.id})")

    def ask(self, user_message: str) -> str:
        self._add_user_message_to_thread(user_message)
        run = self._create_run()

        waiting_limit = 60
        waiting_counter = 0
        while True and waiting_counter < waiting_limit:
            time.sleep(1)
            waiting_counter += 1

            run_status = self._get_run_status(run)
            if run_status.status == 'completed':
                messages = self._get_last_message_from_thread()
                msg = messages.data[0]
                content = msg.content[0].text.value
                print(f"Got reply from {self.assistant.name} (id: {self.assistant.id}):\n{content}\n")
                return content
            else:
                print(f"Waiting for assistant {self.assistant.name} (id: {self.assistant.id}) to process...")
        return f"Something went wrong, got no response for {waiting_limit} seconds."

    def delete(self):
        self.client.beta.assistants.delete(assistant_id=self.assistant.id)
        print(f"{self.assistant.name} action: Deleted {self.assistant.name} (id: {self.assistant.id})")

    def _get_last_message_from_thread(self):
        return self.client.beta.threads.messages.list(thread_id=self.thread.id, limit=1)

    def _get_run_status(self, run):
        run_status = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
        print(f"{self.assistant.name} (id: {self.assistant.id}) action: Running status: {run_status.status}, (run id: {run.id})")
        return run_status

    def _create_run(self):
        run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant.id)
        print(f"{self.assistant.name} (id: {self.assistant.id}) action: Created run {run.id}")
        return run

    def _add_user_message_to_thread(self, user_message):
        print(f"{self.assistant.name} (id: {self.assistant.id}) action: Adding user message to thread {self.thread.id}:\n{user_message}")
        self.client.beta.threads.messages.create(role="user", thread_id=self.thread.id, content=user_message)


class ArbiterAssistantDecorator(RawAssistant):
    def __init__(self, assistant: Assistant, thread: Thread):
        super().__init__(assistant, thread)

    @staticmethod
    def create_arbiter(players: List[Player], game_story: str) -> "ArbiterAssistantDecorator":
        formatted_prompt = ArbiterAssistantDecorator._prepare_prompt(players, game_story)
        instance = RawAssistant.create_with_new_assistant(assistant_name='Arbiter', prompt=formatted_prompt)
        return ArbiterAssistantDecorator(instance.assistant, instance.thread)

    @staticmethod
    def load_arbiter_by_assistant(assistant_id: str) -> "ArbiterAssistantDecorator":
        raw_assistant = RawAssistant.create_with_existing_assistant(assistant_id=assistant_id)
        return ArbiterAssistantDecorator(raw_assistant.assistant, raw_assistant.thread)

    @staticmethod
    def load_arbiter_by_assistant_id_and_thread_id(assistant_id: str, thread_id: str) -> "ArbiterAssistantDecorator":
        instance = RawAssistant.create_with_existing_assistant(assistant_id=assistant_id, new_thread_id=thread_id)
        return ArbiterAssistantDecorator(instance.assistant, instance.thread)

    @staticmethod
    def _prepare_prompt(players: List[Player], game_story: str) -> str:
        players_names_with_roles_and_stories = ""
        for player in players:
            player_info = f"Name: {player.name}\nRole: {player.role}\nStory: {player.backstory}\n\n"
            players_names_with_roles_and_stories += player_info
        players_names_with_roles_and_stories = players_names_with_roles_and_stories.strip()

        return ARBITER_PROMPT.format(
            game_story=game_story,
            players_names_with_roles_and_stories=players_names_with_roles_and_stories
        )


class PlayerAssistantDecorator(RawAssistant):
    def __init__(self, assistant: Assistant, thread: Thread):
        super().__init__(assistant, thread)

    @classmethod
    def create_player(cls, player: Player, game_story: str,
                      players_names_and_stories: str, reply_language_instruction: str) -> "PlayerAssistantDecorator":
        formatted_prompt = cls._prepare_prompt(player, game_story, players_names_and_stories, reply_language_instruction)
        # todo: add the human player name to the names list, right now bot-player doesn't know about the human player at all
        raw_assistant = cls.create_with_new_assistant(
            assistant_name=f"Player {player.name}", prompt=formatted_prompt
        )
        return cls(raw_assistant.assistant, raw_assistant.thread)

    @classmethod
    def load_player_by_assistant_id_with_new_thread(
            cls, assistant_id: str, old_thread_id: Optional[str] = None) -> "PlayerAssistantDecorator":
        raw_assistant = cls.create_with_existing_assistant(assistant_id=assistant_id, old_thread_id=old_thread_id)
        return cls(raw_assistant.assistant, raw_assistant.thread)

    @classmethod
    def load_player_by_assistant_id_and_thread_id(cls, assistant_id: str, thread_id: str) -> "PlayerAssistantDecorator":
        raw_assistant = cls.create_with_existing_assistant(assistant_id=assistant_id, new_thread_id=thread_id)
        return cls(raw_assistant.assistant, raw_assistant.thread)

    @staticmethod
    def _prepare_prompt(player: Player, game_story: str, players_names_and_stories: str,
                        reply_language_instruction: str) -> str:
        def get_win_condition(p: Player):
            if p.role == MafiaRole.MAFIA:
                return "You win if the Mafia members are the majority of the remaining players."
            else:
                return "You win if all the Mafia members are eliminated."
        def get_ally_roles(p: Player):
            if p.role == MafiaRole.MAFIA:
                return [MafiaRole.MAFIA]
            else:
                return [MafiaRole.VILLAGER, MafiaRole.DOCTOR, MafiaRole.DETECTIVE, MafiaRole.ESCORT]
        def get_enemy_roles(p: Player):
            if p.role == MafiaRole.MAFIA:
                return [MafiaRole.VILLAGER, MafiaRole.DOCTOR, MafiaRole.DETECTIVE, MafiaRole.ESCORT]
            else:
                return [MafiaRole.MAFIA]

        return PLAYER_PROMPT.format(
            name=player.name,
            role=player.role,
            personal_story=player.backstory,
            role_motivation=player.role_motivation,
            game_story=game_story,
            players_names_and_stories=players_names_and_stories,
            win_condition=get_win_condition(player),
            ally_roles=get_ally_roles(player),
            enemy_roles=get_enemy_roles(player),
            reply_language_instruction=reply_language_instruction
        )
