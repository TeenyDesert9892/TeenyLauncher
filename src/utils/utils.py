import platform
import pathlib
import psutil
import os

def get_launcher_path():
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".teenylauncher")
    
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "teenylauncher")
    
    else:
        return os.path.join(str(pathlib.Path.home()), ".teenylauncher")


def get_assets_path():
    return os.path.normpath(os.getcwd()+"/src/assets")


def get_ram():
    ram = int(psutil.virtual_memory().total / (1024 ** 2))
    uncompatibleRam = True
    
    while uncompatibleRam:
        if ram % 32 != 0:
            ram -= 1
            
        else:
            uncompatibleRam = False
            
    return ram