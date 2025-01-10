import pygame
from src.core.geometry import *
from src.core.style import *
from src.core.sound import *

class Button:
    def __init__(self, rect: Rect, style: Style, text: str = ""):
        self.rect = rect
        self.style = style
        self.text = text
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def draw(self, canvas):
        # Draw the button background
        pygame.draw.rect(canvas, self.style.colors["background"], self.rect.to_pygame_rect())
        # Draw the button text
        font = self.style.colors.get("font", pygame.font.Font(None, 36))
        text_surface = font.render(self.text, True, self.style.colors["text"])
        canvas.blit(
            text_surface,
            text_surface.get_rect(center=self.rect.to_pygame_rect().center),
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if self.rect.contains(*event.pos):
                if self.callback:
                    self.callback()

class SoundButton(Button):
    def __init__(self, rect: Rect, style: Style, sound_file: Path, text: str = ""):
        super().__init__(rect, style, text)
        self.sound = Sound(sound_file)

    def set_callback(self, callback=None):
        """Automatically sets the callback to play the associated sound."""
        super().set_callback(callback or self.sound.play)