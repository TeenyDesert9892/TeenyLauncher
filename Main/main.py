import customtkinter as ctk
import minecraft_launcher_lib
import os
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.geometry("800x500")
window.iconbitmap("assets/Icon.ico")
window.title("Teeny Launcher")
window.resizable(width=False, height=False)

info = ctk.CTkFrame(master=window, width=500,height=480)
mineconf = ctk.CTkFrame(master=window, width=260,height=480)

entry_name = ctk.CTkEntry(master=mineconf)
entry_ram = ctk.CTkEntry(master=mineconf)

installVersions = ctk.CTkButton(master=mineconf)

selected_versions = ctk.CTkEntry(master=mineconf)
iniciar_minecraft = ctk.CTkButton(master=mineconf)

user = os.getenv('USERNAME')
if os.name == "nt":
    minecraft_directori = f"C:/Users/{user}/AppData/Roaming/.TeenyLauncher"
elif os.name == "posix":
    minecraft_directori = f"/home/{user}/.TeenyLauncher"

versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)

vers = ctk.StringVar(mineconf)
lista_versiones_instaladas = []
for versiones_instaladas in versiones_instaladas:
    lista_versiones_instaladas.append(versiones_instaladas['id'])

if len(lista_versiones_instaladas) != 0:
    vers.set(lista_versiones_instaladas[0])
elif len(lista_versiones_instaladas) == 0:
    vers.set('Sin versiones instaladas')
    lista_versiones_instaladas.append('Sin versiones instaladas')

versions_display = ctk.CTkOptionMenu(master=mineconf, variable=vers, values=lista_versiones_instaladas)

def install_minecraft(version):
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version,minecraft_directori)
        print(f'Se ha instalado la version {version}!')
    else:
        print('No se ingreso ninguna version...')

def install_forge(version):
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    minecraft_launcher_lib.forge.install_forge_version(forge,minecraft_directori)
    print('Forge instalado!')

def install_fabric(version):
    if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(version):
        print("This version is not supported by fabric")
    else:
        minecraft_launcher_lib.fabric.install_fabric(version, minecraft_directori)
        print('Fabric instalado!')

def install_quilt(version):
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

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)
    subprocess.run(minecraft_command)

def verif_ver(ver, type):
    if type == "Vanilla":
        install_minecraft(ver)
    elif type == "Forge":
        install_forge(ver)
    elif type == "Fabric":
        install_fabric(ver)
    elif type == "Quilt":
        install_quilt(ver)
    else:
        return

def install_versions():
    winins = ctk.CTk()
    winins.geometry("300x200")
    winins.iconbitmap("assets/Icon.ico")
    winins.title("Instalar versiones")
    winins.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winins, width=280, height=180)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    ver_name = ctk.CTkEntry(master=frame)
    ver_name.configure(placeholder_text="Numero de la version", font=("",16))
    ver_name.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    ver_types = ["Vanilla", "Forge", "Fabric", "Quilt"]
    def_ver_type = ctk.StringVar(value="Selecciona el tipo e version")

    type_display = ctk.CTkOptionMenu(master=frame,values=ver_types,variable=def_ver_type)
    type_display.configure(font=("Antipasto Pro Extrabold", 16))
    type_display.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    install_button = ctk.CTkButton(master=frame)
    install_button.configure(text="Instalar", font=("Antipasto Pro Extrabold", 16), command=lambda: verif_ver(ver_name.get(), type_display.get()))
    install_button.grid(row=2, column=0, pady=5, padx=5, sticky="nswe")

    winins.mainloop()

def menu():
    info.grid_propagate(False)
    info.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    mineconf.grid_propagate(False)
    mineconf.grid(row=0, column=1, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=mineconf, text="Configuracion Minecraft", font=("Antipasto Pro Extrabold", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    entry_name.configure(placeholder_text="Nombre de usuario", font=("",16))
    entry_name.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    entry_ram.configure(placeholder_text="Uso de ram",font=("",16))
    entry_ram.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    installVersions.configure(text="Instalar versiones de Minecraft", font=("Antipasto Pro Extrabold", 16), command=install_versions)
    installVersions.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    versions_display.configure(font=("",16))
    versions_display.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    iniciar_minecraft.configure(text="Inicar Minecraft", font=("Antipasto Pro Extrabold", 16), command=ejecutar_minecraft)
    iniciar_minecraft.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    window.mainloop()

menu()