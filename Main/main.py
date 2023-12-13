import minecraft_launcher_lib, os, subprocess
import tkinter as tk
from tkinter import simpledialog

user_window = os.environ["USERNAME"]
minecraft_directory = f"C:/Users/{user_window}/AppData/Roaming/.TeenyLauncher"

options = {'username': "User", 'uuid': '', 'token': '', 'jvArguments': ["-Xmx2G"], 'launcherVersion': "1.0.0"} #options.update({'jvArguments': '[-Xmx' + str(int(memoria)) + 'G]'})

def instalar_minecraft(ver):
    if ver == "vanilla":
        version = simpledialog.askstring("Instalar Minecraft", "Ingrese la versión a instalar:")
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)
        print(f'Se ha instalado la versión {version}')
    elif ver == "forge":
        version = simpledialog.askstring("Instalar Forge", "Ingrese la versión de Forge a instalar:")
        forge = minecraft_launcher_lib.forge.find_forge_version(version)
        minecraft_launcher_lib.forge.install_forge_version(forge, minecraft_directory)
        print('Forge instalado')
    elif ver == None:
        return
    else:
        return

def ejecutar_minecraft():
    version = simpledialog.askstring("Ejecutar Minecraft", "Ingrese la versión de Minecraft a ejecutar:")

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
    subprocess.run(minecraft_command)

    print(options)
def menu():
    window = tk.Tk()
    window.iconbitmap("assets/Icon.ico")
    window.title("TeenyLauncher")
    window.geometry("800x500")
    window.config(bg = "#3D3D3D")
    window.resizable(width=0,height=0)

    info = tk.Frame(window, width=600, height=500)
    info.config(bg="#FFFFFF")
    info.grid(row=0,column=0)

    play = tk.Frame(window, width=200, height=500)
    play.config(bg="#3D3D3D")
    play.grid(row=0,column=1)

    NameText = tk.Label(play, text="Nombre de usuario:", fg="#FFFFFF", font=("Antipasto Pro Extrabold", 15), background="#3D3D3D")
    NameText.grid(row=0,column=0,pady=5,sticky=tk.W)
    NameInput = tk.Entry(play)
    NameInput.grid(row=1,column=0,pady=5)

    VersionText = tk.Label(play, text="Version de minecraft:", fg="#FFFFFF", font=("Antipasto Pro Extrabold", 15), background="#3D3D3D")
    VersionText.grid(row=2,column=0,pady=5,sticky=tk.W)
    VersionInput = tk.Entry(play)
    VersionInput.grid(row=3,column=0,pady=5)

    InstalacionTexto = tk.Label(play, text="Tipo de instalacion:", fg="#FFFFFF", font=("Antipasto Pro Extrabold", 15), background="#3D3D3D")
    InstalacionTexto.grid(row=4,column=0,pady=5,sticky=tk.W)
    InstalacionInput = tk.Entry(play)
    InstalacionInput.grid(row=5,column=0,pady=5)

    SubtimButton = tk.Button(play, text="Empezar", fg="#FFFFFF", font=("Antipasto Pro Extrabold", 12), background="#11A11E")
    SubtimButton.grid(row=6,column=0,pady=5)

    window.mainloop()

if __name__ == "__main__":
    menu()