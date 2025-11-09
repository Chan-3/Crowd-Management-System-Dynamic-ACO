"""Grid management module"""
from config import GridConfig, ObstaclePatterns
from utils import get_neighbors_4, distribute_evenly

class Grid:
    def __init__(self, size=GridConfig.SIZE):
        self.size = size
        self.walls = set()
        self.exits = []
        self.fire_cells = set()
        
    def reset(self):
        self.walls.clear()
        self.exits.clear()
        self.fire_cells.clear()
    
    def initialize_obstacles(self):
        self.walls.clear()
        u_shapes = ObstaclePatterns.create_u_shapes(self.size)
        for pos in u_shapes:
            self.walls.add(pos)
        pillars = ObstaclePatterns.create_pillars(self.size)
        for pos in pillars:
            self.walls.add(pos)
        hallways = ObstaclePatterns.create_hallways(self.size)
        for pos in hallways:
            self.walls.add(pos)
    
    def initialize_exits(self, count):
        self.exits.clear()
        positions = distribute_evenly(count, self.size, 'exit')
        for pos in positions:
            if pos not in self.walls:
                self.exits.append(pos)
        corners = [(0, 0), (self.size-1, 0), (0, self.size-1), (self.size-1, self.size-1)]
        for corner in corners:
            if len(self.exits) >= count:
                break
            if corner not in self.walls and corner not in self.exits:
                self.exits.append(corner)
    
    def add_fire(self, x, y):
        if self.is_valid(x, y) and (x, y) not in self.walls:
            self.fire_cells.add((x, y))
    
    def remove_fire(self, x, y):
        self.fire_cells.discard((x, y))
    
    def toggle_wall(self, x, y):
        if not self.is_valid(x, y):
            return
        pos = (x, y)
        if pos in self.walls:
            self.walls.discard(pos)
        else:
            self.walls.add(pos)
    
    def is_valid(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size
    
    def is_walkable(self, x, y):
        if not self.is_valid(x, y):
            return False
        pos = (x, y)
        return pos not in self.walls and pos not in self.fire_cells
    
    def is_exit(self, x, y):
        return (x, y) in self.exits
    
    def has_fire(self, x, y):
        return (x, y) in self.fire_cells
    
    def get_nearest_exit(self, x, y):
        if not self.exits:
            return (self.size // 2, self.size // 2)
        nearest = self.exits[0]
        min_dist = abs(x - nearest[0]) + abs(y - nearest[1])
        for exit_pos in self.exits[1:]:
            dist = abs(x - exit_pos[0]) + abs(y - exit_pos[1])
            if dist < min_dist:
                min_dist = dist
                nearest = exit_pos
        return nearest
    
    def get_walkable_neighbors(self, x, y):
        neighbors = get_neighbors_4(x, y, self.size)
        return [n for n in neighbors if self.is_walkable(n[0], n[1])]
    
    def get_all_walkable_neighbors(self, x, y):
        neighbors = get_neighbors_4(x, y, self.size)
        return [n for n in neighbors if n not in self.walls]
    
    def get_fire_distance(self, x, y):
        if not self.fire_cells:
            return 999
        min_dist = 999
        for fx, fy in self.fire_cells:
            dist = abs(x - fx) + abs(y - fy)
            min_dist = min(min_dist, dist)
        return min_dist