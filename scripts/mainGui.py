import os
import flet as ft

from __main__ import ProcessHandeler
from __main__ import ConfigHandeler
from __main__ import LangHandeler
from __main__ import InstanceHandeler
from __main__ import AccountHandeler

def gui(page: ft.Page):
    # -------------------------------
    # Page Pre-Configuration
    # -------------------------------


    backgroundImages = {"Dark": '/assets/images/bg-dark.png',
                        "Light": '/assets/images/bg-light.png'}


    bgImg = ft.BoxDecoration(image=ft.DecorationImage(ConfigHandeler.get_assets_path()+backgroundImages[ConfigHandeler.Theme],
                                                      fit=ft.ImageFit.COVER))


    page.title = "TeenyLauncher"
    page.window.min_width = 700
    page.window.min_height = 550
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.decoration = bgImg
    
    if ConfigHandeler.EnabledBgImg:
        page.bgcolor = ft.colors.TRANSPARENT
    page.theme_mode = ConfigHandeler.Theme.lower()


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
                                       icon_size=30,
                                       on_click=lambda event: changeMenu("HOME")),
                         ft.IconButton(icon=ft.icons.ACCOUNT_BOX,
                                       icon_size=30,
                                       on_click=lambda event: changeMenu("ACCOUNTS")),
                         ft.IconButton(icon=ft.icons.FOLDER,
                                       icon_size=30,
                                       on_click=lambda event: changeMenu("INSTANCES")),
                         ft.IconButton(icon=ft.icons.SETTINGS,
                                       icon_size=30,
                                       on_click=lambda event: changeMenu("SETTINGS"))],
                        alignment=ft.MainAxisAlignment.CENTER,
                        height=page.height/12,
                        spacing=page.width/5)


    # -------------------------------
    # Info Version changelog function
    # -------------------------------


    def change_info(event):
        for file in os.scandir('assets/version-changelogs'):
            if file.name.replace('.txt', '') ==  event.data:
                infoVersionText.value = open(file.path, 'r', encoding='utf-8').read()
        infoVersionText.update()


    # -------------------------------
    # Info Variables
    # -------------------------------


    infoTextTitle = ft.Text('TeenyLauncher '+ConfigHandeler.version, size=48)


    infoDropdown = ft.Dropdown(LangHandeler.Default_Option,
                               [ft.dropdown.Option(file.name.replace('.txt', ''))
                                for file in os.scandir('assets/version-changelogs')],
                               width=page.width/1.6,
                               on_change=change_info)
    
    
    infoVersionText = ft.Text(open('assets/version-changelogs/V'+ConfigHandeler.version+'.txt', 'r').read())

    
    infoColumn = ft.Column([infoDropdown, infoVersionText],
                                       horizontal_alignment=ft.MainAxisAlignment.CENTER,
                                       width=page.width/1.7,
                                       height=page.height/2)
    

    infoCard = ft.Card(infoColumn)


    infoCardColumn = ft.Column([infoTextTitle, infoCard],
                               alignment=ft.MainAxisAlignment.CENTER,
                               horizontal_alignment=ft.MainAxisAlignment.CENTER,
                               width=page.width/1.5,
                               height=page.height/1.4)


    # -------------------------------
    # Config Functions
    # -------------------------------


    def configPharagraph(menu):
        menus = {LangHandeler.Launcher_Config_Title: normalConfigCardColumn,
                 LangHandeler.Advanced_Config_Title: advancedConfigCardColumn}
        configCard.clean()
        configCard.content = menus[menu.data]
        configCard.update()


    def langChange(dropdown):
        ConfigHandeler.update_config_lang(dropdown.data)
        Message("To apply the languaje changes you need to restart the launcher")


    def themeChange(dropdown):
        ConfigHandeler.update_config_theme(dropdown.data)
        bgImg.image = ft.DecorationImage(ConfigHandeler.get_assets_path()+backgroundImages[ConfigHandeler.Theme],
                                         fit=ft.ImageFit.COVER)
        page.theme_mode = dropdown.data.lower()
        page.update()


    def imageChange(checkBox):
        if checkBox.data == "true":
            page.bgcolor = ft.colors.TRANSPARENT
            ConfigHandeler.EnabledBgImg = True
        else:
            page.bgcolor = ft.colors.BACKGROUND
            ConfigHandeler.EnabledBgImg = False
        page.update()
    
    
    def closeOnPlayChange(checkBox):
        if checkBox.data == "true":
            ConfigHandeler.CloseOnPlay = True
        else:
            ConfigHandeler.CloseOnPlay = False
        page.update()


    def ramTextValueEdit(event=None):
        ramConfigShow.value = str(int(ramConfigSlider.value))+'MB'
        ConfigHandeler.update_config_ram(ramConfigSlider.value)
        ramConfigShow.update()


    def addRam(event=None):
        if ramConfigSlider.value < ConfigHandeler.get_ram():
            ramConfigSlider.value += 32
            ramConfigSlider.update()
            ramTextValueEdit(ramConfigSlider)


    def removeRam(event=None):
        if ramConfigSlider.value > 128:
            ramConfigSlider.value -= 32
            ramConfigSlider.update()
            ramTextValueEdit(ramConfigSlider)


    # -------------------------------
    # Config Variables
    # -------------------------------


    languajeConfigDropdown = ft.Dropdown(LangHandeler.Default_Option,
                                          [ft.dropdown.Option(option.name.removesuffix(".json"))
                                           for option in os.scandir(ConfigHandeler.get_assets_path()+'/assets/lang')
                                           if option.name != "Example.json"],
                                         width=page.width/1.6,
                                         on_change=langChange)


    themeConfigDropdown = ft.Dropdown(LangHandeler.Default_Option,
                                      [ft.dropdown.Option("Light"),
                                       ft.dropdown.Option("Dark")],
                                      width=page.width/1.6,
                                      on_change=themeChange)


    normalConfigCardColumn = ft.Column([ft.Text(LangHandeler.Launcher_Config_Title, size=36),
                                        ft.Text(LangHandeler.Launcher_Config_Lang_Title, size=16),
                                        languajeConfigDropdown,
                                        ft.Text(LangHandeler.Launcher_Config_Theme_Title, size=16),
                                        themeConfigDropdown,
                                        ft.Switch(LangHandeler.Launcher_Config_Img, value=ConfigHandeler.EnabledBgImg, on_change=imageChange),
                                        ft.Switch(LangHandeler.Launcher_Config_On_Close, value=ConfigHandeler.CloseOnPlay, on_change=closeOnPlayChange)],
                                       alignment=ft.MainAxisAlignment.CENTER,
                                       horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                       width=page.width/1.6,
                                       height=page.height/2.2,
                                       scroll=ft.ScrollMode.AUTO)


    ramConfigSlider = ft.Slider(value=ConfigHandeler.RamAmount,
                                min=128,
                                max=ConfigHandeler.get_ram(),
                                divisions=int(ConfigHandeler.get_ram()/32)-4,
                                width=page.width/2.35,
                                on_change=ramTextValueEdit,
                                on_change_start=ramTextValueEdit,
                                on_change_end=ramTextValueEdit)


    ramConfigShow = ft.Text(str(ConfigHandeler.RamAmount)+'MB', size=12)


    ramConfigRow = ft.Row([ramConfigSlider,
                           ft.Row([ft.IconButton(ft.icons.REMOVE, on_click=removeRam),
                                   ramConfigShow,
                                   ft.IconButton(ft.icons.ADD, on_click=addRam)])],
                          alignment=ft.MainAxisAlignment.CENTER,
                          spacing=page.width/50)


    minecraftDirectoryConfigTextField = ft.TextField(ConfigHandeler.Minecraft_Dir,
                                                     width=page.width/2.4)
    
    
    minecraftFirectoryConfigButton = ft.CupertinoFilledButton(LangHandeler.Advanced_Config_Minecraft_Directory,
                                                              width=page.width/5.5,
                                                              on_click=lambda event: ConfigHandeler.update_config_dir(minecraftDirectoryConfigTextField.value))


    openFolderConfigCuppertinoFilledButton = ft.CupertinoFilledButton(LangHandeler.Advanced_Config_Open_Versions_Folder,
                                                                      ft.icons.FOLDER,
                                                                      width=page.width/1.6,
                                                                      on_click=InstanceHandeler.open_instances_folder)


    advancedConfigCardColumn = ft.Column([ft.Text(LangHandeler.Advanced_Config_Title, size=36),
                                          ft.Text(LangHandeler.Advanced_Config_Ram_Title, size=16),
                                          ramConfigRow,
                                          ft.Text(LangHandeler.Advanced_Config_Folder_Title, size=16),
                                          ft.Row([minecraftDirectoryConfigTextField,
                                                  minecraftFirectoryConfigButton],
                                                 alignment=ft.MainAxisAlignment.CENTER),
                                          openFolderConfigCuppertinoFilledButton],
                                         alignment=ft.MainAxisAlignment.CENTER,
                                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                         width=page.width/1.6,
                                         height=page.height/2.2,
                                         scroll=ft.ScrollMode.AUTO)


    configCard = ft.Card(normalConfigCardColumn,
                         width=page.width/1.6,
                         height=page.height/2.2)


    configDropdown = ft.Dropdown(LangHandeler.Default_Option,
                                 [ft.dropdown.Option(LangHandeler.Launcher_Config_Title),
                                  ft.dropdown.Option(LangHandeler.Advanced_Config_Title)],
                                 on_change=configPharagraph,
                                 width=page.width/1.6)


    configCardColumn = ft.Column([ft.Text(LangHandeler.Config_Title, size=36),
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
        menus = {LangHandeler.Create_Instances_Title: addInstanceCardColumn,
                 LangHandeler.Delete_Instances_Title: removeInstanceCardColumn,
                 LangHandeler.Modify_Instances_Title: modifyInstancesCardColumn}
        instancesCard.clean()
        instancesCard.content = menus[menu.data]
        instancesCard.update()


    def update_versions(event=None):
        version, version_list = InstanceHandeler.check_versions(addInstanceType.value)
        for i, ver in enumerate(version_list):
            version_list[i] = ft.dropdown.Option(ver)
        addInstanceVersion.value, addInstanceVersion.options = version, version_list
        
        if event:
            addInstanceVersion.update()
        update_versions_engines(True)


    def update_versions_engines(event=None):
        engine, engine_list = InstanceHandeler.check_engine_ver(addInstanceVersion.value, addInstanceType.value)
        for i, eng in enumerate(engine_list):
            engine_list[i] = ft.dropdown.Option(eng)
        addInstaceEngine.value, addInstaceEngine.options = engine, engine_list
        
        if event:
            addInstaceEngine.update()
    
    
    def modify_versions(event=None):
        version, version_list = InstanceHandeler.check_versions(modifyInstancesType.value)
        for i, ver in enumerate(version_list):
            version_list[i] = ft.dropdown.Option(ver)
        modifyInstancesVersion.value, modifyInstancesVersion.options = version, version_list
        
        if event:
            modifyInstancesVersion.update()
        modify_versions_engines(True)


    def modify_versions_engines(event=None):
        engine, engine_list = InstanceHandeler.check_engine_ver(modifyInstancesVersion.value, modifyInstancesType.value)
        for i, eng in enumerate(engine_list):
            engine_list[i] = ft.dropdown.Option(eng)
        modifyInstancesEngine.value, modifyInstancesEngine.options = engine, engine_list
        
        if event:
            modifyInstancesEngine.update()
    
    
    def update_instances_displays(ins, modIns, remIns):
        updateInstances(ins)
        updateInstancesModify(modIns)
        updateRemoveInstances(remIns)
    
    
    def modify_version_start(event=None):
        ProcessHandeler.add_process(InstanceHandeler.modify_instance,
                                    modifyInstancesName.value,
                                    modifyInstancesType.value,
                                    modifyInstancesVersion.value,
                                    modifyInstancesEngine.value,
                                    callback)
        progressReset()
        update_instances_displays(False, True, False)


    def start_instance_install(event=None):
        ProcessHandeler.add_process(InstanceHandeler.install_instance,
                                    addInstanceName.value,
                                    addInstanceType.value,
                                    addInstanceVersion.value,
                                    addInstaceEngine.value,
                                    callback)
        progressReset()
        update_instances_displays(True, False, False)
    
    
    def start_instance_uninstall(event=None):
        ProcessHandeler.add_process(InstanceHandeler.uninstall_instance,
                                    removeInstancesDropdown.value,
                                    callback)
        progressReset()
        update_instances_displays(True, False, True)
    
    
    def modify_instance_name_updater(event=None):
        if modifyInstancesInstance.value != LangHandeler.Without_Versions:
            modifyInstancesName.value = modifyInstancesInstance.value
            if event:
                modifyInstancesName.update()
    
    
    def modify_instance_name(event=None):
        InstanceHandeler.update_instance_name(modifyInstancesInstance.value,
                                              modifyInstancesName.value)
        update_instances_displays(True, False, False)
    
    
    # -------------------------------
    # Instances Variables
    # -------------------------------


    addInstanceName = ft.TextField(width=page.width/1.7)


    addInstanceType = ft.Dropdown(LangHandeler.Default_Option,
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


    addInstancesButton = ft.CupertinoFilledButton(LangHandeler.Create_Instance_Install_Button,
                                                  icon=ft.icons.ADD_BOX,
                                                  width=page.width/1.7,
                                                  on_click=start_instance_install)


    addInstanceCardColumn = ft.Column([ft.Text(LangHandeler.Create_Instance_Name_Title, size=16),
                                       addInstanceName,
                                       ft.Text(LangHandeler.Create_Instance_Type_Title, size=16),
                                       addInstanceType,
                                       ft.Text(LangHandeler.Create_Instance_Version_Title, size=16),
                                       addInstanceVersion,
                                       ft.Text(LangHandeler.Create_Instance_Engin_Version_Title, size=16),
                                       addInstaceEngine,
                                       addInstancesButton],
                                      scroll=ft.ScrollMode.AUTO,
                                      alignment=ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                      width=page.width/1.6,
                                      height=page.height/2.2)


    removeInstancesDropdown = ft.Dropdown(LangHandeler.Default_Option,
                                          width=page.width/1.7,)


    removeInstancesButton = ft.CupertinoFilledButton(LangHandeler.Delete_Instances_Button,
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
    
    
    modifyInstancesInstance = ft.Dropdown(width=page.width/1.7,
                                          on_change=modify_instance_name_updater)
    
    
    modifyInstancesName = ft.TextField(text_size=16,
                                       width=page.width/2.4)
    
    
    modifyInstancesChangeName = ft.CupertinoFilledButton(LangHandeler.Modify_Instances_Name_Button,
                                                         ft.icons.EDIT,
                                                         width=page.width/5.5,
                                                         on_click=modify_instance_name)
    
    
    modifyInstancesType = ft.Dropdown(LangHandeler.Default_Option,
                                      [ft.dropdown.Option("Vanilla"),
                                       ft.dropdown.Option("Snapshot"),
                                       ft.dropdown.Option("Forge"),
                                       ft.dropdown.Option("Fabric"),
                                       ft.dropdown.Option("Fabric Snapshot"),
                                       ft.dropdown.Option("Quilt"),
                                       ft.dropdown.Option("Quilt Snapshot")],
                                      width=page.width/1.7,
                                      on_change=modify_versions)
    
    
    modifyInstancesVersion = ft.Dropdown(width=page.width/1.7,
                                         on_change=modify_versions_engines)
    
    
    modifyInstancesEngine = ft.Dropdown(width=page.width/1.7)
    
    
    modifyInstanceStartButton = ft.CupertinoFilledButton(LangHandeler.Modify_Instance_Change_Button,
                                                         ft.icons.CHANGE_CIRCLE,
                                                         width=page.width/1.7,
                                                         on_click=modify_version_start)
    
    
    modifyInstancesCardColumn = ft.Column([modifyInstancesInstance,
                                           ft.Text(LangHandeler.Modify_Instance_Name_Title, size=16),
                                           ft.Row([modifyInstancesName,
                                                   modifyInstancesChangeName],
                                                  alignment=ft.MainAxisAlignment.CENTER),
                                           ft.Text(LangHandeler.Modify_Instance_Type_Title, size=16),
                                           modifyInstancesType,
                                           ft.Text(LangHandeler.Modify_Instance_Version_Title, size=16),
                                           modifyInstancesVersion,
                                           ft.Text(LangHandeler.Modify_Instance_Engin_Version_Title, size=16),
                                           modifyInstancesEngine,
                                           modifyInstanceStartButton],
                                          scroll=ft.ScrollMode.AUTO,
                                          alignment=ft.MainAxisAlignment.CENTER,
                                          horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                          width=page.width/1.6,
                                          height=page.height/2.2)


    instancesCard = ft.Card(addInstanceCardColumn,
                            width=page.width/1.6,
                            height=page.height/2.2)


    instancesSelectDropdown = ft.Dropdown(LangHandeler.Default_Option,
                                    [ft.dropdown.Option(LangHandeler.Create_Instances_Title),
                                     ft.dropdown.Option(LangHandeler.Delete_Instances_Title),
                                     ft.dropdown.Option(LangHandeler.Modify_Instances_Title)],
                                    width=page.width/1.6,
                                    on_change=instancesPharagraph)


    instanceCardColumn = ft.Column([ft.Text(LangHandeler.Instances_Title, size=36),
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
        menus = {LangHandeler.Add_Accounts_Title: addAccountColumn,
                 LangHandeler.Delete_Accounts_Title: removeAccountColumn}
        accountsCard.clean()
        accountsCard.content = menus[menu.data]
        accountsCard.update()
            
            
    def update_account_displays(acc, accDel):
        updateAccounts(acc)
        updateRemoveAccounts(accDel)
            
            
    def start_account_creation(event=None):
        AccountHandeler.add_account(addAccountType.value,
                                     addAccountName.value,
                                     addAccountPassword.value,
                                     setStatus,
                                     setProgress,
                                     setMax)
        progressReset()
        update_account_displays(True, False)
    
    
    def start_account_delete(event=None):
        AccountHandeler.del_account(removeAccountDropdown.value,
                                    setStatus,
                                    setProgress,
                                    setMax)
        progressReset()
        update_account_displays(True, True)


    # -------------------------------
    # Account Variables
    # -------------------------------


    addAccountType = ft.Dropdown(LangHandeler.Default_Option,
                                 [ft.dropdown.Option("Premiun"),
                                  ft.dropdown.Option("No Premiun")],
                                 width=page.width/1.7)

    addAccountName = ft.TextField(width=page.width/1.7)


    addAccountPassword = ft.TextField(password=True,
                                      can_reveal_password=True,
                                      width=page.width/1.7)


    addAccountButton = ft.CupertinoFilledButton(LangHandeler.Add_Account_Button,
                                                icon=ft.icons.ACCOUNT_BOX,
                                                width=page.width/1.7,
                                                on_click=start_account_creation)


    addAccountColumn = ft.Column([addAccountType,
                                  ft.Text(LangHandeler.Add_Account_Name, size=16),
                                  addAccountName,
                                  ft.Text(LangHandeler.Add_Account_Password, size=16),
                                  addAccountPassword,
                                  addAccountButton],
                                 alignment=ft.MainAxisAlignment.CENTER,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 scroll=ft.ScrollMode.AUTO,
                                 width=page.width/1.6,
                                 height=page.height/2.2)


    removeAccountDropdown = ft.Dropdown(LangHandeler.Default_Option,
                                        [ft.dropdown.Option(account)
                                         for account in ConfigHandeler.Accounts],
                                        width=page.width/1.7)


    removeAccountButton = ft.CupertinoFilledButton(LangHandeler.Delete_Account_Button,
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


    accountDropdown = ft.Dropdown(LangHandeler.Add_Accounts_Title,
                                                 [ft.dropdown.Option(LangHandeler.Add_Accounts_Title),
                                                  ft.dropdown.Option(LangHandeler.Delete_Accounts_Title)],
                                                 on_change=accountsParagraph,
                                                 width=page.width/1.6)
    
    
    accountsCard = ft.Card(addAccountColumn,
                           width=page.width/1.6,
                           height=page.height/2.2)


    accountCardColumn = ft.Column([ft.Text(LangHandeler.Accounts_Title, size=36),
                                   accountDropdown,
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


    def run_game(event=None):
        if ConfigHandeler.CloseOnPlay:
            page.window.close()
        InstanceHandeler.run_instance(instancesDropdown.value,
                                       accountsDropdown.value)


    # -------------------------------
    # LaunchGame Variables
    # -------------------------------


    accountsDropdown = ft.Dropdown(width=page.width/3.4,
                                   on_change=ConfigHandeler.update_config_default_account)


    instancesDropdown = ft.Dropdown(width=page.width/3.4,
                                    on_change=ConfigHandeler.update_config_default_version)


    launchGameButton = ft.CupertinoFilledButton(LangHandeler.Play_Menu_Start_Game,
                                                icon=ft.icons.PLAY_ARROW_ROUNDED,
                                                width=page.width/3.4,
                                                on_click=run_game)


    launchGameCardColumn = ft.Column([ft.Text(LangHandeler.Play_Menu_Config_Account_Title, size=16),
                                     accountsDropdown,
                                     ft.Text(LangHandeler.Play_Menu_Select_Instance_Title, size=16),
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
    
    
    callback = {"setStatus": setStatus, "setProgress": setProgress, "setMax": setMax}
    
    
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


    progressBar = ft.ProgressBar(value=1,
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

    global Message
    def Message(msg):
        page.open(ft.AlertDialog(content=ft.Text(msg, size=16), open=True))


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


    def update_contents(event=None):
        topCardRow.height = page.height/12
        topCardRow.spacing = page.width/5

        menuCard.width = page.width/1.5
        menuCard.height = page.height/1.4

        infoColumn.width = page.width/1.7
        infoColumn.height = page.height/2
        infoCard.width = page.width/1.7
        infoCard.height = page.height/2
        infoDropdown.width = page.width/1.6
        infoCardColumn.width = page.width/1.5
        infoCardColumn.height = page.height/1.4

        configDropdown.width = page.width/1.6
        configCardColumn.width = page.width/1.5
        configCardColumn.height = page.height/1.4
        configCard.width = page.width/1.6
        configCard.height = page.height/2.2
        configDropdown.width = page.width/1.6

        normalConfigCardColumn.width = page.width/1.6
        normalConfigCardColumn.height = page.height/2.2
        languajeConfigDropdown.width = page.width/1.6
        themeConfigDropdown.width = page.width/1.6

        advancedConfigCardColumn.width = page.width/1.6
        advancedConfigCardColumn.height = page.height/2.2
        ramConfigSlider.width = page.width/2.35
        ramConfigRow.spacing = page.width/50
        minecraftDirectoryConfigTextField.width = page.width/2.4
        minecraftFirectoryConfigButton.width = page.width/5.5
        openFolderConfigCuppertinoFilledButton.width = page.width/1.6

        accountDropdown.width = page.width/1.6
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

        instancesSelectDropdown.width = page.width/1.6
        instanceCardColumn.width = page.width/1.5
        instanceCardColumn.height = page.height/1.4
        instancesDropdown.width = page.width/1.6
        instancesCard.width = page.width/1.6
        instancesCard.height = page.height/2.2

        addInstanceCardColumn.width = page.width/1.6
        addInstanceCardColumn.height = page.height/2.2
        addInstanceName.width = page.width/1.7
        addInstanceType.width = page.width/1.7
        addInstanceVersion.width = page.width/1.7
        addInstaceEngine.width = page.width/1.7
        addInstancesButton.width = page.width/1.7

        removeInstanceCardColumn.width = page.width/1.6
        removeInstanceCardColumn.height = page.height/2.2
        removeInstancesDropdown.width = page.width/1.7
        removeInstancesButton.width = page.width/1.7
        
        modifyInstancesCardColumn.width = page.width/1.6
        modifyInstancesCardColumn.width = page.width/2.2
        modifyInstancesInstance.width = page.width/1.7
        modifyInstancesName.width = page.width/2.4
        modifyInstancesChangeName.width = page.width/5.5
        modifyInstancesType.width = page.width/1.7
        modifyInstancesVersion.width = page.width/1.7
        modifyInstancesEngine.width = page.width/1.7
        modifyInstanceStartButton.width = page.width/1.7

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
        value, options = AccountHandeler.check_accounts()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)
        accountsDropdown.value, accountsDropdown.options = value, options

        if update:
            accountsDropdown.update()
    
    
    def updateRemoveAccounts(update):
        value, options = AccountHandeler.check_accounts()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)
        removeAccountDropdown.value, removeAccountDropdown.options = value, options
        
        if update:
            removeAccountDropdown.update()


    def updateInstances(update):
        value, options = InstanceHandeler.check_instances()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)
        
        instancesDropdown.value, instancesDropdown.options = value, options
        if update:
            instancesDropdown.update()
    
    
    def updateInstancesModify(update):
        value, options = InstanceHandeler.check_instances()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)

        modifyInstancesInstance.value, modifyInstancesInstance.options = value, options
        if update:
            modifyInstancesInstance.update()
    
    
    def updateRemoveInstances(update):
        value, options = InstanceHandeler.check_instances()
        for i, option in enumerate(options):
            options[i] = ft.dropdown.Option(option)

        removeInstancesDropdown.value, removeInstancesDropdown.options = value, options
        if update:
            removeInstancesDropdown.update()


    updateAccounts(False)
    updateRemoveAccounts(False)
    updateInstances(False)
    updateInstancesModify(False)
    updateRemoveInstances(False)
    modify_instance_name_updater()


    page.update()