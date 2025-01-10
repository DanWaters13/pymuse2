import pygame
from src.core.geometry import *
from src.core.style import *
from src.core.sound import *
from src.core.component import Component

class Button(Component):
    def __init__(self, rect: pygame.Rect, style: Style, text: str = ""):
        super().__init__(rect, style)
        self.rect = rect
        self.text = text
        self.callback = None

    def set_callback(self, callback):
        self.callback = callback

    def draw(self, canvas):
        # Draw the button background
        pygame.draw.rect(canvas, self.style.colors["background"], self.rect)
        # Draw the button text
        font = self.style.colors.get("font", pygame.font.Font(None, 36))
        if "text" in self.style.colors:
            text_color = self.style.colors["text"]
        elif "font" in self.style.colors:
            text_color = self.style.colors["font"]
        elif "foreground" in self.style.colors:
            text_color = self.style.colors["foreground"]
        else:
            text_color = (255, 255, 255)

        text_surface = font.render(self.text, True, self.style.colors["text"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        canvas.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            x,y = event.pos
            if self.rect.collidepoint(x,y):
                if self.callback:
                    self.callback()

class SoundButton(Button):
    def __init__(self, rect: Rect, style: Style, sound_file: Path, text: str = ""):
        super().__init__(rect, style, text)
        self.sound = Sound(sound_file)

    def set_callback(self, callback=None):
        """Automatically sets the callback to play the associated sound."""
        super().set_callback(callback or self.sound.play)