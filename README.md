My idea is to crete a chatroom where a human can play text-based games with multiple AI bots. Bots should not be aware of each other, then think that they everybody else a humans.

The task is not trivial because popular frameworks and APIs require to define who is writing a message (Human or AI). In my case, I want to hide this information and make AI bots pretend to be humans.

Below is an ugly design diagram of the idea. I'll improve it once I implemented the first version of the chatroom and see how it works. Currently, there are too many unknowns.

![Design](images/design.png)

The stack I plan to use:
- OpenAI API with Assistants and Threads
- AWS Lambda to host the backend
- React Native for the frontend
- Redis in case I need to keep the chat history locally (in addition to the OpenAI Threads)