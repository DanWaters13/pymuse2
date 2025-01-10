import pygame
from src.core.geometry import *
from src.core.style import *

class Button:
    def __init__(self, rect: Shape2D, style: Style, text: str):
        self.rect = rect
        self.style = style
        self.text = text
        self.callback = None

    def draw(self, canvas: pygame.Surface):
        # Draw background
        pygame.draw.rect(
            canvas,
            self.style.colors.get("background", (50, 50, 50)),
            self.rect.to_pygame_rect(),
        )

        # Draw text
        if self.text:
            font = self.style.colors.get("font", pygame.font.Font(None, 36))
            text_surface = font.render(self.text, True, self.style.colors.get("text", (255, 255, 255)))
            text_rect = text_surface.get_rect(center=self.rect.to_pygame_rect().center)
            canvas.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.contains(*event.pos):
                if self.callback:
                    self.callback()

    def set_callback(self, callback):
        self.callback = callback
