from dotenv import load_dotenv, find_dotenv

from api.assistants import ArbiterAssistant


def run(user_message):
    arbiter = ArbiterAssistant(assistant_id='asst_v1vNl8IcCKctxDCYI01U3I6r')
    arbiter.ask(user_message)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    run('Hey')