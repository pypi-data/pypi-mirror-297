import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_neat_directory():
    neat_dir = os.path.join(os.path.expanduser("~"), ".neat")
    if not os.path.exists(neat_dir):
        os.makedirs(neat_dir)
    return neat_dir

def save_state(file_path, last_folder, recent_files):
    neat_dir = ensure_neat_directory()
    state_file = os.path.join(neat_dir, "state.json")
    with open(state_file, "w") as f:
        json.dump({
            "last_opened_file": file_path,
            "last_accessed_folder": last_folder,
            "recent_files": recent_files
        }, f)

def load_state():
    neat_dir = ensure_neat_directory()
    state_file = os.path.join(neat_dir, "state.json")
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            return json.load(f)
    return {
        "last_opened_file": None,
        "last_accessed_folder": None,
        "recent_files": []
    }

def log_session(message):
    neat_dir = ensure_neat_directory()
    log_file = os.path.join(neat_dir, "log.txt")
    with open(log_file, "a") as f:
        f.write(f"{message}\n")