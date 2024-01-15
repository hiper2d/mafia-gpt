import time
from prompts import ARBITER_PROMPT, PLAYER_PROMPT
from typing import Optional

from openai.types.beta import Assistant, Thread
from openai import OpenAI


class AbstractAssistant:
    def __init__(self, assistant_name: Optional[str] = None, prompt: Optional[str] = None,
                 assistant_id: Optional[str] = None, thread_id: Optional[str] = None):
        self.client = OpenAI()
        if assistant_id:
            self.assistant: Assistant = self.client.beta.assistants.retrieve(assistant_id)
            print(f"Retrieved assistant {self.assistant.id}")
        else:
            self.assistant: Assistant = self.client.beta.assistants.create(
                name=assistant_name,
                instructions=prompt,
                model="gpt-4-1106-preview"
            )
            print(f"Created assistant {self.assistant.id}")

        if thread_id:
            self.thread: Thread = self.client.beta.threads.retrieve(thread_id)
            print(f"Retrieved thread {self.thread.id}")
        else:
            self.thread: Thread = self.client.beta.threads.create()
            print(f"Created thread {self.thread.id}")

    def ask(self, user_message):
        # Add the user message to the thread
        self.client.beta.threads.messages.create(
            role="user",
            thread_id=self.thread.id,
            content=user_message
        )
        # Run assistant
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )
        print(f"Created run {run.id}")

        while True:
            # Wait for 1 second
            time.sleep(1)

            # Retrieve the run status
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
            print(f"Running status: {run_status.status}, (run id: {run.id})")

            if run_status.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id,
                    limit=1
                )
                msg = messages.data[0]
                role = msg.role
                content = msg.content[0].text.value
                print(f"Got reply from {role.capitalize()}:")
                print(f"{content}")
                return content
            else:
                print("Waiting for the Assistant to process...")
                time.sleep(1)


class ArbiterAssistant(AbstractAssistant):
    def __init__(self, assistant_id: Optional[str] = None):
        super().__init__(assistant_name='Arbiter', assistant_id=assistant_id, prompt=ARBITER_PROMPT)


class PlayerAssistant(AbstractAssistant):
    def __init__(self, name: str, assistant_id: Optional[str] = None):
        super().__init__(assistant_name=name, assistant_id=assistant_id, prompt=PLAYER_PROMPT)