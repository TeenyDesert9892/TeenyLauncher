import json
import os
import shutil
import subprocess
import threading

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

def set_languaje(lang):
    langFile = f"assets/lang/{lang}.json"
    global langData
    if os.path.isfile(langFile):
        langData = json.load(open(langFile, "r"))
    else:
        langData = json.load(open("assets/lang/en_en.json", "r"))


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
                message("Add Account Premiun Success", langData[0]["Add_Account_Premiun_Success"])
            else:
                message("Add Account Pasword Remaining", langData[0]["Add_Account_Pasword_Remaining"])
        else:
            message("Add Account Name Remaining", langData[0]["Add_Account_Name_Remaining"])
    elif type == "No Premiun":
        if name != "":
            config[0]["Accounts"][str(name)] = {'User': str(name), 'Uuid': '', 'Token': ''}
            save_config(config)
            check_accounts()
            message("Add Account No Premiun Success", langData[0]["Add_Account_No_Premiun_Success"])
        else:
            message("Add Account Name Remaining", langData[0]["Add_Account_Name_Remaining"])
    else:
        message("Add Account No Type Selected", langData[0]["Add_Account_No_Type_Selected"])


def del_acount_data(account):
    newConfig = [{"Launcher": {'Color': config[0]["Launcher"]["Color"], "Theme": config[0]["Launcher"]["Theme"], "Lang": config[0]["Launcher"]["Lang"], 'Version': config[0]["Launcher"]["Version"]}, 'Accounts': {}}]
    for ac in config[0]["Accounts"]:
        if not ac == account:
            newConfig[0]["Accounts"][str(ac)] = {'User': config[0]["Accounts"][str(ac)]["User"], 'Uuid': config[0]["Accounts"][str(ac)]["Uuid"], 'Token': config[0]["Accounts"][str(ac)]["Token"]}
    save_config(newConfig)
    load_config()
    check_accounts()
    message("Delete_Account_Success", langData[0]["Delete_Account_Success"])

# From here to above is all for minecraft_launcher_lib


if os.name == "nt":
    minecraft_directori = f"C:/Users/{os.getlogin()}/AppData/Roaming/.TeenyLauncher"
elif os.name == "posix":
    minecraft_directori = f"/home/{os.getlogin()}/.TeenyLauncher"


def verif_ver(ver, type):
    if ver != "":
        if type == "Vanilla":
            minecraft_launcher_lib.install.install_minecraft_version(ver, minecraft_directori)
            check_vers()
            message("Install_Vanilla_Version_Success", langData[0]["Install_Vanilla_Version_Success"])
            
        elif type == "Forge":
            forge = minecraft_launcher_lib.forge.find_forge_version(ver)
            if not forge:
                message("Forge Version Unsuported", langData[0]["Forge_Version_Unsuported"])

            else:
                minecraft_launcher_lib.forge.install_forge_version(forge, minecraft_directori)
                check_vers()
                message("Install_Forge_Version_Success", langData[0]["Install_Forge_Version_Success"])

        elif type == "Fabric":
            if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(ver):
                message("Fabric Version Unsuported", langData[0]["Fabric_Version_Unsuported"])
            else:
                minecraft_launcher_lib.fabric.install_fabric(ver, minecraft_directori)
                check_vers()
                message("Install Fabric Version Success", langData[0]["Install_Fabric_Version_Success"])

        elif type == "Quilt":
            if not minecraft_launcher_lib.quilt.is_minecraft_version_supported(ver):
                message("Quilt Version Unsuported", langData[0]["Quilt_Version_Unsuported"])
            else:
                minecraft_launcher_lib.quilt.install_quilt(ver, minecraft_directori)
                check_vers()
                message("Install Quilt Version Success", langData[0]["Install_Quilt_Version_Success"])
        else:
            message("Install Version Not Selected", langData[0]["Install_Version_Not_Selected"])
    else:
        message("Install Version Type Not Selected", langData[0]["Install_Version_Type_Not_Selected"])


def uninstall_minecraft_version(version):
    shutil.rmtree(f'{minecraft_directori}/versions/{version}')
    check_vers()
    message("Uninstall Version Success", langData[0]["Uninstall_Version_Success"])


def ejecutar_minecraft(version, ram, name):
    if name != langData[0]["Without_Accounts"]:
        window.destroy()

        user = config[0]["Accounts"][name]["User"]
        uuid = config[0]["Accounts"][name]["Uuid"]
        token = config[0]["Accounts"][name]["Token"]
        launcherVersion = config[0]["Launcher"]["Version"]

        if ram == "-XmxG":
            ram = "-Xmx2G"

        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, {'username': str(user), 'uuid': str(uuid), 'token': str(token), 'jvArguments': [f"{ram}", f"{ram}"], 'launcherVersion': f"{launcherVersion}"})
        subprocess.run(minecraft_command)
    else:
        message("Without Accounts To Play", langData[0]["Without_Accounts_To_Play"])

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
        accounts.set(langData[0]["Without_Accounts"])
        list_added_accounts.append(langData[0]["Without_Accounts"])
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
        vers.set(langData[0]["Without_Versions"])
        lista_versiones_instaladas.append(langData[0]["Without_Versions"])
    versions_display.configure(variable=vers, values=lista_versiones_instaladas)


def message(title, msg):
    winmsg = ctk.CTk()
    winmsg.geometry("300x200")
    winmsg.iconbitmap("assets/images/Icon.ico")
    winmsg.title(title)
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
    winAddAc.title(langData[0]["Add_Account_Window_Title"])
    winAddAc.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winAddAc, width=280, height=280)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=frame, wraplength=320, text=langData[0]["Add_Account_Title"], font=("", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    type_display = ctk.CTkOptionMenu(master=frame, values=["Premiun", "No Premiun"], variable=ctk.StringVar(value=langData[0]["Add_Account_Type_Default"]), font=("", 16), width=270)
    type_display.grid_propagate(False)
    type_display.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    name_title = ctk.CTkLabel(master=frame, wraplength=320, text=langData[0]["Add_Account_Name"], font=("", 16))
    name_title.grid(row=2, column=0, pady=5, padx=5, sticky="w")

    name_entry = ctk.CTkEntry(master=frame, placeholder_text=langData[0]["Add_Account_Name_Input"], font=("", 16))
    name_entry.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    pasword_title = ctk.CTkLabel(master=frame, wraplength=320, text=langData[0]["Add_Account_Password"], font=("", 16))
    pasword_title.grid(row=4, column=0, pady=5, padx=5, sticky="w")

    pasword_entry = ctk.CTkEntry(master=frame, placeholder_text=langData[0]["Add_Account_Password_Input"], font=("", 16), show="*")
    pasword_entry.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    add_button = ctk.CTkButton(master=frame, text=langData[0]["Add_Account_Create_Button"], font=("", 16), command=lambda: add_acount_data(type_display.get(), name_entry.get(), pasword_entry.get()))
    add_button.grid(row=6, column=0, pady=5, padx=5, sticky="nswe")

    winAddAc.mainloop()


def delete_acount():
    winDelAc = ctk.CTk()
    winDelAc.geometry("250x150")
    winDelAc.iconbitmap("assets/images/Icon.ico")
    winDelAc.title(langData[0]["Delete_Account_Window_Title"])
    winDelAc.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winDelAc, width=230, height=130)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=frame, text=langData[0]["Delete_Account_Title"], font=("", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    addedAcounts = []
    for account in config[0]["Accounts"]:
        addedAcounts.append(account)

    selectedAccount = ctk.CTkOptionMenu(master=frame, variable=ctk.StringVar(master=frame, value=langData[0]["Delete_Account_Select_Default"]), values=addedAcounts, font=("", 16), width=220)
    selectedAccount.grid_propagate(False)
    selectedAccount.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    deleteButton = ctk.CTkButton(master=frame, text=langData[0]["Delete_Account_Button"], font=("", 16), command=lambda: del_acount_data(selectedAccount.get()))
    deleteButton.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    winDelAc.mainloop()


def install_versions():
    winins = ctk.CTk()
    winins.geometry("275x225")
    winins.iconbitmap("assets/images/Icon.ico")
    winins.title(langData[0]["Install_Versions_Window_Title"])
    winins.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winins, width=255, height=205)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    verTitle = ctk.CTkLabel(master=frame, text=langData[0]["Install_Versions_Num_Title"], font=("", 16))
    verTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

    ver_name = ctk.CTkEntry(master=frame, placeholder_text=langData[0]["Install_Versions_Num_Title_Entry"], font=("", 16))
    ver_name.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    modedTitle = ctk.CTkLabel(master=frame, text=langData[0]["Install_Versions_Type_Title"], font=("", 16))
    modedTitle.grid(row=2, column=0, pady=5, padx=5, sticky="w")

    type_display = ctk.CTkOptionMenu(master=frame, values=["Vanilla", "Forge", "Fabric", "Quilt"], variable=ctk.StringVar(value=langData[0]["Install_Version_Type_Default"]), font=("", 16))
    type_display.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    install_button = ctk.CTkButton(master=frame, text=langData[0]["Install_Versions_Install_Button"], font=("", 16), command=lambda: verif_ver(ver_name.get(), type_display.get()))
    install_button.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    winins.mainloop()


def uninstall_versions():
    winuns = ctk.CTk()
    winuns.geometry("300x150")
    winuns.iconbitmap("assets/images/Icon.ico")
    winuns.title(langData[0]["Uninstall_Version_Window_Title"])
    winuns.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winuns, width=280, height=130)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=frame, text=langData[0]["Uninstall_Version_Title"], font=("", 18))
    title.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    display = ctk.CTkOptionMenu(master=frame, font=("", 16))
    display.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    button = ctk.CTkButton(master=frame, text=langData[0]["Uninstall_Version_Button"], font=("", 20), command=lambda: uninstall_minecraft_version(display.get()))
    button.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    vers = ctk.StringVar()
    lista_versiones_instaladas = []

    versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)

    for version_instalada in versiones_instaladas:
        lista_versiones_instaladas.append(version_instalada['id'])

    if len(lista_versiones_instaladas) != 0:
        vers.set(lista_versiones_instaladas[0])
    elif len(lista_versiones_instaladas) == 0:
        vers.set(langData[0]["Without_Versions"])
        lista_versiones_instaladas.append(langData[0]["Without_Versions"])

    display.configure(variable=vers, values=lista_versiones_instaladas)

    winuns.mainloop()


def update_config(lang, color, theme):
    if lang != langData[0]["Info_Configurate_Languaje_Default"]:
        if lang != "empty_example":
            config[0]["Launcher"]["Lang"] = lang
    if color != langData[0]["Info_Configuration_Color_Default"]:
        config[0]["Launcher"]["Color"] = color
    if theme != langData[0]["Info_Configuration_Theme_Default"]:
        config[0]["Launcher"]["Theme"] = theme
    save_config(config)
    window.destroy()
    print("Reloading...")
    main()


def infoEdit(section, lastFrame):
    lastFrame.destroy()
    info = ctk.CTkFrame(master=window, width=500, height=430)
    info.grid_propagate(False)
    info.place(x=10, y=60)

    if section == "LauncherVersion":
        infoTitle = ctk.CTkLabel(master=info, text=f"TeenyLauncher (v{config[0]["Launcher"]["Version"]})", font=("", 36), wraplength=490)
        infoTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        infoVersionInfo = ctk.CTkLabel(master=info, text=langData[0]["TeenyLauncher_Version_Info"], font=("", 16), wraplength=490)
        infoVersionInfo.grid(row=1, column=0, pady=5, padx=5, sticky="w")

    elif section == "Configuration":
        configurationTitle = ctk.CTkLabel(master=info, text=langData[0]["Info_Configuration_Title"], font=("", 36), wraplength=490)
        configurationTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        languajeTitle = ctk.CTkLabel(master=info, text=langData[0]["Info_Configurate_Languaje_Title"], font=("", 16))
        languajeTitle.grid(row=1, column=0, pady=5, padx=5, sticky="w")

        configurationLanguaje = ctk.CTkOptionMenu(master=info, values=[file.name.replace(".json", "") for file in os.scandir("assets/lang") if file.is_file()], variable=ctk.StringVar(value=langData[0]["Info_Configurate_Languaje_Default"]), font=("", 16))
        configurationLanguaje.grid(row=2, column=0, pady=5, padx=5, sticky="we")

        themeTitle = ctk.CTkLabel(master=info, text=langData[0]["Info_Configuration_Theme_Title"], font=("", 16))
        themeTitle.grid(row=3, column=0, pady=5, padx=5, sticky="w")

        configurationColor = ctk.CTkOptionMenu(master=info, values=["Light", "Dark"], variable=ctk.StringVar(value=langData[0]["Info_Configuration_Color_Default"]), font=("", 16))
        configurationColor.grid(row=4, column=0, pady=5, padx=5, sticky="we")

        configurationTheme = ctk.CTkOptionMenu(master=info, values=[file.name.replace(".json", "") for file in os.scandir("assets/themes") if file.is_file()], variable=ctk.StringVar(value=langData[0]["Info_Configuration_Theme_Default"]), font=("", 16))
        configurationTheme.grid(row=5, column=0, pady=5, padx=5, sticky="we")

        configurationSave = ctk.CTkButton(master=info, text=langData[0]["Info_Configuration_Save"], font=("", 16), command=lambda: update_config(configurationLanguaje.get(), configurationColor.get(), configurationTheme.get()))
        configurationSave.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    else:
        infoEdit("LauncherVersion", info)


def main():
    print("Loading Config...")
    if not os.path.exists("assets/config.json"):
        save_config([{"Launcher": {"Color": "Dark", "Theme": "Green", "Lang": "es_es", "Version": "0.2.0"}, "Accounts": {}}])
    load_config()

    print("Loading Launguaje...")
    set_languaje(config[0]["Launcher"]["Lang"])

    print("Loading GUI...")
    ctk.set_appearance_mode(config[0]["Launcher"]["Color"])
    ctk.set_default_color_theme(f"assets/themes/{config[0]["Launcher"]["Theme"]}.json")

    global window
    window = ctk.CTk()
    window.geometry("800x500")
    window.iconbitmap("assets/images/Icon.ico")
    window.title("TeenyLauncher")
    window.resizable(width=False, height=False)

    top = ctk.CTkFrame(master=window, width=780, height=40)
    top.grid_propagate(False)
    top.place(x=10, y=10)

    info = ctk.CTkFrame(master=window)
    infoEdit("LauncherVersion", info)

    versionInfoButton = ctk.CTkButton(master=top, text=f"{langData[0]["Top_Button_Info_Version"]} v{config[0]["Launcher"]["Version"]}", font=("", 20), command=lambda: infoEdit("LauncherVersion", info))
    versionInfoButton.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    configurationButton = ctk.CTkButton(master=top, text=langData[0]["Top_Button_Configuration"], font=("", 20), command=lambda: infoEdit("Configuration", info))
    configurationButton.grid(row=0, column=1, pady=5, padx=5, sticky="nswe")

    mineconfig = ctk.CTkFrame(master=window, width=270, height=430)
    mineconfig.grid_propagate(False)
    mineconfig.place(x=520, y=60)

    acountsTitle = ctk.CTkLabel(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Account_Title"], font=("", 16))
    acountsTitle.grid(row=1, column=0, pady=5, padx=5, sticky="w")

    addAcount = ctk.CTkButton(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Add_Account"], font=("", 16), command=add_acount)
    addAcount.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    deleteAcount = ctk.CTkButton(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Delete_Account"], font=("", 16), command=delete_acount)
    deleteAcount.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    global acount_display
    acount_display = ctk.CTkOptionMenu(master=mineconfig, font=("", 16), width=260)
    acount_display.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    ramTitle = ctk.CTkLabel(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Ram_Title"], font=("", 16))
    ramTitle.grid(row=5, column=0, pady=5, padx=5, sticky="w")

    entry_ram = ctk.CTkEntry(master=mineconfig, placeholder_text=langData[0]["Menu_Minecraft_Config_Ram_Input"], font=("", 16))
    entry_ram.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    versionsTitle = ctk.CTkLabel(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Version_Title"], font=("", 16))
    versionsTitle.grid(row=7, column=0, pady=5, padx=5, sticky="w")

    installVersions = ctk.CTkButton(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Install_Version"], font=("", 16), command=install_versions)
    installVersions.grid(row=8, column=0, pady=5, padx=5, sticky="we")

    uninstallVersions = ctk.CTkButton(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Uninstall_Version"], font=("", 16), command=uninstall_versions)
    uninstallVersions.grid(row=9, column=0, pady=5, padx=5, sticky="we")

    global versions_display
    versions_display = ctk.CTkOptionMenu(master=mineconfig, font=("", 16))
    versions_display.grid(row=10, column=0, pady=5, padx=5, sticky="we")

    runMinecraft = threading.Thread(target=(ejecutar_minecraft), args=(versions_display.get(), f"-Xmx{entry_ram.get()}G", acount_display.get()))

    iniciar_minecraft = ctk.CTkButton(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Run_Minecraft_Button"], font=("", 20), command=lambda: runMinecraft.start())
    iniciar_minecraft.grid(row=11, column=0, pady=5, padx=5, sticky="we")

    print("Loading Accounts...")
    check_accounts()

    print("Loading Versions...")
    check_vers()

    print("Done!")
    window.mainloop()

if __name__ == "__main__":
    print("Starting...")
    main()