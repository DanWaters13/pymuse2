import pygame
from src.core.geometry import Rect, Vector
from src.core.view_component import ComponentView
from src.core.style import Style
from src.core.sound import Sound
from src.core.button import SoundButton
from src.core.slider import Slider  # Import Slider
from src.core.log import log
from pathlib import Path
import traceback as tb
import sys


def test_view(indent="", verbose=True):
    pygame.init()
    try:
        pygame.display.set_caption("Test View with SoundButton and Slider")
        clock = pygame.time.Clock()

        # Initialize a View
        root_view = ComponentView(None, Path("config") / "view.json")

        # Define Style for Button
        button_style = Style()
        button_style.colors = {
            "background": (100, 100, 100),
            "text": (255, 255, 255),
            "font": pygame.font.Font(None, 36),  # Default Pygame font
        }

        # Define SoundButton
        sound_button = SoundButton(
            rect=pygame.Rect(300,400,200,100),
            style=button_style,
            sound_file=Path("audio") / "short.mp3",
            text="Play Sound",
        )
        sound_button.set_callback(sound_button.sound.play)  # Assign callback to play the sound

        # Add SoundButton to View
        root_view.children.append(sound_button)

        # Define Style for Slider
        slider_style = Style()
        slider_style.colors = {
            "background": (80, 80, 80),
            "foreground": (255, 255, 255),
        }

        # Define Slider
        sound = Sound(Path("audio")/"short.mp3")
        slider = Slider(511, 0, 1023, pygame.Rect(300, 400, 400, 20), slider_style)
        slider.callback = lambda: sound.set_speed(slider.current)
        sound.play()

        # Add Slider to View
        root_view.children.append(slider)

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
            root_view.canvas.fill((0, 0, 0))  # Black background

            # Draw the root view and its components
            root_view.draw()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return True
    except Exception as e:
        log(f"View tests failed: {e}", indent, verbose)
        exec_type, exec_value, third = sys.exc_info()
        print(exec_type.__name__)
        print(exec_value)
        tb.print_tb(third)
        return False
