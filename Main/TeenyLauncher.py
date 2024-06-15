import json
import os
import pathlib
import pickle
import platform
import random
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

import customtkinter as ctk
import minecraft_launcher_lib as mllb
import psutil
from PIL import Image

print("This code was made by TeenyDesert9892")

version = "0.6.0"

version_info = "TeenyLauncher V0.6.0 BIG update:\n" \
               "\n" \
               "In this version I added a ton of things like a background img which\n" \
               "you can choese to use it or not, a config option to change te path\n" \
               "of the launcher files and I have improve the gui looking and working"

launcherConfig = {"Color": "Dark",
                  "Theme": "Green",
                  "Lang": "en_en",
                  "DefaultAccount": "",
                  "DefaultVersion": "",
                  "Version": version,
                  "EnabledBgImg": True,
                  "RamAmount": 2048}


def get_launcher_path():
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".TeenyLauncher")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "TeenyLauncher")
    else:
        return os.path.join(str(pathlib.Path.home()), ".TeenyLauncher")


def open_versions_folder():
    if os.name == "nt":
        os.startfile(minecraft_directory)
    elif os.name == "posix":
        os.system(f'xdg-open "{minecraft_directory}"')


def save_config(data=str):
    with open(f"{get_launcher_path()}/launcher_config.pkl", "wb") as pickleFile:
        pickle.dump(data, pickleFile)


def load_config():
    with open(f"{get_launcher_path()}/launcher_config.pkl", "rb") as pickleFile:
        global config
        config = pickle.load(pickleFile)

def set_languaje(lang=str):
    langFile = str(f"Main/assets/lang/{lang}.json")
    if not os.path.exists(langFile):
        langFile = str(f"assets/lang/{lang}.json")

    global langData
    if os.path.isfile(langFile):
        langData = json.load(open(langFile, "r"))
    else:
        langData = json.load(open("Main/assets/lang/en_en.json", "r"))


def add_acount_data(type=str, name=str, pasword=str):
    if type == "Premiun":
        if name != "":
            if pasword != "":
                progressMessage.configure(text=str(f"Adding {name} premiun account"))
                progressPercentage.set(value=0 / 1)
                progressLabel.configure(text="0/1")

                try:
                    auth_response = mllb.microsoft_types.MinecraftAuthenticateResponse(username=name, roles=[], access_token="", token_type="", expires_in=1)
                    auth_token = mllb.microsoft_account.authenticate_with_minecraft(name, pasword)
                    profile = mllb.microsoft_account.get_profile(access_token=auth_token)
                    store_info = mllb.microsoft_account.get_store_information(access_token=auth_token)

                    print(auth_response)
                    print(auth_token)
                    print(profile)
                    print(store_info)

                    # config[0]["Accounts"][str(name)] = {'User': str(name), 'Uuid': str(), 'Token': str()}
                    # save_config(config)
                    check_accounts()

                    progressPercentage.set(value=1)
                    progressLabel.configure(text="1/1")

                    text_message("Add Account Premiun Success", langData[0]["Add_Account_Premiun_Success"])

                except:
                    text_message("Add Account Premiun Failure", langData[0]["Add_Account_Premiun_Failure"])

                reset_progress()

            else:
                text_message("Add Account Pasword Remaining", langData[0]["Add_Account_Pasword_Remaining"])

        else:
            text_message("Add Account Name Remaining", langData[0]["Add_Account_Name_Remaining"])

    elif type == "No Premiun":
        if name != "":
            progressMessage.configure(text=str(f"Creating {name} no premiun account"))
            progressPercentage.set(value=0 / 1)
            progressLabel.configure(text="0/1")

            try:
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

                config[0]["Accounts"][str(name)] = {'User': str(name),
                                                    'Uuid': str(uuid),
                                                    'Token': '0'}
                save_config(config)
                check_accounts()

                progressPercentage.set(value=1)
                progressLabel.configure(text="1/1")

                text_message("Add Account No Premiun Success", langData[0]["Add_Account_No_Premiun_Success"])
            except:
                text_message("Add Account No Premiun Failure", langData[0]["Add_Account_No_Premiun_Failure"])
            reset_progress()
        else:
            text_message("Add Account Name Remaining", langData[0]["Add_Account_Name_Remaining"])
    else:
        text_message("Add Account No Type Selected", langData[0]["Add_Account_No_Type_Selected"])


def del_acount_data(account=str):
    progressMessage.configure(text=str(f"Deleting {account} account"))
    progressPercentage.set(value=0 / 1)
    progressLabel.configure(text="0/1")

    try:
        launcherSettings = {}
        for setting in config[0]["Launcher"]:
            launcherSettings[setting] = config[0]["Launcher"][setting]

        newConfig = [{"Launcher": launcherSettings, 'Accounts': {}}]

        for ac in config[0]["Accounts"]:
            if ac != account:
                newConfig[0]["Accounts"][str(ac)] = {'User': config[0]["Accounts"][str(ac)]["User"],
                                                     'Uuid': config[0]["Accounts"][str(ac)]["Uuid"],
                                                     'Token': config[0]["Accounts"][str(ac)]["Token"]}

        save_config(newConfig)
        load_config()
        check_accounts()

        progressPercentage.set(value=1)
        progressLabel.configure(text="1/1")

        text_message("Delete_Account_Success", langData[0]["Delete_Account_Success"])
    except:
        text_message("Delete Account Failure", langData[0]["Delete_Account_Failure"])
    reset_progress()


def install_minecraft_verison(name=str, ver=str, type=str, mod=str):
    def save_version(data):
        file = open(str(f"{minecraft_directory}/{name}/version.txt"), "w")
        file.write(data)
        file.close()

    callback = {"setStatus": set_progress_status, "setProgress": set_current_proggres, "setMax": set_progress_max}

    alreadyExistsName = False

    for dir in os.scandir(minecraft_directory):
        if name == dir.name:
            alreadyExistsName = True

    if not alreadyExistsName:
        if name != "":
            if ver != "":
                if type == "Vanilla" or type == "Snapshot":
                    try:
                        mllb.install.install_minecraft_version(versionid=ver,
                                                               minecraft_directory=str(f"{minecraft_directory}/{name}"),
                                                               callback=callback)

                        save_version(ver)
                        check_vers()

                        text_message("Install Vanilla Version Success", langData[0]["Install_Vanilla_Version_Success"])

                    except:
                        if os.path.exists(str(f"{minecraft_directory}/{name}")):
                            shutil.rmtree(str(f"{minecraft_directory}/{name}"))

                        text_message("Install Vanilla Version Failure", langData[0]["Install_Vanilla_Version_Failure"])

                elif type == "Forge":
                    try:
                        mllb.forge.install_forge_version(versionid=mod,
                                                         path=str(f"{minecraft_directory}/{name}"),
                                                         callback=callback)

                        save_version(mod.replace("-", "-forge-"))
                        check_vers()

                        text_message("Install_Forge_Version_Success", langData[0]["Install_Forge_Version_Success"])

                    except:
                        if os.path.exists(str(f"{minecraft_directory}/{name}")):
                            shutil.rmtree(str(f"{minecraft_directory}/{name}"))

                        text_message("Install Forge Version Failure", langData[0]["Install_Forge_Version_Failure"])

                elif type == "Fabric" or type == "Fabric Snapshot":
                    try:
                        mllb.fabric.install_fabric(minecraft_version=ver,
                                                   minecraft_directory=str(f"{minecraft_directory}/{name}"),
                                                   loader_version=mod,
                                                   callback=callback)

                        save_version(str(f"fabric-loader-{mod}-{ver}"))
                        check_vers()

                        text_message("Install Fabric Version Success", langData[0]["Install_Fabric_Version_Success"])

                    except:
                        if os.path.exists(str(f"{minecraft_directory}/{name}")):
                            shutil.rmtree(str(f"{minecraft_directory}/{name}"))

                        text_message("Install Fabric Version Failure", langData[0]["Install_Fabric_Version_Failure"])

                elif type == "Quilt" or type == "Quilt Snapshot":
                    try:
                        mllb.quilt.install_quilt(minecraft_version=ver,
                                                 minecraft_directory=str(f"{minecraft_directory}/{name}"),
                                                 loader_version=mod,
                                                 callback=callback)

                        save_version(str(f"quilt-loader-{mod}-{ver}"))
                        check_vers()

                        text_message("Install Quilt Version Success", langData[0]["Install_Quilt_Version_Success"])

                    except:
                        if os.path.exists(str(f"{minecraft_directory}/{name}")):
                            shutil.rmtree(str(f"{minecraft_directory}/{name}"))

                        text_message("Install Quilt Version Failure", langData[0]["Install_Quilt_Version_Failure"])

                else:
                    text_message("Install Version Not Selected", langData[0]["Install_Version_Not_Selected"])

                reset_progress()

            else:
                text_message("Install Version Type Not Selected", langData[0]["Install_Version_Type_Not_Selected"])

        else:
            text_message("Install Version Not Name", langData[0]["Install_Version_Not_Name"])

    else:
        text_message("Install Version Not Name", langData[0]["Install_Version_Not_Name"])


def uninstall_minecraft_version(version=str):
    try:
        progressMessage.configure(text=str(f"Uninstalling {version}"))
        progressPercentage.set(value=0 / 1)
        progressLabel.configure(text="0/1")

        shutil.rmtree(f"{minecraft_directory}/{version}")

        check_vers()

        progressPercentage.set(value=1)
        progressLabel.configure(text="1/1")

        text_message("Uninstall Version Success", langData[0]["Uninstall_Version_Success"])
        reset_progress()
    except:
        text_message("Uninstall Version Failure", langData[0]["Uninstall_Version_Failure"])

def run_minecraft(version=str):
    print("Saving data...")
    config[0]["Launcher"]["DefaultAccount"] = account_display.get()
    config[0]["Launcher"]["DefaultVersion"] = versions_display.get()

    save_config(config)

    print("Starting minecraft...")
    name = account_display.get()

    if name != langData[0]["Without_Accounts"]:
        window.destroy()

        ram = f"-Xmx{config[0]['Launcher']['RamAmount']}M"
        user = config[0]["Accounts"][name]["User"]
        uuid = config[0]["Accounts"][name]["Uuid"]
        token = config[0]["Accounts"][name]["Token"]
        launcherVersion = config[0]["Launcher"]["Version"]

        options = {'username': user,
                   'uuid': uuid,
                   'token': token,
                   'jvArguments': f"[{str(ram)}, {str(ram)}]",
                   'launcherVersion': launcherVersion}

        print("Running:", version, mllb.utils.get_installed_versions(f"{minecraft_directory}/{version}")[0]["id"])

        file = open(str(f"{minecraft_directory}/{version}/version.txt"), "r")
        file_ver = file.read()
        file.close()

        minecraft_command = mllb.command.get_minecraft_command(file_ver, str(f"{minecraft_directory}/{version}"), options)
        subprocess.run(minecraft_command)

        print("Restarting...")
        main()
    else:
        text_message("Without Accounts To Play", langData[0]["Without_Accounts_To_Play"])


def check_accounts():
    accounts = ctk.StringVar()
    list_added_accounts = []

    for account_added in config[0]["Accounts"]:
        list_added_accounts.append(account_added)

    if len(list_added_accounts) != 0:
        if config[0]["Launcher"]["DefaultAccount"] == "" or config[0]["Launcher"]["DefaultAccount"] == langData[0]["Without_Accounts"]:
            config[0]["Launcher"]["DefaultAccount"] = list_added_accounts[0]
        is_added = False

        for account_added in list_added_accounts:
            if config[0]["Launcher"]["DefaultAccount"] == account_added:
                is_added = True

        if not is_added:
            config[0]["Launcher"]["DefaultAccount"] = list_added_accounts[0]
        accounts.set(config[0]["Launcher"]["DefaultAccount"])

    elif len(list_added_accounts) == 0:
        accounts.set(langData[0]["Without_Accounts"])
        list_added_accounts.append(langData[0]["Without_Accounts"])

    account_display.configure(variable=accounts, values=list_added_accounts)
    selectedAccount.configure(variable=accounts, values=list_added_accounts)


def check_vers():
    versions = ctk.StringVar()
    installed_version_list = []

    for installed_version in os.scandir(minecraft_directory):
        if installed_version.name != "launcher_config.pkl" and installed_version.name != "minecraft_directory.txt":
            installed_version_list.append(installed_version.name)

    if len(installed_version_list) != 0:
        if config[0]["Launcher"]["DefaultVersion"] == "" or config[0]["Launcher"]["DefaultVersion"] == langData[0]["Without_Versions"]:
            config[0]["Launcher"]["DefaultVersion"] = installed_version_list[0]
        is_installed = False

        for installed_version in installed_version_list:
            if config[0]["Launcher"]["DefaultVersion"] == installed_version:
                is_installed = True

        if not is_installed:
            config[0]["Launcher"]["DefaultVersion"] = installed_version_list[0]
        versions.set(config[0]["Launcher"]["DefaultVersion"])

    elif len(installed_version_list) == 0:
        versions.set(langData[0]["Without_Versions"])
        installed_version_list.append(langData[0]["Without_Versions"])

    versions_display.configure(variable=versions, values=installed_version_list)
    unsVerDisplay.configure(variable=versions, values=installed_version_list)


def text_message(title=str, msg=str):
    winmsg = ctk.CTk()
    winmsg.geometry("300x275")
    winmsg.title(title)
    winmsg.resizable(width=False, height=False)

    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        winmsg.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    msgframe = ctk.CTkScrollableFrame(master=winmsg,
                                      width=260,
                                      height=120)
    msgframe.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    msgtxt = ctk.CTkLabel(master=msgframe,
                          text=msg,
                          font=("", 16),
                          wraplength=260)
    msgtxt.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    msgbtn = ctk.CTkButton(master=winmsg,
                           text="Ok",
                           font=("", 16),
                           width=280,
                           command=lambda: winmsg.destroy())
    msgbtn.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    winmsg.mainloop()


def update_config(lang=str, color=str, bgImg=bool, theme=str, ram=int, dir=str):
    window.destroy()

    print("Saving data...")

    if lang != langData[0]["Info_Configurate_Language_Default"]:
        if lang != "empty_example":
            config[0]["Launcher"]["Lang"] = lang

    if color != langData[0]["Info_Configuration_Color_Default"]:
        config[0]["Launcher"]["Color"] = color

    if theme != langData[0]["Info_Configuration_Theme_Default"]:
        config[0]["Launcher"]["Theme"] = theme

    config[0]["Launcher"]["EnabledBgImg"] = bgImg
    config[0]["Launcher"]["RamAmount"] = ram

    global minecraft_directory
    rPathDir = open(f"{get_launcher_path()}/minecraft_directory.txt", "r")

    if dir != rPathDir.read() and dir != "":
        if os.path.exists(os.path.normpath(dir)):
            wPathDir = open(f"{get_launcher_path()}/minecraft_directory.txt", "w")
            wPathDir.write(os.path.normpath(dir))
            wPathDir.close()

            for file in os.scandir(os.path.normpath(minecraft_directory)):
                if file.name != "minecraft_directory.txt" and file.name != "launcher_config.pkl":
                    shutil.move(os.path.normpath(minecraft_directory+"/"+file.name), os.path.normpath(dir))

            minecraft_directory = dir
        else:
            print("Unable to change dir (does not exist)")

    rPathDir.close()

    config[0]["Launcher"]["DefaultAccount"] = account_display.get()
    config[0]["Launcher"]["DefaultVersion"] = versions_display.get()

    save_config(config)

    print("Reloading...")
    main()


def set_progress_status(status=str):
    try:
        progressMessage.configure(text=status)
    except:
        pass


def set_current_proggres(progress=int):
    try:
        global current_max_progress
        progressLabel.configure(text=str(f"{progress}/{current_max_progress}"))
        progressPercentage.set(value=progress/current_max_progress)
    except:
        pass


def set_progress_max(new_max=int):
    try:
        global current_max_progress
        current_max_progress = new_max
    except:
        pass


def reset_progress():
    global current_max_progress
    progressMessage.configure(text="No tasks running")
    progressLabel.configure(text="0/0")
    progressPercentage.set(value=1)
    current_max_progress = 0


def infoEdit(win=ctk.CTkScrollableFrame):
    global last_option

    try:
        last_option.place_forget()
    except:
        pass
    
    win.place(x=5, y=50)

    last_option = win


def main():
    print("Loading Config...")
    load_config()
    if config[0]["Launcher"]["Version"] != version:
        config[0]["Launcher"]["Version"] = version
    for setting in launcherConfig:
        try:
            config[0]["Launcher"][setting]
        except:
            config[0]["Launcher"][setting] = launcherConfig[setting]

    print("Loading Launguaje...")
    set_languaje(config[0]["Launcher"]["Lang"])

    print("Loading GUI...")
    ctk.set_appearance_mode(config[0]["Launcher"]["Color"])

    themeDir = f"Main/assets/themes/{config[0]['Launcher']['Theme']}.json"
    if not os.path.exists(themeDir):
        themeDir = f"assets/themes/{config[0]['Launcher']['Theme']}.json"

    ctk.set_default_color_theme(themeDir)

    global window
    window = ctk.CTk()
    window.geometry("800x500")
    window.title("TeenyLauncher")
    window.resizable(False, False)

    try:
        iconImage = "Main/assets/images/Icon.ico"
        if not os.path.exists(iconImage):
            iconImage = "assets/images/Icon.ico"
        window.iconbitmap(iconImage)
    except:
        print("Unable to load logo...")

    if config[0]["Launcher"]["EnabledBgImg"] == True:
        backgroundImg = ctk.CTkLabel(master=window,
                                     text="",
                                     image=ctk.CTkImage(Image.open("assets/images/background-light.png"),
                                                        Image.open("assets/images/background-dark.png"),
                                                        (800, 500)))
        backgroundImg.place(x=0, y=0)

    top = ctk.CTkFrame(master=window, height=50)
    top.place(x=5, y=5)

    launcherInfoButton = ctk.CTkButton(master=top,
                                       text=f"{langData[0]['Top_Button_Info_Version']} V{config[0]['Launcher']['Version']}",
                                       font=("", 20),
                                       width=188,
                                       command=lambda: infoEdit(launcherInfo))
    launcherInfoButton.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    configInfoButton = ctk.CTkButton(master=top,
                                     text=langData[0]["Top_Button_Configuration"],
                                     font=("", 20),
                                     width=188,
                                     command=lambda: infoEdit(configInfo))
    configInfoButton.grid(row=0, column=1, pady=5, padx=5, sticky="nswe")

    versionInfoButton = ctk.CTkButton(master=top,
                                      text=langData[0]["Top_Button_Versions"],
                                      font=("", 20),
                                      width=188,
                                      command=lambda: infoEdit(versionInfo))
    versionInfoButton.grid(row=0, column=2, pady=5, padx=5, sticky="nswe")

    accountInfoButton = ctk.CTkButton(master=top,
                                      text=langData[0]["Top_Button_Accounts"],
                                      font=("", 20),
                                      width=188,
                                      command=lambda: infoEdit(accountInfo))
    accountInfoButton.grid(row=0, column=3, pady=5, padx=5, sticky="nswe")

    global launcherInfo
    launcherInfo = ctk.CTkScrollableFrame(master=window, width=485, height=390)

    global configInfo
    configInfo = ctk.CTkScrollableFrame(master=window, width=485, height=390)

    global versionInfo
    versionInfo = ctk.CTkScrollableFrame(master=window, width=485, height=390)

    global accountInfo
    accountInfo = ctk.CTkScrollableFrame(master=window, width=485, height=390)

    # ------------------------------------
    #        LauncherInfo objects
    # ------------------------------------

    infoTitle = ctk.CTkLabel(master=launcherInfo,
                             text=str(f"TeenyLauncher V{config[0]['Launcher']['Version']}"),
                             font=("", 36),
                             wraplength=475)
    infoTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

    count = 0
    for line in version_info.split("\n"):
        infoVersionInfo = ctk.CTkLabel(master=launcherInfo,
                                       text=line,
                                       font=("", 16),
                                       wraplength=475)
        infoVersionInfo.grid(row=1+count, column=0, pady=0, padx=5, sticky="w")
        count += 1

    # ------------------------------------
    #         ConfigInfo objects
    # ------------------------------------

    configurationTitle = ctk.CTkLabel(master=configInfo,
                                      text=langData[0]["Info_Configuration_Title"],
                                      font=("", 36),
                                      wraplength=475)
    configurationTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

    languajeTitle = ctk.CTkLabel(master=configInfo,
                                 text=langData[0]["Info_Configurate_Language_Title"],
                                 font=("", 16),
                                 wraplength=475)
    languajeTitle.grid(row=1, column=0, pady=5, padx=5, sticky="w")

    langDir = "Main/assets/lang"
    if not os.path.exists(langDir):
        langDir = "assets/lang"

    configurationLanguaje = ctk.CTkOptionMenu(master=configInfo,
                                              values=[file.name.replace(".json", "")
                                                      for file in os.scandir(langDir)
                                                      if file.is_file() if file.name != "example_file.json"],
                                              variable=ctk.StringVar(value=langData[0]["Info_Configurate_Language_Default"]),
                                              font=("", 16),
                                              width=475)
    configurationLanguaje.grid(row=2, column=0, pady=5, padx=5, sticky="w")

    themeTitle = ctk.CTkLabel(master=configInfo,
                              text=langData[0]["Info_Configuration_Theme_Title"],
                              font=("", 16),
                              wraplength=475)
    themeTitle.grid(row=3, column=0, pady=5, padx=5, sticky="w")

    configurationColor = ctk.CTkOptionMenu(master=configInfo,
                                           values=["Light", "Dark"],
                                           variable=ctk.StringVar(
                                           value=langData[0]["Info_Configuration_Color_Default"]),
                                           font=("", 16),
                                           width=475)
    configurationColor.grid(row=4, column=0, pady=5, padx=5, sticky="w")

    themeDir = "Main/assets/themes"
    if not os.path.exists(themeDir):
        themeDir = "assets/themes"

    configurationTheme = ctk.CTkOptionMenu(master=configInfo,
                                           values=[file.name.replace(".json", "")
                                                   for file in os.scandir(themeDir)
                                                   if file.is_file()], variable=ctk.StringVar(
                                           value=langData[0]["Info_Configuration_Theme_Default"]),
                                           font=("", 16),
                                           width=475)
    configurationTheme.grid(row=5, column=0, pady=5, padx=5, sticky="w")

    configurationBackgroundImg = ctk.CTkCheckBox(master=configInfo,
                                                 width=475,
                                                 text=langData[0]["Info_Configuration_Img"],
                                                 variable=ctk.Variable(value=config[0]["Launcher"]["EnabledBgImg"]),
                                                 font=("", 16))
    configurationBackgroundImg.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    advancedTitle = ctk.CTkLabel(master=configInfo,
                                 text=langData[0]["Info_Configuration_Advanced_Title"],
                                 font=("", 36),
                                 wraplength=475)
    advancedTitle.grid(row=7, column=0, pady=5, padx=5, sticky="w")

    configurationRamTitle = ctk.CTkLabel(master=configInfo,
                                         text=langData[0]["Info_Configuration_Advanced_Ram_Title"],
                                         font=("", 16),
                                         wraplength=475)
    configurationRamTitle.grid(row=8, column=0, pady=5, padx=5, sticky="w")

    pc_ram = int(psutil.virtual_memory().total / (1024.0 ** 2))
    uncompatibleRam = True
    while uncompatibleRam:
        if pc_ram % 32 != 0:
            pc_ram -= 1
        else:
            uncompatibleRam = False

    configurationRam = ctk.CTkSlider(master=configInfo,
                                     height=10,
                                     from_=0,
                                     to=pc_ram,
                                     number_of_steps=int(pc_ram/32),
                                     command=lambda value: configurationRamText.configure(text=f"{int(value)}MB"),
                                     width=475)
    configurationRam.grid(row=9, column=0, pady=5, padx=5, sticky="w")
    configurationRam.set(config[0]["Launcher"]["RamAmount"])

    configurationRamText = ctk.CTkLabel(master=configInfo,
                                        font=("", 12),
                                        text=str(f"{config[0]['Launcher']['RamAmount']}MB"),
                                        wraplength=475)
    configurationRamText.grid(row=10, column=0, pady=5, padx=5, sticky="w")

    configurationDirectoryTitle = ctk.CTkLabel(master=configInfo,
                                               font=("", 16),
                                               text=langData[0]["Info_Config_Folder_Title"],
                                               wraplength=475)
    configurationDirectoryTitle.grid(row=11, column=0, pady=5, padx=5, sticky="w")

    configurationDirectory = ctk.CTkEntry(master=configInfo,
                                          font=("", 16),
                                          placeholder_text=minecraft_directory,
                                          width=475)
    configurationDirectory.grid(row=12, column=0, pady=5, padx=5, sticky="w")

    configurationOpenDir = ctk.CTkButton(master=configInfo,
                                         text=langData[0]["Info_Config_Open_Versions_Folder"],
                                         font=("", 16),
                                         width=475,
                                         command=open_versions_folder)
    configurationOpenDir.grid(row=13, column=0, pady=5, padx=5, sticky="we")

    configurationSave = ctk.CTkButton(master=configInfo,
                                      text=langData[0]["Info_Configuration_Save"],
                                      font=("", 20),
                                      width=475,
                                      command=lambda: update_config(lang=configurationLanguaje.get(),
                                                                    color=configurationColor.get(),
                                                                    bgImg=configurationBackgroundImg.get(),
                                                                    theme=configurationTheme.get(),
                                                                    ram=int(configurationRam.get()),
                                                                    dir=configurationDirectory.get()))
    configurationSave.grid(row=14, column=0, pady=5, padx=5, sticky="w")

    # ------------------------------------
    #        VersionInfo objects
    # ------------------------------------

    def check_versions(type):
        versions = {}
        first_ver = ""
        first = True

        if type == "Vanilla" or type == "Forge":
            for version in mllb.utils.get_version_list():
                if version["type"] == "release":
                    versions[version["id"]] = version["id"]
                    if first:
                        first_ver = version["id"]
                        first = False

        elif type == "Snapshot":
            for version in mllb.utils.get_version_list():
                if version["type"] == "snapshot":
                    versions[version["id"]] = version["id"]
                    if first:
                        first_ver = version["id"]
                        first = False

        elif type == "Fabric":
            for version in mllb.utils.get_version_list():
                if mllb.fabric.is_minecraft_version_supported(version["id"]) and version["type"] == "release":
                    versions[version["id"]] = version["id"]
                    if first:
                        first_ver = version["id"]
                        first = False

        elif type == "Fabric Snapshot":
            for version in mllb.utils.get_version_list():
                if mllb.fabric.is_minecraft_version_supported(version["id"]) and version["type"] == "snapshot":
                    versions[version["id"]] = version["id"]
                    if first:
                        first_ver = version["id"]
                        first = False

        elif type == "Quilt":
            for version in mllb.utils.get_version_list():
                if mllb.quilt.is_minecraft_version_supported(version["id"]) and version["type"] == "release":
                    versions[version["id"]] = version["id"]
                    if first:
                        first_ver = version["id"]
                        first = False

        elif type == "Quilt Snapshot":
            for version in mllb.utils.get_version_list():
                if mllb.quilt.is_minecraft_version_supported(version["id"]) and version["type"] == "snapshot":
                    versions[version["id"]] = version["id"]
                    if first:
                        first_ver = version["id"]
                        first = False

        ver_select.configure(values=versions, variable=ctk.StringVar(value=first_ver))
        check_engine_ver(first_ver)

    def check_engine_ver(ver):
        engine_type = ver_type_display.get()
        engines = {}
        first_engine = ""
        first = True
        if engine_type == "Forge":
            for version in mllb.forge.list_forge_versions():
                if version.startswith(ver):
                    engines[version] = version
                    if first:
                        first_engine = version
                        first = False

        elif engine_type == "Fabric" or engine_type == "Fabric Snapshot":
            for version in mllb.fabric.get_all_loader_versions():
                engines[version["version"]] = version["version"]
                if first:
                    first_engine = version["version"]
                    first = False

        elif engine_type == "Quilt" or engine_type == "Quilt Snapshot":
            for version in mllb.quilt.get_all_loader_versions():
                engines[version["version"]] = version["version"]
                if first:
                    first_engine = version["version"]
                    first = False

        mod_ver.configure(values=engines, variable=ctk.StringVar(value=first_engine))

    versionsTitle = ctk.CTkLabel(master=versionInfo,
                                 text=langData[0]["Versions_Title"],
                                 font=("", 36),
                                 wraplength=475)
    versionsTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

    insTitle = ctk.CTkLabel(master=versionInfo,
                            text=langData[0]["Install_Versions_Title"],
                            font=("", 24),
                            wraplength=475)
    insTitle.grid(row=1, column=0, pady=5, padx=5, sticky="w")

    profile_name = ctk.CTkEntry(master=versionInfo,
                                placeholder_text=langData[0]["Install_Versions_Name_Entry"],
                                font=("", 16),
                                width=475)
    profile_name.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    type_title = ctk.CTkLabel(master=versionInfo,
                              text=langData[0]["Install_Versions_Type_Title"],
                              font=("", 16),
                              wraplength=475)
    type_title.grid(row=3, column=0, pady=5, padx=5, sticky="w")

    ver_type_display = ctk.CTkOptionMenu(master=versionInfo,
                                     values=["Vanilla", "Snapshot", "Forge", "Fabric", "Fabric Snapshot", "Quilt", "Quilt Snapshot"],
                                     variable=ctk.StringVar(value=langData[0]["Install_Version_Type_Default"]),
                                     font=("", 16),
                                     width=475,
                                     command=check_versions)
    ver_type_display.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    ver_title = ctk.CTkLabel(master=versionInfo,
                             text=langData[0]["Install_Versions_Version_Title"],
                             font=("", 16),
                             wraplength=475)
    ver_title.grid(row=5, column=0, pady=5, padx=5, sticky="w")

    ver_select = ctk.CTkOptionMenu(master=versionInfo,
                                   values=[""],
                                   variable=ctk.StringVar(value=""),
                                   font=("", 16),
                                   width=475,
                                   command=check_engine_ver)
    ver_select.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    mod_ver_title = ctk.CTkLabel(master=versionInfo,
                                 text=langData[0]["Install_Versions_Mod_Version_Title"],
                                 font=("", 16),
                                 wraplength=475)
    mod_ver_title.grid(row=7, column=0, pady=5, padx=5, sticky="w")

    mod_ver = ctk.CTkOptionMenu(master=versionInfo,
                                values=[""],
                                variable=ctk.StringVar(value=""),
                                font=("", 16),
                                width=475)
    mod_ver.grid(row=8, column=0, pady=5, padx=5, sticky="we")

    install_button = ctk.CTkButton(master=versionInfo,
                                   text=langData[0]["Install_Versions_Install_Button"],
                                   font=("", 16),
                                   width=475,
                                   command=lambda: threads.submit(install_minecraft_verison,
                                                                  name=profile_name.get(),
                                                                  ver=ver_select.get(),
                                                                  type=ver_type_display.get(),
                                                                  mod=mod_ver.get()))
    install_button.grid(row=9, column=0, pady=5, padx=5, sticky="we")

    unsTitle = ctk.CTkLabel(master=versionInfo,
                         text=langData[0]["Uninstall_Version_Title"],
                         font=("", 24),
                         wraplength=475)
    unsTitle.grid(row=10, column=0, pady=10, padx=10, sticky="w")

    global unsVerDisplay
    unsVerDisplay = ctk.CTkOptionMenu(master=versionInfo,
                                font=("", 16),
                                width=475)
    unsVerDisplay.grid(row=11, column=0, pady=5, padx=5, sticky="we")

    button = ctk.CTkButton(master=versionInfo,
                           text=langData[0]["Uninstall_Version_Button"],
                           font=("", 20),
                           width=475,
                           command=lambda: threads.submit(uninstall_minecraft_version,
                                                          version=unsVerDisplay.get()))
    button.grid(row=12, column=0, pady=5, padx=5, sticky="we")

    # ------------------------------------
    #         AccountInfo objects
    # ------------------------------------

    accountsTitle = ctk.CTkLabel(master=accountInfo,
                                 text=langData[0]["Account_Title"],
                                 font=("", 36),
                                 wraplength=475)
    accountsTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

    addAcTitle = ctk.CTkLabel(master=accountInfo,
                              wraplength=475,
                              text=langData[0]["Add_Account_Title"],
                              font=("", 24))
    addAcTitle.grid(row=1, column=0, pady=5, padx=5, sticky="w")

    type_display = ctk.CTkOptionMenu(master=accountInfo,
                                     values=["Premiun", "No Premiun"],
                                     variable=ctk.StringVar(value=langData[0]["Add_Account_Type_Default"]),
                                     font=("", 16),
                                     width=475)
    type_display.grid_propagate(False)
    type_display.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    name_title = ctk.CTkLabel(master=accountInfo,
                              wraplength=475,
                              text=langData[0]["Add_Account_Name"],
                              font=("", 16))
    name_title.grid(row=3, column=0, pady=5, padx=5, sticky="w")

    name_entry = ctk.CTkEntry(master=accountInfo,
                              placeholder_text=langData[0]["Add_Account_Name_Input"],
                              font=("", 16),
                              width=475)
    name_entry.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    pasword_title = ctk.CTkLabel(master=accountInfo,
                                 wraplength=475,
                                 text=langData[0]["Add_Account_Password"],
                                 font=("", 16))
    pasword_title.grid(row=5, column=0, pady=5, padx=5, sticky="w")

    pasword_entry = ctk.CTkEntry(master=accountInfo,
                                 placeholder_text=langData[0]["Add_Account_Password_Input"],
                                 font=("", 16),
                                 width=475,
                                 show="*")
    pasword_entry.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    add_button = ctk.CTkButton(master=accountInfo,
                               text=langData[0]["Add_Account_Create_Button"],
                               font=("", 16),
                               width=475,
                               command=lambda: threads.submit(add_acount_data,
                                                              type_display.get(),
                                                              name_entry.get(),
                                                              pasword_entry.get()))
    add_button.grid(row=7, column=0, pady=5, padx=5, sticky="we")

    delActitle = ctk.CTkLabel(master=accountInfo,
                              wraplength=475,
                              text=langData[0]["Delete_Account_Title"],
                              font=("", 24))
    delActitle.grid(row=8, column=0, pady=5, padx=5, sticky="w")

    global selectedAccount
    selectedAccount = ctk.CTkOptionMenu(master=accountInfo,
                                        variable=ctk.StringVar(value=langData[0]["Delete_Account_Select_Default"]),
                                        values=[account for account in config[0]["Accounts"]],
                                        font=("", 16),
                                        width=220)
    selectedAccount.grid(row=9, column=0, pady=5, padx=5, sticky="we")

    deleteButton = ctk.CTkButton(master=accountInfo,
                                 text=langData[0]["Delete_Account_Button"],
                                 font=("", 16),
                                 command=lambda: threads.submit(del_acount_data,
                                                                selectedAccount.get()))
    deleteButton.grid(row=10, column=0, pady=5, padx=5, sticky="we")

    progressFrame = ctk.CTkFrame(master=window, height=40, width=790)
    progressFrame.grid_propagate(False)
    progressFrame.place(x=5, y=460)

    global current_max_progress
    current_max_progress = 1

    global progressMessage
    progressMessage = ctk.CTkLabel(master=progressFrame,
                                   font=("", 14),
                                   text="No tasks running",
                                   wraplength=200,
                                   width=200)
    progressMessage.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    global progressPercentage
    progressPercentage = ctk.CTkProgressBar(master=progressFrame,
                                            width=460,
                                            height=10,
                                            variable=ctk.Variable(value=1))
    progressPercentage.grid(row=0, column=1, pady=15, padx=5, sticky="nwe")

    global progressLabel
    progressLabel = ctk.CTkLabel(master=progressFrame,
                                 wraplength=100,
                                 width=100,
                                 text="0/0",
                                 font=("", 14))
    progressLabel.grid(row=0, column=2, pady=5, padx=5, sticky="nwe")

    mineconfig = ctk.CTkScrollableFrame(master=window, width=250, height=390)
    mineconfig.place(x=520, y=50)

    accTitle = ctk.CTkLabel(master=mineconfig,
                            wraplength=240,
                            text=langData[0]["Menu_Minecraft_Config_Account"],
                            font=("", 24))
    accTitle.grid(row=0, column=0, pady=5, padx=5, sticky="w")

    global account_display
    account_display = ctk.CTkOptionMenu(master=mineconfig, font=("", 16), width=240)
    account_display.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    startGameTitle = ctk.CTkLabel(master=mineconfig,
                                  text=langData[0]["Menu_Minecraft_Start_Game_Title"],
                                  font=("", 24),
                                  wraplength=240)
    startGameTitle.grid(row=2, column=0, pady=5, padx=5, sticky="w")

    global versions_display
    versions_display = ctk.CTkOptionMenu(master=mineconfig,
                                         font=("", 16),
                                         width=240)
    versions_display.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    startMinecraft = ctk.CTkButton(master=mineconfig,
                                   text=langData[0]["Menu_Minecraft_Start_Game"],
                                   font=("", 20),
                                   width=240,
                                   command=lambda: run_minecraft(versions_display.get()))
    startMinecraft.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    print("Loading Accounts...")
    check_accounts()

    print("Loading Versions...")
    check_vers()

    print("Done!")

    infoEdit(launcherInfo)
    window.mainloop()


if __name__ == "__main__":
    threads = ThreadPoolExecutor(max_workers=1)

    if not os.path.exists(get_launcher_path()):
        os.mkdir(get_launcher_path())

    if not os.path.exists(f"{get_launcher_path()}/minecraft_directory.txt"):
        with open(f"{get_launcher_path()}/minecraft_directory.txt", "w") as file:
            file.write(get_launcher_path())
            file.close()

    with open(f"{get_launcher_path()}/minecraft_directory.txt", "r") as dirPath:
        minecraft_directory = dirPath.read()
        dirPath.close()

    if not os.path.exists(f"{get_launcher_path()}/launcher_config.pkl"):
        save_config([{"Launcher": launcherConfig, "Accounts": {}}])

    print("Starting...")
    main()

    print("Saving data...")
    config[0]["Launcher"]["DefaultAccount"] = account_display.get()
    config[0]["Launcher"]["DefaultVersion"] = versions_display.get()
    save_config(config)

    print("Program finished!")