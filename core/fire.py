"""Fire simulation module"""
import random
from config import FireConfig
from utils import get_random_empty_cell

class Fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.intensity = 1
        self.age = 0
        
    def update(self):
        self.age += 1
        if self.age > 0 and self.age % FireConfig.INTENSITY_GROWTH_RATE == 0:
            if self.intensity < FireConfig.MAX_INTENSITY:
                self.intensity += 1
    
    def get_spread_probability(self):
        return FireConfig.SPREAD_RATE * self.intensity

class FireManager:
    def __init__(self, grid):
        self.grid = grid
        self.fires = []
        self.spawn_countdown = FireConfig.SPAWN_DELAY
        self.initial_fire_count = 0
        self.spawned = False
        
    def set_fire_count(self, count):
        self.initial_fire_count = count
    
    def reset(self):
        self.fires.clear()
        self.grid.fire_cells.clear()
        self.spawn_countdown = FireConfig.SPAWN_DELAY
        self.spawned = False
    
    def update(self, time_step):
        if not self.spawned and time_step >= FireConfig.SPAWN_DELAY:
            self.spawn_initial_fires()
            self.spawned = True
        for fire in self.fires:
            fire.update()
        self.spread_fire()
    
    def spawn_initial_fires(self):
        if self.initial_fire_count <= 0:
            return
        for _ in range(self.initial_fire_count):
            for _ in range(50):
                pos = get_random_empty_cell(self.grid, self.grid.exits)
                min_exit_dist = min(
                    abs(pos[0] - ex[0]) + abs(pos[1] - ex[1])
                    for ex in self.grid.exits
                )
                if min_exit_dist > 10:
                    self.add_fire(pos[0], pos[1])
                    break
    
    def add_fire(self, x, y):
        if not self.grid.is_valid(x, y):
            return
        if (x, y) in self.grid.walls or (x, y) in self.grid.exits:
            return
        if not self.grid.has_fire(x, y):
            fire = Fire(x, y)
            self.fires.append(fire)
            self.grid.add_fire(x, y)
    
    def spread_fire(self):
        new_fires = []
        for fire in self.fires:
            neighbors = self.grid.get_all_walkable_neighbors(fire.x, fire.y)
            spread_prob = fire.get_spread_probability()
            for nx, ny in neighbors:
                if self.grid.has_fire(nx, ny):
                    continue
                if random.random() < spread_prob:
                    new_fires.append((nx, ny))
        for x, y in new_fires:
            self.add_fire(x, y)
    
    def get_fire_cells(self):
        return [(f.x, f.y) for f in self.fires]
    
    def get_fire_count(self):
        return len(self.fires)
    
    def get_fires(self):
        return self.fires