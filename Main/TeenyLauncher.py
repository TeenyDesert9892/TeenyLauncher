import json
import os
import shutil
import subprocess

import customtkinter as ctk
import minecraft_launcher_lib

print("This code was made by TeenyDesert9892")

# Load data and config


def save_config(data):
    with open("assets/config.json", "w") as jsonlFile:
        json.dump(data, jsonlFile, indent=4)


def load_config():
    with open("assets/config.json", "r") as jsonlFile:
        global config
        config = json.load(jsonlFile)


if not os.path.exists("assets/config.json"):
    save_config([{"Launcher": {"Color": "dark", "Version": "0.2.0"}, "Accounts": {"Default": {"User": "Default", "Uuid": "", "Token": ""}}}])
load_config()


def add_acount_data(type, name, pasword):
    if type == "Premiun":
        if name != "":
            if pasword != "":
                auth_code = minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(url='https://TeenyLauncherMinecraft/redirect')
                print(auth_code)
                minecraft_launcher_lib.microsoft_account.complete_login(client_id='d56f21dc-e9f4-439b-b45e-8b4c42c6f541', client_secret=None, redirect_uri=str(f'https://TeenyLauncherMinecraft/redirect?code={auth_code}&state=<optional'), auth_code=auth_code, code_verifier=None)

                config[0]["Accounts"][str(name)] = {'User': str(name), 'Uuid': str(), 'Token': str()}
                save_config(config)
                check_accounts()
                message(f"La cuenta premiun {name} fue creada correctamente!")
            else:
                message("Introduce una clave")
        else:
            message("Introduce un nombre")
    elif type == "No Premiun":
        if name != "":
            config[0]["Accounts"][str(name)] = {'User': str(name), 'Uuid': '', 'Token': ''}
            save_config(config)
            check_accounts()
            message(f"La cuenta no premiun {name} fue creada correctamente!")
        else:
            message("Introduce un nombre")
    else:
        message("Seleccina un tipo de cuanta")


def del_acount_data(account):
    newConfig = [{"Launcher": {'Color': config[0]["Launcher"]["Color"], 'Version': config[0]["Launcher"]["Version"]}, 'Accounts': {}}]
    for ac in config[0]["Accounts"]:
        if not ac == account:
            newConfig[0]["Accounts"][str(ac)] = {'User': config[0]["Accounts"][str(ac)]["User"], 'Uuid': config[0]["Accounts"][str(ac)]["Uuid"], 'Token': config[0]["Accounts"][str(ac)]["Token"]}
    save_config(newConfig)
    load_config()
    check_accounts()
    message(f"La cuenta {account} fue eliminada correctamente!")


# Configure ctk and config

ctk.set_appearance_mode(config[0]["Launcher"]["Color"])
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.geometry("800x500")
window.iconbitmap("assets/images/Icon.ico")
window.title("TeenyLauncher")
window.resizable(width=False, height=False)

top = ctk.CTkFrame(master=window, width=780, height=40)

versionInfoButton = ctk.CTkButton(master=top)
configurationButton = ctk.CTkButton(master=top)

mineconfig = ctk.CTkFrame(master=window, width=260, height=430)

addAcount = ctk.CTkButton(master=mineconfig)
deleteAcount = ctk.CTkButton(master=mineconfig)
acount_display = ctk.CTkOptionMenu(master=mineconfig)

entry_ram = ctk.CTkEntry(master=mineconfig)

installVersions = ctk.CTkButton(master=mineconfig)
uninstallVersions = ctk.CTkButton(master=mineconfig)
versions_display = ctk.CTkOptionMenu(master=mineconfig)

iniciar_minecraft = ctk.CTkButton(master=mineconfig)

# From here to above is all for minecraft_launcher_lib


if os.name == "nt":
    minecraft_directori = f"C:/Users/{os.getlogin()}/AppData/Roaming/.TeenyLauncher"
elif os.name == "posix":
    minecraft_directori = f"/home/{os.getlogin()}/.TeenyLauncher"


def install_minecraft(version):
    minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directori)
    check_vers()
    message(f"La version {version} de minecraft vanilla se ha instalado correctamente!")


def install_forge(version):
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    if not forge:
        message("Esta version no tiene soporte por parte de el equipo de Forge.")
    else:
        minecraft_launcher_lib.forge.install_forge_version(forge, minecraft_directori)
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


def uninstall_minecraft_version(version):
    shutil.rmtree(f'{minecraft_directori}/versions/{version}')
    check_vers()
    message(f"La version {version} ha sido desinstalada con exito!")


def ejecutar_minecraft(version, ram):
    window.destroy()

    name = acount_display.get()
    user = config[0]["Accounts"][name]["User"]
    uuid = config[0]["Accounts"][name]["Uuid"]
    token = config[0]["Accounts"][name]["Token"]
    launcherVersion = config[0]["Launcher"]["Version"]

    if ram == "-XmxG":
        ram = "-Xmx2G"

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, {'username': str(user), 'uuid': str(uuid), 'token': str(token), 'jvArguments': [f"{ram}", f"{ram}"], 'launcherVersion': f"{launcherVersion}"})
    subprocess.run(minecraft_command)

# From here to above is all for customtkinter


def check_accounts():
    accounts = ctk.StringVar()
    list_added_accounts = []
    accounts_added = config[0]["Accounts"]

    for account_added in accounts_added:
        list_added_accounts.append(account_added)

    if len(list_added_accounts) != 0:
        accounts.set(list_added_accounts[0])
    elif len(list_added_accounts) == 0:
        accounts.set('Sin cuentas')
        list_added_accounts.append('Sin cuentas')
    acount_display.configure(variable=accounts, values=list_added_accounts)


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
    winmsg.iconbitmap("assets/images/Icon.ico")
    winmsg.title("Mensaje")
    winmsg.resizable(width=False, height=False)

    msgframe = ctk.CTkFrame(master=winmsg, width=280, height=140)
    msgframe.grid_propagate(False)
    msgframe.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    msgtxt = ctk.CTkLabel(master=msgframe, text=msg, font=("", 16), wraplength=280)
    msgtxt.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    msgbtn = ctk.CTkButton(master=winmsg, text="Ok", font=("", 16), command=winmsg.destroy)
    msgbtn.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    winmsg.mainloop()


def add_acount():
    winAddAc = ctk.CTk()
    winAddAc.geometry("300x300")
    winAddAc.iconbitmap("assets/images/Icon.ico")
    winAddAc.title("Configurar nueva cuenta")
    winAddAc.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winAddAc, width=280, height=280)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=frame, wraplength=320, text="Agregar cuenta", font=("", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    ac_types = ["Premiun", "No Premiun"]
    def_ac_type = ctk.StringVar(value="Selecciona el tipo de cuenta")

    type_display = ctk.CTkOptionMenu(master=frame, values=ac_types, variable=def_ac_type, font=("", 16), width=270)
    type_display.grid_propagate(False)
    type_display.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    name_title = ctk.CTkLabel(master=frame, wraplength=320, text="Nombre de usuario", font=("", 16))
    name_title.grid(row=2, column=0, pady=5, padx=5, sticky="w")

    name_entry = ctk.CTkEntry(master=frame, placeholder_text="Introduce nombre de usuario", font=("", 16))
    name_entry.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    pasword_title = ctk.CTkLabel(master=frame, wraplength=320, text="Clave solo premiun", font=("", 16))
    pasword_title.grid(row=4, column=0, pady=5, padx=5, sticky="w")

    pasword_entry = ctk.CTkEntry(master=frame, placeholder_text="Introduce clave", font=("", 16), show="*")
    pasword_entry.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    add_button = ctk.CTkButton(master=frame, text="Agregar", font=("", 16), command=lambda: add_acount_data(type_display.get(), name_entry.get(), pasword_entry.get()))
    add_button.grid(row=6, column=0, pady=5, padx=5, sticky="nswe")

    winAddAc.mainloop()


def delete_acount():
    winDelAc = ctk.CTk()
    winDelAc.geometry("250x150")
    winDelAc.iconbitmap("assets/images/Icon.ico")
    winDelAc.title("Eliminar Cuenta")
    winDelAc.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winDelAc, width=230, height=130)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=frame, text="Eliminar Cuenta", font=("", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    addedAcounts = []
    for account in config[0]["Accounts"]:
        addedAcounts.append(account)

    selectedAccount = ctk.CTkOptionMenu(master=frame, variable=ctk.StringVar(master=frame, value="Selecciona una cuenta"), values=addedAcounts, font=("", 16), width=220)
    selectedAccount.grid_propagate(False)
    selectedAccount.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    deleteButton = ctk.CTkButton(master=frame, text="Eliminar", font=("", 16), command=lambda: del_acount_data(selectedAccount.get()))
    deleteButton.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    winDelAc.mainloop()


def install_versions():
    winins = ctk.CTk()
    winins.geometry("275x200")
    winins.iconbitmap("assets/images/Icon.ico")
    winins.title("Instalar versiones")
    winins.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winins, width=255, height=180)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    ver_name = ctk.CTkEntry(master=frame, placeholder_text="Numero de la version", font=("", 16))
    ver_name.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    ver_types = ["Vanilla", "Forge", "Fabric", "Quilt"]
    def_ver_type = ctk.StringVar(value="Selecciona el tipo de version")

    type_display = ctk.CTkOptionMenu(master=frame, values=ver_types, variable=def_ver_type, font=("", 16))
    type_display.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    install_button = ctk.CTkButton(master=frame, text="Instalar", font=("", 16), command=lambda: verif_ver(ver_name.get(), type_display.get()))
    install_button.grid(row=2, column=0, pady=5, padx=5, sticky="nswe")

    winins.mainloop()


def uninstall_versions():
    winuns = ctk.CTk()
    winuns.geometry("275x200")
    winuns.iconbitmap("assets/images/Icon.ico")
    winuns.title("Desinstalar versiones")
    winuns.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winuns, width=255, height=180)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    display = ctk.CTkOptionMenu(master=frame, font=("", 16))
    display.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    button = ctk.CTkButton(master=frame, text="Desinstalar", font=("", 24), command=lambda: uninstall_minecraft_version(display.get()))
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


def infoEdit(section, lastFrame):
    lastFrame.destroy()
    info = ctk.CTkFrame(master=window, width=500, height=430)
    info.grid_propagate(False)
    info.place(x=10, y=60)

    if section == "VersionInfo":
        infoTitle = ctk.CTkLabel(master=info, text="TeenyLauncher (v0.1.2)", font=("", 36), wraplength=490)
        infoTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        infoVersionInfo = ctk.CTkLabel(master=info, text="", font=("", 16), wraplength=490)
        infoVersionInfo.grid(row=1, column=0, pady=5, padx=5, sticky="w")
    elif section == "Configuration":
        configurationTitle = ctk.CTkLabel(master=info, text="Configuracion del launcher", font=("", 36), wraplength=490)
        configurationTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")
    else:
        message("Hubo un problema tratando de cargar la interfaz")
    info.update()


def menu():
    top.grid_propagate(False)
    top.place(x=10, y=10)

    info = ctk.CTkFrame(master=window)
    infoEdit("VersionInfo", info)

    versionInfoButton.configure(text="Info v0.1.2", font=("", 20), command=lambda: infoEdit("VersionInfo", info))
    versionInfoButton.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    configurationButton.configure(text="Configuracion", font=("", 20), command=lambda: infoEdit("Configuration", info))
    configurationButton.grid(row=0, column=1, pady=5, padx=5, sticky="nswe")

    mineconfig.grid_propagate(False)
    mineconfig.place(x=520, y=60)

    configTitle = ctk.CTkLabel(master=mineconfig, text="Configuracion Minecraft", font=("", 24))
    configTitle.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    addAcount.configure(text="Agregar cuenta de Minecraft", font=("", 16), command=add_acount)
    addAcount.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    deleteAcount.configure(text="Eliminar cuenta de Minecraft", font=("", 16), command=delete_acount)
    deleteAcount.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    acount_display.configure(font=("", 16))
    acount_display.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    entry_ram.configure(placeholder_text="Uso de ram",font=("", 16))
    entry_ram.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    installVersions.configure(text="Instalar versiones de Minecraft", font=("", 16), command=install_versions)
    installVersions.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    uninstallVersions.configure(text="Desinstalar versiones de Minecraft", font=("", 16), command=uninstall_versions)
    uninstallVersions.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    versions_display.configure(font=("", 16))
    versions_display.grid(row=7, column=0, pady=5, padx=5, sticky="we")

    iniciar_minecraft.configure(text="Inicar Minecraft", font=("", 16), command=lambda: ejecutar_minecraft(versions_display.get(), f"-Xmx{entry_ram.get()}G"))
    iniciar_minecraft.grid(row=8, column=0, pady=5, padx=5, sticky="we")

    window.mainloop()


check_accounts()
check_vers()
menu()
