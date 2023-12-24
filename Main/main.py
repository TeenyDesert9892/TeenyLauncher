import customtkinter as ctk
import minecraft_launcher_lib
import os
import subprocess
import tkinter

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.geometry("800x500")
window.iconbitmap("assets/Icon.ico")
window.title("Teeny Launcher")

info = ctk.CTkFrame(master=window, width=500,height=480)

mineconf = ctk.CTkFrame(master=window, width=260,height=480)

selected_versions = ctk.CTkEntry(master=mineconf)

entry_name = ctk.CTkEntry(master=mineconf)

entry_ram = ctk.CTkEntry(master=mineconf)

user = os.getenv('USERNAME')
if os.name == "nt":
    minecraft_directori = f"C:/Users/{user}/AppData/Roaming/.TeenyLauncher"
elif os.name == "posix":
    minecraft_directori = f"/home/{user}/.TeenyLauncher"

versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)

lista_versiones_instaladas = []
for versiones_instaladas in versiones_instaladas:
    lista_versiones_instaladas.append(versiones_instaladas['id'])

if len(lista_versiones_instaladas) != 0:
    vers = tkinter.StringVar(mineconf)
    vers.set(lista_versiones_instaladas[0])
elif len(lista_versiones_instaladas) == 0:
    vers = tkinter.StringVar(mineconf)
    vers.set('sin versiones instaladas')
    lista_versiones_instaladas.append('Sin versiones instaladas')

versions_display = ctk.CTkOptionMenu(mineconf,vers,*lista_versiones_instaladas)

def install_minecraft():
    version = selected_versions.get()
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version,minecraft_directori)
        print(f'Se ha instalado la version {version}!')
    else:
        print('No se ingreso ninguna version...')

def install_forge():
    version = selected_versions.get()
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    minecraft_launcher_lib.forge.install_forge_version(forge,minecraft_directori)
    print('Forge instalado!')

def install_fabric():
    version = selected_versions.get()
    if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(version):
        print("This version is not supported by fabric")
    else:
        minecraft_launcher_lib.fabric.install_fabric(version, minecraft_directori)
        print('Fabric instalado!')

def install_quilt():
    version = selected_versions.get()
    if not minecraft_launcher_lib.quilt.is_minecraft_version_supported(version):
        print("This version is not supported by quilt")
    else:
        minecraft_launcher_lib.quilt.install_quilt(version, minecraft_directori)
        print('Quilt instalado!')

def ejecutar_minecraft():
    mine_user = entry_name.get()
    version = vers.get()
    ram = f"-Xmx{entry_ram.get()}G"

    options = {'username': mine_user,'uuid' : '','token': '','jvArguments': [ram,ram],'launcherVersion': "1.0.0"}

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version,minecraft_directori,options)
    subprocess.run(minecraft_command)

#def instalar_versiones_normales():


#def instalar_versiones_forge():


#def instalar_versiones_fabric():


#def instalar_versiones_quilt():


def menu():
    info.grid_propagate(False)
    info.grid(row=0,column=0,pady=10,padx=10,sticky="nswe")

    mineconf.grid_propagate(False)
    mineconf.grid(row=0,column=1,pady=10,padx=10,sticky="nswe")

    title = ctk.CTkLabel(master=mineconf,text="Iniciar Minecraft",font=("Antipasto Pro Extrabold",24))
    title.grid(row=0,column=0,pady=5,padx=5,sticky="we")

    entry_name.configure(placeholder_text="Nombre de usuario",font=("Antipasto Pro Extrabold",16))
    entry_name.grid(row=2,column=0,pady=5,padx=5,sticky="we")

    entry_ram.configure(placeholder_text="Uso de ram",font=("Antipasto Pro Extrabold",16))
    entry_ram.grid(row=3,column=0,pady=5,padx=5,sticky="we")

    selected_versions.configure(placeholder_text="Version a elegir",font=("Antipasto Pro Extrabold",16))
    selected_versions.grid(row=1,column=0,pady=5,padx=5,sticky="we")

    versions_display.grid(row=1,column=0,pady=5,padx=5,sticky="we")

    window.mainloop()

menu()