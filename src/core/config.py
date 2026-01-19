import os
import pickle
import shutil
import psutil

from utils import utils


Version = "0.9.0"

if not os.path.exists(utils.get_launcher_path()):
    os.mkdir(utils.get_launcher_path())

if not os.path.exists(f"{utils.get_launcher_path()}/config.pkl"):
    Theme = "Dark"
    Lang = "English"
    DefaultAccount = ""
    DefaultInstance = ""
    CloseOnPlay = True
    EnabledBgImg = False
    RamAmount = 2048
    Minecraft_Dir = os.path.normpath(utils.get_launcher_path())
    Accounts = {}


pickleFile = open(utils.get_launcher_path()+'/config.pkl', 'rb')
configFile = pickle.load(pickleFile)

Theme = configFile["Launcher"]["Theme"]
Lang = configFile["Launcher"]["Lang"]
DefaultAccount = configFile["Launcher"]["DefaultAccount"]
DefaultInstance = configFile["Launcher"]["DefaultInstance"]
CloseOnPlay = configFile["Launcher"]["CloseOnPlay"]
EnabledBgImg = configFile["Launcher"]["EnabledBgImg"]
RamAmount = configFile["Launcher"]["RamAmount"]
Minecraft_Dir = configFile["Launcher"]["Minecraft_Dir"]
Accounts = configFile["Accounts"]


def save_config():
    pickleFile = open(utils.get_launcher_path()+'/config.pkl', 'wb')
    pickle.dump({"Launcher": {"Theme": Theme,
                                "Lang": Lang,
                                "DefaultAccount": DefaultAccount,
                                "DefaultInstance": DefaultInstance,
                                "CloseOnPlay": CloseOnPlay,
                                "Version": Version,
                                "EnabledBgImg": EnabledBgImg,
                                "RamAmount": int(RamAmount),
                                "Minecraft_Dir": Minecraft_Dir},
                    "Accounts": Accounts}, pickleFile)


def get_assets_path():
    return os.path.normpath(os.getcwd()+"/src/assets")


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
    Lang = lang


def update_config_theme(theme):
    Theme = theme


def update_config_bg(bgImg):
    EnabledBgImg = bgImg


def update_config_ram(ram):
    RamAmount = ram


def update_config_default_account(defaultAccount):
    DefaultAccount = defaultAccount.data


def update_config_default_version(defaultInstance):
    DefaultInstance = defaultInstance.data


def update_config_dir(dir):
    if dir != Minecraft_Dir and dir != "":
        if os.path.exists(os.path.normpath(dir)):
            for file in os.scandir(os.path.normpath(Minecraft_Dir)):
                shutil.move(os.path.normpath(Minecraft_Dir+"/"+file.name), os.path.normpath(dir))

            Minecraft_Dir = os.path.normpath(dir)
        else:
            pass