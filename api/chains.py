import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel


def init_keys():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")


def init_chat(verbose=True) -> BaseChatModel:
    return ChatOpenAI(verbose=verbose)

