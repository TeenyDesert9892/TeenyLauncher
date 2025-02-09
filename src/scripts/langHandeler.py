import json

from __main__ import ConfigHandeler


class langHandeler:
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

        self.Create_Version_Success = ""
        self.Create_Version_Failure = ""

        self.Install_Version_Already_Exsists = ""
        self.Install_Version_Without_Name = ""
        self.Install_Version_Not_Selected = ""
        self.Install_Version_Type_Not_Selected = ""

        self.Delete_Instances_Title = ""
        self.Delete_Instances_Button = ""

        self.Delete_Instance_Success = ""
        self.Delete_Instance_Failure = ""
        
        self.Modify_Instances_Title = ""
        self.Modify_Instance_Name_Title = ""
        self.Modify_Instances_Name_Button = ""
        self.Modify_Instance_Type_Title = ""
        self.Modify_Instance_Version_Title = ""
        self.Modify_Instance_Engin_Version_Title = ""
        self.Modify_Instance_Change_Button = ""

        self.Without_Versions = ""
        self.Without_Versions_To_Play = ""

        self.Config_Title = ""
        self.Launcher_Config_Title = ""
        self.Launcher_Config_Lang_Title = ""
        self.Launcher_Config_Theme_Title = ""
        self.Launcher_Config_Img = ""
        self.Launcher_Config_On_Close = ""

        self.Advanced_Config_Title = ""
        self.Advanced_Config_Ram_Title = ""
        self.Advanced_Config_Folder_Title = ""
        self.Advanced_Config_Minecraft_Directory = ""
        self.Advanced_Config_Open_Versions_Folder = ""

        self.Play_Menu_Config_Account_Title = ""
        self.Play_Menu_Select_Instance_Title = ""
        self.Play_Menu_Start_Game = ""

        self.Incompatible_JDK = ""
        self.Default_Option = "Default"
        self.Nothing = ""

        self.set_lang()
        

    def set_lang(self):
        with open(ConfigHandeler.get_assets_path()+'/lang/'+ConfigHandeler.Lang+'.json', "r") as langFile:
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

            self.Create_Instance_Success = lang["Create_Instance_Success"]
            self.Create_Instance_Failure = lang["Create_Instance_Failure"]

            self.Install_Version_Already_Exsists = lang["Install_Version_Already_Exsists"]
            self.Install_Version_Without_Name = lang["Install_Version_Without_Name"]
            self.Install_Version_Not_Selected = lang["Install_Version_Not_Selected"]
            self.Install_Version_Type_Not_Selected = lang["Install_Version_Type_Not_Selected"]

            self.Delete_Instances_Title = lang["Delete_Instances_Title"]
            self.Delete_Instances_Button = lang["Delete_Instances_Button"]

            self.Delete_Instance_Success = lang["Delete_Instance_Success"]
            self.Delete_Instance_Failure = lang["Delete_Instance_Failure"]
            
            self.Modify_Instances_Title = lang["Modify_Instances_Title"]
            self.Modify_Instance_Name_Title = lang["Modify_Instance_Name_Title"]
            self.Modify_Instances_Name_Button = lang["Modify_Instances_Name_Button"]
            self.Modify_Instance_Type_Title = lang["Modify_Instance_Type_Title"]
            self.Modify_Instance_Version_Title = lang["Modify_Instance_Version_Title"]
            self.Modify_Instance_Engin_Version_Title = lang["Modify_Instance_Engin_Version_Title"]
            self.Modify_Instance_Change_Button = lang["Modify_Instance_Change_Button"]

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
            self.Advanced_Config_Minecraft_Directory = lang["Advanced_Config_Minecraft_Directory"]
            self.Advanced_Config_Open_Versions_Folder = lang["Advanced_Config_Open_Versions_Folder"]

            self.Play_Menu_Config_Account_Title = lang["Play_Menu_Config_Account_Title"]
            self.Play_Menu_Select_Instance_Title = lang["Play_Menu_Select_Instance_Title"]
            self.Play_Menu_Start_Game = lang["Play_Menu_Start_Game"]

            self.Incompatible_JDK = lang["Incompatible_JDK"]