from pathlib import Path
import pygame

class Style:
    def __init__(self, font_path="LiberationMono-Regular.ttf", font_size=24, **colors):
        self.font_path = Path(font_path)
        self.font_size = font_size
        self.colors = {label: value for label, value in colors.items()}

        # Initialize pygame font
        pygame.font.init()
        if self.font_path.exists():
            self.font = pygame.font.Font(str(self.font_path), self.font_size)
        else:
            raise FileNotFoundError(f"Font file not found: {self.font_path}")
