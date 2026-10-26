<!--
DRAFT v1, 26 Oct 2026 (private). Before this repo goes public (portfolio rule P6), the ideas chat runs the go-public check. Still open:
- the elevation-data attribution for the city board in the top image;
- Google's terms for the Gemini-made base map (engine/base/);
- a proper name/trademark check on "2350";
- no friend quotes or family context without the person's OK;
- "An outside playtest" filled in once the friend's season is back.
-->

# 2350

**A strategy game about the next two centuries, designed in seven AI-run playtests.**

![The same engine at four scales: Sydney's four powers, Australia's four areas, South America, and the world](images/four-scales.jpg)

> Friends share one future, and in the year 2350 their citizens judge them for it.

You run one bloc of the world from the 2140s to 2350. You build, trade, ally, spy, threaten and go to war. At the end, your own people look back and score you: **out of what was possible, how good a future did you give them?** Highest score wins.

There's no app. The game's engine is a rules file: an AI game master reads it and runs everything, including the rivals, the dice, the secrets and the score. The player never reads a rule.

This repo is a case study of how I designed it with AI: what I tried, what the playtests showed, and what changed because of them.

## Play it in two minutes

1. Download [`play/game-master.txt`](play/game-master.txt) and [`play/world-board.jpg`](play/world-board.jpg).
2. Open ChatGPT, Claude or Gemini, start a new chat and upload both.
3. Type **Let's play 2350**. The one-page card, [`play/how-to-play.png`](play/how-to-play.png), is all a player needs to read.

A game takes about an hour: six eras, three questions each. The rules file holds a sample sealed envelope (the rivals' hidden temperaments and cards), so don't read it if you want to play. A Korean edition exists and joins the repo once a native speaker has checked it.

## How it was made

| Who | What they did |
|---|---|
| **Me** | The game design, every playtest decision, and the calls on what changed |
| **Claude** (Anthropic) | Game master for every season, the board engine code and the design docs |
| **Gemini** (Google) | The stylised base map the boards are drawn on |

**The loop:** play a whole season in chat with tap answers, write down what broke, change the rules, then play the next season at a different scale. Seven seasons over three days in October 2026.

| Season | Scale | I played | Eras | How it ended |
|---|---|---|---|---|
| 1 | Continental | Oceania, against Asia | 7 | *2350: The Continent Everything Ran Through* |
| 2 | Continental | Africa, against Europe and the Gulf | 8 | *2350: Pax Africana* |
| 3 | Country | Australia's Tropic North | 8 | *2350: The Kept Word* |
| 4 | Continental | South America's Andes | 8 | *2350: The Whole Truth* |
| 5 | City | Sydney's Port | 6 | *2350: One Port* |
| 6 | Global | Asia | 10 | *2350: The Open Gate* |
| 7 | Regional | South Korea, in East Asia | 3 of 8 | Dropped (see [What didn't work](#what-didnt-work)) |

## What the playtests changed

Every rule below came from a problem that showed up in play or in feedback.

- **If everyone picks a disaster and they all happen, picking is pointless.** → **The hidden hand.** Each bloc secretly adds one shock card. One is drawn as the prologue, and the rest become live risks that may or may not fire.
- **A rival hit me and paid nothing for it.** → **No free hits.** Rivals pay for their moves exactly as a player does.
- **I destroyed a rival's base with a secret weapon I'd never built.** → **No conjured capabilities.** Anything big has to trace back to earlier investment, with a cost and a chance of being found out.
- **The human kept running away with the game.** → **The hidden verdict.** Your own people judge you, weighted by what they value and what they lived through. In season 4 the most powerful region I'd ever built finished third.
- **"I protected them for the entire season" (when the score felt too harsh).** → **Every hardship adds weight to what it threatened, and the score became "the 100":** each value splits into delivered, out of reach (the world's fault) and let down.
- **Does scoring by your own citizens push people away from helping others?** → **The world slice.** Fifteen points are judged by other countries' citizens. I re-scored two finished seasons to test it, and it bit hardest on the season where I'd invaded my neighbours.
- **Rivals should push back when it makes sense, but not so often it gets predictable.** → **Grievance with hidden breaking points.** A rival acts only with a motive, the means and a window, and you can see it coming in rumours and in what their people say.
- **A board gamer who read the pitch found it complicated, with no clear objective.** → **The player never reads the rules.** One card, a one-line goal, and the AI runs the rest.

There were smaller interface lessons too:

- **Three questions per card at most.** A four-question card dropped questions off my screen.
- **Anything to read gets its own turn,** so a question card never covers something I still have to read.

## The score: "the 100"

![A 2350 card: Asia's verdict at 80%, split into delivered, out of reach and let down, with every rival's ring](images/2350-card.jpg)

The weights grow out of each season: the culture you build and the hardships your people live through. So there's no single strategy to learn. Play your way, and your way becomes part of how you're judged.

## Testing the AI, not just the game

- **The memory test.** A fresh AI game master got only a structured record of season 6, about a hundred numbered facts. It answered 20 of 20 questions, said "not in the record" to both trick questions, and ran a consistent eleventh era. It also caught four contradictions I'd made in live play without noticing. That's the case for a consistency check whenever a fact is written.
- **The any-AI dry run.** A fresh agent ran the rules file through setup and a first era with no other help.
    - It applied the hidden-hand swap correctly.
    - It cut a Risk-style invasion down to what had actually been built, rolled for it in the open, and charged a cost.
    - It raised the target's grievance on schedule.
- **Sealing without files.** A chat AI can't hide notes between turns, so each era's hidden state goes on one encoded line at the end of its message. That line is its memory and its proof that it didn't change the rivals' moves after seeing your answer.
- **A Korean edition** from the same rules: a language layer plus a fixed name list, so the place names never drift.

## What didn't work

- **Season 7 didn't land, and I dropped it after three eras.** It used five real East Asian countries.
    - The live real-world tensions made the game master cautious, so the eras read like today's news with the dates changed.
    - Pure chance meant no shock fired in four rolls.
    - Building tools mid-season broke the momentum, and it was the seventh season in three days.
    - **What came out of it:** shock odds that rise each era nothing fires, and keeping real flashpoints one step removed.
- **Painted era images.** I generated an image of my region each era. They never matched the boards: first too washed out, then too bleak. The boards stayed and the images went.
- **The runaway leader is still open.** The verdict makes leading not enough, but so far every brake on a leading human has been voluntary or has come at the end of the game.

## The boards

![Season 6's finale: every bloc's verdict ring on the world board](images/season6-finale.jpg)

Every board is drawn in code (Python, Pillow, NumPy), so it costs nothing to redraw and always matches real geography.

- **Countries:** real country shapes from Natural Earth, warped onto the stylised base map with a fitted thin-plate spline.
- **Strength:** shows as glow, and borders carry over from era to era.
- **Each era's events:** stored as a small data file of numbered beats.
- **The city board:** built from real elevation data, so low ground floods for real.

## What's next

- **An outside playtest.** A friend is playing a season on ChatGPT with only the card and the rules file. *(Results to come.)*
- **Multiplayer:** friends sharing one world, the concept this all started from.
- **The Fleets add-on:** play a fleet with no land, in a world where ships are the only thing that crosses between the sealed networks.

## Repo map

```
play/      the rules file for any chat AI, the how-to-play card, the world board
engine/    the board renderer, with season 6 as sample data (see engine/README.md)
images/    the pictures in this README
```

Still to come: an atlas of every finished season, and the design journal behind it.

## Credits

- **Map data:** [Natural Earth](https://www.naturalearthdata.com/) (public domain). City elevation from AWS Terrain Tiles *(attribution to add)*.
- **Fonts:** Rajdhani and Share Tech Mono (in `engine/fonts/`, with their SIL Open Font License files), and IBM Plex Sans on the card.
- **Base map art:** made with Google Gemini.
- **Game master:** Claude, by Anthropic.

## Licence

Code (`engine/*.py`): MIT, in [`LICENSE`](LICENSE). The rules, the card, the design text, the season data and the images: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), so they can be shared and adapted, but not sold. See [`LICENSE-CONTENT.md`](LICENSE-CONTENT.md).

© 2026 Mike O'Halloran
