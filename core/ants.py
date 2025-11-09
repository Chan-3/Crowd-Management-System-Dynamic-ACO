"""Ant Colony Optimization module"""
import random
from config import ACOConfig
from utils import weighted_random_choice, get_random_empty_cell

class Ant:
    def __init__(self, x, y, ant_id):
        self.x = x
        self.y = y
        self.id = ant_id
        self.path = [(x, y)]
        self.visited = {(x, y)}
        self.found_exit = False
        self.stuck_counter = 0
        
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.path = [(x, y)]
        self.visited = {(x, y)}
        self.found_exit = False
        self.stuck_counter = 0
    
    def move(self, grid, pheromone_map):
        if self.found_exit:
            return
        if grid.is_exit(self.x, self.y):
            self.found_exit = True
            return
        neighbors = grid.get_walkable_neighbors(self.x, self.y)
        if not neighbors:
            self.stuck_counter += 1
            if self.stuck_counter > 5:
                new_pos = get_random_empty_cell(grid)
                self.reset(new_pos[0], new_pos[1])
            return
        probabilities = []
        valid_neighbors = []
        for nx, ny in neighbors:
            if (nx, ny) in self.visited and len(neighbors) > 1:
                continue
            pheromone = pheromone_map.get(nx, ny)
            exit_pos = grid.get_nearest_exit(nx, ny)
            distance = abs(nx - exit_pos[0]) + abs(ny - exit_pos[1]) + 1
            heuristic = 1.0 / distance
            prob = (pheromone ** ACOConfig.ALPHA) * (heuristic ** ACOConfig.BETA)
            probabilities.append(prob)
            valid_neighbors.append((nx, ny))
        if not valid_neighbors:
            valid_neighbors = neighbors
            probabilities = [1.0] * len(neighbors)
        if valid_neighbors:
            next_cell = weighted_random_choice(valid_neighbors, probabilities)
            if next_cell:
                self.x, self.y = next_cell
                self.path.append((self.x, self.y))
                self.visited.add((self.x, self.y))
                self.stuck_counter = 0
    
    def get_path_length(self):
        return len(self.path)
    
    def get_path_quality(self):
        if not self.found_exit:
            return 0.0
        return ACOConfig.Q / self.get_path_length()

class AntColony:
    def __init__(self, grid, pheromone_map, num_ants=ACOConfig.ANT_COUNT):
        self.grid = grid
        self.pheromone_map = pheromone_map
        self.num_ants = num_ants
        self.ants = []
        self.best_path_length = float('inf')
        self.iteration = 0
        
    def initialize_ants(self):
        self.ants.clear()
        for i in range(self.num_ants):
            pos = get_random_empty_cell(self.grid)
            ant = Ant(pos[0], pos[1], i)
            self.ants.append(ant)
    
    def run_iteration(self):
        for ant in self.ants:
            max_moves = 100
            moves = 0
            while not ant.found_exit and moves < max_moves:
                ant.move(self.grid, self.pheromone_map)
                moves += 1
        successful_ants = [ant for ant in self.ants if ant.found_exit]
        if successful_ants:
            for ant in successful_ants:
                quality = ant.get_path_quality()
                self.pheromone_map.deposit_path(ant.path, quality)
                path_len = ant.get_path_length()
                if path_len < self.best_path_length:
                    self.best_path_length = path_len
        self.pheromone_map.evaporate()
        self.initialize_ants()
        self.iteration += 1
        return {
            'iteration': self.iteration,
            'successful_ants': len(successful_ants),
            'best_path_length': self.best_path_length if self.best_path_length != float('inf') else 0,
            'avg_pheromone': self.pheromone_map.get_average_value()
        }
    
    def get_ants(self):
        return self.ants