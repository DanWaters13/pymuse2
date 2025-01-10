import pygame
from typing import List
from src.core.style import Style
from collections.abc import Callable

class View:
    def __init__(self, width: int, height: int):
        """Initialize a view with a black canvas."""
        self.width = width
        self.height = height
        self.children: List[View] = []

        # Initialize Pygame and set up a display
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Generic View")
        self.background_color = (0, 0, 0)  # Black background

    def add_child(self, child: 'View'):
        """Add a child component to this view."""
        self.children.append(child)

    def draw(self):
        """Draw the view and its children."""
        self.screen.fill(self.background_color)
        for child in self.children:
            child.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event: pygame.event.Event):
        """Propagate events to child components."""
        for child in self.children:
            child.handle_event(event)

    def mainloop(self):
        """Run the main event loop for the view."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_event(event)
            self.draw()

        pygame.quit()

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, style: Style, on_click: Callable):
        """Initialize the button."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.style = style
        self.on_click = on_click
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface: pygame.Surface):
        """Draw the button."""
        pygame.draw.rect(surface, self.style.background_color, self.rect)
        text_surface = self.font.render(self.text, True, self.style.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event):
        """Handle click events."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            if self.rect.collidepoint(event.pos):
                self.on_click()
