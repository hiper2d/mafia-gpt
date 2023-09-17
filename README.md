# ai-chatroom-with-games

In this project I experiment with ability to chat with many LLMs. My goal is to create group chats for people and multiple AIs, and play some games together.
I use Python, LangChain and Streamlit for this. I'm going to replace Streamlit with Flask and React Native later.

## Ideas

I started from multiple chat modals (ChatOpenAI). They don't have a memory, so I have to maintain the common memory for them. However, each LLM has it's personal initial prompt that is not shared to other LLMs. This should add unique personalities and hidden identities.

Other ideas I'm going to explore later is using Agents with their personal memories and thinking process. This is more advanced stuff, so I'll try it once I exhaust the previous idea capabilities with a shared memory and simple LLMs.

## Setup

I use `pipenv` to manage dependencies. Install it and create a new virtual environment for a project. I'll provide some guidance how to setup it together with Intellij Idea/PyCharm setup for the project.