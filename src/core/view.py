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

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return  # Don't delegate further

        # Handle escape key press to quit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
            return  # Don't delegate further

        # Delegate to child components
        for component in self.children:
            if hasattr(component, "handle_event"):
                component.handle_event(event)

    def mainloop(self):
        """Run the main event loop for the view."""
        running = True
        while running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()

        pygame.quit()

