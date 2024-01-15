import json

from dotenv import load_dotenv, find_dotenv

from api.assistants import ArbiterAssistant


def run(user_message):
    arbiter = ArbiterAssistant(assistant_id='asst_s1xiaYU5DJXaxNrzapQMRvId')
    arbiter.ask(user_message)


if __name__ == '__main__':
    load_dotenv(find_dotenv())

    messages = [
        {"user_id": 1, "message": "I want to eat sushi"},
        {"user_id": 2, "message": "Sushi? No, you should each taco"},
        {"user_id": 1, "message": "Taco? No, I want to eat sushi"},
        {"user_id": 3, "message": "I want him hungry. Don't let hem to eat anything!"},
    ]
    messages_str = json.dumps(messages, indent=4)
    run(messages_str)