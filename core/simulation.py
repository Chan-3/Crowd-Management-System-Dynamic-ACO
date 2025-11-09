"""Simulation controller module"""
import csv
import os
from config import LogConfig, ACOConfig, EvacuationConfig

class SimulationController:
    def __init__(self, grid, pheromone_map, ant_colony, people_manager, fire_manager):
        self.grid = grid
        self.pheromone_map = pheromone_map
        self.ant_colony = ant_colony
        self.people_manager = people_manager
        self.fire_manager = fire_manager
        self.phase = 'idle'
        self.initialized = False
        self.running = False
        self.time_step = 0
        self.log_dir = None
        self.convergence_log = []
        self.evacuation_log = []
        
    def initialize(self, crowd_size, exit_count, fire_count):
        self.grid.reset()
        self.pheromone_map.reset()
        self.time_step = 0
        self.convergence_log.clear()
        self.evacuation_log.clear()
        self.grid.initialize_obstacles()
        self.grid.initialize_exits(exit_count)
        self.people_manager.initialize_people(crowd_size)
        self.fire_manager.set_fire_count(fire_count)
        self.fire_manager.reset()
        if LogConfig.ENABLE_LOGGING:
            self.log_dir = LogConfig.get_run_dir()
        self.initialized = True
        self.phase = 'idle'
        print(f"Initialized: {crowd_size} people, {exit_count} exits, {fire_count} fire sources")
    
    def start(self):
        if not self.initialized:
            print("Cannot start: not initialized")
            return
        self.running = True
        self.phase = 'aco'
        self.time_step = 0
        print("Starting ACO phase...")
    
    def stop(self):
        self.running = False
        print("Simulation stopped")
    
    def reset(self):
        self.phase = 'idle'
        self.initialized = False
        self.running = False
        self.time_step = 0
        self.grid.reset()
        self.pheromone_map.reset()
        self.fire_manager.reset()
        print("Simulation reset")
    
    def update(self):
        if not self.running:
            return
        if self.phase == 'aco':
            self.update_aco_phase()
        elif self.phase == 'evacuation':
            self.update_evacuation_phase()
    
    def update_aco_phase(self):
        result = self.ant_colony.run_iteration()
        self.convergence_log.append({
            'iteration': result['iteration'],
            'best_path_length': result['best_path_length']
        })
        if result['iteration'] >= ACOConfig.ITERATIONS:
            print(f"ACO complete. Best path: {result['best_path_length']}")
            self.phase = 'evacuation'
            self.time_step = 0
            print("Starting evacuation phase...")
    
    def update_evacuation_phase(self):
        self.time_step += 1
        self.fire_manager.update(self.time_step)
        self.people_manager.update_all(self.pheromone_map)
        if self.time_step % 5 == 0:
            self.pheromone_map.evaporate()
        stats = self.people_manager.get_statistics()
        self.evacuation_log.append({
            'time_step': self.time_step,
            'evacuated': stats['evacuated'],
            'remaining': stats['remaining'],
            'fire_cells': self.fire_manager.get_fire_count()
        })
        if not self.people_manager.has_active_people():
            self.finish_simulation()
        if self.time_step >= EvacuationConfig.MAX_STEPS:
            print("Max steps reached")
            self.finish_simulation()
    
    def finish_simulation(self):
        print("Simulation finished")
        stats = self.people_manager.get_statistics()
        print(f"Results: {stats['evacuated']}/{stats['total']} evacuated in {self.time_step} steps")
        if LogConfig.ENABLE_LOGGING and self.log_dir:
            self.save_logs()
        self.phase = 'finished'
        self.running = False
    
    def save_logs(self):
        convergence_file = os.path.join(self.log_dir, 'convergence.csv')
        with open(convergence_file, 'w', newline='') as f:
            if self.convergence_log:
                writer = csv.DictWriter(f, fieldnames=['iteration', 'best_path_length'])
                writer.writeheader()
                writer.writerows(self.convergence_log)
        evacuation_file = os.path.join(self.log_dir, 'evacuation.csv')
        with open(evacuation_file, 'w', newline='') as f:
            if self.evacuation_log:
                writer = csv.DictWriter(f, fieldnames=['time_step', 'evacuated', 'remaining', 'fire_cells'])
                writer.writeheader()
                writer.writerows(self.evacuation_log)
        print(f"Logs saved to {self.log_dir}")
    
    def get_statistics(self):
        if self.phase == 'evacuation' or self.phase == 'finished':
            stats = self.people_manager.get_statistics()
            stats['time_steps'] = self.time_step
            return stats
        else:
            return {
                'total': len(self.people_manager.people),
                'evacuated': 0,
                'remaining': len(self.people_manager.people),
                'progress': 0,
                'time_steps': 0
            }
    
    def is_initialized(self):
        return self.initialized
    
    def is_running(self):
        return self.running
    
    def get_phase(self):
        return self.phase