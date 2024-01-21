# Mafia with AI

I'm building the [Mafia party-game](https://en.wikipedia.org/wiki/Mafia_(party_game)) with AI bots.

Bots are not aware of each other. Each of them gets instructions to pretend to be a human and to hide their true identity. Bots are aware of their roles, their teammates and the game rules, so they have everything to play to win.
I also want to add some roleplay to the game so there is an ongoing conversation between all participants. There is a story and bots should develop it though the conversation and their game actions. 

Below is an ugly design diagram of the idea. I'll improve it once I implemented the first version of the chatroom and see how it works. Currently, there are too many unknowns.

![Design](images/design.png)

The stack I plan to use:
- OpenAI API with Assistants and Threads
- AWS Lambda functions to host the backend logic
- Redis (most probably in AWS) to store the chat history and the game state
- React Native for the frontend