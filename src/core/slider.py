from src.core.component import Component
from src.core.style import Style
import pygame

class Slider(Component):
    def __init__(self, current = 0, min_val=0, max_val=1023, rect:pygame.Rect = pygame.Rect(0, 0, 100, 50), style:Style = Style()):
        super().__init__(rect, style)
        self.value = 512
        self.current = current
        self.min_val = min_val
        self.max_val = max_val



    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
            if self.contains_point(event.pos[0], event.pos[1]):
                self.update_value(event.pos[0])

        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:  # Drag
            if self.contains_point(event.pos[0], event.pos[1]):
                self.update_value(event.pos[0])

    def draw(self, surface):
        if "foreground" in self.style.colors:
            foreground = self.style.colors["foreground"]
        else:
            foreground = (255, 255, 255)
        if "background" in self.style.colors:
            background = self.style.colors["background"]
        else:
            background = (80, 80, 80)
        slider_width = self.rect.width
        handle_x = self.rect.x + int(
            (self.current - self.min_val) / (self.max_val - self.min_val) * slider_width
        )
        handle_y = self.rect.y + self.rect.height // 2
        handle_width = self.rect.height  # Handle is a square
        handle_rect = pygame.Rect(
            handle_x - handle_width // 2, self.rect.y, handle_width, self.rect.height
        )

        pygame.draw.rect(surface, background, self.rect)
        pygame.draw.rect(surface, foreground, handle_rect)

    def update_value(self, mouse_x):
        """
        Update the slider's current value based on the mouse position.
        :param mouse_x: The x-coordinate of the mouse.
        """
        slider_start = self.rect.x
        slider_end = self.rect.x + self.rect.width
        # Clamp mouse_x to within the slider range
        mouse_x = max(slider_start, min(slider_end, mouse_x))

        # Update current value based on position
        self.current = self.min_val + (
            (mouse_x - slider_start) / (slider_end - slider_start)
        ) * (self.max_val - self.min_val)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos
            if self.rect.contains(pygame.Rect(x,y,1,1)):
                print("clicked")
        return

