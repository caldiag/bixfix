import os
import shutil

def ensure_directory_exists(directory):
    if not os.path.exists(f"logs/{directory}"):
        os.makedirs(f"logs/{directory}")
        return
    shutil.rmtree("logs")