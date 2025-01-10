from src.core.sound import Sound
from src.core.log import log
from pathlib import Path

def test_sound(indent="", verbose=True):
    try:
        # Define the path to a test sound file
        sound_file_path = Path("audio") / "short.mp3"
        
        # Create a Sound instance
        sound = Sound(file_path=sound_file_path)
        
        # Test playing the sound
        sound.play()
        log("Sound played successfully.", indent, verbose)
        
        # Test pausing the sound
        sound.pause()
        log("Sound paused successfully.", indent, verbose)
        
        # Test stopping the sound
        sound.stop()
        log("Sound stopped successfully.", indent, verbose)
        
        # Test repeating the sound
        sound.repeat(1)
        log("Sound set to repeat successfully.", indent, verbose)
        
        # Stop after testing repeat
        sound.stop()
        log("Sound stopped successfully.", indent, verbose)
        return True
    except Exception as e:
        log(f"{indent}Error during sound tests: {e}", indent, verbose)
        return False
