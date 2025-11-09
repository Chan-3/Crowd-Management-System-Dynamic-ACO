"""Main application"""
import pygame
import sys
from config import UIConfig, GridConfig
from core.grid import Grid
from core.pheromone import PheromoneMap
from core.ants import AntColony
from core.people import PeopleManager
from core.fire import FireManager
from core.simulation import SimulationController
from ui.hud import HUD
from ui.renderer_pygame import Renderer

class EvacuationSimulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((UIConfig.WINDOW_WIDTH, UIConfig.WINDOW_HEIGHT))
        pygame.display.set_caption("Office Evacuation Simulator — Dynamic ACO")
        self.clock = pygame.time.Clock()
        self.grid = Grid(GridConfig.SIZE)
        self.pheromone_map = PheromoneMap(GridConfig.SIZE)
        self.ant_colony = AntColony(self.grid, self.pheromone_map)
        self.people_manager = PeopleManager(self.grid)
        self.fire_manager = FireManager(self.grid)
        self.simulation = SimulationController(self.grid, self.pheromone_map, self.ant_colony,
                                               self.people_manager, self.fire_manager)
        self.hud = HUD()
        self.renderer = Renderer(self.screen, UIConfig.GRID_OFFSET_X, UIConfig.GRID_OFFSET_Y)
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            action = self.hud.handle_event(event)
            if action == 'initialize':
                self.handle_initialize()
            elif action == 'start':
                self.handle_start()
            elif action == 'stop':
                self.handle_stop()
            elif action == 'reset':
                self.handle_reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_grid_click(event)
    
    def handle_initialize(self):
        params = self.hud.get_parameters()
        self.simulation.initialize(params['crowd_size'], params['exits'], params['fire_sources'])
    
    def handle_start(self):
        self.simulation.start()
    
    def handle_stop(self):
        self.simulation.stop()
    
    def handle_reset(self):
        self.simulation.reset()
    
    def handle_grid_click(self, event):
        if not self.simulation.is_initialized() or self.simulation.is_running():
            return
        mouse_x, mouse_y = event.pos
        grid_x, grid_y = self.renderer.screen_to_grid(mouse_x, mouse_y)
        if not self.grid.is_valid(grid_x, grid_y):
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.grid.add_fire(grid_x, grid_y)
        elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            if (grid_x, grid_y) not in self.grid.exits:
                self.grid.exits.append((grid_x, grid_y))
        else:
            self.grid.toggle_wall(grid_x, grid_y)
    
    def update(self):
        if self.simulation.is_running():
            params = self.hud.get_parameters()
            speed = params['speed']
            if speed > 0.1:
                self.simulation.update()
    
    def render(self):
        self.screen.fill(UIConfig.BG_COLOR)
        params = self.hud.get_parameters()
        self.renderer.draw_complete_scene(self.grid, self.pheromone_map, self.people_manager,
                                         self.fire_manager, params['show_pheromone'], 
                                         self.simulation.get_phase())
        if self.simulation.get_phase() == 'aco':
            self.renderer.draw_ants(self.ant_colony)
        statistics = self.simulation.get_statistics()
        self.hud.draw(self.screen, statistics)
        self.hud.update_button_states(self.simulation.is_initialized(), self.simulation.is_running())
        pygame.display.flip()
    
    def run(self):
        print("=" * 60)
        print("Office Evacuation Simulator — Dynamic ACO")
        print("=" * 60)
        print("\nControls:")
        print("  1. Set parameters (Crowd Size, Exits, Fire Points)")
        print("  2. Click 'Initialize' to setup simulation")
        print("  3. Click 'Start' to run ACO + Evacuation")
        print("  4. Use 'Stop' to pause, 'Reset' to clear")
        print("\nGrid Editing (when not running):")
        print("  - Left Click: Toggle wall")
        print("  - Shift + Click: Add fire")
        print("  - Ctrl + Click: Add exit")
        print("\n" + "=" * 60 + "\n")
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            params = self.hud.get_parameters()
            speed = params['speed']
            if speed > 0.9:
                fps = 120
            elif speed > 0.7:
                fps = 60
            elif speed > 0.5:
                fps = 30
            elif speed > 0.3:
                fps = 15
            else:
                fps = 5
            self.clock.tick(fps)
        pygame.quit()
        sys.exit()

def main():
    try:
        simulator = EvacuationSimulator()
        simulator.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == '__main__':
    main()