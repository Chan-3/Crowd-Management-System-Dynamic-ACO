"""Utility functions"""
import math
import random

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_neighbors_4(x, y, grid_size):
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            neighbors.append((nx, ny))
    return neighbors

def get_neighbors_8(x, y, grid_size):
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                neighbors.append((nx, ny))
    return neighbors

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def validate_input(value, min_val, max_val, default):
    try:
        num = int(value)
        return clamp(num, min_val, max_val)
    except:
        return default

def weighted_random_choice(choices, weights):
    if not choices or not weights:
        return None
    total = sum(weights)
    if total <= 0:
        return random.choice(choices)
    weights = [w / total for w in weights]
    r = random.random()
    cumulative = 0
    for choice, weight in zip(choices, weights):
        cumulative += weight
        if r <= cumulative:
            return choice
    return choices[-1]

def get_random_empty_cell(grid_obj, avoid_list=None):
    avoid_list = avoid_list or []
    for _ in range(1000):
        x = random.randint(0, grid_obj.size - 1)
        y = random.randint(0, grid_obj.size - 1)
        if grid_obj.is_walkable(x, y) and (x, y) not in avoid_list:
            return x, y
    for y in range(grid_obj.size):
        for x in range(grid_obj.size):
            if grid_obj.is_walkable(x, y) and (x, y) not in avoid_list:
                return x, y
    return 0, 0

def distribute_evenly(count, grid_size, cell_type='exit'):
    positions = []
    if count <= 0:
        return positions
    edges = []
    edges.extend([(x, 0) for x in range(grid_size)])
    edges.extend([(x, grid_size-1) for x in range(grid_size)])
    edges.extend([(0, y) for y in range(1, grid_size-1)])
    edges.extend([(grid_size-1, y) for y in range(1, grid_size-1)])
    if count >= len(edges):
        return edges[:count]
    step = len(edges) // count
    for i in range(count):
        idx = i * step
        positions.append(edges[idx])
    return positions