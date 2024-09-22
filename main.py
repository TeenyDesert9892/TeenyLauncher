import os
from concurrent.futures import ThreadPoolExecutor

import flet as ft

from scripts import configHandeler
from scripts import jdkHandeler
from scripts import accountsHandeler
from scripts import instancesHandeler

config = configHandeler.config
lang = configHandeler.lang
assets_path = configHandeler.get_assets_path()

def main(page: ft.Page):
    # -------------------------------
    # Page Pre-Configuration
    # -------------------------------

    backgroundImages = {"Dark": '/images/bg-dark.png', "Light": '/images/bg-light.png'}

    bgImg = ft.BoxDecoration(image=ft.DecorationImage(assets_path+backgroundImages[config.Theme],
                                                      fit=ft.ImageFit.COVER))

    page.title = "TeenyLauncher"
    page.window.min_width = 800
    page.window.min_height = 550
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.decoration = bgImg
    if config.EnabledBgImg:
        page.bgcolor = ft.colors.TRANSPARENT
    page.theme_mode = config.Theme.lower()

    # -------------------------------
    # Top Change Function
    # -------------------------------

    def changeMenu(menu):
        menus = {"HOME": infoCardColumn,
                 "ACCOUNTS": accountCardColumn,
                 "INSTANCES": instanceCardColumn,
                 "SETTINGS": configCardColumn}
        menuCard.clean()
        menuCard.content = menus[menu]
        menuCard.update()

    # -------------------------------
    # Top Buttons
    # -------------------------------

    topCardRow = ft.Row([ft.IconButton(icon=ft.icons.HOME,
                                       icon_color="#555555",
                                       icon_size=30,
                                       on_click=lambda e: changeMenu("HOME")),
                         ft.IconButton(icon=ft.icons.ACCOUNT_BOX,
                                       icon_color="#555555",
                                       icon_size=30,
                                       on_click=lambda e: changeMenu("ACCOUNTS")),
                         ft.IconButton(icon=ft.icons.FOLDER,
                                       icon_color="#555555",
                                       icon_size=30,
                                       on_click=lambda e: changeMenu("INSTANCES")),
                         ft.IconButton(icon=ft.icons.SETTINGS,
                                       icon_color="#555555",
                                       icon_size=30,
                                       on_click=lambda e: changeMenu("SETTINGS"))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        height=page.height/12,
                        spacing=page.width/5)

    # -------------------------------
    # Info Variables
    # -------------------------------

    infoCardColumn = ft.Column([ft.Text('TeenyLauncher', size=48),
                               ft.Text(configHandeler.version_info, size=16)],
                               alignment=ft.MainAxisAlignment.CENTER,
                               horizontal_alignment=ft.MainAxisAlignment.CENTER,
                               width=page.width/1.5,
                               height=page.height/1.4)

    # -------------------------------
    # Config Functions
    # -------------------------------

    def configPharagraph(menu):
        menus = {lang.Launcher_Config_Title: normalConfigCardColumn,
                 lang.Advanced_Config_Title: advancedConfigCardColumn}
        configCard.clean()
        configCard.content = menus[menu.data]
        configCard.update()

    def langChange(dropdown):
        configHandeler.update_config_lang(dropdown.data)
        Message("To apply the languaje changes you need to restart the launcher")

    def themeChange(dropdown):
        configHandeler.update_config_theme(dropdown.data)
        bgImg.image = ft.DecorationImage(assets_path+backgroundImages[config.Theme],
                                         fit=ft.ImageFit.COVER)
        page.theme_mode = dropdown.data.lower()
        page.update()

    def imageChange(checkBox):
        if checkBox.data == "true":
            page.bgcolor = ft.colors.TRANSPARENT
            config.EnabledBgImg = True
        else:
            page.bgcolor = ft.colors.BACKGROUND
            config.EnabledBgImg = False
        page.update()
    
    def closeOnPlayChange(checkBox):
        if checkBox.data == "true":
            config.CloseOnPlay = True
        else:
            config.CloseOnPlay = False
        page.update()

    def ramTextValueEdit(e=None):
        ramConfigShow.value = str(int(ramConfigSlider.value))+'MB'
        configHandeler.update_config_ram(ramConfigSlider.value)
        ramConfigShow.update()

    def addRam(e=None):
        if ramConfigSlider.value < configHandeler.get_ram():
            ramConfigSlider.value += 32
            ramConfigSlider.update()
            ramTextValueEdit(ramConfigSlider)

    def removeRam(e=None):
        if ramConfigSlider.value > 128:
            ramConfigSlider.value -= 32
            ramConfigSlider.update()
            ramTextValueEdit(ramConfigSlider)

    # -------------------------------
    # Config Variables
    # -------------------------------

    languajeConfigDropdown = ft.Dropdown(lang.Default_Option,
                                          [ft.dropdown.Option(option.name.removesuffix(".json"))
                                           for option in os.scandir(assets_path+'/lang')
                                           if option.name != "Example.json"],
                                         width=page.width/1.6,
                                         on_change=langChange)

    themeConfigDropdown = ft.Dropdown(lang.Default_Option,
                                      [ft.dropdown.Option("Light"),
                                       ft.dropdown.Option("Dark")],
                                      width=page.width/1.6,
                                      on_change=themeChange)

    normalConfigCardColumn = ft.Column([ft.Text(lang.Launcher_Config_Title, size=36),
                                        ft.Text(lang.Launcher_Config_Lang_Title, size=16),
                                        languajeConfigDropdown,
                                        ft.Text(lang.Launcher_Config_Theme_Title, size=16),
                                        themeConfigDropdown,
                                        ft.Switch(lang.Launcher_Config_Img, value=config.EnabledBgImg, on_change=imageChange),
                                        ft.Switch(lang.Launcher_Config_On_Close, value=config.CloseOnPlay, on_change=closeOnPlayChange)],
                                       alignment=ft.MainAxisAlignment.CENTER,
                                       horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                       width=page.width/1.6,
                                       height=page.height/2.2,
                                       scroll=ft.ScrollMode.AUTO)

    ramConfigSlider = ft.Slider(value=config.RamAmount,
                                min=128,
                                max=configHandeler.get_ram(),
                                divisions=int(configHandeler.get_ram()/32)-4,
                                width=page.width/2.35,
                                on_change=ramTextValueEdit,
                                on_change_start=ramTextValueEdit,
                                on_change_end=ramTextValueEdit)

    ramConfigShow = ft.Text(str(config.RamAmount)+'MB', size=12)

    ramConfigRow = ft.Row([ramConfigSlider,
                           ft.Row([ft.IconButton(ft.icons.REMOVE, on_click=removeRam),
                                   ramConfigShow,
                                   ft.IconButton(ft.icons.ADD, on_click=addRam)])],
                          alignment=ft.MainAxisAlignment.CENTER,
                          spacing=page.width/50)

    minecraftDirectoryConfigTextField = ft.TextField(configHandeler.minecraft_directory, width=page.width/1.6)

    openFolderConfigCuppertinoFilledButton = ft.CupertinoFilledButton(lang.Advanced_Config_Open_Versions_Folder,
                                                                      ft.icons.FOLDER,
                                                                      width=page.width/1.6,
                                                                      on_click=instancesHandeler.open_instances_folder)

    advancedConfigCardColumn = ft.Column([ft.Text(lang.Advanced_Config_Title, size=36),
                                          ft.Text(lang.Advanced_Config_Ram_Title, size=16),
                                          ramConfigRow,
                                          ft.Text(lang.Advanced_Config_Folder_Title, size=16),
                                          minecraftDirectoryConfigTextField,
                                          openFolderConfigCuppertinoFilledButton],
                                         alignment=ft.MainAxisAlignment.CENTER,
                                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                         width=page.width/1.6,
                                         height=page.height/2.2,
                                         scroll=ft.ScrollMode.AUTO)

    configCard = ft.Card(normalConfigCardColumn,
                         width=page.width/1.6,
                         height=page.height/2.2)

    configDropdown = ft.Dropdown(lang.Default_Option,
                                 [ft.dropdown.Option(lang.Launcher_Config_Title),
                                  ft.dropdown.Option(lang.Advanced_Config_Title)],
                                 on_change=configPharagraph,
                                 width=page.width/1.6)

    configCardColumn = ft.Column([ft.Text(lang.Config_Title, size=36),
                                  configDropdown,
                                  configCard],
                                 width=page.width/1.5,
                                 height=page.height/1.4,
                                 alignment=ft.MainAxisAlignment.CENTER,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # -------------------------------
    # Instances Functions
    # -------------------------------

    def instancesPharagraph(menu):
        menus = {lang.Create_Instances_Title: addInstanceCardColumn,
                 lang.Delete_Instances_Title: removeInstanceCardColumn}
        instancesCard.clean()
        instancesCard.content = menus[menu.data]
        instancesCard.update()

    def update_versions(e=None):
        version, version_list = instancesHandeler.check_versions(addInstanceType.value)
        for i, ver in enumerate(version_list):
            version_list[i] = ft.dropdown.Option(ver)
        addInstanceVersion.value, addInstanceVersion.options = version, version_list
        addInstanceVersion.update()
        update_versions_engines()

    def update_versions_engines(e=None):
        engine, engine_list = instancesHandeler.check_engine_ver(addInstanceVersion.value, addInstanceType.value)
        for i, eng in enumerate(engine_list):
            engine_list[i] = ft.dropdown.Option(eng)
        addInstaceEngine.value, addInstaceEngine.options = engine, engine_list
        addInstaceEngine.update() 

    def start_instance_install(e=None):
        instancesHandeler.install_instance(addInstanceName.value,
                                           addInstanceType.value,
                                           addInstanceVersion.value,
                                           addInstaceEngine.value,
                                           setStatus,
                                           setProgress,
                                           setMax,
                                           Message)
        progressReset()
        updateInstances(True)
        updateRemoveInstances(True)
    
    def start_instance_uninstall(e=None):
        instancesHandeler.uninstall_instance(removeInstancesDropdown.value,
                                             setStatus,
                                             setProgress,
                                             setMax,
                                             Message)
        progressReset()
        updateInstances(True)
        updateRemoveInstances(True)

    # -------------------------------
    # Instances Variables
    # -------------------------------

    addInstanceName = ft.TextField(width=page.width/1.7)

    addInstanceType = ft.Dropdown(lang.Default_Option,
                                  [ft.dropdown.Option("Vanilla"),
                                   ft.dropdown.Option("Snapshot"),
                                   ft.dropdown.Option("Forge"),
                                   ft.dropdown.Option("Fabric"),
                                   ft.dropdown.Option("Fabric Snapshot"),
                                   ft.dropdown.Option("Quilt"),
                                   ft.dropdown.Option("Quilt Snapshot")],
                                  width=page.width/1.7,
                                  on_change=update_versions)

    addInstanceVersion = ft.Dropdown(width=page.width/1.7,
                                     on_change=update_versions_engines)

    addInstaceEngine = ft.Dropdown(width=page.width/1.7)

    addInstancesButton = ft.CupertinoFilledButton(lang.Create_Instance_Install_Button,
                                                  icon=ft.icons.ADD_BOX,
                                                  width=page.width/1.7,
                                                  on_click=start_instance_install)

    addInstanceCardColumn = ft.Column([ft.Text(lang.Create_Instance_Name_Title, size=16),
                                       addInstanceName,
                                       ft.Text(lang.Create_Instance_Type_Title, size=16),
                                       addInstanceType,
                                       ft.Text(lang.Create_Instance_Version_Title, size=16),
                                       addInstanceVersion,
                                       ft.Text(lang.Create_Instance_Engin_Version_Title, size=16),
                                       addInstaceEngine,
                                       addInstancesButton],
                                      scroll=ft.ScrollMode.AUTO,
                                      alignment=ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                      width=page.width/1.6,
                                      height=page.height/2.2)

    removeInstancesDropdown = ft.Dropdown(lang.Default_Option,
                                          width=page.width/1.7,)

    removeInstancesButton = ft.CupertinoFilledButton(lang.Delete_Instances_Button,
                                                     icon=ft.icons.CANCEL,
                                                     width=page.width/1.7,
                                                     on_click=start_instance_uninstall)

    removeInstanceCardColumn = ft.Column([removeInstancesDropdown,
                                          removeInstancesButton],
                                         scroll=ft.ScrollMode.AUTO,
                                         alignment=ft.MainAxisAlignment.CENTER,
                                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                         width=page.width/1.6,
                                         height=page.height/2.2)

    instancesCard = ft.Card(addInstanceCardColumn,
                            width=page.width/1.6,
                            height=page.height/2.2)

    instancesSelectDropdown = ft.Dropdown(lang.Default_Option,
                                    [ft.dropdown.Option(lang.Create_Instances_Title),
                                     ft.dropdown.Option(lang.Delete_Instances_Title)],
                                    width=page.width/1.6,
                                    on_change=instancesPharagraph)

    instanceCardColumn = ft.Column([ft.Text(lang.Instances_Title, size=36),
                                    instancesSelectDropdown,
                                    instancesCard],
                                   alignment=ft.MainAxisAlignment.CENTER,
                                   horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                   width=page.width/1.5,
                                   height=page.height/1.4)

    # -------------------------------
    # Account Functions
    # -------------------------------

    def accountsParagraph(menu):
        menus = {lang.Add_Accounts_Title: addAccountColumn,
                 lang.Delete_Accounts_Title: removeAccountColumn}
        accountsCard.clean()
        accountsCard.content = menus[menu.data]
        accountsCard.update()
    
    def start_account_creation(e=None):
        accountsHandeler.add_account(addAccountType.value,
                                    addAccountName.value,
                                    addAccountPassword.value,
                                    setStatus,
                                    setProgress,
                                    setMax,
                                    Message)
        progressReset()
        updateAccounts(True)
        updateRemoveAccounts(True)
    
    def start_account_delete(e=None):
        accountsHandeler.del_account(removeAccountDropdown.value,
                                     setStatus,
                                     setProgress,
                                     setMax,
                                     Message)
        progressReset()
        updateAccounts(True)
        updateRemoveAccounts(True)

    # -------------------------------
    # Account Variables
    # -------------------------------

    addAccountType = ft.Dropdown(lang.Default_Option,
                                 [ft.dropdown.Option("Premiun"),
                                  ft.dropdown.Option("No Premiun")],
                                 width=page.width/1.7)

    addAccountName = ft.TextField(width=page.width/1.7)

    addAccountPassword = ft.TextField(password=True,
                                      can_reveal_password=True,
                                      width=page.width/1.7)

    addAccountButton = ft.CupertinoFilledButton(lang.Add_Account_Button,
                                                icon=ft.icons.ACCOUNT_BOX,
                                                width=page.width/1.7,
                                                on_click=start_account_creation)

    addAccountColumn = ft.Column([addAccountType,
                                  ft.Text(lang.Add_Account_Name, size=16),
                                  addAccountName,
                                  ft.Text(lang.Add_Account_Password, size=16),
                                  addAccountPassword,
                                  addAccountButton],
                                 alignment=ft.MainAxisAlignment.CENTER,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 scroll=ft.ScrollMode.AUTO,
                                 width=page.width/1.6,
                                 height=page.height/2.2)

    removeAccountDropdown = ft.Dropdown(lang.Default_Option,
                                        [ft.dropdown.Option(account)
                                         for account in config.Accounts],
                                        width=page.width/1.7)

    removeAccountButton = ft.CupertinoFilledButton(lang.Delete_Account_Button,
                                                   width=page.width/1.7,
                                                   icon=ft.icons.CANCEL,
                                                   on_click=start_account_delete)

    removeAccountColumn = ft.Column([removeAccountDropdown,
                                     removeAccountButton],
                                    scroll=ft.ScrollMode.AUTO,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    width=page.width/1.6,
                                    height=page.height/2.2)

    accountsCard = ft.Card(addAccountColumn,
                           width=page.width/1.6,
                           height=page.height/2.2)

    accountCardColumn = ft.Column([ft.Text(lang.Accounts_Title, size=36),
                                     ft.Dropdown(lang.Add_Accounts_Title,
                                                 [ft.dropdown.Option(lang.Add_Accounts_Title),
                                                  ft.dropdown.Option(lang.Delete_Accounts_Title)],
                                                 on_change=accountsParagraph,
                                                 width=page.width/1.6),
                                     accountsCard],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    width=page.width/1.5,
                                    height=page.height/1.4)

    # -------------------------------
    # Menu Card
    # -------------------------------

    menuCard = ft.Card(infoCardColumn,
                       width=page.width/1.5,
                       height=page.height/1.4)

    # -------------------------------
    # LaunchGame Functions
    # -------------------------------

    def run_game(e=None):
        if config.CloseOnPlay:
            page.window.close()
        instancesHandeler.run_instance(instancesDropdown.value,
                                       accountsDropdown.value,
                                       Message)

    # -------------------------------
    # LaunchGame Variables
    # -------------------------------

    accountsDropdown = ft.Dropdown(width=page.width/3.4)

    instancesDropdown = ft.Dropdown(width=page.width/3.4)

    launchGameButton = ft.CupertinoFilledButton(lang.Play_Menu_Start_Game,
                                                icon=ft.icons.PLAY_ARROW_ROUNDED,
                                                width=page.width/3.4,
                                                on_click=run_game)

    launchGameCardColumn = ft.Column([ft.Text(lang.Play_Menu_Config_Account_Title, size=16),
                                     accountsDropdown,
                                     ft.Text(lang.Play_Menu_Select_Instance_Title, size=16),
                                     instancesDropdown,
                                     launchGameButton],
                                     alignment=ft.MainAxisAlignment.CENTER,
                                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                     width=page.width/3.25,
                                     height=page.height/1.4)

    launchGameCard = ft.Card(launchGameCardColumn,
                             width=page.width/3.25,
                             height=page.height/1.4)

    # -------------------------------
    # ProgressBar Functions
    # -------------------------------

    def setStatus(status=str):
        try:
            progressBarMessage.value = status
            progressBarRow.update()
        except:
            pass

    def setProgress(progress=int):
        try:
            global maxProgress
            progressBarPercentage.value = str(progress)+'/'+str(maxProgress)
            progressBar.value= progress/maxProgress
            progressBarRow.update()
        except:
            pass

    def setMax(max=int):
        try:
            global maxProgress
            maxProgress = max
            progressBarRow.update()
        except:
            pass
    
    def progressReset():
        global current_max_progress
        progressBarMessage.value = "No tasks running"
        progressBarPercentage.value = "0/0"
        progressBar.value = 1
        current_max_progress = 0   
        progressBarRow.update()

    # -------------------------------
    # ProgressBar Variables
    # -------------------------------

    progressBarMessage = ft.Text("No tasks running",
                                 width=page.width/9,
                                 text_align=ft.TextAlign.CENTER)

    progressBar = ft.ProgressBar(value=0.5,
                                 width=page.width/2)

    progressBarPercentage = ft.Text("0/0",
                                    width=page.width/10,
                                    text_align=ft.TextAlign.CENTER)

    progressBarRow = ft.Row([progressBarMessage,
                             progressBar,
                             progressBarPercentage],
                            alignment=ft.MainAxisAlignment.CENTER,
                            height=page.height/10)
    
    # -------------------------------
    # Page Message
    # -------------------------------

    def Message(msg):
        alertMsg = ft.AlertDialog(content=ft.Text(msg, size=16))
        page.open(alertMsg)

    # -------------------------------
    # StartUp Page
    # -------------------------------

    page.add(ft.Card(topCardRow),
             ft.Row([menuCard,
                     launchGameCard],
                    alignment=ft.MainAxisAlignment.CENTER),
             ft.Card(progressBarRow))

    # -------------------------------
    # Page Updates
    # -------------------------------

    def update_contents(e=None):
        topCardRow.height = page.height/12
        topCardRow.spacing = page.width/5

        menuCard.width = page.width/1.5
        menuCard.height = page.height/1.4

        infoCardColumn.width = page.width/1.5
        infoCardColumn.height = page.height/1.4

        configCardColumn.width = page.width/1.5
        configCardColumn.height = page.height/1.4
        configCard.width = page.width/1.6
        configCard.height = page.height/2.2
        configDropdown.width = page.width/1.6

        normalConfigCardColumn.width = page.width/1.6
        normalConfigCardColumn.height = page.height/2.2
        languajeConfigDropdown.width = page.width/1.6
        themeConfigDropdown.width = page.width/3.2

        advancedConfigCardColumn.width = page.width/1.6
        advancedConfigCardColumn.height = page.height/2.2
        ramConfigSlider.width = page.width/2.35
        ramConfigRow.spacing = page.width/50
        minecraftDirectoryConfigTextField.width = page.width/1.6
        openFolderConfigCuppertinoFilledButton.width = page.width/1.6

        accountCardColumn.width = page.width/1.5
        accountCardColumn.height = page.height/1.4
        accountsCard.width = page.width/1.6
        accountsCard.height = page.height/2.2

        addAccountColumn.width = page.width/1.6
        addAccountColumn.height = page.height/2.2
        addAccountType.width = page.width/1.7
        addAccountName.width = page.width/1.7
        addAccountPassword.width = page.width/1.7
        addAccountButton.width = page.width/1.7

        removeAccountColumn.width = page.width/1.6
        removeAccountColumn.height = page.height/2.2

        instanceCardColumn.width = page.width/1.5
        instanceCardColumn.height = page.height/1.4
        instancesDropdown.width = page.width/1.6
        instancesCard.width = page.width/1.6
        instancesCard.height = page.height/2.2

        addInstanceCardColumn.width = page.width/1.6
        addInstanceCardColumn.height = page.height/2.2
        addInstanceName.width = page.width/1.7
        addInstanceVersion.width = page.width/1.7
        addInstaceEngine.width = page.width/1.7
        addInstancesButton.width = page.width/1.7

        removeInstanceCardColumn.width = page.width/1.6
        removeInstanceCardColumn.height = page.height/2.2
        removeInstancesDropdown.width = page.width/1.7
        removeInstancesButton.width = page.width/1.7

        launchGameCard.width = page.width/3.25
        launchGameCard.height = page.height/1.4

        launchGameCardColumn.width = page.width/3.25
        launchGameCardColumn.height = page.height/1.4
        accountsDropdown.width = page.width/3.4
        instancesDropdown.width = page.width/3.4
        launchGameButton.width = page.width/3.4

        progressBarRow.height = page.height/10
        progressBar.width = page.width/2
        page.update()

    page.on_resized = update_contents

    def updateAccounts(update):
        value, options = accountsHandeler.check_accounts()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)
        accountsDropdown.value, accountsDropdown.options = value, options

        if update:
            accountsDropdown.update()
    
    def updateRemoveAccounts(update):
        value, options = accountsHandeler.check_accounts()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)
        removeAccountDropdown.value, removeAccountDropdown.options = value, options
        
        if update:
            removeAccountDropdown.update()

    def updateInstances(update):
        value, options = instancesHandeler.check_instances()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)
        
        instancesDropdown.value, instancesDropdown.options = value, options
        if update:
            instancesDropdown.update()
    
    def updateRemoveInstances(update):
        value, options = instancesHandeler.check_instances()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)

        removeInstancesDropdown.value, removeInstancesDropdown.options = value, options
        if update:
            removeInstancesDropdown.update()

    accountsDropdown.on_change = configHandeler.update_config_default_account
    instancesDropdown.on_change = configHandeler.update_config_default_version

    updateAccounts(False)
    updateRemoveAccounts(False)
    updateInstances(False)
    updateRemoveInstances(False)

    page.update()


if __name__ == "__main__":
    tasks = ThreadPoolExecutor(max_workers=1)
    ft.app(main)
    config.save_config()