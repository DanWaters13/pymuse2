from pathlib import Path
import soundfile as sf
import sounddevice as sd
import numpy as np
from scipy.signal import resample
from src.core.json_manager import JSONManager
from src.core.engine import Engine
import os

class Sound:
    def __init__(self, file_path, config_path=Path("config")/"sound.json"):
        # Load configuration
        config = JSONManager.load_json(config_path)
        self.sample_rate = config.get("default_sample_rate", 44100)
        self.channels = config.get("default_channels", 2)
        self.dtype = config.get("default_dtype", "float32")

        # Load the sound file
        self.file_path = file_path
        if not os.path.exists(f"{self.file_path}"):
            raise FileNotFoundError(f"Sound file not found: {self.file_path}")
        
        # Read audio data and properties
        self.data, self.samplerate = sf.read(f"{self.file_path}", dtype=self.dtype)
        
        # Resample if necessary
        if self.samplerate != self.sample_rate:
            num_samples = int(len(self.data) * self.sample_rate / self.samplerate)
            self.data = resample(self.data, num_samples)
            self.samplerate = self.sample_rate
        
        # Convert dtype if necessary
        self.data = self.data.astype(self.dtype)

        # Validate channels
        if len(self.data.shape) == 1 and self.channels == 2:
            # Convert mono to stereo
            self.data = np.column_stack((self.data, self.data))
        elif len(self.data.shape) != self.channels:
            raise ValueError(f"Expected {self.channels} channels, but got {self.data.shape[1]}.")

        # Playback control
        self.stream = None

    def _create_stream(self):
        """Creates a sounddevice stream for playback."""
        self.stream = sd.OutputStream(samplerate=self.sample_rate, channels=self.channels, dtype=self.dtype)
        self.stream.start()

    def play(self, time_ms=0):
        """Plays the sound, optionally from a specific time."""
        start_sample = int(time_ms / 1000 * self.sample_rate)
        if self.stream is None or not self.stream.active:
            self._create_stream()
        self.stream.write(self.data[start_sample:])

    def pause(self):
        """Pauses the sound playback."""
        if self.stream and self.stream.active:
            self.stream.stop()

    def stop(self):
        """Stops the sound playback."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def repeat(self, num=-1):
        """Repeats the sound indefinitely."""
        if self.stream is None or not self.stream.active:
            self._create_stream()
        while num == -1 or num > 0:
            self.stream.write(self.data)
            if num > 0:
                num -= 1


class LiveInputSound:
    def __init__(self, file_path, engine: Engine):
        self.engine = engine
        self.data, self.samplerate = sf.read(f"{file_path}")
        self.stream = None

    def play(self):
        """Start the playback stream."""
        self.stream = sd.OutputStream(
            samplerate=self.samplerate,
            channels=self.data.shape[1],
            callback=self.audio_callback,
        )
        self.stream.start()

    def audio_callback(self, outdata, frames, time, status):
        """Stream callback for dynamic playback speed."""
        play_speed = self.engine.get_play_speed()
        if play_speed == 0:
            outdata.fill(0)
            return

        step = int(play_speed * self.samplerate)
        indices = np.arange(0, frames * step, step, dtype=int) % len(self.data)
        outdata[:] = self.data[indices]

    def stop(self):
        """Stop the playback stream."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
