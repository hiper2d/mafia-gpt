# Mafia with AI

I'm building the [Mafia party-game](https://en.wikipedia.org/wiki/Mafia_(party_game)) with AI bots.

Bots are not aware of each other. Each of them gets instructions to pretend to be a human and to hide their true
identity. Bots are aware of their roles, their teammates and the game rules, so they have everything to play to win.
I also want to add some roleplay to the game so there is an ongoing conversation between all participants. There is a
story and bots should develop it though the conversation and their game actions.

Below is an ugly design diagram of the idea. I'll improve it once I implemented the first version of the chatroom and
see how it works. Currently, there are too many unknowns.

![Design](images/design.png)

The stack I plan to use:

- OpenAI API with Assistants and Threads
- AWS Lambda functions to host the backend logic
- Redis (most probably in AWS) to store the chat history and the game state
- React Native for the frontend

# The game logic

Right now the whole game is in just few functions. They imitate backend endpoints (I plan to use AWS lambda but to be
able to run locally as REST endpoints on a local web server). There is no client yet.

### init_game

This function creates a new game, generates the story, bot-players, assign random roles and save this all into Redis. It
also creates OpenAI assistants for the game master (arbiter) and bot-players. Each assistant has a separate OpenAI
thread. They are saved into the game object in Redis. If the game stops, its state is saved and can be continued at any
moment.

Each bot-player knows their name, a personal story, and a secret role. They are instructed not to reveal roles and
follow personal stories during the conversation. Bots know names and stories each other. I plan to add characters later.
Right now lots of stuff is hardcoded but I want all the stories to be generated by AI. Bots know the rules of the game
and should try to win. Winning conditions are different for different roles. I plan to update bot assistants'
instructions during the game so they always aware of the current game state (which day, who is alive, who is the main
suspect, etc.). Bots are instructed that they are talking to multiple human players. They should also pretend to be
humans and to hide their true identity.

### get_welcome_messages_from_all_players

Asks each bot player to generate a welcome message. Return all messages in a list. I plan to merge it into
the `init_game` function.

### talk_to_all

This is there the game begins. A user sends some message to the chat to other players.
The message is received by the Arbiter AI whose responsibility it to get all the latest messages and to decide which
bot-players should reply. Then bot-assistants reply one by one. They don't know about the arbiter AI and think that this
is just the conversation going. They instructed to accept input from multiple players at a time.

The function returns a list of replies from one or more bot-players. The game state is updated and saved to Redis.
Arbiter AI will need those messages to have the complete history of the conversion. It will also be needed for UI in the
future.

### tbd

This is all for now. I need more functions to drive the mate night where players with roles provide their actions.
I need to implement the logic of killing players and letting other players know about it. I need to make sure that they
keep track on the main game events. Most probably, I'll compact the most important info (using LLM of course) and store
it in assistants' instructions. OpenAI API allows to update them.

After that the game will be complete. Sounds like I should have something playable in few weeks :beer:

# Setup

### Run Redis

I prefer to run it with Docker Compose. There is a config in the root directory, just run it. You need to have docker
and docker-compose installed.

```bash
docker-compose up
```

### Run Python functions

Before running Python code, rename the [.env.template](.env.template) file into `.env` and fill in the values. All
environmental variables from it will be loaded by functions and used to talk to the external APIs (Redis, OpenAI).

I don't have any better runner than Python junit tests for now. In future, I'll use a web server with UI in React Native
for the local development. I'll deploy functions to Lambdas and host UI somewhere separately.
Each function has a separate test. It does not make sense to run all of them, only for the function you want to run.
To run tests, install Python dependencies using `Pipenv` (more details about it is [below](#pipenv_setup)), then run a
test you need like this:

   ```bash
   python -m unittest test_lambda_functions.TestGameFunctions.test_init_game
   ```

### <a id="pipenv_setup"></a>Pipenv setup and dependency installation

I use `pipenv` to manage dependencies. Install it, create a virtual environment, activate it and install dependencies.

1. Install `pipenv` using official [docs](https://pipenv.pypa.io/en/latest/install/#installing-pipenv). For example, on
   Mac:
    ```bash
    pip install pipenv --user
    ```

2. Add `pipenv` to PATH if it's not there. For example, I had to add to the `~/.zshrc` file the following line:
    ```bash
    export PATH="/Users/hiper2d/Library/Python/3.11/bin:$PATH"
    ```

3. Install packages and create a virtual environment for the project:
    ```bash
    cd <project dir> # navigate to the project dir
    pipenv install
    ```
   This should create a virtual environment and install all dependencies from `Pipfile.lock` file.

   If for any reason you need to create a virtual environment manually, use the following command:
    ```bash
    pip install virtualenv # install virtualenv if you don't have it
    virtualenv --version # check if it's installed
    cd <virtualenv dir> # for example, my virtual envs as here: /Users/hiper2d/.local/share/virtualenvs
    virtualenv <virtualenv name> # I usually use a project name
    ```

4. To swtich to the virtual environment, use the following command:
    ```bash
    cd <project dir>
    pipenv shell
    ```
   If this fails, then do the following:
    ```bash
    cd <virtualenv dir>/bin
    source activate
    ```