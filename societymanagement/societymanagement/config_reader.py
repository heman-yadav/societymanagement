import json
import os

def load_config():
    """
    Loads the configuration from a JSON file.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    print('config_path: ',config_path)
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        print(f"Error: config.json not found at {config_path}")
        return {}
    except json.JSONDecodeError:
        # Handle invalid JSON
        print(f"Error: Could not decode config.json. Check for syntax errors.")
        return {}

# Load the config data when this module is imported
CONFIG = load_config()