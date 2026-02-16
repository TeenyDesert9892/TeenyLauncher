import json
import os

from core import config

from utils import utils

lang_file = utils.get_assets_path()+'/lang/'+config.settings.Lang+'.json'

if not os.path.exists(lang_file):
    lang_file = utils.get_assets_path()+'/lang/en.json'

with open(lang_file, "r") as file:
    lang = json.load(file)
    
    Accounts_Title = lang["Accounts_Title"]
    Add_Accounts_Title = lang["Add_Accounts_Title"]
    Add_Account_Name = lang["Add_Account_Name"]
    Add_Account_Password = lang["Add_Account_Password"]
    Add_Account_Button = lang["Add_Account_Button"]

    Add_Account_Premium_Success = lang["Add_Account_Premium_Success"]
    Add_Account_No_Premium_Success = lang["Add_Account_No_Premium_Success"]
    Add_Account_Premium_Failure = lang["Add_Account_Premium_Failure"]
    Add_Account_No_Premium_Failure = lang["Add_Account_No_Premium_Failure"]
    Add_Account_Name_Already_Exsists = lang["Add_Account_Name_Already_Exsists"]
    Add_Account_Name_Remaining = lang["Add_Account_Name_Remaining"]
    Add_Account_Password_Remaining = lang["Add_Account_Password_Remaining"]
    Add_Account_No_Type_Selected = lang["Add_Account_No_Type_Selected"]

    Delete_Accounts_Title = lang["Delete_Accounts_Title"]
    Delete_Account_Button = lang["Delete_Account_Button"]
    Delete_Account_Success = lang["Delete_Account_Success"]
    Delete_Account_Failure = lang["Delete_Account_Failure"]

    Without_Accounts = lang["Without_Accounts"]
    Without_Accounts_To_Play = lang["Without_Accounts_To_Play"]

    Instances_Title = lang["Instances_Title"]
    Create_Instances_Title = lang["Create_Instances_Title"]
    Create_Instance_Name_Title = lang["Create_Instance_Name_Title"]
    Create_Instance_Type_Title = lang["Create_Instance_Type_Title"]
    Create_Instance_Version_Title = lang["Create_Instance_Version_Title"]
    Create_Instance_Engin_Version_Title = lang["Create_Instance_Engin_Version_Title"]
    Create_Instance_Install_Button = lang["Create_Instance_Install_Button"]

    Create_Instance_Success = lang["Create_Instance_Success"]
    Create_Instance_Failure = lang["Create_Instance_Failure"]

    Install_Version_Already_Exsists = lang["Install_Version_Already_Exsists"]
    Install_Version_Without_Name = lang["Install_Version_Without_Name"]
    Install_Version_Not_Selected = lang["Install_Version_Not_Selected"]
    Install_Version_Type_Not_Selected = lang["Install_Version_Type_Not_Selected"]

    Delete_Instances_Title = lang["Delete_Instances_Title"]
    Delete_Instances_Button = lang["Delete_Instances_Button"]

    Delete_Instance_Success = lang["Delete_Instance_Success"]
    Delete_Instance_Failure = lang["Delete_Instance_Failure"]
    
    Modify_Instances_Title = lang["Modify_Instances_Title"]
    Modify_Instance_Name_Title = lang["Modify_Instance_Name_Title"]
    Modify_Instances_Name_Button = lang["Modify_Instances_Name_Button"]
    Modify_Instance_Type_Title = lang["Modify_Instance_Type_Title"]
    Modify_Instance_Version_Title = lang["Modify_Instance_Version_Title"]
    Modify_Instance_Engin_Version_Title = lang["Modify_Instance_Engin_Version_Title"]
    Modify_Instance_Change_Button = lang["Modify_Instance_Change_Button"]

    Without_Versions = lang["Without_Versions"]
    Without_Versions_To_Play = lang["Without_Versions_To_Play"]

    Config_Title = lang["Config_Title"]
    Launcher_Config_Title = lang["Launcher_Config_Title"]
    Launcher_Config_Lang_Title = lang["Launcher_Config_Lang_Title"]
    Launcher_Config_Theme_Title = lang["Launcher_Config_Theme_Title"]
    Launcher_Config_Img = lang["Launcher_Config_Img"]
    Launcher_Config_On_Close = lang["Launcher_Config_On_Close"]

    Advanced_Config_Title = lang["Advanced_Config_Title"]
    Advanced_Config_Ram_Title = lang["Advanced_Config_Ram_Title"]
    Advanced_Config_Folder_Title = lang["Advanced_Config_Folder_Title"]
    Advanced_Config_Minecraft_Directory = lang["Advanced_Config_Minecraft_Directory"]
    Advanced_Config_Open_Versions_Folder = lang["Advanced_Config_Open_Versions_Folder"]

    Play_Menu_Config_Account_Title = lang["Play_Menu_Config_Account_Title"]
    Play_Menu_Select_Instance_Title = lang["Play_Menu_Select_Instance_Title"]
    Play_Menu_Start_Game = lang["Play_Menu_Start_Game"]

    Incompatible_JDK = lang["Incompatible_JDK"]
    
    Default_Option = ""