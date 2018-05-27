import sys
sys.path.append("/home/kajetan/Aaaasprzedamopla")
from models import Human, Zombie, ALL_HUMANS, ALL_ZOMBIES
import settings
from itertools import product
import json

import random
for _ in range(1000):
    Human((random.random()*settings.MAP_SIZE_X, random.random()*settings.MAP_SIZE_Y))

for _ in range(300):
    Zombie((random.random()*settings.MAP_SIZE_X, random.random()*settings.MAP_SIZE_Y))

grid_iter = list(
    product(list(range(settings.GRID_SIZE_X)),
            list(range(settings.GRID_SIZE_Y)))
)


ts = list()
ts2 = list()

h = 0.5 / (24 * 60)

for t in range(24 * 60):
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
    ts2.append((len(humans), len(zombies)))

with open('Visualisation/ts0.js', 'w') as outfile:
    outfile.write("locs = " + json.dumps(ts))