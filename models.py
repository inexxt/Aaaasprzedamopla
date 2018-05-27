import numpy as np
import random
import json

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from scipy.spatial import KDTree

import settings
import helpers

HUMAN_INDEX = 1
ZOMBIE_INDEX = 1


class Map(object):
    def __init__(self, fname="./buildings_backup_meters.json", map_fname="./polygon_poznan_meters.json"):
        with open(fname, "r") as f:
            b_backup = json.load(f)
            buildings = b_backup['buildings']
        with open(map_fname, "r") as f:
            self.map_poly = json.load(f)["boundary"]

        self.width, self.height = b_backup["_11"]
        self.buildings_dict = {helpers.mean(x): x for x in buildings}
        self.bmeans = list(self.buildings_dict.keys())
        self.tree = KDTree(list(self.bmeans))

    def does_collide(self, finish_point):
        ks = self.tree.query(finish_point, k=5)
        for k in ks[1]:
            p = self.buildings_dict[self.bmeans[k]]
            poly = Polygon(p)
            point = Point(finish_point[0], finish_point[1])
            if poly.contains(point):
                return True
        return False

    def out_of_map(self, xy):
        return helpers.out_of_poly(xy, self.map_poly)

    def going_out_of_map(self, xy):
        return helpers.going_out_of_poly(xy, self.map_poly)

    def validate(self, pos, vector):
        finish_point = pos + vector
        sp = (pos, finish_point)
        ks = self.tree.query(finish_point, k=5)
        for k in ks[1]:
            p = self.buildings_dict[self.bmeans[k]]
            for ab in zip(p + [p[0]], [p[-1]] + p):
                if helpers.intersect(sp, ab):
                    return helpers.solution(sp, ab)
        return finish_point

    def get_square(self, pos):
        return max(0, min(int(settings.GRID_SIZE_X * (pos[0] / self.width)), settings.GRID_SIZE_X - 1)),\
               max(0, min(int(settings.GRID_SIZE_Y * (pos[1] / self.height)), settings.GRID_SIZE_Y - 1))


MAP = Map()

HUMANS_GRID = np.array([[set() for _ in range(settings.GRID_SIZE_X)] for __ in range(settings.GRID_SIZE_Y)])
ZOMBIES_GRID = np.array([[set() for _ in range(settings.GRID_SIZE_X)] for __ in range(settings.GRID_SIZE_Y)])
ALL_HUMANS = set()
ALL_ZOMBIES = set()


class Agent(object):
    def __init__(self, pos):
        if not isinstance(pos, np.ndarray):
            self.pos = np.array(pos)
        else:
            self.pos = pos
        self.add_to_set()
        self.grid_x, self.grid_y = MAP.get_square(pos)
        self.attach_to_grid()

    def attach_to_grid(self):
        pass

    def remove_from_grid(self):
        pass

    def add_to_set(self):
        pass

    def remove_from_set(self):
        pass

    def kill(self):
        self.remove_from_set()
        self.remove_from_grid()

    def dist(self, agent):
        return np.linalg.norm(self.pos - agent.pos)

    def update_pos(self, pos):
        self.remove_from_grid()

        if MAP.going_out_of_map((self.pos, pos)):
            self.remove_from_set()
            return

        if not isinstance(pos, np.ndarray):
            self.pos = np.array(pos)
        else:
            self.pos = pos

        self.grid_x, self.grid_y = MAP.get_square(pos)
        self.attach_to_grid()

    def update(self):
        pass

    def random_walk(self, power=1.):
        if power > 0.1:
            potential_vector = np.random.normal(scale=power, size=2)
            vector_validated = MAP.validate(self.pos, potential_vector)
            power -= np.linalg.norm(vector_validated - self.pos)
            self.update_pos(vector_validated)
            self.random_walk(power=power / 2)  # zderzenie z przeszkodą

    def adjacent_squares(self):
        return zip(range(min(0, self.grid_x - 1), max(settings.GRID_SIZE_X, self.grid_x + 1)),
                   range(min(0, self.grid_y - 1), max(settings.GRID_SIZE_Y, self.grid_y + 1)))


class Zombie(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        self.age = random.choice(range(settings.ZOMBIE_MAX_AGE))
        # global ZOMBIE_INDEX
        # self.name = f"Zombie {ZOMBIE_INDEX}"
        # ZOMBIE_INDEX += 1

    def chase_human(self, human):
        chase_vector = (human.pos - self.pos)
        chase_v_norm = np.linalg.norm(human.pos - self.pos)
        if chase_v_norm > 1:
            chase_vector /= chase_v_norm

        chase_validated = MAP.validate(self.pos, chase_vector)
        power = 1 - np.linalg.norm(chase_validated - self.pos)
        self.update_pos(chase_validated)
        self.random_walk(power=power / 2)  # zderzenie z przeszkodą

    def add_to_set(self):
        ALL_ZOMBIES.add(self)

    def remove_from_set(self):
        ALL_ZOMBIES.remove(self)

    def attach_to_grid(self):
        ZOMBIES_GRID[self.grid_x, self.grid_y].add(self)

    def remove_from_grid(self):
        ZOMBIES_GRID[self.grid_x, self.grid_y].remove(self)

    def update(self):
        if self.age > settings.ZOMBIE_MAX_AGE:
            self.kill()
            return
        self.age += 1
        potential_humans = set()

        # Okoliczne kwadraciki.
        for gx, gy in self.adjacent_squares():
            potential_humans |= HUMANS_GRID[gx, gy]

        if potential_humans:
            human = min(potential_humans, key=lambda h: self.dist(h))
            if self.dist(human) > settings.ZOMBIE_PROXIMITY:
                self.random_walk()
            elif self.dist(human) > settings.ZOMBIE_FIGHT:
                self.chase_human(human)
            else:
                self.fight(human, potential_humans)
        self.random_walk()

    def fight(self, human, potential_humans):
        potential_zombies = set()
        for gx, gy in self.adjacent_squares():
            potential_zombies |= ZOMBIES_GRID[gx, gy]
        nof_humans = len(list(filter(lambda h: self.dist(h) <= settings.ZOMBIE_FIGHT, potential_humans)))
        nof_zombies = len(list(filter(lambda z: self.dist(z) <= settings.ZOMBIE_FIGHT, potential_zombies)))

        if nof_zombies != 0:
            p_zombie_dies = settings.P_ZOMBIE_DIES * (nof_humans / nof_zombies)
            zombie_dies = p_zombie_dies > random.random()
        else:
            zombie_dies = True

        if zombie_dies:
            self.age = settings.ZOMBIE_MAX_AGE + 1
        else:
            self.infect(human)

    def infect(self, human):
        self.age = min(0, self.age - settings.BRAIN_VALUE)
        Zombie(human.pos)
        human.kill()


class Human(Agent):
    def __init__(self, pos):
        super().__init__(pos)
        # global HUMAN_INDEX
        # self.name = f"Human {HUMAN_INDEX}"
        # HUMAN_INDEX += 1

    def attach_to_grid(self):
        HUMANS_GRID[self.grid_x, self.grid_y].add(self)

    def remove_from_grid(self):
        HUMANS_GRID[self.grid_x, self.grid_y].remove(self)

    def add_to_set(self):
        ALL_HUMANS.add(self)

    def remove_from_set(self):
        ALL_HUMANS.remove(self)

    def run_away(self, zombie):
        chase_vector = 2 * (-(zombie.pos - self.pos) / np.linalg.norm(zombie.pos - self.pos))

        chase_validated = MAP.validate(self.pos, chase_vector)
        power = 2 - np.linalg.norm(chase_validated - self.pos)
        self.update_pos(chase_validated)
        self.random_walk(power=power / 2)  # zderzenie z przeszkodą

    def update(self):
        potential_zombies = set()

        # Okoliczne kwadraciki.
        for gx, gy in self.adjacent_squares():
            potential_zombies |= ZOMBIES_GRID[gx, gy]

        if potential_zombies:
            zombie = min(potential_zombies, key=lambda z: self.dist(z))
            if self.dist(zombie) > settings.ZOMBIE_PROXIMITY:
                self.random_walk()
            elif self.dist(zombie) > settings.ZOMBIE_FIGHT:
                self.run_away(zombie)

        self.random_walk()