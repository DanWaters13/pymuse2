import json
from pathlib import Path
import os

class JSONManager:
    @staticmethod
    def load_json(file_path):
        """Loads JSON data from the specified file."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_json(data, file_path):
        """Saves JSON data to the specified file."""
        with os.path.open(f"{file_path}", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

class ViewConfig:
    DEFAULTS = {
        "default_width": 800,
        "default_height": 600,
        "default_delay": 60,
    }

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        if not os.path.exists(f"{self.config_path}"):
            self.config = self.DEFAULTS
            JSONManager.save_json(f"{self.config_path}", self.config)
        else:
            self.config = JSONManager.load_json(self.config_path)

    @property
    def default_width(self):
        return self.config.get("default_width", self.DEFAULTS["default_width"])

    @property
    def default_height(self):
        return self.config.get("default_height", self.DEFAULTS["default_height"])

    @property
    def default_delay(self):
        return self.config.get("default_delay", self.DEFAULTS["default_delay"])