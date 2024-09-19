# Play Maker - Create Game Plans for Ultimate Frisbee

## Description

[Ultimate Frisbee](https://en.wikipedia.org/wiki/Ultimate_frisbee) is a game played between two teams of 7 players. It is very similar to American Football, but instead of a football, a flying disc is used. Other large distinctions are that Ultimate is a non-contact sport, and you cannot move while holding the disc. Similarly to American Football, a team scores after they possess the disc in their opponent's end (scoring) zone. A player can throw the disc to other team members and can then move again. Although massively simplified, these rules explain the game PlayMaker aims to simulate.

PlayMaker generates game plans for sequences of moves a team can make to score while on offense. It uses a Markov chain to transition between states (moves). It uses pygame to visually represent players on the field (reduced to 5 for simplicity) and display the sequence of moves. The player marked in red is the player holding the disc.

## Usage

- `python3 PlayMaker.py`

  - Runs PlayMaker for one point.

- `./run_playmaker.sh n`
  - Runs PlayMaker for n points.

## Personal Significance

I started playing Ultimate when I was in fifth grade and have played ever since. I am very familiar with the rules of the game and common offensive strategies used to try and score points. For Bowdoin's D-III team, I play on the offensive line that is responsible for coming up with game plans to score points. PlayMaker does exactly this. When making the transition matrix, I used my experience to approximate how likely transitions are between states so that the simulation could more closely mimic a real world point.

When I landed on this idea, I knew I wanted to pursue it. It is extremely cool to me that sequences produced by PlayMaker are viable and could work at practices this week.

## Challenges

This project was a challenging undertaking. The largest challenge was in accurately keeping track of the internal game state and displaying it with pygame. This was my first time using pygame, but I was able to get going with it fairly quickly.

States involving cuts (e.g. STACK_DEEP_CUT, STACK_IN_CUT, etc.) where difficult to display because I really wanted to display the cut itself, the pass, and also the rest of the players repositioning, but I was able to accomplish this after troubleshooting.

This is an important challenge for me because I have heard lots about pygame and I wanted to start to work with it. I'm sure with this project I've just scratched the surface of what it is capable of.

There is so much more I would've liked to do with this project. To name a couple:

- Animate players moving
- Animate the disc moving
- Draw arrows to show where a player or disc is about to move
- Add in defenders (even if they don't do anything)
- Use a more complex transition matrix with more states
- Show all 7 players

## Is PlayMaker Creative?

I would argue PlayMaker is combinatorial-ly creative. It is able to generate move sequences and display them by combining existing moves and placing them in a sequence that makes conventional sense and according to common tactics. However, it does not really transform offensive planning in Ultimate, or further explore this domain.

I would wonder to see how useful the output would be in a real game. If it created amazing game plans, it would be more creative.

## Known Issues

- Sometimes PlayMaker may raise a ValueError stating "Too many cuts".
  - Since the number of players is reduced for simplicity, there are less players to make cuts, so there might not be enough players to make a cut. This occurs when there are a lot of consecutive "cut" moves.

## Sources

ChatGPT and GitHub CoPilot for help with pygame and troubleshooting.
