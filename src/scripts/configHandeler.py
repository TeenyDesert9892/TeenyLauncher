import json
import os
import pathlib
import pickle
import platform
import shutil
import psutil


class configHandeler:
    def __init__(self):
        self.version = "0.8.0"
        
        if not os.path.exists(self.get_launcher_path()):
            os.mkdir(self.get_launcher_path())
        
        self.Theme = "Dark"
        self.Lang = "English"
        self.DefaultAccount = ""
        self.DefaultInstance = ""
        self.CloseOnPlay = True
        self.Version = self.version
        self.EnabledBgImg = False
        self.RamAmount = 2048
        self.Minecraft_Dir = os.path.normpath(self.get_launcher_path())
        self.Accounts = {}

        if not os.path.exists(f"{self.get_launcher_path()}/config.pkl"):
            self.save_config()
        self.load_config()


    def send_message(self, msg):
        from __main__ import MainGui
        
        MainGui.Message(msg)


    def save_config(self):
        pickleFile = open(self.get_launcher_path()+'/config.pkl', 'wb')
        pickle.dump({"Launcher": {"Theme": self.Theme,
                                    "Lang": self.Lang,
                                    "DefaultAccount": self.DefaultAccount,
                                    "DefaultInstance": self.DefaultInstance,
                                    "CloseOnPlay": self.CloseOnPlay,
                                    "Version": self.Version,
                                    "EnabledBgImg": self.EnabledBgImg,
                                    "RamAmount": int(self.RamAmount),
                                    "Minecraft_Dir": self.Minecraft_Dir},
                        "Accounts": self.Accounts}, pickleFile)
    

    def load_config(self):
        pickleFile = open(self.get_launcher_path()+'/config.pkl', 'rb')
        configFile = pickle.load(pickleFile)

        try: self.Theme = configFile["Launcher"]["Theme"]
        except: pass
        
        try: self.Lang = configFile["Launcher"]["Lang"]
        except: pass
        
        try: self.DefaultAccount = configFile["Launcher"]["DefaultAccount"]
        except: pass
        
        try: self.DefaultInstance = configFile["Launcher"]["DefaultInstance"]
        except: pass
        
        try: self.CloseOnPlay = configFile["Launcher"]["CloseOnPlay"]
        except: pass
        
        try: self.Version = configFile["Launcher"]["Version"]
        except: pass
        
        try: self.EnabledBgImg = configFile["Launcher"]["EnabledBgImg"]
        except: pass
        
        try: self.RamAmount = configFile["Launcher"]["RamAmount"]
        except: pass
        
        try: self.Minecraft_Dir = configFile["Launcher"]["Minecraft_Dir"]
        except: pass
        
        try: self.Accounts = configFile["Accounts"]
        except: pass
    

    def get_assets_path(self, path=os.getcwd()):
        if os.path.exists(path+'/src'):
            return path+'/src'
        return path


    def get_launcher_path(self):
        if platform.system() == "Windows":
            return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".teenylauncher")
        elif platform.system() == "Darwin":
            return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "teenylauncher")
        else:
            return os.path.join(str(pathlib.Path.home()), ".teenylauncher")


    def get_ram(self):
        ram = int(psutil.virtual_memory().total / (1024 ** 2))
        uncompatibleRam = True
        while uncompatibleRam:
            if ram % 32 != 0:
                ram -= 1
            else:
                uncompatibleRam = False
        return ram


    def update_config_lang(self, lang):
        self.Lang = lang


    def update_config_theme(self, theme):
        self.Theme = theme


    def update_config_bg(self, bgImg):
        self.EnabledBgImg = bgImg


    def update_config_ram(self, ram):
        self.RamAmount = ram


    def update_config_default_account(self, defaultAccount):
        self.DefaultAccount = defaultAccount.data


    def update_config_default_version(self, defaultInstance):
        self.DefaultInstance = defaultInstance.data


    def update_config_dir(self, dir):
        if dir != self.Minecraft_Dir and dir != "":
            if os.path.exists(os.path.normpath(dir)):
                for file in os.scandir(os.path.normpath(self.Minecraft_Dir)):
                    shutil.move(os.path.normpath(self.Minecraft_Dir+"/"+file.name), os.path.normpath(dir))

                self.Minecraft_Dir = os.path.normpath(dir)
            else:
                pass