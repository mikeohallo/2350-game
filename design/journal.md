# Design journal

This is how 2350 was designed, written up from my working notes. The method was simple: play a whole season in a chat with an AI game master, write down what broke, change the rules, then play again at a different scale. Seven seasons over three days in October 2026 (23–25 Oct), plus a memory test, a dry run of the rules file, and a separate AI session acting as critic at set points.

What happened in each season is in the [atlas](../atlas/). This page is about the rules: what they are now, and what each one came out of.

**Contents:** [The game on one page](#the-game-on-one-page) · [Ground rules](#ground-rules) · [How winning was found](#how-winning-was-found) · [What each season taught](#what-each-season-taught) · [Testing the AI](#testing-the-ai) · [Boards and images](#boards-and-images) · [Interface lessons](#interface-lessons) · [Still open](#still-open) · [Not yet played](#not-yet-played)

---

## The game on one page

**The premise.** A hot century from the 2020s: heat, storms, failing harvests, rising seas, people on the move. In the 2140s comes the Blackout. The world's networks break apart, and every region now runs its grids, farms and trade on its own sealed network, run by its own AI. Each season plays forward from there, in eras, to the year 2350.

**You are your region:** its government and its AI together. How much your region hands to its AI is one of your culture choices, not who you are.

**Session zero** sets up the world before play:
- **The scale:** one city, one country, one continent, or the world.
- **The number of eras.**
- **The hidden-hand draft:** everyone secretly adds one shock card to the world (a collapsed current, a failed monsoon, a methane burst). One is drawn as the prologue and has already happened by the first era. The rest stay live in the pool, and nobody knows who put which card in until 2350.
- **A founding culture:** three quick choices. What holds your people together, what they keep from before, and how their cities live.

**Each era:**
1. **A risk roll.** On a 1, a card from the pool fires.
2. **A short briefing** of what your networks can see. Every item ends with a "For you" line saying what it means for you.
3. **Three rumours, one of them false.**
4. **What your people say, and what theirs say.** These are your only clues to how you're being judged.
5. **Three questions,** at least one about home and one facing out. Every option is defensible and none is plainly right. You can always answer in your own words instead.
6. **The results,** with costs as well as gains, then the board.

**The world remembers.** Every answer is stored with its place and year, and choices come back eras later. Across seven seasons, this was the strongest pillar.

**The hooks are the engine.** What each region depends on another for holds the peace and sets up the clashes. A water contract ran the whole of season 3. A tapped cable ran season 2.

**Fog comes from the sealed networks.** Until regions make contact, rivals are rumours. Contact comes in degrees: a cable landing, a border touching, a leaky firewalled link, a link bought from the Moon.

**Contested ground nobody starts with.** The Thaw, the Arctic, Antarctica and the Moon Link at world scale, or an unclaimed interior at country scale. In season 3, every area's networks raced into Australia's red centre, and it ended as a national border.

**Designed but not yet built:** a building layer for the eventual app. Six meters per place (cool, water, power, people, mood and tech), a queue of opportunities that rivals can take if you leave them, and "taps buy control, not power", so going deeper into a city makes it more yours without making it stronger. The playtests were run by hand in chat, with the AI keeping track. The numbers are the engine, not the toy, and in a real build they'd be plain code that everyone can see.

---

## Ground rules

Each of these came from something going wrong.

- **It takes itself seriously.** Anything big needs a cause in what's already true, a believable mechanism and a reason people would actually do it. The very first test round had a wildcard where Sydney sold the Opera House to Aotearoa to pay for a war. It couldn't happen and nobody would do it, so it was withdrawn, and this rule was born.

- **War is allowed, but land isn't the score.** Invasion and war are real moves, fought for the reasons people really fight. Holding land only counts through what it does for your people. Nobody is knocked out: clashes change borders, rights and fortunes, never who's playing.
  - **The clearest proof (season 6):** Asia gave away half its land and lost nothing on the verdict, because its people valued the families on that land, not the land itself.

- **No conjured capabilities.** Anything big has to trace back to earlier investment, with a cost and a chance of being found out.
  - **Where it came from:** in season 4 I destroyed a rival base with a weapon I'd never built.
  - **Why it matters for multiplayer:** with human rivals, nobody could have seen that weapon coming or answered it.

- **No free hits.** The AI-run rivals pay for their moves exactly as a player does.
  - **Where it came from:** in season 6 a rival, caught tapping my network, publicly accused me of building decoy networks. As first played, it hurt me and cost them nothing. But the accusation was a confession, so it was corrected to hit them harder.

- **Rash decisions have consequences.** The game shows what each choice commits you to, so nobody needs a photographic memory, but it doesn't stop you contradicting yourself. A contradiction becomes a story and an opening for someone, not just a penalty.
  - **Where it came from:** in season 1 I half-funded a dig under Sydney, and the half-built tunnels became a whole underclass, "the Unfinished".

- **Mostly player against player.** The tension comes from rivals, not from managing your own population. Your places are the prize rivals compete for, not a problem to babysit.

- **Rivals push back when it makes sense.** Not all the time, or it gets predictable. The mechanism:
  - every act between two regions is tagged as help, harm (sized 1–3) or neutral;
  - harms build a rival's **grievance** against you, and every rival has a hidden **breaking point** that differs each season (patient, steady or hawkish);
  - a rival acts only with a **motive, the means and a window**: you're stretched, a disaster has just hit you, or allies are lining up;
  - you can see it coming in the rumours and in what their people say, and one rumour can be a false alarm.

- **Orientation is the game's job.** In season 4, playing a continent I didn't know, place names meant nothing to me. The fixes:
  - only names that are on the board;
  - a label for every place a briefing mentions;
  - a "For you" line on every item;
  - a card for each rival saying what it wants.

---

## How winning was found

I deliberately left winning undecided until there had been enough play to judge it. This is how it got settled, season by season.

1. **Closing votes (seasons 2 and 3).** Season 2 ended in a renewal vote, where each people voted on whether to keep its rulers. Season 3 ended in a convention, one vote per area, on what the country becomes. That second one was the first real brake on a runaway leader: I led every era, but with one vote of four I only got my outcome by giving up dominance.
   - **The problem:** with human players, people will just vote against whoever looks strongest. And the winner mustn't be visible early, or players who think they can't win lose interest or turn disruptive.

2. **A secret goal picked at session zero:** considered and dropped. You'd have to know what's coming to choose one, which kills the surprise of each era, and it locks you onto one goal for the whole game.

3. **The hidden verdict (season 4).** In 2350, each region's own people judge their rulers. No player votes on another.
   - **The weights grow out of the season:** the culture you built and the hardships your people lived through. They differ for every region and every season, so there's no single strategy to learn.
   - **You never see the numbers during play.** The only hints are what your people say.
   - **The result:** my Andes, the most powerful area of any season, finished third, judged hardest on the council vote it took away from its own people. The weakest area won. It was still decidable in the last era (restoring the council would have put the Andes first), and every score traced back to something that happened. It felt fair.

4. **"The 100" (after season 5).** Season 5's score felt too harsh: "I protected them for the entire season." The cause was that safety was never weighted. Two changes followed:
   - **Every hardship adds weight to what it threatened** (a heat wave to safety, a drought to water), so getting your people through one counts.
   - **The score became a ring of everything a people wanted.** Each value splits into delivered, out of reach (the world's fault: disasters and the draft, never rivals' moves, which you could have answered) and let down. The headline is "of what was possible, you delivered X%". Season 6's 80% for Asia felt right: "I led the world, but you can't keep everyone happy."

5. **The world slice (after season 6).** A question I asked myself: does a score from your own citizens alone push players away from helping other countries? Partly. So 15 of the 100 points are now judged by **other countries' citizens**, never their players.
   - **Testing it:** I re-scored two finished seasons. In season 6 the order barely moved, because helping others had mostly paid off at home anyway.
   - **Where it bit:** in season 4, my Andes, rated 0.08 by the world after two invasions and the strike, dropped from 43 to 38 and fell further behind.
   - **What the slice is for:** the case the home score misses, a people that doesn't mind its rulers' aggression. A predatory bloc on 70 at home that the world rates 0.08 ends up around 61. A generous bloc on 60 at home that the world rates 0.9 ends up around 65.
   - **Two fixes came out of the re-scores:**
     - size the slice by culture, so staying out of things remains a valid way to play;
     - tag every act as it happens, rather than judging it afterwards.

6. **The objective in one line (season 7 onwards):** highest score wins. It took an outside reader saying the objective wasn't clear to make me write it down that plainly.

**Sealed as you go.** In season 7, each era's weights were sealed before the results were written, and each rival's moves were locked before I answered. That way the game master can't shape the score or the rivals around what I chose.

---

## What each season taught

**Season 1 · Oceania against Asia, continental, 7 eras.** Building choices work as moves against other players, and the hooks are the engine. My best moves weren't on the menu: a firewalled link and a tapped reef gate. A board game can't let a player do something nobody designed; an AI game master can judge whether it's plausible and resolve it. My own verdict was "super fun", with notes: more questions about my own region's culture, more questions per era, and world events that don't fire every era.

**Season 2 · Africa against Europe and the Gulf, 8 eras.** "The world remembers" held across 235 years. A half-built canal caused a shortfall later on. A tap planted in era II was detected in era VI, exposed in VII and denied in VIII. Culture questions gave the region its own identity without being stat bonuses. **The key finding:** a kind integrator strategy, pulling every rival inside your system rather than beating them, ran away with the game, and nothing in the rules put a real brake on it.

**Season 3 · Australia, country scale, 8 eras.** The same engine works at country scale, with borders that actually move: a breakaway, a claim on the centre, a secession. The AI areas played the leader cleverly by going around it, not through it. My own deals backfired in good ways: technology I sold leaked onward to a third area. And the closing vote was the first rule that made a leader pay.

**Season 4 · South America, an unfamiliar region, 8 eras.** The hidden verdict worked as both a brake and a story. Culture as a layer (a founding culture, plus one life question per era) carried a whole arc. War worked as a move, with its consequences arriving through the world rather than through rules. I pushed the season dark on purpose to stress the game, and it exposed the conjured weapon.

**Season 5 · Sydney, city scale, 6 eras.** The first plan copied the country model, with districts as players. Before playing, I challenged it: sealed networks make no sense inside one city, and a city game shouldn't be about running areas. So it became four **powers** competing for influence across the districts. Organised crime worked as the city's war, and it died when the scarcity it lived on did. Rumours turned from fog into a weapon. And the missing safety weight led to "the 100".

**Season 6 · The world, global scale, 10 eras.** Global scale works, with continents as blocs and the Thaw as the contested middle.
- **The hidden-hand draft** replaced a draft where every chosen shock happened. If everyone picks a disaster and they all happen, picking is pointless.
- **One risk roll per era,** at the start.
- **A bloc born mid-season:** the Thaw went from unclaimed ground to settlers to a nation and a member.
- **My own card bookended the season:** "the Amazon tips" was drawn as the prologue, and I closed the century by guaranteeing the Amazon's rain.
- **The runaway leader again:** I led all ten eras, and every brake on me was one I chose.

**Season 7 · East Asia, five real countries, dropped in its fourth era.** The first season under the full new rules: the world slice, tags, sealed weights and rival pushback.
- **What worked:** the mechanics ran cleanly. A consequence planted three eras earlier paid off, when power I'd sold a neighbour for its minerals quietly restarted its weapons programme. Culture moved the weights.
- **Why the story didn't land:**
  - **Too close to today.** Every earlier season used invented blocs or areas. Five real countries with live tensions made the game master cautious, so the eras read like today's news with the dates changed.
  - **Pure chance left four eras without a single shock,** so every era had the same shape.
  - **Broken momentum:** I built the rules file for friends (below) in the middle of the season, twice. And seven seasons in three days was a lot.
- **The lessons, not yet adopted as rules:** shock odds that rise each era nothing fires; keep real flashpoints one step removed; vary the shape of the questions; pace the testing.

---

## Testing the AI

**The memory test.** The biggest risk to "the world remembers" is an AI contradicting itself as the record grows.
- **The setup:** I wrote season 6 up as a structured record, about a hundred numbered facts (when, where, who, what, and who knows it), plus each bloc's holdings, the agreements in force and the verdict. A fresh game master that had never seen the season got only that record.
- **The result:** it answered 20 of 20 questions, and on both trick questions it said "not in the record" instead of inventing an answer. It then ran a consistent eleventh era, honouring "no free hits" without being told to.
- **The bonus:** it caught four contradictions made during live play that nobody had noticed.
- **What it argues for in a real build:**
  - facts that carry links and a status (active, ended or replaced);
  - living tables of agreements and holdings;
  - every rumour stored with its truth;
  - a contradiction check every time a fact is written.

**A rules file any AI can run.** A friend who loves board games like Risk read the pitch and found it interesting but complicated, with no clear objective, and reading the rules felt like work. So the player never reads the rules. The AI game master gets them in a file, and the player gets a one-page card.
- **Dice in the open:** the AI rolls every die and shows the number.
- **A standings table every era,** to stand in for the live boards.
- **A sealed envelope prepared in advance:** each rival's temperament and breaking point, and the draft cards. This stops the AI inventing them to suit the player.
- **Sealing without files:** a chat AI can't hide notes between turns, so each era's hidden state goes on one base64 line at the end of its message. That line is its memory, and its proof that it locked the rivals' moves before seeing your answer. It's all decoded at the finale.

**The dry run.** A fresh AI session (Claude, standing in for ChatGPT) ran the file through setup and a first era with nothing else to go on, against a second AI session playing a Risk-style player.
- **The draft:** the player picked the same shock card as one of the AI-run blocs, so it gave that bloc its reserve card instead, as the rules say, and kept every card's owner hidden.
- **The invasion:** it cut the player's invasion down to what had actually been built, a few thousand troops at one port, rolled for it in the open, and charged a cost for it.
- **The pushback:** the targeted rival's grievance climbed on schedule.
- **Two fixes came out of it:** tell the player to skip the scrambled line, and define what makes a culture outward- or inward-looking.

**A Korean edition.** The same rules in English, with a language section and a fixed Korean name list so place names never drift between eras. One catch: the fallback cipher for hiding notes by hand only scrambles English letters, so the hidden notes have to stay in English. It's not yet checked by a native speaker, so it isn't in this repo yet.

---

## Boards and images

- **Photo-realistic scenes of 2350 didn't work.** They looked like today.
- **Boards drawn in code did.** A quiet stylised world map with no names is the base, and each season is drawn on top in code from its record. That makes every board free to redraw and always geographically correct.
  - **Strength shows as glow,** so a region's territory and border brighten as it grows.
  - **Borders carry over** from era to era, and a fresh breakaway is hatched in its old owner's colour.
  - **Earlier networks stay as dim lines,** so the build-up is visible.
- **City scale needed its own board,** drawn from real elevation data so the low ground floods for real, with a magnified inset for the crowded inner harbour.
- **Painted era images were tried and dropped.** First too washed out, then too bleak. The boards tell the story better.

---

## Interface lessons

- **Three questions per card at most.** A four-question card dropped questions off my screen.
- **Anything to read gets its own turn,** ending with a "go". The question card hides what's above it, so it only comes up when there's nothing left to read. The rhythm per era: briefing, go, questions, results and board, go.
- **Tap answers, with your own words always allowed.** The "other" moves, where I invented a play and the game master judged it, were consistently the best moments of every season.

---

## Still open

- **The runaway leader.** The verdict makes leading not enough, but so far every brake on a leading human has been voluntary or has come at the end. Rival pushback is the world-side brake, and it hasn't yet been tested against a human who leads all season. One test not yet run: a season played as the weakest region.
- **Multiplayer is untested.** The cheapest real test is two people, three eras, one phone.
- **Flat seasons.** Rising shock odds are the leading fix.
- **No dominant strategy.** The goal is no dominant strategy, not no strategy: depth you can get better at, with no line that solves it. Weights that change every season, scales that change the closing vote, and themed shock pools are the main sources of variety.
- **Friends drop off.** A game played an era a day among friends is easy to drift away from. That's part of the reason for a rules file the AI carries, so a friend can start without reading anything.
- **Contested truth is expensive.** A different version of history for each player is the source of the best drama (season 2's tap), and it multiplies the consistency problem. It can come later, after the shared world works.
- **Politics in a mixed group.** Every option should be defensible and the premise presented as the game's world, not a position. Country scale and real places raise the stakes, which season 7 showed.

---

## Not yet played

- **The Fleets add-on:** play a fleet with no land. In a world of sealed networks, ships are the one thing that crosses between them.
  - **What changes:** position matters, ports are won by influence, and the sea itself changes as the Arctic opens and ports drown.
  - **Kinds of fleet:** a merchant house, a salvage guild, an ice-towing company, a navy for hire, a drowned nation.
  - **Mixed seasons:** some players are regions and some are fleets, asymmetric the way the board game Root is.
- **Other roles in the same world:** a network (an AI house regions run on), a movement, the Moon colony, a dynasty, a displaced people, or a bloc born mid-season as the seat a late-joining friend takes.
- **Other modes:**
  - a **cities** season, where each player is a city competing for people, capital and hub status;
  - a **co-op** season against the century itself;
  - an **archive** mode after a season, uncovering each other's hidden moves;
  - **the next century,** starting from a finished atlas.
