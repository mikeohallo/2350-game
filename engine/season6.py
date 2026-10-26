"""Season 6 record: the world, six continental blocs plus unclaimed ground. Filled era by era."""
NUMS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
YEARS = ['2145-2165', '2165-2185', '2185-2205', '2205-2225', '2225-2245', '2245-2265', '2265-2285', '2285-2305', '2305-2330', '2330-2350']
ERAS = [dict(n=NUMS[i], years=YEARS[i], head='', line='', event=None, hot=[], beats=[], strength={}) for i in range(10)]

SETUP = dict(
  title='SESSION ZERO · THE WORLD', sub='Six continents, sealed apart by the Blackout. Pick yours.',
  column=[0, 0, 1, 1, 1, 2, 2, 2],
  hot=[('canada_north', 'nam', 0.5, 9), ('southwest', 'HEAT', 0.6, 7), ('amazon', 'sam', 0.5, 9), ('northsea', 'eur', 0.4, 6),
       ('med', 'HEAT', 0.5, 6), ('sahara', 'SUN', 0.6, 10), ('congo', 'afr', 0.5, 8), ('himalaya', 'WATER', 0.6, 8),
       ('india', 'HEAT', 0.6, 7), ('eastchina', 'asi', 0.5, 7), ('australia', 'SUN', 0.4, 9), ('aotearoa', 'oce', 0.5, 4),
       ('siberia', 'centre', 0.4, 14), ('arctic', 'ICE', 0.4, 10)],
  sections=[
    ('nam', 'NORTH AMERICA', 'Canada to Panama, with Greenland', [
      (1, 'nam', 'canada_north', 'The North Opens', 'Canada’s north thaws into farmland and new cities, and the Arctic door opens beside it.'),
      (2, 'HEAT', 'southwest', 'The Burning South', 'The south-west and Mexico run short of water; the Gulf coast takes the storms.')]),
    ('sam', 'SOUTH AMERICA', 'The Andes to the Amazon', [
      (3, 'sam', 'amazon', 'The Flying Rivers', 'The Amazon makes the continent’s rain, if it stays standing.'),
      (4, 'MINERALS', 'andes', 'The Lithium Triangle', 'The metal every battery and grid on Earth needs.')]),
    ('eur', 'EUROPE', 'The Atlantic to the Urals', [
      (5, 'eur', 'northsea', 'The Cold North', 'The Atlantic current is slowing: harsher northern winters in a hotter world.'),
      (6, 'HEAT', 'med', 'The Burning Mediterranean', 'Heat domes over the south; the shore everyone else wants to cross.')]),
    ('afr', 'AFRICA', 'The whole continent', [
      (7, 'PEOPLE', 'lagos', 'The Youngest Continent', 'By 2100 one person in three on Earth is African: the century’s workforce.'),
      (8, 'SUN', 'sahara', 'Sun and Rivers', 'The Sahara’s sun and the Congo’s river: the most untapped power on Earth.')]),
    ('asi', 'ASIA', 'The Middle East to Japan', [
      (9, 'WATER', 'himalaya', 'The Water Towers', 'Himalayan ice feeds the rivers of billions, and it is melting.'),
      (10, 'HEAT', 'india', 'The Heat Ceiling', 'Parts of South Asia and the Gulf pass the limit of what bodies can bear outdoors.')]),
    ('oce', 'OCEANIA', 'Australia, Aotearoa and the Pacific', [
      (11, 'oce', 'aotearoa', 'The Cool Refuge', 'Aotearoa stays cool and wet; Australia has sun and minerals to spare.'),
      (12, 'WATER', 'pacificw', 'The Sinking Islands', 'The Pacific’s atoll nations are losing their land to the sea.')]),
    ('centre', 'UNCLAIMED', 'No bloc starts with these', [
      (13, 'centre', 'siberia', 'The Thaw', 'Siberia’s permafrost melts: the biggest new farmland and the biggest methane risk on Earth.'),
      (14, 'ICE', 'arctic', 'The Arctic', 'Summer ice gone: new sea lanes over the top of the world, and the seabed beneath.'),
      (15, 'ICE', 'antarctica', 'Antarctica', 'The last continent, its treaty long expired.'),
      (16, 'STAR', 'moonlink', 'The Moon Link', 'The only connection that could reach every sealed network. No one has built it yet.')]),
  ])

# century draft, hidden-hand rule (agreed 24 Oct): one card drawn at random is the prologue; the rest are live risks
DRAFT = dict(drawn='The Amazon tips', drawn_by='asi',
             pool=['The heat ceiling', 'The water towers fail', 'The Atlantic current collapses', 'The fast sea rise', 'The methane burst'])

PLAYER = 'asi'

ERAS[0].update(
  head='MACHINES IN THE THAW', line='Asia feeds itself by machine, twice, and gambles on the heat',
  strength={'asi':1.2,'eur':1.05,'afr':1.0,'nam':1.1,'sam':0.7,'oce':0.95},
  transfers=[('thaw_east','centre','asi'), ('thaw_west','centre','eur')],
  refs=[('the Urals', (60, 58), 'l'), ('Altai', (87, 49.5), 'l'), ('Amur', (130, 50), 'r'), ('the Gulf', (51, 26), 'l')],
  hot=[('eastchina','asi',0.5,6),('india','HEAT',0.5,6),('gulf','HEAT',0.4,4),('sahara','SUN',0.5,8),('amazon','HEAT',0.5,8),
       ('northsea','eur',0.3,5),('canada_north','nam',0.35,8),('aotearoa','oce',0.4,4)],
  beats=[
    dict(id=1, c='asi', at=(112, 53), r=6, s=0.8, title='Machine Farms in the Thaw', line='AI-run farms from the Altai to the Amur, few settlers, all on the network. Grain flows south by 2165.'),
    dict(id=2, c='eur', at=(72, 58), r=5, s=0.7, title='Settlers From the West', line='Europe’s families cross the Urals and live on the land they claim. Siberia’s towns befriend neighbours, not machines.'),
    dict(id=3, c='FOOD', at=(118, 32), r=4, s=0.6, title='Sky Farms', line='Whole levels of the sky cities turn to farms: a third of their food by 2165. The green levels are the best addresses.'),
    dict(id=4, c='HEAT', at=(74, 27), r=5, s=0.7, title='The Gamble', line='No card fires this era. Hundreds of millions stay on the hot plains, and the heat-ceiling card stays in the pool.'),
    dict(id=5, c='SUN', flow=dict(what='SUN', dep=1, style='contact', pts=[(5,24),(20,25),(33,27),(45,26),(51,26)]), title='The Sahara Belt', line='Africa’s solar fields spread, and its first cables run east toward the Gulf. It has power to spare; you are short.'),
    dict(id=6, c='nam', flow=dict(what='nam', dep=1, pts=[(-150,71),(-110,74),(-60,76),(-10,75),(40,74),(90,75),(140,73),(170,68)]), title='The Arctic Opens', line='North America’s ships cross the top of the world in summer: to Europe first, a trickle to Asia.'),
    dict(id=7, c='sam', at=(-60, -10), r=6, s=0.6, title='South America Sells', line='It blames you, and sells you lithium cheap anyway. It is too desperate not to.'),
  ])


ERAS[1].update(
  head='THE GREAT BUILD', line='Asia refuses the link, builds its own power, and the towns go east',
  strength={'asi':1.3,'eur':1.15,'afr':1.1,'nam':1.1,'sam':0.7,'oce':0.95},
  transfers=[('yenisei_towns','centre','asi')],
  ghost=[dict(what='nam', pts=[(-150,71),(-110,74),(-60,76),(-10,75),(40,74),(90,75),(140,73),(170,68)])],
  refs=[('Yenisei', (87, 62), 'l'), ('Gobi', (105, 43), 'r'), ('Thar', (71, 27), 'l'), ('South China Sea', (114, 14), 'r')],
  hot=[('eastchina','asi',0.4,6),('himalaya','POWER',0.5,5),('sahara','SUN',0.5,8),('northsea','eur',0.4,5),('canada_north','nam',0.3,8),
       ('amazon','HEAT',0.4,8),('aotearoa','oce',0.35,4)],
  beats=[
    dict(id=1, c='POWER', at=(104, 42), r=7, s=0.8, title='The Great Build', line='Solar on the Gobi and the Thar, steppe wind, Himalayan pumped hydro, offshore wind. By 2185 Asia has more clean power than it can use.'),
    dict(id=2, c='HEAT', at=(116, 30), r=4, s=0.5, title='The Brownouts', line='Through the 2170s the sky cities ration power; only the green levels stay lit.'),
    dict(id=3, c='asi', at=(96, 63), r=6, s=0.7, title='The Towns Go East', line='Grain and a place on the network: nearly every town east of the Yenisei joins, and a few to the west.'),
    dict(id=4, c='PEOPLE', at=(80, 22), r=4, s=0.5, title='By Need', line='The green levels go to the old, the sick and families with children. The poor trust the network; the engineers resent it.'),
    dict(id=5, c='SUN', flow=dict(what='SUN', dep=2, pts=[(5,25),(9,31),(11,36),(10,41),(8,47)]), title='Africa Turns North', line='Refused by Asia, Africa runs its cables under the Mediterranean. Europe takes the link, and cheap power.'),
    dict(id=6, c='DATA', at=(22, 49), r=3, s=0.5, title='The Tap', line='The link carried a hidden tap. Africa can see inside Europe\u2019s network. Europe doesn\u2019t know.'),
    dict(id=7, c='eur', at=(68, 56), r=4, s=0.5, title='Europe Grows Wary', line='Your network is spreading into lands its people farm. The Yenisei line is still undrawn.'),
  ])


ERAS[2].update(
  head='THE ICE GOES', line='The water towers fail; Asia shares equally, drinks the sky, and catches Africa in the mirror',
  event='THE WATER TOWERS FAIL',
  strength={'asi':1.25,'eur':1.2,'afr':1.15,'nam':1.15,'sam':0.7,'oce':0.95},
  transfers=[('west_towns_back','asi','eur')],
  ghost=[dict(what='nam', pts=[(-150,71),(-110,74),(-60,76),(-10,75),(40,74),(90,75),(140,73),(170,68)]),
         dict(what='SUN', pts=[(5,25),(9,31),(11,36),(10,41),(8,47)])],
  refs=[('Ganges', (84, 25.5), 'r'), ('Indus', (70, 27), 'l'), ('Mekong delta', (106, 10), 'r'), ('Gujarat', (71, 22.5), 'l')],
  hot=[('himalaya','HEAT',0.6,6),('india','HEAT',0.5,6),('eastchina','asi',0.35,6),('sahara','SUN',0.4,8),('northsea','eur',0.4,5),
       ('canada_north','nam',0.3,8),('aotearoa','oce',0.3,4)],
  beats=[
    dict(id=1, c='HEAT', at=(86, 31), r=5, s=0.8, title='The Water Towers Fail', line='The glaciers collapse in the 2190s. The great rivers flood with the monsoon and shrink to a trickle in the dry season.'),
    dict(id=2, c='WATER', at=(80, 25), r=4, s=0.5, title='Equal Shares', line='Every nation the same share. Asia holds together; the crowded plains go hungry; the upstream nations feel robbed.'),
    dict(id=3, c='WATER', flow=dict(what='WATER', dep=2, pts=[(70,22),(80,19),(90,22),(98,17),(106,11)]), title='Water From the Air', line='Condenser towers on the humid plains and coasts, powered by the Great Build: a quarter of the dry-season water by 2205.'),
    dict(id=4, c='DATA', flow=dict(what='DATA', dep=1, style='contact', pts=[(30,15),(42,20),(52,25)]), title='The Mirror', line='Africa gets a link into a mirror of your network. It tries to plant a tap; you catch it and keep the code. Africa thinks it worked.'),
    dict(id=5, c='eur', at=(86, 60), r=3, s=0.6, title='Europe\u2019s Cable', line='Europe\u2019s own network reaches the western Siberian towns; some switch back. The Yenisei divides two networks.'),
    dict(id=6, c='nam', at=(-10, 74), r=5, s=0.5, title='The Arctic Pact', line='Europe and North America quietly agree to share the northern lanes and seabed, without you. Africa told you.'),
    dict(id=7, c='POWER', at=(120, 25), r=3, s=0.4, title='Paying the Engineers', line='Wages and power credits bring them back. They buy private cooling on the hot levels: money starts to buy comfort.'),
  ])


ERAS[3].update(
  head='THE NORTHERN COMPACT', line='Asia claims the Arctic shore, tells Europe the truth, and loses Africa',
  strength={'asi':1.35,'eur':1.15,'afr':0.9,'nam':1.2,'sam':0.75,'oce':0.95},
  transfers=[('thaw_north','centre','asi')],
  ghost=[dict(what='WATER', pts=[(70,22),(80,19),(90,22),(98,17),(106,11)]), dict(what='SUN', pts=[(5,25),(9,31),(11,36),(10,41),(8,47)])],
  refs=[('Bering Strait', (-169, 66), 'r'), ('Lena', (126, 70), 'l'), ('Yenisei mouth', (82, 72), 'l')],
  hot=[('eastchina','asi',0.35,6),('india','WATER',0.4,6),('canada_north','nam',0.4,8),('northsea','eur',0.35,5),('congo','afr',0.35,7),
       ('amazon','sam',0.3,7)],
  beats=[
    dict(id=1, c='asi', at=(152, 69), r=6, s=0.8, title='The Siberian Coast', line='Asia claims the Arctic shore from the Yenisei to the Bering Strait, the sea route and the seabed. Ports, icebreakers, grain shipped north by river.'),
    dict(id=2, c='nam', at=(-150, 61), r=4, s=0.7, title='Standoff on the Ice', line='North America calls it a grab and sends icebreakers and patrols through the Bering Strait. No shots.'),
    dict(id=3, c='eur', at=(30, 56), r=4, s=0.6, title='Telling Europe', line='Forty years of proof. Europe tears out the tap, cuts Africa\u2019s price, and won\u2019t back North America against you.'),
    dict(id=4, c='afr', at=(28, -12), r=5, s=0.6, title='Africa Finds the Mirror', line='Its tap into Asia hit a decoy. Accusing Asia of traps, it admits it tapped two blocs. Trust in Africa falls everywhere.'),
    dict(id=5, c='WATER', at=(82, 24), r=4, s=0.6, title='The Towers Decide', line='Condensers where the shortfall is worst: half the Ganges and Indus plains\u2019 dry-season water. The upstream nations got nothing back.'),
    dict(id=6, c='sam', flow=dict(what='sam', dep=2, pts=[(-60,-15),(-70,0),(-85,15),(-95,30),(-98,42)]), title='The Americas Join', line='South America\u2019s lithium for North America\u2019s grain. South America finds a partner, and it isn\u2019t you.'),
  ])


ERAS[4].update(
  head='THE COLD ATLANTIC', line='The current stops; Asia feeds Europe, gates Africa’s power and moves its plains north',
  event='THE ATLANTIC CURRENT COLLAPSES',
  strength={'asi':1.4,'eur':1.05,'afr':0.95,'nam':1.15,'sam':0.8,'oce':0.95},
  ghost=[dict(what='WATER', pts=[(70,22),(80,19),(90,22),(98,17),(106,11)]), dict(what='SUN', pts=[(5,25),(9,31),(11,36),(10,41),(8,47)]),
         dict(what='sam', pts=[(-60,-15),(-70,0),(-85,15),(-95,30),(-98,42)])],
  refs=[('Yenisei', (87, 62), 'l'), ('the Sahel', (2, 14), 'l'), ('Amur', (130, 50), 'r'), ('the Gulf', (51, 26), 'l')],
  hot=[('northsea','ICE',0.5,7),('newyork','HEAT',0.35,4),('india','WATER',0.35,6),('siberia','asi',0.5,10),('eastchina','asi',0.3,6),
       ('andes','STAR',0.4,4),('congo','afr',0.3,6)],
  beats=[
    dict(id=1, c='ICE', at=(-30, 52), r=6, s=0.7, title='The Current Stops', line='The Atlantic’s heat stops flowing north. Northern Europe can’t farm its winters; North America’s east coast gives up low ground; the Sahel dries.'),
    dict(id=2, c='FOOD', flow=dict(what='FOOD', dep=2, pts=[(112,55),(98,56),(86,57),(70,56),(52,54),(32,53)]), title='The Yenisei Treaty', line='Thaw grain at a fair price, power at cost. Europe recognises your coast and fixes the Yenisei, and turns North America down.'),
    dict(id=3, c='SUN', flow=dict(what='SUN', dep=2, pts=[(8,24),(22,25),(34,27),(44,26),(51,26),(58,27)]), title='The Sealed Gate', line='Africa’s power at cost through the Gulf cable, past a gate you control. The council hands over its code and opens up.'),
    dict(id=4, c='DATA', at=(47, 21), r=3, s=0.5, title='The Old Code', line='2241: an old copy of the tap code is tried on the gate. It holds. The trail leads to Africa’s fallen leaders.'),
    dict(id=5, c='PEOPLE', flow=dict(what='PEOPLE', dep=2, pts=[(80,24),(84,34),(92,44),(104,52),(118,58),(128,62)]), title='North to the Thaw', line='New towns on the Lena, the Amur and the Arctic ports, places by need. Sixty million by 2245, on thawing ground.'),
    dict(id=6, c='WATER', at=(77, 13), r=4, s=0.5, title='The Lighter Monsoon', line='Two dry years in the 2240s; the towers make a third less. With fewer people on the plains, no one goes without.'),
    dict(id=7, c='STAR', at=(-68, -20), r=4, s=0.6, title='The Moon Link', line='The Americas’ first test launch from the Andes in 2238; the second blows up. Your warning, with Europe: “no one should own it”. Their answer: “then join”.'),
  ])


ERAS[5].update(
  head='THE LANDBRIDGE', line='Asia joins Europe and Africa into the biggest network on Earth, and burns the Thaw’s methane for all three',
  strength={'asi':1.45,'eur':1.1,'afr':1.05,'nam':1.05,'sam':0.8,'oce':1.0},
  ghost=[dict(what='FOOD', pts=[(112,55),(98,56),(86,57),(70,56),(52,54),(32,53)]), dict(what='PEOPLE', pts=[(80,24),(84,34),(92,44),(104,52),(118,58),(128,62)]),
         dict(what='sam', pts=[(-60,-15),(-70,0),(-85,15),(-95,30),(-98,42)])],
  refs=[('Lena', (126, 70), 'l'), ('the Sahel', (2, 14), 'l'), ('the Gulf', (51, 26), 'r'), ('Yenisei', (87, 62), 'l')],
  hot=[('gulf','asi',0.5,5),('siberia','POWER',0.5,10),('sahara','WATER',0.35,8),('northsea','eur',0.35,6),('andes','STAR',0.35,4),
       ('australia','oce',0.35,8),('eastchina','asi',0.3,6)],
  beats=[
    dict(id=1, c='asi', flow=dict(what='asi', dep=3, pts=[(6,22),(22,27),(38,29),(51,26),(62,36),(76,48),(87,57),(70,56),(50,53),(30,48),(16,40),(9,33),(6,24)]), title='The Landbridge', line='The 2256 Gulf summit joins Asia, Europe and Africa by ground cable: most of the people on Earth. Three networks meet at shared gates, most of them Asia’s.'),
    dict(id=2, c='WATER', at=(-6, 7), r=5, s=0.6, title='The Towers Go to Africa', line='The condenser design for the Sahel’s south and coasts, for Africa’s vote and more Sahara power. In the dry north they barely work.'),
    dict(id=3, c='DATA', at=(17, 21), r=3, s=0.5, title='The Proof', line='The council breaks the fallen leaders’ network; the trail leads to the Sahara power traders. In the north: “Asia’s orders”.'),
    dict(id=4, c='POWER', at=(128, 66), r=6, s=0.7, title='Catching the Methane', line='Wells, caps and flares over the worst seeps; the gas lights Europe’s winters through the Landbridge. Millions of square kilometres can’t all be capped.'),
    dict(id=5, c='STAR', at=(-30, 8), r=5, s=0.6, title='The Relay Goes Live', line='2263: the Moon Link switches on. North America cuts its price and calls Asia a hypocrite: “no one should own the crossroads”.'),
    dict(id=6, c='oce', at=(150, -30), r=4, s=0.6, title='Oceania Opens', line='2264: Oceania joins the relay, its first link to the world in a century, without opening to its neighbours.'),
    dict(id=7, c='sam', at=(-62, -30), r=3, s=0.5, title='South America Looks Over', line='Launch money falls short with three members on the relay. It quietly asks the Landbridge about lithium.'),
  ])


ERAS[6].update(
  head='THE KEYS', line='Asia shares the keys and publishes its watch, brings South America in, and cools its people',
  strength={'asi':1.5,'eur':1.15,'afr':1.1,'nam':0.95,'sam':0.9,'oce':1.0},
  ghost=[dict(what='asi', pts=[(6,22),(22,27),(38,29),(51,26),(62,36),(76,48),(87,57),(70,56),(50,53),(30,48),(16,40),(9,33),(6,24)])],
  refs=[('the Gulf', (51, 26), 'r'), ('Lagos', (3.4, 6.5), 'l'), ('Gobi', (105, 43), 'r'), ('Yenisei', (87, 62), 'l')],
  hot=[('india','ICE',0.5,7),('eastchina','ICE',0.4,6),('gulf','DATA',0.35,4),('lagos','afr',0.4,5),('amazon','sam',0.35,8),
       ('siberia','FOOD',0.4,10),('canada_north','nam',0.25,8)],
  beats=[
    dict(id=1, c='DATA', at=(56, 31), r=4, s=0.6, title='The Open Watch', line='Joint keys at every gate. Asia’s watch stays, and reports to every member the same day, its own logs included. Europe proposes one power market.'),
    dict(id=2, c='sam', flow=dict(what='sam', dep=2, pts=[(-38,-7),(-27,-3),(-15,2),(-4,5),(3,6)]), title='The Fourth Member', line='2271: South America’s cable lands at Africa’s gate. Lithium flows east; North America ends the grain deal; the Thaw feeds South America.'),
    dict(id=3, c='ICE', at=(108, 38), r=5, s=0.7, title='The Coolcells', line='Lithium packs charged by the Gobi’s sun run cooling through the hot nights, with skins that shed heat to the sky. Six in ten hot homes by 2285.'),
    dict(id=4, c='ICE', at=(78, 21), r=5, s=0.7, title='The Cool Halls', line='Public cooled halls on every hot level, open to all summer. In the worst heat of the 2270s they held millions through the nights.'),
    dict(id=5, c='POWER', at=(25, -10), r=3, s=0.5, title='Cooling for Sale', line='Africa’s cities, Europe’s burning south and South America’s north buy at a fair price. The money goes to a fund for Asia’s labs.'),
    dict(id=6, c='FOOD', at=(110, 58), r=4, s=0.6, title='The Short Harvest', line='2279: four continents eat from the Thaw, and the harvest falls short. Every share is cut by need, Asia’s plains included.'),
    dict(id=7, c='nam', at=(-100, 42), r=5, s=0.5, title='North America Alone', line='Europe turns down its grain; the Landbridge leaves its commons unanswered. “The Old World has its network. We have the Moon.”'),
  ])


ERAS[7].update(
  head='THE LAST CONTINENT', line='One market, the world’s biggest labs, cooled streets, a council across the Yenisei, and Oceania in',
  strength={'asi':1.55,'eur':1.15,'afr':1.15,'nam':0.9,'sam':0.95,'oce':1.05},
  ghost=[dict(what='asi', pts=[(6,22),(22,27),(38,29),(51,26),(62,36),(76,48),(87,57),(70,56),(50,53),(30,48),(16,40),(9,33),(6,24)]),
         dict(what='sam', pts=[(-38,-7),(-27,-3),(-15,2),(-4,5),(3,6)])],
  refs=[('to the Antarctic Peninsula', (-62, -49), 'r'), ('to the Ross Sea', (172, -48), 'l'), ('Ganges', (84, 25.5), 'r'), ('Yenisei', (87, 62), 'l')],
  hot=[('india','ICE',0.5,7),('eastchina','DATA',0.45,6),('siberia','PEOPLE',0.4,10),('australia','oce',0.4,8),('sahara','SUN',0.35,8),
       ('southwest','nam',0.3,5)],
  beats=[
    dict(id=1, c='POWER', at=(45, 45), r=6, s=0.6, title='One Market', line='2289: four continents trade power at one price. Asia earns the most and every profit goes to the labs. Africa sells for volume.'),
    dict(id=2, c='DATA', at=(119, 33), r=4, s=0.7, title='The Biggest Labs on Earth', line='By 2305 Asia’s labs lead the world in cooling, food, materials and networks.'),
    dict(id=3, c='ICE', at=(80, 26), r=5, s=0.7, title='Cool Streets', line='Shade canopies with cooled air, pale streets and cooling suits. The Ganges and Indus cities can work outside most summers.'),
    dict(id=4, c='HEAT', at=(72, 17), r=3, s=0.5, title='The 2293 Summer', line='Asia’s homes pay the market price too: cooling bills triple for three months. The halls and streets carry everyone else.'),
    dict(id=5, c='PEOPLE', at=(92, 60), r=5, s=0.6, title='The Yenisei Council', line='One council for the Thaw-born of both banks: bridges, river, wells and farms. “Neither East nor West.”'),
    dict(id=6, c='oce', flow=dict(what='oce', dep=2, pts=[(133,-14),(126,-9),(118,-4),(110,2),(106,8)]), title='Oceania Joins, 51–49', line='2297: food and minerals through a link into Asia. It keeps the relay and its share of the Southern Claim.'),
    dict(id=7, c='nam', at=(-88, -44), r=4, s=0.6, title='The Southern Claim', line='Bases on the Peninsula and the Ross Sea; the first iceberg reaches the dry south-west in 2301. No one challenges it.'),
  ])


ERAS[8].update(
  head='ONE WORLD', line='The Thaw stands on its own, North America comes in, and the Sunshade is tested under the Rain Pact',
  strength={'asi':1.3,'eur':1.1,'afr':1.15,'nam':1.05,'sam':0.95,'oce':1.05,'thw':1.0},
  transfers=[('thaw_all','asi','thw'), ('thaw_all','eur','thw'), ('thaw_all','centre','thw')],
  ghost=[dict(what='asi', pts=[(6,22),(22,27),(38,29),(51,26),(62,36),(76,48),(87,57),(70,56),(50,53),(30,48),(16,40),(9,33),(6,24)]),
         dict(what='sam', pts=[(-38,-7),(-27,-3),(-15,2),(-4,5),(3,6)]), dict(what='oce', pts=[(133,-14),(126,-9),(118,-4),(110,2),(106,8)])],
  refs=[('the Urals', (60, 58), 'l'), ('Bering Strait', (-169, 66), 'r'), ('Arabian Sea', (64, 15), 'l'), ('the Sahel', (2, 14), 'l')],
  hot=[('siberia','thw',0.5,12),('india','HEAT',0.35,6),('gulf','STAR',0.3,4),('newyork','nam',0.35,6),('eastchina','asi',0.35,6),
       ('sahara','WATER',0.3,8),('amazon','sam',0.3,7)],
  beats=[
    dict(id=1, c='thw', at=(122, 62), r=7, s=0.7, title='The Thaw Stands', line='2314: Asia lets it go and Europe follows. The Thaw, Urals to Bering, 150 million people, its own network and the sixth seat. Its first act: a fifty-year grain deal with Asia.'),
    dict(id=2, c='nam', flow=dict(what='nam', dep=2, pts=[(-75,42),(-55,47),(-35,50),(-15,50),(-5,48)]), title='North America Comes In', line='2318: the open watch from day one; the old logs sealed until 2350. Seventh member. Every network on Earth can reach every other.'),
    dict(id=3, c='WATER', at=(30, 34), r=4, s=0.5, title='The Rain Pact', line='2321: all seven sign first. Whoever loses rain to the shade gets water, food and places from everyone else.'),
    dict(id=4, c='STAR', at=(64, 15), r=5, s=0.7, title='The Test', line='2324–2329 over the Arabian Sea, watched by all. A full shade: half the worst heat days, rain shifted south across the Sahel. The Amazon still uncertain.'),
    dict(id=5, c='sam', at=(-50, -4), r=4, s=0.5, title='The Last No', line='South America won’t say yes until it knows what the shade does to the Amazon’s rain.'),
    dict(id=6, c='asi', at=(106, 27), r=5, s=0.5, title='Asia, Smaller', line='Half its land and all its gas gone. Still the richest, with the biggest labs, and it leads a Landbridge that is now the whole world.'),
  ])


ERAS[9].update(
  head='THE BURST', line='The Thaw’s ground lets go; South America leads the relief, the world builds the Sunshade, and Asia makes cooling free',
  event='THE METHANE BURST',
  strength={'asi':1.35,'eur':1.1,'afr':1.15,'nam':1.0,'sam':1.05,'oce':1.0,'thw':0.95},
  ghost=[dict(what='asi', pts=[(6,22),(22,27),(38,29),(51,26),(62,36),(76,48),(87,57),(70,56),(50,53),(30,48),(16,40),(9,33),(6,24)]),
         dict(what='nam', pts=[(-75,42),(-55,47),(-35,50),(-15,50),(-5,48)]), dict(what='sam', pts=[(-38,-7),(-27,-3),(-15,2),(-4,5),(3,6)]),
         dict(what='oce', pts=[(133,-14),(126,-9),(118,-4),(110,2),(106,8)])],
  refs=[('the Andes', (-68, -20), 'l'), ('Lena', (126, 70), 'l'), ('the Sahel', (2, 14), 'l'), ('Ganges', (84, 25.5), 'r')],
  hot=[('siberia','HEAT',0.6,13),('india','ICE',0.45,7),('eastchina','ICE',0.35,6),('amazon','WATER',0.4,8),('sahara','WATER',0.3,8),
       ('gulf','STAR',0.3,5)],
  beats=[
    dict(id=1, c='HEAT', at=(128, 60), r=7, s=0.7, title='The Ground Lets Go', line='The 2330s: the deep permafrost gives way. Craters, slumping towns, the tundra burning. The old wells near the towns hold; the far ground pours out.'),
    dict(id=2, c='sam', flow=dict(what='sam', dep=2, pts=[(-62,-12),(-40,2),(-12,22),(15,38),(45,52),(80,60),(105,62)]), title='South America Leads the Relief', line='Heavy-lift craft from the Andes carry shelters and lithium north. Europe and the Thaw rebuild on safe ground; the Landbridge pays. The Thaw’s council falls in 2338 for hiding the warming.'),
    dict(id=3, c='WATER', at=(-58, -4), r=5, s=0.6, title='The Amazon Guarantee', line='2333: all seven sign. If the shade cuts the Amazon’s rain, the Landbridge replaces it with towers and payments. South America says yes.'),
    dict(id=4, c='STAR', at=(60, 6), r=9, s=0.55, title='The Sunshade', line='2336: built and run by all seven. The burst’s heat cancelled, the worst heat days halved. The rain shifts south over the Sahel; the Rain Pact pays.'),
    dict(id=5, c='ICE', at=(84, 19), r=5, s=0.7, title='Free Cooling', line='2335: coolcells and their power in every home, paid by the labs and the public purse. By 2342 home cooling is free; new research slows.'),
    dict(id=6, c='DATA', at=(-112, 50), r=4, s=0.5, title='The Archive Opens', line='1 January 2350: no Landbridge traffic seen, but fifty years of every relay member’s pattern logged, Oceania’s included.'),
  ])


FINALE = dict(
  title='THE OPEN GATE',
  sub='2350 · how each bloc’s own people judged its century',
  # delivered, out of reach (the world: events and the draft), let down
  verdict={'asi': (74, 7, 19), 'eur': (58, 14, 28), 'oce': (60, 8, 32), 'sam': (50, 20, 30), 'afr': (52, 10, 38), 'thw': (44, 18, 38), 'nam': (45, 10, 45)},
  arcs={
    'asi': 'Sealed and short of power in 2145; in 2350 it leads one world network, with free cooling in every home. It gave away half its land.',
    'eur': 'Settlers in the Thaw, tapped for forty years, frozen by the Atlantic, fed by Asia. Warm again, west of the Urals.',
    'oce': 'Closed for a century, then on the relay, then in the Landbridge by 51 to 49. Logged by the relay it trusted.',
    'sam': 'Broken by the Amazon’s tipping at the start. Launch sites, lithium, the fourth seat, and the leader of the Thaw’s relief.',
    'afr': 'The century’s sun. Caught tapping two blocs, its leaders fell; the council rebuilt trust through the Landbridge.',
    'thw': 'Machines, then settlers, then 150 million people. A nation in 2314, burned in the 2330s, rebuilt on safe ground.',
    'nam': 'Opened the Arctic, built the road to the Moon, and spent the century outside. In at last, and watched.',
  },
  networks=[dict(what='asi', pts=[(6,22),(22,27),(38,29),(51,26),(62,36),(76,48),(87,57),(70,56),(50,53),(30,48),(16,40),(9,33),(6,24)]),
            dict(what='sam', pts=[(-38,-7),(-27,-3),(-15,2),(-4,5),(3,6)]), dict(what='nam', pts=[(-75,42),(-55,47),(-35,50),(-15,50),(-5,48)]),
            dict(what='oce', pts=[(133,-14),(126,-9),(118,-4),(110,2),(106,8)]), dict(what='thw', pts=[(112,55),(108,48),(104,42)])],
  draft='The draft: the Amazon tips (the prologue, Asia’s own card) · fired: the water towers fail (III), the Atlantic current collapses (V), the methane burst (X) · never fired: the heat ceiling, the fast sea rise',
)
