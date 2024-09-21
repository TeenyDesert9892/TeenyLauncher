import json
import os
import pathlib
import pickle
import platform
import shutil
import psutil

version = "0.7.0"

version_info = "V0.7.0 update:\n" \
               "\n" \
               "In this version I have compleately remade the launcher so its looks better using the flet framework and also I improved " \
               "and remaded a big part of the code what it wasn't something easy at all\n" \
               "\n" \
               "I hope you like how it is going" \
               "\n" \
               "By: TeenyDesert9892"

lang = []

def get_assets_path(path=os.getcwd()):
    return path

def get_launcher_path():
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".TeenyLauncher")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "TeenyLauncher")
    else:
        return os.path.join(str(pathlib.Path.home()), ".TeenyLauncher")

class Config:
    def __init__(self):
        self.Theme = "Dark"
        self.Lang = "English"
        self.DefaultAccount = ""
        self.DefaultInstance = ""
        self.CloseOnPlay = True
        self.Version = version
        self.EnabledBgImg = False
        self.RamAmount = 2048
        self.Accounts = {}

        if not os.path.exists(f"{get_launcher_path()}/launcher_config.pkl"):
            self.save_config()
        self.load_config()

    def save_config(self):
        with open(f"{get_launcher_path()}/launcher_config.pkl", "wb") as pickleFile:
            pickle.dump({"Launcher": {"Theme": self.Theme,
                                      "Lang": self.Lang,
                                      "DefaultAccount": self.DefaultAccount,
                                      "DefaultInstance": self.DefaultInstance,
                                      "CloseOnPlay": self.CloseOnPlay,
                                      "Version": self.Version,
                                      "EnabledBgImg": self.EnabledBgImg,
                                      "RamAmount": int(self.RamAmount)},
                         "Accounts": self.Accounts}, pickleFile)

    def load_config(self):
        with open(f"{get_launcher_path()}/launcher_config.pkl", "rb") as pickleFile:
            configFile = pickle.load(pickleFile)

            self.Theme = configFile["Launcher"]["Theme"]
            self.Lang = configFile["Launcher"]["Lang"]
            self.DefaultAccount = configFile["Launcher"]["DefaultAccount"]
            self.DefaultInstance = configFile["Launcher"]["DefaultInstance"]
            self.CloseOnPlay = configFile["Launcher"]["CloseOnPlay"]
            self.Version = configFile["Launcher"]["Version"]
            self.EnabledBgImg = configFile["Launcher"]["EnabledBgImg"]
            self.RamAmount = configFile["Launcher"]["RamAmount"]
            self.Accounts = configFile["Accounts"]

config = Config()

class Lang:
    def __init__(self):
        self.Accounts_Title = ""
        self.Add_Accounts_Title = ""
        self.Add_Account_Name = ""
        self.Add_Account_Password = ""
        self.Add_Account_Button = ""
        
        self.Add_Account_Premium_Success = ""
        self.Add_Account_No_Premium_Success = ""
        self.Add_Account_Premium_Failure = ""
        self.Add_Account_No_Premium_Failure = ""
        self.Add_Account_Name_Already_Exsists = ""
        self.Add_Account_Name_Remaining = ""
        self.Add_Account_Password_Remaining = ""
        self.Add_Account_No_Type_Selected = ""

        self.Delete_Accounts_Title = ""
        self.Delete_Account_Button = ""
        self.Delete_Account_Success = ""
        self.Delete_Account_Failure = ""

        self.Without_Accounts = ""
        self.Without_Accounts_To_Play = ""

        self.Instances_Title = ""
        self.Create_Instances_Title = ""
        self.Create_Instance_Name_Title = ""
        self.Create_Instance_Type_Title = ""
        self.Create_Instance_Version_Title = ""
        self.Create_Instance_Engin_Version_Title = ""
        self.Create_Instance_Install_Button = ""

        self.Install_Vanilla_Version_Success = ""
        self.Install_Vanilla_Version_Failure = ""
        self.Install_Forge_Version_Success = ""
        self.Install_Forge_Version_Failure = ""
        self.Install_Fabric_Version_Success = ""
        self.Install_Fabric_Version_Failure = ""
        self.Install_Quilt_Version_Success = ""
        self.Install_Quilt_Version_Failure = ""

        self.Install_Version_Already_Exsists = ""
        self.Install_Version_Without_Name = ""
        self.Install_Version_Not_Selected = ""
        self.Install_Version_Type_Not_Selected = ""

        self.Delete_Instances_Title = ""
        self.Delete_Instances_Button = ""

        self.Delete_Instance_Success = ""
        self.Delete_Instance_Failure = ""

        self.Without_Versions = ""
        self.Without_Versions_To_Play = ""

        self.Config_Title = ""
        self.Launcher_Config_Title = ""
        self.Launcher_Config_Lang_Title = ""
        self.Launcher_Config_Theme_Title = ""
        self.Launcher_Config_Img = ""
        Launcher_Config_On_Close = ""

        self.Advanced_Config_Title = ""
        self.Advanced_Config_Ram_Title = ""
        self.Advanced_Config_Folder_Title = ""
        self.Advanced_Config_Open_Versions_Folder = ""

        self.Play_Menu_Config_Account_Title = ""
        self.Play_Menu_Select_Instance_Title = ""
        self.Play_Menu_Start_Game = ""

        self.Incompatible_JDK = ""
        self.Default_Option = "Default"
        self.Nothing = ""

        self.set_lang()
    def set_lang(self):
        with open(f"{get_assets_path()}/assets/lang/{config.Lang}.json", "r") as langFile:
            lang = json.load(langFile)
            self.Accounts_Title = lang["Accounts_Title"]
            self.Add_Accounts_Title = lang["Add_Accounts_Title"]
            self.Add_Account_Name = lang["Add_Account_Name"]
            self.Add_Account_Password = lang["Add_Account_Password"]
            self.Add_Account_Button = lang["Add_Account_Button"]

            self.Add_Account_Premium_Success = lang["Add_Account_Premium_Success"]
            self.Add_Account_No_Premium_Success = lang["Add_Account_No_Premium_Success"]
            self.Add_Account_Premium_Failure = lang["Add_Account_Premium_Failure"]
            self.Add_Account_No_Premium_Failure = lang["Add_Account_No_Premium_Failure"]
            self.Add_Account_Name_Already_Exsists = lang["Add_Account_Name_Already_Exsists"]
            self.Add_Account_Name_Remaining = lang["Add_Account_Name_Remaining"]
            self.Add_Account_Password_Remaining = lang["Add_Account_Password_Remaining"]
            self.Add_Account_No_Type_Selected = lang["Add_Account_No_Type_Selected"]

            self.Delete_Accounts_Title = lang["Delete_Accounts_Title"]
            self.Delete_Account_Button = lang["Delete_Account_Button"]
            self.Delete_Account_Success = lang["Delete_Account_Success"]
            self.Delete_Account_Failure = lang["Delete_Account_Failure"]

            self.Without_Accounts = lang["Without_Accounts"]
            self.Without_Accounts_To_Play = lang["Without_Accounts_To_Play"]

            self.Instances_Title = lang["Instances_Title"]
            self.Create_Instances_Title = lang["Create_Instances_Title"]
            self.Create_Instance_Name_Title = lang["Create_Instance_Name_Title"]
            self.Create_Instance_Type_Title = lang["Create_Instance_Type_Title"]
            self.Create_Instance_Version_Title = lang["Create_Instance_Version_Title"]
            self.Create_Instance_Engin_Version_Title = lang["Create_Instance_Engin_Version_Title"]
            self.Create_Instance_Install_Button = lang["Create_Instance_Install_Button"]

            self.Install_Vanilla_Version_Success = lang["Install_Vanilla_Version_Success"]
            self.Install_Vanilla_Version_Failure = lang["Install_Vanilla_Version_Failure"]
            self.Install_Forge_Version_Success = lang["Install_Forge_Version_Success"]
            self.Install_Forge_Version_Failure = lang["Install_Forge_Version_Failure"]
            self.Install_Fabric_Version_Success = lang["Install_Fabric_Version_Success"]
            self.Install_Fabric_Version_Failure = lang["Install_Fabric_Version_Failure"]
            self.Install_Quilt_Version_Success = lang["Install_Quilt_Version_Success"]
            self.Install_Quilt_Version_Failure = lang["Install_Quilt_Version_Failure"]

            self.Install_Version_Already_Exsists = lang["Install_Version_Already_Exsists"]
            self.Install_Version_Without_Name = lang["Install_Version_Without_Name"]
            self.Install_Version_Not_Selected = lang["Install_Version_Not_Selected"]
            self.Install_Version_Type_Not_Selected = lang["Install_Version_Type_Not_Selected"]

            self.Delete_Instances_Title = lang["Delete_Instances_Title"]
            self.Delete_Instances_Button = lang["Delete_Instances_Button"]

            self.Delete_Instance_Success = lang["Delete_Instance_Success"]
            self.Delete_Instance_Failure = lang["Delete_Instance_Failure"]

            self.Without_Versions = lang["Without_Versions"]
            self.Without_Versions_To_Play = lang["Without_Versions_To_Play"]

            self.Config_Title = lang["Config_Title"]
            self.Launcher_Config_Title = lang["Launcher_Config_Title"]
            self.Launcher_Config_Lang_Title = lang["Launcher_Config_Lang_Title"]
            self.Launcher_Config_Theme_Title = lang["Launcher_Config_Theme_Title"]
            self.Launcher_Config_Img = lang["Launcher_Config_Img"]
            self.Launcher_Config_On_Close = lang["Launcher_Config_On_Close"]

            self.Advanced_Config_Title = lang["Advanced_Config_Title"]
            self.Advanced_Config_Ram_Title = lang["Advanced_Config_Ram_Title"]
            self.Advanced_Config_Folder_Title = lang["Advanced_Config_Folder_Title"]
            self.Advanced_Config_Open_Versions_Folder = lang["Advanced_Config_Open_Versions_Folder"]

            self.Play_Menu_Config_Account_Title = lang["Play_Menu_Config_Account_Title"]
            self.Play_Menu_Select_Instance_Title = lang["Play_Menu_Select_Instance_Title"]
            self.Play_Menu_Start_Game = lang["Play_Menu_Start_Game"]

            self.Incompatible_JDK = lang["Incompatible_JDK"]

lang = Lang()

def get_ram():
    ram = int(psutil.virtual_memory().total / (1024 ** 2))
    uncompatibleRam = True
    while uncompatibleRam:
        if ram % 32 != 0:
            ram -= 1
        else:
            uncompatibleRam = False
    return ram

def update_config_lang(lang):
    config.Lang = lang

def update_config_theme(theme):
    config.Theme = theme

def update_config_bg(bgImg):
    config.EnabledBgImg = bgImg

def update_config_ram(ram):
    config.RamAmount = ram

def update_config_default_account(defaultAccount):
    config.DefaultAccount = defaultAccount.data

def update_config_default_version(defaultInstance):
    config.DefaultInstance = defaultInstance.data

def update_config_dir(dir):
    global minecraft_directory
    readPathDir = open(f"{get_launcher_path()}/minecraft_directory.txt", "r")

    if dir != readPathDir.read() and dir != "":
        if os.path.exists(os.path.normpath(dir)):
            writePathDir = open(f"{get_launcher_path()}/minecraft_directory.txt", "w")
            writePathDir.write(os.path.normpath(dir))
            writePathDir.close()

            for file in os.scandir(os.path.normpath(minecraft_directory)):
                if file.name != "minecraft_directory.txt" and file.name != "launcher_config.pkl":
                    shutil.move(os.path.normpath(minecraft_directory+"/"+file.name), os.path.normpath(dir))

            minecraft_directory = dir
        else:
            print("Unable to change dir (does not exist)")
    readPathDir.close()


if not os.path.exists(get_launcher_path()):
    os.mkdir(get_launcher_path())

if not os.path.exists(f"{get_launcher_path()}/minecraft_directory.txt"):
    with open(f"{get_launcher_path()}/minecraft_directory.txt", "w") as file:
        file.write(get_launcher_path())
        file.close()

with open(f"{get_launcher_path()}/minecraft_directory.txt", "r") as dirPath:
    minecraft_directory = dirPath.read()
    dirPath.close()