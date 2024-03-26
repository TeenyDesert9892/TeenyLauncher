import subprocess

pkgList = ["pip", "customtkinter", "minecraft_launcher_lib", "icecream"]

for pkg in pkgList:
    subprocess.run("python -m pip install --upgrade " + pkg)