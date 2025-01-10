import pygame
from src.core.style import Style

class Component:
    def __init__(self, rect: pygame.Rect, style:Style = Style()):
        """
        Base class for UI components.
        """
        self.parent = None  # Parent view
        self.children = []  # List of child components
        self.rect = rect or pygame.Rect(0, 0, 100, 50)  # Default size and position
        self.style = style or Style()

    def draw(self, surface):
        """
        Draw the component to the given surface. Override this in subclasses.
        :param surface: The pygame surface to draw on.
        """
        pass

    def handle_event(self, event):
        """
        Handle input events like mouse clicks or key presses. Override in subclasses.
        :param event: A pygame event.
        """
        for child in self.children:
            child.handle_event(event)

    def add_child(self, component):
        """
        Add a child component to this component.
        :param component: The child component to add.
        """
        self.children.append(component)
        component.parent = self

    def remove_child(self, component):
        """
        Remove a child component from this component.
        :param component: The child component to remove.
        """
        self.children.remove(component)
        component.parent = None

    def set_rect(self, x, y, width, height):
        """
        Set the position and size of this component.
        :param x: X position.
        :param y: Y position.
        :param width: Width of the component.
        :param height: Height of the component.
        """
        self.rect = pygame.Rect(x, y, width, height)

    def get_absolute_position(self):
        """
        Get the absolute position of this component in the window, taking parent offset into account.
        :return: (x, y) tuple representing the absolute position.
        """
        x, y = self.rect.topleft
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            x += parent_x
            y += parent_y
        return x, y

    def contains_point(self, x, y):
        """
        Check if a point is inside this component's rectangle.
        :param x: X coordinate of the point.
        :param y: Y coordinate of the point.
        :return: True if the point is inside the component, False otherwise.
        """
        return self.rect.collidepoint(x, y)


