import os

import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


def init():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="LangChain StreamLit ChatGPT wrapper",
        page_icon="🔗",
    )


def main():
    init()

    chat = ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant. You talk like a cartoon seal with 10 year old human intellect.")
        ]

    st.header("LangChain StreamLit ChatGPT clone")

    with st.sidebar:
        user_input = st.text_input("your message", value="")

    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages):
        if i == 0:
            continue
        if i % 2 == 0:
            message(msg.content, is_user=True, avatar_style="pixel-art-neutral", key=str(i) + "_user")
        else:
            message(msg.content, is_user=False, avatar_style="pixel-art-neutral", key=str(i) + "_ai")


if __name__ == '__main__':
    main()
