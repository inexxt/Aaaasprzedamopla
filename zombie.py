import sys
sys.path.append("/home/kajetan/Aaaasprzedamopla")
from models import Human, Zombie, ALL_HUMANS, ALL_ZOMBIES, MAP
import settings
from itertools import product
import json
from tqdm import tqdm


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

import multiprocessing as mp
from helpers import flatten


def parmap(f, ll):
    with mp.Pool(processes=mp.cpu_count()) as p:
        ret = p.map(f, ll)
    return ret


for t in tqdm(range(24 * 60)):
    # settings.P_ZOMBIE_DIES += h # Temporarliy turned off - modification of state
    # HISTORY BOOKKEEPING
    humans = [tuple(x.pos) for x in ALL_HUMANS]
    zombies = [tuple(x.pos) for x in ALL_ZOMBIES]
    ts.append((humans, zombies))

    def upd(x):
        x.update()
    zz = ALL_ZOMBIES.copy()
    hh = ALL_HUMANS.copy()
    parmap(upd, zz)
    parmap(upd, hh)

    for z in zz:
        z.unremove_from_grid()
    for h in hh:
        h.unremove_from_grid()

    ts2.append(dict(humans=len(humans), zombies=len(zombies), all=len(humans)+len(zombies)))

with open('Visualisation/ts0.js', 'w') as outfile:
    outfile.write(f"locs = {json.dumps(ts)},\n")
