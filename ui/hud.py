"""HUD and Control Panel"""
import pygame
from config import UIConfig, GridConfig
from utils import validate_input

class Button:
    def __init__(self, x, y, width, height, text, enabled=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.enabled = enabled
        self.hovered = False
        
    def draw(self, surface, font):
        if not self.enabled:
            color = UIConfig.BUTTON_DISABLED
        elif self.hovered:
            color = UIConfig.BUTTON_HOVER
        else:
            color = UIConfig.BUTTON_BG
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, UIConfig.INPUT_BORDER, self.rect, 2)
        text_surface = font.render(self.text, True, UIConfig.PANEL_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.enabled and self.rect.collidepoint(event.pos):
                return True
        return False

class InputField:
    def __init__(self, x, y, width, height, default_value, min_val, max_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = str(default_value)
        self.min_val = min_val
        self.max_val = max_val
        self.active = False
        
    def draw(self, surface, font):
        color = UIConfig.INPUT_BORDER if self.active else UIConfig.INPUT_BG
        pygame.draw.rect(surface, UIConfig.INPUT_BG, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        text_surface = font.render(self.text, True, UIConfig.PANEL_TEXT)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif event.unicode.isdigit():
                self.text += event.unicode
    
    def get_value(self):
        return validate_input(self.text, self.min_val, self.max_val, (self.min_val + self.max_val) // 2)

class Checkbox:
    def __init__(self, x, y, size, text, checked=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.text = text
        self.checked = checked
        self.text_pos = (x + size + 10, y)
        
    def draw(self, surface, font):
        pygame.draw.rect(surface, UIConfig.INPUT_BG, self.rect)
        pygame.draw.rect(surface, UIConfig.INPUT_BORDER, self.rect, 2)
        if self.checked:
            pygame.draw.line(surface, UIConfig.PANEL_TEXT, (self.rect.x + 3, self.rect.y + 3),
                           (self.rect.right - 3, self.rect.bottom - 3), 2)
            pygame.draw.line(surface, UIConfig.PANEL_TEXT, (self.rect.right - 3, self.rect.y + 3),
                           (self.rect.x + 3, self.rect.bottom - 3), 2)
        text_surface = font.render(self.text, True, UIConfig.PANEL_TEXT)
        surface.blit(text_surface, self.text_pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                return True
        return False

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, default_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.dragging = False
        
    def draw(self, surface, font):
        track_y = self.rect.y + self.rect.height // 2
        pygame.draw.line(surface, UIConfig.INPUT_BORDER, (self.rect.x, track_y),
                        (self.rect.right, track_y), 4)
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + int(ratio * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 8, self.rect.y, 16, self.rect.height)
        pygame.draw.rect(surface, UIConfig.PANEL_TEXT, handle_rect)
        pygame.draw.rect(surface, UIConfig.INPUT_BORDER, handle_rect, 2)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_value(event.pos[0])
    
    def update_value(self, mouse_x):
        ratio = (mouse_x - self.rect.x) / self.rect.width
        ratio = max(0.0, min(1.0, ratio))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
    
    def get_value(self):
        return self.value

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.Font(None, UIConfig.FONT_SIZE_TITLE)
        self.font_label = pygame.font.Font(None, UIConfig.FONT_SIZE_LABEL)
        self.font_button = pygame.font.Font(None, UIConfig.FONT_SIZE_BUTTON)
        self.font_stat = pygame.font.Font(None, UIConfig.FONT_SIZE_STAT)
        self.panel_x = 20
        self.panel_y = 50
        y_offset = self.panel_y + 50
        self.crowd_input = InputField(self.panel_x + 180, y_offset, 180, 30,
            GridConfig.DEFAULT_CROWD_SIZE, GridConfig.MIN_CROWD_SIZE, GridConfig.MAX_CROWD_SIZE)
        y_offset += 40
        self.exit_input = InputField(self.panel_x + 180, y_offset, 180, 30,
            GridConfig.DEFAULT_EXITS, GridConfig.MIN_EXITS, GridConfig.MAX_EXITS)
        y_offset += 40
        self.fire_input = InputField(self.panel_x + 180, y_offset, 180, 30,
            GridConfig.DEFAULT_FIRE_SOURCES, GridConfig.MIN_FIRE_SOURCES, GridConfig.MAX_FIRE_SOURCES)
        y_offset += 50
        self.init_button = Button(self.panel_x + 20, y_offset, 340, 40, "Initialize", True)
        y_offset += 50
        self.start_button = Button(self.panel_x + 20, y_offset, 100, 40, "Start", False)
        self.stop_button = Button(self.panel_x + 130, y_offset, 100, 40, "Stop", False)
        self.reset_button = Button(self.panel_x + 240, y_offset, 100, 40, "Reset", True)
        y_offset += 50
        self.speed_slider = Slider(self.panel_x + 100, y_offset, 260, 20, 0.0, 1.0, 0.5)
        y_offset += 40
        self.show_pheromone_checkbox = Checkbox(self.panel_x + 50, y_offset, 20, "Show Pheromone", False)
        y_offset += 30
        self.show_2d_checkbox = Checkbox(self.panel_x + 50, y_offset, 20, "2.5D style", False)
        self.stats_y = y_offset + 60
        self.legend_y = self.stats_y + 150
        
    def draw(self, surface, statistics):
        panel_rect = pygame.Rect(0, 0, UIConfig.PANEL_WIDTH, UIConfig.WINDOW_HEIGHT)
        pygame.draw.rect(surface, UIConfig.PANEL_BG, panel_rect)
        title_surface = self.font_title.render("Office Evacuation Simulator — Dynamic ACO", True, UIConfig.PANEL_TEXT)
        surface.blit(title_surface, (10, 10))
        y = self.panel_y
        controls_text = self.font_label.render("Controls", True, UIConfig.PANEL_TEXT)
        surface.blit(controls_text, (self.panel_x, y))
        y += 50
        label = self.font_label.render("Crowd Size", True, UIConfig.PANEL_TEXT)
        surface.blit(label, (self.panel_x + 20, y + 5))
        self.crowd_input.draw(surface, self.font_label)
        y += 40
        label = self.font_label.render("Exits", True, UIConfig.PANEL_TEXT)
        surface.blit(label, (self.panel_x + 20, y + 5))
        self.exit_input.draw(surface, self.font_label)
        y += 40
        label = self.font_label.render("Fire Points", True, UIConfig.PANEL_TEXT)
        surface.blit(label, (self.panel_x + 20, y + 5))
        self.fire_input.draw(surface, self.font_label)
        y += 50
        self.init_button.draw(surface, self.font_button)
        y += 50
        self.start_button.draw(surface, self.font_button)
        self.stop_button.draw(surface, self.font_button)
        self.reset_button.draw(surface, self.font_button)
        y += 50
        speed_label = self.font_label.render("Speed", True, UIConfig.PANEL_TEXT)
        surface.blit(speed_label, (self.panel_x + 20, y))
        self.speed_slider.draw(surface, self.font_label)
        y += 40
        self.show_pheromone_checkbox.draw(surface, self.font_label)
        y += 30
        self.show_2d_checkbox.draw(surface, self.font_label)
        y = self.stats_y
        stats_title = self.font_label.render("Statistics", True, UIConfig.PANEL_TEXT)
        surface.blit(stats_title, (self.panel_x, y))
        y += 30
        stats_texts = [
            f"Total: {statistics.get('total', 0)}",
            f"Evacuated: {statistics.get('evacuated', 0)}",
            f"Remaining: {statistics.get('remaining', 0)} | Progress: {statistics.get('progress', 0):.1f}%",
            f"Time (steps): {statistics.get('time_steps', 0)}"
        ]
        for text in stats_texts:
            text_surface = self.font_stat.render(text, True, UIConfig.PANEL_TEXT)
            surface.blit(text_surface, (self.panel_x + 20, y))
            y += 25
        y = self.legend_y
        legend_title = self.font_label.render("Legend", True, UIConfig.PANEL_TEXT)
        surface.blit(legend_title, (self.panel_x, y))
        y += 30
        legend_items = [
            ("Person", UIConfig.PERSON_COLOR),
            ("Obstacle", UIConfig.WALL_COLOR),
            ("Exit", UIConfig.EXIT_COLOR),
            ("Fire", UIConfig.FIRE_COLOR),
            ("Pheromone (overlay)", (255, 255, 200))
        ]
        for text, color in legend_items:
            box_rect = pygame.Rect(self.panel_x + 50, y, 20, 20)
            pygame.draw.rect(surface, color, box_rect)
            pygame.draw.rect(surface, UIConfig.INPUT_BORDER, box_rect, 1)
            text_surface = self.font_stat.render(text, True, UIConfig.PANEL_TEXT)
            surface.blit(text_surface, (self.panel_x + 80, y + 2))
            y += 25
        y += 10
        hint_surface = self.font_stat.render("Mouse: L=Wall  Shift+L=Fire  Ctrl+L=Exit", True, (150, 150, 150))
        surface.blit(hint_surface, (self.panel_x + 20, y))
    
    def handle_event(self, event):
        self.crowd_input.handle_event(event)
        self.exit_input.handle_event(event)
        self.fire_input.handle_event(event)
        if self.init_button.handle_event(event):
            return 'initialize'
        if self.start_button.handle_event(event):
            return 'start'
        if self.stop_button.handle_event(event):
            return 'stop'
        if self.reset_button.handle_event(event):
            return 'reset'
        self.speed_slider.handle_event(event)
        self.show_pheromone_checkbox.handle_event(event)
        self.show_2d_checkbox.handle_event(event)
        return None
    
    def update_button_states(self, initialized, running):
        self.init_button.enabled = not running
        self.start_button.enabled = initialized and not running
        self.stop_button.enabled = running
        self.reset_button.enabled = not running
    
    def get_parameters(self):
        return {
            'crowd_size': self.crowd_input.get_value(),
            'exits': self.exit_input.get_value(),
            'fire_sources': self.fire_input.get_value(),
            'show_pheromone': self.show_pheromone_checkbox.checked,
            'show_2d': self.show_2d_checkbox.checked,
            'speed': self.speed_slider.get_value()
        }