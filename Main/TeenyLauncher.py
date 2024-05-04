import json
import os
import pickle
import random
import shutil
import subprocess
import threading

import customtkinter as ctk
import minecraft_launcher_lib as mllb

print("This code was made by TeenyDesert9892")

version = "0.3.2"

# Load data and config

def get_short_user():
    count = 0
    user = ""
    for char in os.getlogin():
        if count < 6:
            user += char
            count += 1
    return user

if os.name == "nt":
    try:
        minecraft_directory = f"C:/Users/{os.getlogin()}/AppData/Roaming/.TeenyLauncher"
    except:
        minecraft_directory = f"C:/Users/{get_short_user()}/AppData/Roaming/.TeenyLauncher"

elif os.name == "posix":
    try:
        minecraft_directory = f"/home/{os.getlogin()}/.TeenyLauncher"
    except:
        minecraft_directory = f"/home/{get_short_user()}/.TeenyLauncher"


def save_config(data):
    with open(f"{minecraft_directory}/launcher_config.pkl", "wb") as pickleFile:
        pickle.dump(data, pickleFile)


def load_config():
    with open(f"{minecraft_directory}/launcher_config.pkl", "rb") as pickleFile:
        global config
        config = pickle.load(pickleFile)

def set_languaje(lang):
    langFile = f"Main/assets/lang/{lang}.json"
    if not os.path.exists(langFile):
        langFile = f"assets/lang/{lang}.json"
    global langData
    if os.path.isfile(langFile):
        langData = json.load(open(langFile, "r"))
    else:
        langData = json.load(open("Main/assets/lang/en_en.json", "r"))


def create_uuid():
    uuid = ""

    def create_chain(lenghth):
        chain = ""
        for i in range(0, lenghth):
            char = random.randint(0, 15)
            chain += str(hexa_num(char))
        return chain

    def hexa_num(num):
        letters = ["a", "b", "c", "d", "e", "f"]
        if num >= 0 and num <= 9:
            return str(num)
        else:
            return letters[num-10]

    uuid += create_chain(8)
    uuid += "-"
    for i in range(0, 3):
        uuid += create_chain(4)
        uuid += "-"
    uuid += create_chain(12)
    return uuid


def add_acount_data(type, name, pasword):
    addAcInfo.configure(text="Creating...")
    if type == "Premiun":
        if name != "":
            if pasword != "":
                auth_code = mllb.microsoft_account.get_auth_code_from_url(url='https://TeenyLauncherMinecraft/redirect')
                print(auth_code)
                mllb.microsoft_account.complete_login(client_id='d56f21dc-e9f4-439b-b45e-8b4c42c6f541', client_secret=None, redirect_uri=str(f'https://TeenyLauncherMinecraft/redirect?code={auth_code}&state=<optional'), auth_code=auth_code, code_verifier=None)

                config[0]["Accounts"][str(name)] = {'User': str(name), 'Uuid': str(), 'Token': str()}
                save_config(config)
                check_accounts()
                addAcInfo.configure(text="Create exit!")
                text_message("Add Account Premiun Success", langData[0]["Add_Account_Premiun_Success"])
            else:
                addAcInfo.configure(text="Create failure...")
                text_message("Add Account Pasword Remaining", langData[0]["Add_Account_Pasword_Remaining"])
        else:
            addAcInfo.configure(text="Create failure...")
            text_message("Add Account Name Remaining", langData[0]["Add_Account_Name_Remaining"])
    elif type == "No Premiun":
        if name != "":
            uuid = create_uuid()
            config[0]["Accounts"][str(name)] = {'User': str(name), 'Uuid': str(uuid), 'Token': '0'}
            save_config(config)
            check_accounts()
            addAcInfo.configure(text="Create exit!")
            text_message("Add Account No Premiun Success", langData[0]["Add_Account_No_Premiun_Success"])
        else:
            addAcInfo.configure(text="Create failure...")
            text_message("Add Account Name Remaining", langData[0]["Add_Account_Name_Remaining"])
    else:
        addAcInfo.configure(text="Create failure...")
        text_message("Add Account No Type Selected", langData[0]["Add_Account_No_Type_Selected"])


def del_acount_data(account, *args):
    delAcInfo.configure(text="Deleting...")
    newConfig = [{"Launcher": {'Color': config[0]["Launcher"]["Color"], "Theme": config[0]["Launcher"]["Theme"], "Lang": config[0]["Launcher"]["Lang"], 'Version': config[0]["Launcher"]["Version"]}, 'Accounts': {}}]
    for ac in config[0]["Accounts"]:
        if not ac == account:
            newConfig[0]["Accounts"][str(ac)] = {'User': config[0]["Accounts"][str(ac)]["User"], 'Uuid': config[0]["Accounts"][str(ac)]["Uuid"], 'Token': config[0]["Accounts"][str(ac)]["Token"]}
    save_config(newConfig)
    load_config()
    check_accounts()
    delAcInfo.configure(text="Delete exit!")
    text_message("Delete_Account_Success", langData[0]["Delete_Account_Success"])

# From here to above is all for mllb


def install_minecraft_verison(ver, type):
    installInfo.configure(text="Installing...")
    if ver != "":
        if type == "Vanilla":
            mllb.install.install_minecraft_version(ver, minecraft_directory)
            check_vers()
            installInfo.configure(text="Install succes!")
            text_message("Install_Vanilla_Version_Success", langData[0]["Install_Vanilla_Version_Success"])

        elif type == "Forge":
            if not mllb.forge.find_forge_version(ver):
                text_message("Forge Version Unsuported", langData[0]["Forge_Version_Unsuported"])
            else:
                mllb.forge.install_forge_version(mllb.forge.find_forge_version(ver), minecraft_directory)
                check_vers()
                installInfo.configure(text="Install succes!")
                text_message("Install_Forge_Version_Success", langData[0]["Install_Forge_Version_Success"])

        elif type == "Fabric":
            if not mllb.fabric.is_minecraft_version_supported(ver):
                text_message("Fabric Version Unsuported", langData[0]["Fabric_Version_Unsuported"])
            else:
                mllb.fabric.install_fabric(ver, minecraft_directory)
                check_vers()
                installInfo.configure(text="Install succes!")
                text_message("Install Fabric Version Success", langData[0]["Install_Fabric_Version_Success"])

        elif type == "Quilt":
            if not mllb.quilt.is_minecraft_version_supported(ver):
                text_message("Quilt Version Unsuported", langData[0]["Quilt_Version_Unsuported"])
            else:
                mllb.quilt.install_quilt(ver, minecraft_directory)
                check_vers()
                installInfo.configure(text="Install succes!")
                text_message("Install Quilt Version Success", langData[0]["Install_Quilt_Version_Success"])
        else:
            installInfo.configure(text="Install failure...")
            text_message("Install Version Not Selected", langData[0]["Install_Version_Not_Selected"])
    else:
        installInfo.configure(text="Install failure...")
        text_message("Install Version Type Not Selected", langData[0]["Install_Version_Type_Not_Selected"])


def uninstall_minecraft_version(version, *args):
    uninstallInfo.configure(text="Uninstalling...")
    shutil.rmtree(f"{minecraft_directory}/versions/{version}")
    check_vers()
    text_message("Uninstall Version Success", langData[0]["Uninstall_Version_Success"])
    uninstallInfo.configure(text="Uninstall success!")

def run_minecraft(version, ram):
    print("Saving data...")
    config[0]["Launcher"]["DefaultAccount"] = account_display.get()
    config[0]["Launcher"]["DefaultVersion"] = versions_display.get()
    save_config(config)
    print("Starting minecraft...")
    name = account_display.get()
    if name != langData[0]["Without_Accounts"]:
        window.destroy()

        user = config[0]["Accounts"][name]["User"]
        uuid = config[0]["Accounts"][name]["Uuid"]
        token = config[0]["Accounts"][name]["Token"]
        launcherVersion = config[0]["Launcher"]["Version"]

        if ram == "-XmxG":
            ram = "-Xmx2G"

        print("Running:", version)
        minecraft_command = mllb.command.get_minecraft_command(version, minecraft_directory, {'username': str(user), 'uuid': str(uuid), 'token': str(token), 'jvArguments': str(f"[{str(ram)}, {str(ram)}]"), 'launcherVersion': str(launcherVersion)})
        subprocess.run(minecraft_command)
        print("Restarting...")
        main()
    else:
        text_message("Without Accounts To Play", langData[0]["Without_Accounts_To_Play"])

# From here to above is all for customtkinter


def check_accounts():
    accounts = ctk.StringVar()
    list_added_accounts = []
    accounts_added = config[0]["Accounts"]

    for account_added in accounts_added:
        list_added_accounts.append(account_added)

    if len(list_added_accounts) != 0:
        if config[0]["Launcher"]["DefaultAccount"] == "Null":
            accounts.set(list_added_accounts[0])
        else:
            accounts.set(config[0]["Launcher"]["DefaultAccount"])
    elif len(list_added_accounts) == 0:
        accounts.set(langData[0]["Without_Accounts"])
        list_added_accounts.append(langData[0]["Without_Accounts"])
    account_display.configure(variable=accounts, values=list_added_accounts)


def check_vers():
    vers = ctk.StringVar()
    lista_versiones_instaladas = []
    versiones_instaladas = mllb.utils.get_installed_versions(minecraft_directory)

    for version_instalada in versiones_instaladas:
        lista_versiones_instaladas.append(version_instalada['id'])

    if len(lista_versiones_instaladas) != 0:
        if config[0]["Launcher"]["DefaultVersion"] == "Null":
            vers.set(lista_versiones_instaladas[0])
        else:
            vers.set(config[0]["Launcher"]["DefaultVersion"])
    elif len(lista_versiones_instaladas) == 0:
        vers.set(langData[0]["Without_Versions"])
        lista_versiones_instaladas.append(langData[0]["Without_Versions"])
    versions_display.configure(variable=vers, values=lista_versiones_instaladas)


def text_message(title, msg):
    winmsg = ctk.CTk()
    winmsg.geometry("300x200")
    winmsg.title(title)
    winmsg.resizable(width=False, height=False)
    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        winmsg.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    msgframe = ctk.CTkFrame(master=winmsg, width=280, height=140)
    msgframe.grid_propagate(False)
    msgframe.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    msgtxt = ctk.CTkLabel(master=msgframe, text=msg, font=("", 16), wraplength=280)
    msgtxt.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    msgbtn = ctk.CTkButton(master=winmsg, text="Ok", font=("", 16), command=lambda: winmsg.destroy())
    msgbtn.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    winmsg.mainloop()


def add_acount():
    def add_ac_thread(type, name, password):
        thread = threading.Thread(target=add_acount_data, args=(type, name, password), daemon=True)
        thread.start()

    winAddAc = ctk.CTk()
    winAddAc.geometry("300x325")
    winAddAc.title(langData[0]["Add_Account_Window_Title"])
    winAddAc.resizable(width=False, height=False)
    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        winAddAc.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    AddAcframe = ctk.CTkFrame(master=winAddAc, width=280, height=305)
    AddAcframe.grid_propagate(False)
    AddAcframe.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=AddAcframe, wraplength=320, text=langData[0]["Add_Account_Title"], font=("", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    type_display = ctk.CTkOptionMenu(master=AddAcframe, values=["Premiun", "No Premiun"], variable=ctk.StringVar(value=langData[0]["Add_Account_Type_Default"]), font=("", 16), width=270)
    type_display.grid_propagate(False)
    type_display.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    name_title = ctk.CTkLabel(master=AddAcframe, wraplength=320, text=langData[0]["Add_Account_Name"], font=("", 16))
    name_title.grid(row=2, column=0, pady=5, padx=5, sticky="w")

    name_entry = ctk.CTkEntry(master=AddAcframe, placeholder_text=langData[0]["Add_Account_Name_Input"], font=("", 16))
    name_entry.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    pasword_title = ctk.CTkLabel(master=AddAcframe, wraplength=320, text=langData[0]["Add_Account_Password"], font=("", 16))
    pasword_title.grid(row=4, column=0, pady=5, padx=5, sticky="w")

    pasword_entry = ctk.CTkEntry(master=AddAcframe, placeholder_text=langData[0]["Add_Account_Password_Input"], font=("", 16), show="*")
    pasword_entry.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    add_button = ctk.CTkButton(master=AddAcframe, text=langData[0]["Add_Account_Create_Button"], font=("", 16), command=lambda: add_ac_thread(type_display.get(), name_entry.get(), pasword_entry.get()))
    add_button.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    global addAcInfo
    addAcInfo = ctk.CTkLabel(master=AddAcframe, text="", font=("", 16))
    addAcInfo.grid(row=7, column=0, pady=5, padx=5, sticky="we")

    winAddAc.mainloop()


def delete_acount():
    def del_ac_thread(account):
        thread = threading.Thread(target=del_acount_data, args=(account, None), daemon=True)
        thread.start()

    winDelAc = ctk.CTk()
    winDelAc.geometry("250x175")
    winDelAc.title(langData[0]["Delete_Account_Window_Title"])
    winDelAc.resizable(width=False, height=False)
    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        winDelAc.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    DelAcframe = ctk.CTkFrame(master=winDelAc, width=230, height=155)
    DelAcframe.grid_propagate(False)
    DelAcframe.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=DelAcframe, text=langData[0]["Delete_Account_Title"], font=("", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    selectedAccount = ctk.CTkOptionMenu(master=DelAcframe, variable=ctk.StringVar(master=DelAcframe, value=langData[0]["Delete_Account_Select_Default"]), values=[account for account in config[0]["Accounts"]], font=("", 16), width=220)
    selectedAccount.grid_propagate(False)
    selectedAccount.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    deleteButton = ctk.CTkButton(master=DelAcframe, text=langData[0]["Delete_Account_Button"], font=("", 16), command=lambda: del_ac_thread(selectedAccount.get()))
    deleteButton.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    global delAcInfo
    delAcInfo = ctk.CTkLabel(master=DelAcframe, text="", font=("", 16))
    delAcInfo.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    winDelAc.mainloop()


def install_versions():
    def install_thread(version, type):
        thread = threading.Thread(target=install_minecraft_verison, args=(version, type), demon=True)
        thread.start()
    
    winins = ctk.CTk()
    winins.geometry("275x250")
    winins.title(langData[0]["Install_Versions_Window_Title"])
    winins.resizable(width=False, height=False)
    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        winins.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    Insframe = ctk.CTkFrame(master=winins, width=255, height=225)
    Insframe.grid_propagate(False)
    Insframe.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    verTitle = ctk.CTkLabel(master=Insframe, text=langData[0]["Install_Versions_Num_Title"], font=("", 16))
    verTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

    ver_name = ctk.CTkEntry(master=Insframe, placeholder_text=langData[0]["Install_Versions_Num_Title_Entry"], font=("", 16), width=245)
    ver_name.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    modedTitle = ctk.CTkLabel(master=Insframe, text=langData[0]["Install_Versions_Type_Title"], font=("", 16))
    modedTitle.grid(row=2, column=0, pady=5, padx=5, sticky="w")

    type_display = ctk.CTkOptionMenu(master=Insframe, values=["Vanilla", "Forge", "Fabric", "Quilt"], variable=ctk.StringVar(value=langData[0]["Install_Version_Type_Default"]), font=("", 16))
    type_display.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    install_button = ctk.CTkButton(master=Insframe, text=langData[0]["Install_Versions_Install_Button"], font=("", 16), command=lambda: install_thread(ver_name.get(), type_display.get()))
    install_button.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    global installInfo
    installInfo = ctk.CTkLabel(master=Insframe, text="", font=("", 16))
    installInfo.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    winins.mainloop()


def uninstall_versions():
    def uninstall_thread(version):
        thread = threading.Thread(target=uninstall_minecraft_version, args=(version, None), daemon=True)
        thread.start()
    
    winuns = ctk.CTk()
    winuns.geometry("300x175")
    winuns.title(langData[0]["Uninstall_Version_Window_Title"])
    winuns.resizable(width=False, height=False)
    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        winuns.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    Unsframe = ctk.CTkFrame(master=winuns, width=280, height=155)
    Unsframe.grid_propagate(False)
    Unsframe.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=Unsframe, text=langData[0]["Uninstall_Version_Title"], font=("", 18))
    title.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    display = ctk.CTkOptionMenu(master=Unsframe, font=("", 16))
    display.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    button = ctk.CTkButton(master=Unsframe, text=langData[0]["Uninstall_Version_Button"], font=("", 20), command=lambda: uninstall_thread(display.get()))
    button.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    global uninstallInfo
    uninstallInfo = ctk.CTkLabel(master=Unsframe, text="", font=("", 16))
    uninstallInfo.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    vers = ctk.StringVar()
    lista_versiones_instaladas = []

    versiones_instaladas = mllb.utils.get_installed_versions(minecraft_directory)

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
    print("Saving data...")
    if lang != langData[0]["Info_Configurate_Languaje_Default"]:
        if lang != "empty_example":
            config[0]["Launcher"]["Lang"] = lang
    if color != langData[0]["Info_Configuration_Color_Default"]:
        config[0]["Launcher"]["Color"] = color
    if theme != langData[0]["Info_Configuration_Theme_Default"]:
        config[0]["Launcher"]["Theme"] = theme
    config[0]["Launcher"]["DefaultAccount"] = account_display.get()
    config[0]["Launcher"]["DefaultVersion"] = versions_display.get()
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
        infoTitle = ctk.CTkLabel(master=info, text=str(f"TeenyLauncher (v{config[0]['Launcher']['Version']})"), font=("", 36), wraplength=490)
        infoTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        infoVersionInfo = ctk.CTkLabel(master=info, text=langData[0]["TeenyLauncher_Version_Info"], font=("", 16), wraplength=490)
        infoVersionInfo.grid(row=1, column=0, pady=5, padx=5, sticky="w")

    elif section == "Configuration":
        configurationTitle = ctk.CTkLabel(master=info, text=langData[0]["Info_Configuration_Title"], font=("", 36), wraplength=490)
        configurationTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

        languajeTitle = ctk.CTkLabel(master=info, text=langData[0]["Info_Configurate_Languaje_Title"], font=("", 16))
        languajeTitle.grid(row=1, column=0, pady=5, padx=5, sticky="w")

        langDir = "Main/assets/lang"
        if not os.path.exists(langDir):
            langDir = "assets/lang"

        configurationLanguaje = ctk.CTkOptionMenu(master=info, values=[file.name.replace(".json", "") for file in os.scandir(langDir) if file.is_file()], variable=ctk.StringVar(value=langData[0]["Info_Configurate_Languaje_Default"]), font=("", 16))
        configurationLanguaje.grid(row=2, column=0, pady=5, padx=5, sticky="we")

        themeTitle = ctk.CTkLabel(master=info, text=langData[0]["Info_Configuration_Theme_Title"], font=("", 16))
        themeTitle.grid(row=3, column=0, pady=5, padx=5, sticky="w")

        configurationColor = ctk.CTkOptionMenu(master=info, values=["Light", "Dark"], variable=ctk.StringVar(value=langData[0]["Info_Configuration_Color_Default"]), font=("", 16))
        configurationColor.grid(row=4, column=0, pady=5, padx=5, sticky="we")

        themeDir = "Main/assets/themes"
        if not os.path.exists(themeDir):
            themeDir = "assets/themes"

        configurationTheme = ctk.CTkOptionMenu(master=info, values=[file.name.replace(".json", "") for file in os.scandir(themeDir) if file.is_file()], variable=ctk.StringVar(value=langData[0]["Info_Configuration_Theme_Default"]), font=("", 16))
        configurationTheme.grid(row=5, column=0, pady=5, padx=5, sticky="we")

        configurationSave = ctk.CTkButton(master=info, text=langData[0]["Info_Configuration_Save"], font=("", 16), command=lambda: update_config(configurationLanguaje.get(), configurationColor.get(), configurationTheme.get()))
        configurationSave.grid(row=6, column=0, pady=5, padx=5, sticky="we")
    else:
        infoEdit("LauncherVersion", info)


def main():

    print("Loading Config...")
    load_config()
    if config[0]["Launcher"]["Version"] != version:
        config[0]["Launcher"]["Version"] = version

    print("Loading Launguaje...")
    set_languaje(config[0]["Launcher"]["Lang"])

    print("Loading GUI...")
    ctk.set_appearance_mode(config[0]["Launcher"]["Color"])

    themesDir = f"Main/assets/themes/{config[0]['Launcher']['Theme']}.json"
    if not os.path.exists(themesDir):
        themesDir = f"assets/themes/{config[0]['Launcher']['Theme']}.json"

    ctk.set_default_color_theme(themesDir)

    global window
    window = ctk.CTk()
    window.geometry("800x500")
    window.title("TeenyLauncher")
    window.resizable(width=False, height=False)
    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        window.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    top = ctk.CTkFrame(master=window, width=780, height=40)
    top.grid_propagate(False)
    top.place(x=10, y=10)

    info = ctk.CTkFrame(master=window)
    infoEdit("LauncherVersion", info)

    versionInfoButton = ctk.CTkButton(master=top, text=f"{langData[0]['Top_Button_Info_Version']} v{config[0]['Launcher']['Version']}", font=("", 20), command=lambda: infoEdit("LauncherVersion", info))
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

    global account_display
    account_display = ctk.CTkOptionMenu(master=mineconfig, font=("", 16), width=260)
    account_display.grid(row=4, column=0, pady=5, padx=5, sticky="we")

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

    iniciar_minecraft = ctk.CTkButton(master=mineconfig, text=langData[0]["Menu_Minecraft_Config_Run_Minecraft_Button"], font=("", 20), command=lambda: run_minecraft(versions_display.get(), str(f"-Xmx{entry_ram.get()}G")))
    iniciar_minecraft.grid(row=11, column=0, pady=5, padx=5, sticky="we")

    print("Loading Accounts...")
    check_accounts()

    print("Loading Versions...")
    check_vers()

    print("Done!")
    window.mainloop()


if __name__ == "__main__":
    try:
        if not mllb.utils.is_minecraft_installed(minecraft_directory):
            print("Installing launcher libraries... (This may take a while)")
            mllb.install.install_minecraft_version(mllb.utils.get_latest_version()['release'], minecraft_directory)
    except:
        print("The base libraries wasn't installed correctly please check your wifi...")
    if not os.path.exists(f"{minecraft_directory}/launcher_config.pkl"):
        save_config([{"Launcher": {"Color": "Dark", "Theme": "Green", "Lang": "es_es", "DefaultAccount": "Null", "DefaultVersion": "Null", "Version": str(version)}, "Accounts": {}}])
    print("Starting...")
    main()
    print("Saving data...")
    config[0]["Launcher"]["DefaultAccount"] = account_display.get()
    config[0]["Launcher"]["DefaultVersion"] = versions_display.get()
    save_config(config)
    print("Program finished!")