import sys
sys.path.append("/home/kajetan/Aaaasprzedamopla")
from models import Human, Zombie, ALL_HUMANS, ALL_ZOMBIES, MAP
import settings
from itertools import product
import json

import random
for _ in range(100):
    random_point = (random.random()*MAP.width, random.random()*MAP.height)
    while MAP.does_collide(random_point):
        random_point = (random.random() * MAP.width, random.random() * MAP.height)
    Human(random_point)

for _ in range(30):
    random_point = (random.random()*MAP.width, random.random()*MAP.height)
    while MAP.does_collide(random_point):
        random_point = (random.random() * MAP.width, random.random() * MAP.height)
    Zombie(random_point)

grid_iter = list(
    product(list(range(settings.GRID_SIZE_X)),
            list(range(settings.GRID_SIZE_Y)))
)


ts = list()
ts2 = list()

h = 0.5 / (24 * 60)

for t in range(1 * 60):
    settings.P_ZOMBIE_DIES += h
    humans = list()
    zombies = list()
    for zombie in ALL_ZOMBIES.copy():
        zombies.append(tuple(zombie.pos))
        zombie.update()
    for human in ALL_HUMANS.copy():
        humans.append(tuple(human.pos))
        human.update()
    ts.append((humans.copy(), zombies.copy()))
    ts2.append(dict(humans=len(humans), zombies=len(zombies), all=len(humans)+len(zombies)))

with open('Visualisation/ts0.js', 'w') as outfile:
    outfile.write(f"locs = {json.dumps(ts)},\n")
