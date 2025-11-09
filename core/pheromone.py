"""Pheromone management module"""
import numpy as np
from config import ACOConfig, GridConfig

class PheromoneMap:
    def __init__(self, size=GridConfig.SIZE):
        self.size = size
        self.map = np.ones((size, size), dtype=float) * 0.01
        self.evaporation_rate = ACOConfig.EVAPORATION
        
    def reset(self):
        self.map = np.ones((self.size, self.size), dtype=float) * 0.01
    
    def get(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.map[x, y]
        return 0.0
    
    def deposit(self, x, y, amount):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.map[x, y] += amount
            self.map[x, y] = min(self.map[x, y], 10.0)
    
    def deposit_path(self, path, amount):
        for x, y in path:
            self.deposit(x, y, amount)
    
    def evaporate(self):
        self.map *= (1.0 - self.evaporation_rate)
        self.map = np.maximum(self.map, 0.01)
    
    def get_max_value(self):
        return np.max(self.map)
    
    def get_average_value(self):
        return np.mean(self.map)
    
    def normalize_for_display(self):
        max_val = self.get_max_value()
        if max_val <= 0:
            return np.zeros((self.size, self.size), dtype=np.uint8)
        normalized = (self.map / max_val * 255).astype(np.uint8)
        return normalized