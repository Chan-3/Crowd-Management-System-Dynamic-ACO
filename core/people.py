"""Human evacuation agents module"""
from collections import deque
from config import EvacuationConfig, ACOConfig
from utils import weighted_random_choice, get_random_empty_cell

class Person:
    def __init__(self, x, y, person_id):
        self.x = x
        self.y = y
        self.id = person_id
        self.active = True
        self.path_history = deque(maxlen=10)
        self.path_history.append((x, y))
        self.evacuated = False
        self.evacuation_time = 0
        self.reroute_count = 0
        self.stuck_counter = 0
        
    def move(self, grid, pheromone_map, all_people):
        if not self.active or self.evacuated:
            return
        if grid.is_exit(self.x, self.y):
            self.evacuated = True
            self.active = False
            return
        if grid.has_fire(self.x, self.y):
            self.active = False
            return
        neighbors = grid.get_walkable_neighbors(self.x, self.y)
        if not neighbors:
            self.stuck_counter += 1
            if self.stuck_counter > 10:
                new_pos = get_random_empty_cell(grid)
                self.x, self.y = new_pos
                self.stuck_counter = 0
                self.reroute_count += 1
            return
        scores = []
        valid_neighbors = []
        for nx, ny in neighbors:
            score = self.calculate_move_score(nx, ny, grid, pheromone_map, all_people)
            if score > 0:
                scores.append(score)
                valid_neighbors.append((nx, ny))
        if valid_neighbors and scores:
            next_cell = weighted_random_choice(valid_neighbors, scores)
            if next_cell:
                self.x, self.y = next_cell
                self.path_history.append((self.x, self.y))
                self.stuck_counter = 0
        self.evacuation_time += 1
    
    def calculate_move_score(self, x, y, grid, pheromone_map, all_people):
        pheromone = pheromone_map.get(x, y)
        exit_pos = grid.get_nearest_exit(x, y)
        distance = abs(x - exit_pos[0]) + abs(y - exit_pos[1]) + 1
        heuristic = 1.0 / distance
        fire_penalty = self.get_fire_penalty(x, y, grid)
        congestion = self.get_congestion_factor(x, y, all_people)
        score = (pheromone ** ACOConfig.ALPHA) * (heuristic ** ACOConfig.BETA)
        score *= fire_penalty * congestion
        return max(0.0, score)
    
    def get_fire_penalty(self, x, y, grid):
        if grid.has_fire(x, y):
            return 0.0
        fire_dist = grid.get_fire_distance(x, y)
        if fire_dist >= 5:
            return 1.0
        penalty = EvacuationConfig.FIRE_PENALTY ** (5 - fire_dist)
        return max(0.01, penalty)
    
    def get_congestion_factor(self, x, y, all_people):
        count = 0
        radius = EvacuationConfig.CONGESTION_RADIUS
        for person in all_people:
            if not person.active or person.id == self.id:
                continue
            dist = abs(person.x - x) + abs(person.y - y)
            if dist <= radius:
                count += 1
        if count == 0:
            return 1.0
        factor = 1.0 / (1.0 + EvacuationConfig.CONGESTION_PENALTY * count)
        return max(0.1, factor)

class PeopleManager:
    def __init__(self, grid):
        self.grid = grid
        self.people = []
        
    def initialize_people(self, count):
        self.people.clear()
        for i in range(count):
            pos = get_random_empty_cell(self.grid, self.grid.exits)
            person = Person(pos[0], pos[1], i)
            self.people.append(person)
    
    def update_all(self, pheromone_map):
        for person in self.people:
            if person.active:
                person.move(self.grid, pheromone_map, self.people)
    
    def get_statistics(self):
        total = len(self.people)
        evacuated = sum(1 for p in self.people if p.evacuated)
        remaining = sum(1 for p in self.people if p.active)
        casualties = total - evacuated - remaining
        avg_time = 0
        if evacuated > 0:
            avg_time = sum(p.evacuation_time for p in self.people if p.evacuated) / evacuated
        total_reroutes = sum(p.reroute_count for p in self.people)
        return {
            'total': total,
            'evacuated': evacuated,
            'remaining': remaining,
            'casualties': casualties,
            'progress': (evacuated / total * 100) if total > 0 else 0,
            'avg_evacuation_time': avg_time,
            'total_reroutes': total_reroutes
        }
    
    def has_active_people(self):
        return any(p.active for p in self.people)
    
    def get_people(self):
        return self.people
    
    def get_active_people(self):
        return [p for p in self.people if p.active]