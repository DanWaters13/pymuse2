import pygame
from typing import List
from src.core.style import Style
from collections.abc import Callable
from pathlib import Path
from src.core.json_manager import *

class View:
    def __init__(self, canvas=None, config_path=Path("config")/"view.json"):
        self.view_config = ViewConfig(config_path)

        # Use the configuration values
        self.width = self.view_config.default_width
        self.height = self.view_config.default_height
        self.delay = self.view_config.default_delay

        # Initialize canvas
        self.canvas = canvas or pygame.display.set_mode((self.width, self.height))
        self.children = []
        self.running = True


    def add_child(self, child: 'View'):
        """Add a child component to this view."""
        self.children.append(child)

    def draw(self):
        """Draw the view and its children."""
        self.canvas.fill((0,0,0))
        for child in self.children:
            child.draw(self.canvas)
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

