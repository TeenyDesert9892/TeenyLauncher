import os
import subprocess

subprocess.run(str(f"{os.getcwd()}/venv/Scripts/Python.exe {os.getcwd()}/Main/scripts/InstallAndUpdate.py"), shell=True)
subprocess.run(str(f"{os.getcwd()}/venv/Scripts/Python.exe {os.getcwd()}/Main/TeenyLauncher.py"), shell=True)