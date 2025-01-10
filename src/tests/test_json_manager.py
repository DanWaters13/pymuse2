from pathlib import Path
from src.core.json_manager import JSONManager

def test_json_manager(indent="", verbose=True):
    try:
        # Define the path to the test configuration
        config_path = Path("config/sound.json")
        
        # Load the JSON file
        data = JSONManager.load_json(config_path)
        
        # Validate its contents
        expected_name = "SoundConfig"
        expected_sample_rate = 44100
        expected_channels = 2
        
        if (data.get("name") == expected_name and 
            data.get("default_sample_rate") == expected_sample_rate and 
            data.get("default_channels") == expected_channels):
            
            if verbose:
                print(f"{indent}JSON configuration loaded and validated successfully.")
            return True
        else:
            if verbose:
                print(f"{indent}Validation failed. Data: {data}")
            return False
    except Exception as e:
        if verbose:
            print(f"{indent}Error during test: {e}")
        return False
