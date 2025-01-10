import json
from pathlib import Path

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
        file_path = Path(file_path)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
