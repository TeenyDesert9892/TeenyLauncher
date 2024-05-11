@echo off
title TeenyLauncher
"w-venv/Scripts/Python.exe" -m pip install --upgrade pip
"w-venv/Scripts/Python.exe" -m pip install --upgrade psutil
"w-venv/Scripts/Python.exe" -m pip install --upgrade pillow
"w-venv/Scripts/Python.exe" -m pip install --upgrade packaging
"w-venv/Scripts/Python.exe" -m pip install --upgrade setuptools
"w-venv/Scripts/Python.exe" -m pip install --upgrade customtkinter
"w-venv/Scripts/Python.exe" -m pip install --upgrade minecraft_launcher_lib
"w-venv/Scripts/Python.exe" -m pip install --upgrade icecream
"w-venv/Scripts/Python.exe" Main/TeenyLauncher.py