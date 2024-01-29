import time
from typing import Optional, Tuple, List

from openai.types.beta import Assistant, Thread
from openai import OpenAI

from api.ai.prompts import PLAYER_PROMPT, ARBITER_PROMPT
from api.models import MafiaRole, Player


class AbstractAssistant:
    def __init__(self, assistant_name: str, prompt: str, assistant_id: Optional[str] = None,
                 thread_id: Optional[str] = None):
        self.client = OpenAI()
        # fixme: temporary disabled for Redis save/load testing
        # if assistant_id:
        #     self.assistant: Assistant = self.client.beta.assistants.retrieve(assistant_id)
        #     print(f"Retrieved assistant {self.assistant.id}")
        # else:
        #     self.assistant: Assistant = self.client.beta.assistants.create(
        #         name=assistant_name,
        #         instructions=prompt,
        #         model="gpt-4-0125-preview"
        #     )
        #     print(f"Created assistant {self.assistant.id}")
        #
        # if thread_id:
        #     self.thread: Thread = self.client.beta.threads.retrieve(thread_id)
        #     print(f"Retrieved thread {self.thread.id}")
        # else:
        #     self.thread: Thread = self.client.beta.threads.create()
        #     print(f"Created thread {self.thread.id}")

    def ask(self, user_message):
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
                role = msg.role
                content = msg.content[0].text.value
                print(f"Got reply from {role.capitalize()}:")
                print(f"{content}")
                return content
            else:
                print("Waiting for the Assistant to process...")
        return f"Something went wrong, got no response for {waiting_limit} seconds."

    def _get_last_message_from_thread(self):
        return self.client.beta.threads.messages.list(thread_id=self.thread.id, limit=1)

    def _get_run_status(self, run):
        run_status = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
        print(f"Running status: {run_status.status}, (run id: {run.id})")
        return run_status

    def _create_run(self):
        run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant.id)
        print(f"Created run {run.id}")
        return run

    def _add_user_message_to_thread(self, user_message):
        self.client.beta.threads.messages.create(role="user", thread_id=self.thread.id, content=user_message)


class ArbiterAssistant(AbstractAssistant):
    def __init__(self, players: List[Player], game_story: str,
                 assistant_id: Optional[str] = None, thread_id: Optional[str] = None):
        players_names_with_roles_and_stories = ""
        for i, player in enumerate(players):
            player_info = f"Name: {player.name}\nRole: {player.role}\nStory: {player.backstory}"
            if i != len(players)-1:
                player_info += "\n\n"
            players_names_with_roles_and_stories += player_info

        formatted_prompt = ARBITER_PROMPT.format(
            game_story=game_story,
            players_names_with_roles_and_stories=players_names_with_roles_and_stories
        )
        super().__init__(
            assistant_name='Arbiter', assistant_id=assistant_id, thread_id=thread_id, prompt=formatted_prompt
        )

    @staticmethod
    def create_arbiter(players: List[Player], game_story: str) -> "ArbiterAssistant":
        return ArbiterAssistant(players=players, game_story=game_story)

    @staticmethod
    def load_arbiter_by_assistant_id_with_new_thread(
            assistant_id: str, players: List[Player], game_story: str
    ) -> "ArbiterAssistant":
        return ArbiterAssistant(players=players, game_story=game_story, assistant_id=assistant_id)

    @staticmethod
    def load_arbiter_by_assistant_id_and_thread_id(
            players: List[Player], game_story: str, assistant_id: str, thread_id: str
    ) -> "ArbiterAssistant":
        return ArbiterAssistant(
            players=players, game_story=game_story, assistant_id=assistant_id, thread_id=thread_id
        )


class PlayerAssistant(AbstractAssistant):
    def __init__(self, name: Optional[str], role: Optional[MafiaRole], backstory: Optional[str],
                 player_names: List[str], assistant_id: Optional[str] = None, thread_id: Optional[str] = None):
        formatted_prompt = PLAYER_PROMPT.format(
            game_name='', # todo: remove, we focus on Mafia only for now
            name=name,
            role=role,
            game_rules='', # todo: embed into the prompt
            players_names=player_names,
            backstory=backstory
        )
        super().__init__(assistant_name=name, assistant_id=assistant_id, thread_id=thread_id, prompt=formatted_prompt)

    @staticmethod
    def create_player(name: str, backstory: str, role: MafiaRole, player_names: List[str]) -> "PlayerAssistant":
        return PlayerAssistant(name=name, backstory=backstory, role=role, player_names=player_names)

    @staticmethod
    def load_player_by_assistant_id_with_new_thread(
            name: str, backstory: str, role: MafiaRole,player_names: List[str], assistant_id: str
    ) -> "PlayerAssistant":
        return PlayerAssistant(
            name=name, backstory=backstory, role=role, player_names=player_names, assistant_id=assistant_id
        )

    @staticmethod
    def load_player_by_assistant_id_and_thread_id(
            name: str, backstory: str, role: MafiaRole,player_names: List[str], assistant_id: str, thread_id: str
    ) -> "PlayerAssistant":
        return PlayerAssistant(
            name=name, backstory=backstory, role=role, player_names=player_names,
            assistant_id=assistant_id, thread_id=thread_id
        )