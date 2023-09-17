import os
from typing import List

import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from api.chains import init_keys, init_chat
from api.messages import PlayerMessage
from api.players import Player


def init_streamlit():
    st.set_page_config(
        page_title="LangChain StreamLit ChatGPT wrapper",
        page_icon="🔗",
    )


def main():
    init_keys()
    init_streamlit()

    chat = init_chat()

    if "messages" not in st.session_state:
        st.session_state.all_messages = []

    st.header("LangChain StreamLit ChatGPT clone")

    bot = Player(name="Bot", number_of_players=2)

    with st.sidebar:
        user_input = st.text_input("your message", value="")

    if user_input:
        st.session_state.all_messages.append(PlayerMessage(name="Player1", is_user=True, content=user_input))
        with st.spinner("Thinking..."):
            response = chat([bot.system_message] + st.session_state.all_messages)
        st.session_state.all_messages.append(PlayerMessage(name="Player2", content=response.content))

    messages: List[PlayerMessage] = st.session_state.get('messages', [])
    for i, msg in enumerate(messages):
        if msg.is_user:
            message(msg.content, is_user=True, avatar_style="pixel-art-neutral", key=str(i) + "_user")
        else:
            message(msg.content, is_user=False, avatar_style="pixel-art-neutral", key=str(i) + "_ai")


if __name__ == '__main__':
    main()
