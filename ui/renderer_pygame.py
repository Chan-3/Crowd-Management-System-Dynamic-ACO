"""Pygame renderer"""
import pygame
from config import UIConfig, CELL_SIZE

class Renderer:
    def __init__(self, surface, offset_x, offset_y):
        self.surface = surface
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.cell_size = CELL_SIZE
        
    def grid_to_screen(self, x, y):
        screen_x = self.offset_x + x * self.cell_size
        screen_y = self.offset_y + y * self.cell_size
        return screen_x, screen_y
    
    def screen_to_grid(self, screen_x, screen_y):
        grid_x = (screen_x - self.offset_x) // self.cell_size
        grid_y = (screen_y - self.offset_y) // self.cell_size
        return grid_x, grid_y
    
    def draw_grid_background(self, grid_size):
        grid_width = grid_size * self.cell_size
        grid_height = grid_size * self.cell_size
        grid_rect = pygame.Rect(self.offset_x, self.offset_y, grid_width, grid_height)
        pygame.draw.rect(self.surface, UIConfig.BG_COLOR, grid_rect)
        for x in range(grid_size + 1):
            start_x = self.offset_x + x * self.cell_size
            pygame.draw.line(self.surface, UIConfig.GRID_COLOR,
                           (start_x, self.offset_y), (start_x, self.offset_y + grid_height), 1)
        for y in range(grid_size + 1):
            start_y = self.offset_y + y * self.cell_size
            pygame.draw.line(self.surface, UIConfig.GRID_COLOR,
                           (self.offset_x, start_y), (self.offset_x + grid_width, start_y), 1)
    
    def draw_cell(self, x, y, color):
        screen_x, screen_y = self.grid_to_screen(x, y)
        rect = pygame.Rect(screen_x + 1, screen_y + 1, self.cell_size - 2, self.cell_size - 2)
        pygame.draw.rect(self.surface, color, rect)
    
    def draw_circle(self, x, y, color, radius_ratio=0.4):
        screen_x, screen_y = self.grid_to_screen(x, y)
        center_x = screen_x + self.cell_size // 2
        center_y = screen_y + self.cell_size // 2
        radius = int(self.cell_size * radius_ratio)
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius)
    
    def draw_circle_with_outline(self, x, y, color, outline_color, radius_ratio=0.4):
        screen_x, screen_y = self.grid_to_screen(x, y)
        center_x = screen_x + self.cell_size // 2
        center_y = screen_y + self.cell_size // 2
        radius = int(self.cell_size * radius_ratio)
        pygame.draw.circle(self.surface, outline_color, (center_x, center_y), radius + 2)
        pygame.draw.circle(self.surface, color, (center_x, center_y), radius)
    
    def draw_walls(self, grid):
        for wall_x, wall_y in grid.walls:
            self.draw_cell(wall_x, wall_y, UIConfig.WALL_COLOR)
    
    def draw_exits(self, grid):
        for exit_x, exit_y in grid.exits:
            self.draw_cell(exit_x, exit_y, UIConfig.EXIT_COLOR)
    
    def draw_pheromones(self, pheromone_map):
        normalized = pheromone_map.normalize_for_display()
        for y in range(pheromone_map.size):
            for x in range(pheromone_map.size):
                intensity = normalized[x, y]
                if intensity > 20:
                    alpha = min(200, intensity)
                    color = (255, 255, 200)
                    screen_x, screen_y = self.grid_to_screen(x, y)
                    rect = pygame.Rect(screen_x + 1, screen_y + 1, self.cell_size - 2, self.cell_size - 2)
                    temp_surface = pygame.Surface((self.cell_size - 2, self.cell_size - 2))
                    temp_surface.set_alpha(alpha)
                    temp_surface.fill(color)
                    self.surface.blit(temp_surface, rect)
    
    def draw_people(self, people_manager):
        for person in people_manager.get_people():
            if person.active:
                self.draw_circle(person.x, person.y, UIConfig.PERSON_COLOR, 0.35)
    
    def draw_fires(self, fire_manager):
        for fire in fire_manager.get_fires():
            radius_ratio = 0.3 + (fire.intensity * 0.1)
            self.draw_circle_with_outline(fire.x, fire.y, UIConfig.FIRE_COLOR, (255, 100, 0), radius_ratio)
    
    def draw_ants(self, ant_colony):
        for ant in ant_colony.get_ants():
            if not ant.found_exit:
                self.draw_circle(ant.x, ant.y, (200, 200, 0), 0.2)
    
    def draw_complete_scene(self, grid, pheromone_map, people_manager, fire_manager, show_pheromone, phase):
        self.draw_grid_background(grid.size)
        if show_pheromone and phase != 'aco':
            self.draw_pheromones(pheromone_map)
        self.draw_walls(grid)
        self.draw_exits(grid)
        if phase == 'evacuation':
            self.draw_fires(fire_manager)
            self.draw_people(people_manager)
        elif phase == 'aco':
            if show_pheromone:
                self.draw_pheromones(pheromone_map)