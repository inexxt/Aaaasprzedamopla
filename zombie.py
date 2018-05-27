import sys
sys.path.append("/home/kajetan/Aaaasprzedamopla")
from models import Human, Zombie, ALL_HUMANS, ALL_ZOMBIES
import settings
from itertools import product
import json

import random
for _ in range(100):
    Human((random.random()*settings.MAP_SIZE_X, random.random()*settings.MAP_SIZE_Y))

for _ in range(100):
    Zombie((random.random()*settings.MAP_SIZE_X, random.random()*settings.MAP_SIZE_Y))

grid_iter = list(
    product(list(range(settings.GRID_SIZE_X)),
            list(range(settings.GRID_SIZE_Y)))
)


ts = list()
ts2 = list()

for t in range(60):
    humans = list()
    zombies = list()
    for zombie in ALL_ZOMBIES.copy():
        zombies.append(tuple(zombie.pos))
        zombie.update()
    for human in ALL_HUMANS.copy():
        humans.append(tuple(human.pos))
        human.update()
    ts.append((humans.copy(), zombies.copy()))
    ts2.append((len(humans), len(zombies)))

with open('Visualisation/ts0.js', 'w') as outfile:
    json.dump(ts, outfile)