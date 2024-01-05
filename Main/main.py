import customtkinter as ctk
import minecraft_launcher_lib
import os
import subprocess
import shutil
from scripts import configupdate

print("This code was made by TeenyDesert9892")

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
uninstallVersions = ctk.CTkButton(master=mineconf)

versions_display = ctk.CTkOptionMenu(master=mineconf)
updateVersions = ctk.CTkButton(master=mineconf)
iniciar_minecraft = ctk.CTkButton(master=mineconf)

user = os.getenv('USERNAME')
if os.name == "nt":
    minecraft_directori = f"C:/Users/{user}/AppData/Roaming/.TeenyLauncher"
elif os.name == "posix":
    minecraft_directori = f"/home/{user}/.TeenyLauncher"

def check_vers():
    vers = ctk.StringVar()
    lista_versiones_instaladas = []
    versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)

    for version_instalada in versiones_instaladas:
        lista_versiones_instaladas.append(version_instalada['id'])

    if len(lista_versiones_instaladas) != 0:
        vers.set(lista_versiones_instaladas[0])
    elif len(lista_versiones_instaladas) == 0:
        vers.set('Sin versiones instaladas')
        lista_versiones_instaladas.append('Sin versiones instaladas')
    versions_display.configure(variable=vers, values=lista_versiones_instaladas)

def message(msg):
    winmsg = ctk.CTk()
    winmsg.geometry("300x200")
    winmsg.iconbitmap("assets/Icon.ico")
    winmsg.title("Mensaje")
    winmsg.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winmsg, width=280, height=140)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    msgtxt = ctk.CTkLabel(master=frame, text=msg, font=("Antipasto Pro Extrabold", 16),wraplength=280)
    msgtxt.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    msgbtn = ctk.CTkButton(master=winmsg,text="Ok", font=("Antipasto Pro Extrabold", 16),command=winmsg.destroy)
    msgbtn.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    winmsg.mainloop()

def install_minecraft(version):
    minecraft_launcher_lib.install.install_minecraft_version(version,minecraft_directori)
    check_vers()
    message(f"La version de minecraft vanilla se ha instalado correctamente!")

def install_forge(version):
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    if not forge:
        message("Esta version no tiene soporte por parte de el equipo de Forge.")
    else:
        minecraft_launcher_lib.forge.install_forge_version(forge,minecraft_directori)
        check_vers()
        message("La version de minecraft forge se ha instalado correctamente!")

def install_fabric(version):
    if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(version):
        message("Esta version no tiene soporte por parte de el equipo de Fabric.")
    else:
        minecraft_launcher_lib.fabric.install_fabric(version, minecraft_directori)
        check_vers()
        message('La version de minecraft fabric se ha instalado correctamente!')

def install_quilt(version):
    if not minecraft_launcher_lib.quilt.is_minecraft_version_supported(version):
        message("Esta version no tiene soporte por parte de el equipo de Quilt.")
    else:
        minecraft_launcher_lib.quilt.install_quilt(version, minecraft_directori)
        check_vers()
        message("La version de minecraft quilt se ha instalado correctamente!")

def ejecutar_minecraft(user, version, ram):
    options = {'username': user,'uuid' : '','token': '','jvArguments': [ram,ram],'launcherVersion': "1.0.0"}

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)
    subprocess.run(minecraft_command)

def verif_ver(ver, type):
    if ver != "":
        if type == "Vanilla":
            install_minecraft(ver)
        elif type == "Forge":
            install_forge(ver)
        elif type == "Fabric":
            install_fabric(ver)
        elif type == "Quilt":
            install_quilt(ver)
        else:
            message("Selecciona un tipo de verion!")
    else:
        message("Introduce el numero de la version!")

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

def uninstall_minecraft_version(version):
    shutil.rmtree(minecraft_directori + '/versions/' + version)
    check_vers()
    message(f"La version {version} ha sido desinstalada con exito!")

def uninstall_versions():
    winuns = ctk.CTk()
    winuns.geometry("300x200")
    winuns.iconbitmap("assets/Icon.ico")
    winuns.title("Desinstalar versiones")
    winuns.resizable(width=False, height=False)

    display = ctk.CTkOptionMenu(master=winuns,font=("",16))
    display.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    button = ctk.CTkButton(master=winuns,text="Desinstalar",font=("Antipasto Pro Extrabold", 24),command=lambda: uninstall_minecraft_version(display.get()))
    button.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    vers = ctk.StringVar()
    lista_versiones_instaladas = []

    versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)

    for version_instalada in versiones_instaladas:
        lista_versiones_instaladas.append(version_instalada['id'])

    if len(lista_versiones_instaladas) != 0:
        vers.set(lista_versiones_instaladas[0])
    elif len(lista_versiones_instaladas) == 0:
        vers.set('Sin versiones instaladas')
        lista_versiones_instaladas.append('Sin versiones instaladas')

    display.configure(variable=vers, values=lista_versiones_instaladas)

    winuns.mainloop()

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

    uninstallVersions.configure(text="Desinstalar versiones de Minecraft", font=("Antipasto Pro Extrabold", 16), command=uninstall_versions)
    uninstallVersions.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    versions_display.configure(font=("",16))
    versions_display.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    iniciar_minecraft.configure(text="Inicar Minecraft", font=("Antipasto Pro Extrabold", 16), command=lambda: ejecutar_minecraft(entry_name.get(), versions_display.get(), f"-Xmx{entry_ram.get()}G"))
    iniciar_minecraft.grid(row=7, column=0, pady=5, padx=5, sticky="we")

    window.mainloop()

check_vers()
menu()