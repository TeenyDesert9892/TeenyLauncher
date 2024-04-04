import subprocess

def Update():
    pkgList = ["pip", "customtkinter", "pillow", "minecraft_launcher_lib", "icecream"]
    for pkg in pkgList:
        subprocess.run("python -m pip install --upgrade " + pkg, shell=True)

if __name__ == "__main__":
    Update()