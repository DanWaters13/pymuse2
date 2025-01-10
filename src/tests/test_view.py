import pygame
from src.core.geometry import Rect, Vector
from src.core.view import View
from src.core.button import Button
from src.core.style import Style

def test_view(indent="", verbose=True):
    pygame.init()
    pygame.display.set_caption("Test View with Button")
    clock = pygame.time.Clock()

    # Initialize a View
    root_view = View(800, 600)

    # Define Style for Button
    button_style = Style()
    button_style.colors = {
        "background": (100, 100, 100),
        "text": (255, 255, 255),
        "font": pygame.font.Font(None, 36),  # Default Pygame font
    }

    # Define Button
    button_rect = Rect(Vector(300, 250), Vector(200, 100))
    button = Button(rect=button_rect, style=button_style, text="short.mp3")

    def button_clicked():
        print("Button clicked!")

    button.set_callback(button_clicked)

    # Add Button to View
    root_view.children.append(button)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle events for the root view and its components
            root_view.handle_event(event)

        # Clear screen
        root_view.screen.fill((0, 0, 0))  # Black background

        # Draw the root view and its components
        root_view.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return True
