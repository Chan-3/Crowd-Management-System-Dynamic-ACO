"""Configuration settings for ACO Evacuation Simulator"""
import os
from datetime import datetime

# Grid Configuration
class GridConfig:
    SIZE = 50
    CELL_SIZE = 15
    DEFAULT_CROWD_SIZE = 50
    DEFAULT_EXITS = 4
    DEFAULT_FIRE_SOURCES = 2
    MIN_CROWD_SIZE = 1
    MAX_CROWD_SIZE = 200
    MIN_EXITS = 1
    MAX_EXITS = 10
    MIN_FIRE_SOURCES = 0
    MAX_FIRE_SOURCES = 20

# ACO Configuration
class ACOConfig:
    ANT_COUNT = 100
    ITERATIONS = 50
    ALPHA = 1.0
    BETA = 2.0
    EVAPORATION = 0.1
    Q = 100

# Evacuation Configuration
class EvacuationConfig:
    FIRE_PENALTY = 0.1
    CONGESTION_PENALTY = 0.7
    MOVEMENT_SPEED = 1
    VISION_RANGE = 5
    CONGESTION_RADIUS = 2
    MAX_STEPS = 1000

# Fire Configuration
class FireConfig:
    SPAWN_DELAY = 15
    SPREAD_RATE = 0.15
    MAX_INTENSITY = 3
    INTENSITY_GROWTH_RATE = 10

# UI Configuration
class UIConfig:
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    PANEL_WIDTH = 400
    GRID_OFFSET_X = 420
    GRID_OFFSET_Y = 50
    FPS = 60
    BG_COLOR = (248, 248, 248)
    GRID_COLOR = (220, 220, 220)
    WALL_COLOR = (128, 108, 96)
    EXIT_COLOR = (76, 175, 80)
    PERSON_COLOR = (33, 150, 243)
    FIRE_COLOR = (255, 152, 0)
    PHEROMONE_COLOR = (255, 255, 200)
    PANEL_BG = (45, 45, 48)
    PANEL_TEXT = (220, 220, 220)
    BUTTON_BG = (70, 70, 73)
    BUTTON_HOVER = (90, 90, 93)
    BUTTON_DISABLED = (50, 50, 52)
    INPUT_BG = (60, 60, 63)
    INPUT_BORDER = (100, 100, 103)
    FONT_SIZE_TITLE = 24
    FONT_SIZE_LABEL = 16
    FONT_SIZE_BUTTON = 18
    FONT_SIZE_STAT = 14

# Logging Configuration
class LogConfig:
    ENABLE_LOGGING = True
    LOG_DIR = "runs"
    
    @staticmethod
    def get_run_dir():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = os.path.join(LogConfig.LOG_DIR, timestamp)
        os.makedirs(run_dir, exist_ok=True)
        return run_dir

# Obstacle Patterns
class ObstaclePatterns:
    @staticmethod
    def create_u_shapes(grid_size):
        obstacles = []
        for x in range(10, 20):
            obstacles.append((x, 10))
            obstacles.append((x, 18))
        for y in range(10, 19):
            obstacles.append((10, y))
        for x in range(30, 40):
            obstacles.append((x, 10))
            obstacles.append((x, 18))
        for y in range(10, 19):
            obstacles.append((39, y))
        return obstacles
    
    @staticmethod
    def create_pillars(grid_size):
        return [(15, 25), (15, 26), (25, 25), (25, 26), 
                (35, 25), (35, 26), (20, 35), (20, 36), (30, 35), (30, 36)]
    
    @staticmethod
    def create_hallways(grid_size):
        hallways = []
        for x in range(10, 40):
            if x not in range(20, 30):
                hallways.append((x, 30))
        return hallways

GRID_SIZE = GridConfig.SIZE
CELL_SIZE = GridConfig.CELL_SIZE