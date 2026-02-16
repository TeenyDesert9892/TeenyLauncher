import json
import os
import json
import shutil

from utils import utils


Version = "0.9.0"

if not os.path.exists(utils.get_launcher_path()):
    os.mkdir(utils.get_launcher_path())

class Settings:
    def __init__(self):
        self.configFile = os.path.normpath(utils.get_launcher_path()+'/config.json')

        if not os.path.exists(self.configFile):
            self.Theme = "Dark"
            self.Lang = "en"
            self.DefaultAccount = ""
            self.DefaultInstance = ""
            self.CloseOnPlay = True
            self.EnabledBgImg = False
            self.RamAmount = 2048
            self.Minecraft_Dir = os.path.normpath(utils.get_launcher_path())
            self.Accounts = {}
            
            self.save_config()
        else:
            self.load_config()
        

    def save_config(self):
        jsonFile = open(self.configFile, 'w')
        json.dump({"Launcher": {"Theme": self.Theme,
                                    "Lang": self.Lang,
                                    "DefaultAccount": self.DefaultAccount,
                                    "DefaultInstance": self.DefaultInstance,
                                    "CloseOnPlay": self.CloseOnPlay,
                                    "Version": Version,
                                    "EnabledBgImg": self.EnabledBgImg,
                                    "RamAmount": int(self.RamAmount),
                                    "Minecraft_Dir": self.Minecraft_Dir},
                        "Accounts": self.Accounts},
                jsonFile,
                indent=4)

    def load_config(self):
        jsonFile = open(self.configFile, 'r')
        configFile = json.load(jsonFile)

        self.Theme = configFile["Launcher"]["Theme"]
        self.Lang = configFile["Launcher"]["Lang"]
        self.DefaultAccount = configFile["Launcher"]["DefaultAccount"]
        self.DefaultInstance = configFile["Launcher"]["DefaultInstance"]
        self.CloseOnPlay = configFile["Launcher"]["CloseOnPlay"]
        self.EnabledBgImg = configFile["Launcher"]["EnabledBgImg"]
        self.RamAmount = configFile["Launcher"]["RamAmount"]
        self.Minecraft_Dir = configFile["Launcher"]["Minecraft_Dir"]
        self.Accounts = configFile["Accounts"]

settings = Settings()

def update_config_lang(lang):
    settings.Lang = lang

def update_config_theme(theme):
    settings.Theme = theme


def update_config_bg(bgImg):
    settings.EnabledBgImg = bgImg

def update_config_ram(ram):
    settings.RamAmount = ram


def update_config_default_account(defaultAccount):
    settings.DefaultAccount = defaultAccount.data

def update_config_default_version(defaultInstance):
    settings.DefaultInstance = defaultInstance.data


def update_config_dir(dir):
    if dir != settings.Minecraft_Dir and dir != "":
        if os.path.exists(os.path.normpath(dir)):
            for file in os.scandir(os.path.normpath(settings.Minecraft_Dir)):
                shutil.move(os.path.normpath(settings.Minecraft_Dir+"/"+file.name), os.path.normpath(dir))

            settings.Minecraft_Dir = os.path.normpath(dir)
        else:
            pass