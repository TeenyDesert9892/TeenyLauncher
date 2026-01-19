import platform
import pathlib
import os

def get_launcher_path():
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".teenylauncher")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "teenylauncher")
    else:
        return os.path.join(str(pathlib.Path.home()), ".teenylauncher")