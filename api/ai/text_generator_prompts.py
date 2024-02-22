GAME_GENERATION_PROMPT = """\
You have the following theme: {theme}.

Generate a game scene for a Mafia party-game in the theme. A scene includes a place where players should spend few days
and nights. Create a short story around this place, and set the atmosphere for the game.

Temperaments indicate how peaceful or aggressive a player is and include:

Generate a JSON array with {num_players} objects for a Mafia party-game in the theme. Each object represents a player
and should have a 'name' (a unique thematic name), a 'backstory' (few sentences about the story or origin of this
player), and a 'temperament' (chosen from the list below). Don't use the following name: {human_player_name}.
All names must be one word names.

Temperaments indicate how peaceful or aggressive a player is and include:

- Shy: Exhibits fear and apprehension towards others, afraid of confrontation and scared by the prospect of being
  harmed. Tends to avoid the spotlight and feels uncomfortable around aggressive players.
- Proactive: Combines confidence, risk-taking, and a desire to lead or control situations. Characters with this
  temperament are assertive, bold in their actions, and seek to dominate their environment, often taking the initiative
  in confrontations and strategy.
- Aggressive: Quick to engage in conflict, sees aggression as a tool to assert dominance and achieve goals, often acting
  with little provocation.
  
If the theme is a known movie or book, use character from it to create players.

Return the JSON object like this:
{{
"theme": "Western",
"game_scene": "In the heart of a bustling mid-west saloon, the air filled with the sound of piano tunes and clinking
glasses, a diverse group of individuals finds shelter from a howling snowstorm. Each person, a stranger to the next,
carries a story colored by the trials of the Wild West. As the fire crackles in the hearth and the storm rages on,
unseen tensions and hidden tales weave a tapestry of intrigue and suspense.",
"players": [
    {{"name": "John Doe", "backstory": "A mysterious stranger with a troubled past.", "temperament": \
"Proactive: Combines confidence, risk-taking, and a desire to lead or control situations. Characters with this \
temperament are assertive, bold in their actions, and seek to dominate their environment, often taking the initiative \
in confrontations and strategy"}},
    {{"name": "Jane Doe", "backstory": "A local doctor known for her kindness.", "temperament": \
"Shy: Exhibits fear and apprehension towards others, afraid of confrontation and scared by the prospect of being \
harmed. Tends to avoid the spotlight and feels uncomfortable around aggressive players"}}
]
}}\
"""
