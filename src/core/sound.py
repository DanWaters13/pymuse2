from pathlib import Path
import soundfile as sf
import sounddevice as sd
import numpy as np
from scipy.signal import resample
from src.core.json_manager import JSONManager
from src.core.engine import Engine
import os

import threading
import soundfile as sf
import sounddevice as sd
import numpy as np

class Sound:
    def __init__(self, file_path, speed=1.0, chunk_size=1024):
        self.file_path = file_path
        self.speed = speed  # Speed multiplier (-1.0 for reverse, 0 for pause, 1.0 for normal)
        self.chunk_size = chunk_size
        self.stop_flag = threading.Event()
        self.play_thread = None

        # Load the audio file
        self.audio_data, self.sample_rate = sf.read(f"{file_path}", dtype='float32')
        self.current_position = 0

    def set_speed(self, speed):
        """Set the playback speed dynamically."""
        self.speed = speed

    def _generate_chunk(self):
        """Generate the next chunk of audio based on the current speed."""
        if self.speed == 0:  # Pause
            return np.zeros((self.chunk_size, self.audio_data.shape[1]))

        # Calculate step size based on speed
        step = self.speed
        indices = np.arange(self.current_position, 
                            self.current_position + step * self.chunk_size, 
                            step)

        # Wrap indices if they go out of bounds
        indices = np.mod(indices, len(self.audio_data)).astype(int)

        # Update current position
        self.current_position = indices[-1]

        return self.audio_data[indices]

    def _play_loop(self):
        """Continuously stream audio chunks."""
        while not self.stop_flag.is_set():
            chunk = self._generate_chunk()
            sd.play(chunk, samplerate=self.sample_rate, blocking=True)

    def play(self):
        """Start playback in a separate thread."""
        self.stop_flag.clear()
        if not self.play_thread or not self.play_thread.is_alive():
            self.play_thread = threading.Thread(target=self._play_loop)
            self.play_thread.start()

    def stop(self):
        """Stop playback."""
        self.stop_flag.set()
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join()