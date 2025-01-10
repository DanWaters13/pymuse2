import pygame
from src.core.geometry import Rect, Vector
from src.core.view import View
from src.core.style import Style
from src.core.button import SoundButton
from src.core.log import log
from pathlib import Path

def test_view(indent="", verbose=True):
    pygame.init()
    try:
        pygame.display.set_caption("Test View with SoundButton")
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

        # Define SoundButton
        button_rect = Rect(Vector(300, 250), Vector(200,100))
        sound_button = SoundButton(rect=button_rect, style=button_style, \
                sound_file=Path("audio")/"short.mp3", text="Play Sound")
        sound_button.set_callback(sound_button.sound.play)  # Assign the callback to play the sound

        # Add SoundButton to View
        root_view.children.append(sound_button)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                # Handle events for the root view and its components
                root_view.handle_event(event)
            if not running:
                break
            # Clear screen
            root_view.screen.fill((0, 0, 0))  # Black background

            # Draw the root view and its components
            root_view.draw()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return True
    except Exception as e:
        log(f"Exception: {e}", indent, verbose)
        return False