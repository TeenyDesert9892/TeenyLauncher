import flet as ft

from core import lang
from core import config

from services import instances

from ui import info_ui
from ui import accounts_ui
from ui import instances_ui
from ui import config_ui


# -------------------------------
# Page Pre-Configuration
# -------------------------------

page = None

backgroundImages = {"Dark": '/assets/images/bg-dark.png',
                    "Light": '/assets/images/bg-light.png'}


bgImg = ft.BoxDecoration(image=ft.DecorationImage(config.get_assets_path()+backgroundImages[config.Theme],
                                                    fit=ft.BoxFit.COVER))

 # -------------------------------
# Top Change Function
# -------------------------------


def changeMenu(menu):
    menus = {"HOME": info_ui.infoCardColumn,
                "ACCOUNTS": accounts_ui.accountCardColumn,
                "INSTANCES": instances_ui.instanceCardColumn,
                "SETTINGS": config_ui.configCardColumn}
    menuCard.content = menus[menu]
    menuCard.update()
    


# -------------------------------
# Top Buttons
# -------------------------------


topCardRow = ft.Row([ft.IconButton(icon=ft.Icons.HOME,
                                    icon_size=30,
                                    on_click=lambda event: changeMenu("HOME")),
                        ft.IconButton(icon=ft.Icons.ACCOUNT_BOX,
                                    icon_size=30,
                                    on_click=lambda event: changeMenu("ACCOUNTS")),
                        ft.IconButton(icon=ft.Icons.FOLDER,
                                    icon_size=30,
                                    on_click=lambda event: changeMenu("INSTANCES")),
                        ft.IconButton(icon=ft.Icons.SETTINGS,
                                    icon_size=30,
                                    on_click=lambda event: changeMenu("SETTINGS"))],
                    alignment=ft.MainAxisAlignment.CENTER)


# -------------------------------
# Menu Card
# -------------------------------


menuCard = ft.Card(info_ui.infoCardColumn)


# -------------------------------
# LaunchGame Functions
# -------------------------------


def run_game(event=None):
    if config.CloseOnPlay:
        page.window.close()
    instances.run_instance(instancesDropdown.value,
                                    accountsDropdown.value)


# -------------------------------
# LaunchGame Variables
# -------------------------------


accountsDropdown = ft.Dropdown(on_text_change=config.update_config_default_account)


instancesDropdown = ft.Dropdown(on_text_change=config.update_config_default_version)


launchGameButton = ft.CupertinoFilledButton(lang.Play_Menu_Start_Game,
                                            icon=ft.Icons.PLAY_ARROW_ROUNDED,
                                            on_click=run_game)


launchGameCardColumn = ft.Column([ft.Text(lang.Play_Menu_Config_Account_Title, size=16),
                                    accountsDropdown,
                                    ft.Text(lang.Play_Menu_Select_Instance_Title, size=16),
                                    instancesDropdown,
                                    launchGameButton],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)


launchGameCard = ft.Card(launchGameCardColumn)


# -------------------------------
# ProgressBar Functions
# -------------------------------


class Callback:
    def __init__(self): 
        self.maxProgress = 0
        
        
    def setStatus(self, status: str):
        try:
            progressBarMessage.value = status
            progressBarRow.update()
        except:
            pass


    def setProgress(self, progress: int):
        try:
            progressBarPercentage.value = str(progress)+'/'+str(self.maxProgress)
            progressBar.value = progress/self.maxProgress
            progressBarRow.update()
        except:
            pass


    def setMax(self, max: int):
        try:
            self.maxProgress = max
            progressBarRow.update()
        except:
            pass
    
    
    def progressReset(self):
        global current_max_progress
        progressBarMessage.value = "No tasks running"
        progressBarPercentage.value = "0/0"
        progressBar.value = 1
        current_max_progress = 0
        progressBarRow.update()


callback = Callback()


# -------------------------------
# ProgressBar Variables
# -------------------------------


progressBarMessage = ft.Text("No tasks running",
                                text_align=ft.TextAlign.CENTER)


progressBar = ft.ProgressBar(value=1)


progressBarPercentage = ft.Text("0/0",
                                text_align=ft.TextAlign.CENTER)

progressBarRow = ft.Row([progressBarMessage,
                            progressBar,
                            progressBarPercentage],
                        alignment=ft.MainAxisAlignment.CENTER)


# -------------------------------
# Page Message
# -------------------------------

def Message(msg: str):
    page.show_dialog(ft.AlertDialog(title=ft.Text("Message:", size=24), content=ft.Text(msg, size=16)))


# -------------------------------
# Page Updates
# -------------------------------


def update_contents(evnet):
    topCardRow.height = evnet.height/12
    topCardRow.spacing = evnet.width/5

    menuCard.width = evnet.width/1.5
    menuCard.height = evnet.height/1.4
    
    info_ui.resize(evnet)
    
    accounts_ui.resize(evnet)

    instances_ui.resize(evnet)
    
    config_ui.resize(evnet)

    launchGameCard.width = evnet.width/3.25
    launchGameCard.height = evnet.height/1.4

    launchGameCardColumn.width = evnet.width/3.25
    launchGameCardColumn.height = evnet.height/1.4
    accountsDropdown.width = evnet.width/3.4
    instancesDropdown.width = evnet.width/3.4
    launchGameButton.width = evnet.width/3.4

    progressBarRow.height = evnet.height/10
    progressBar.width = evnet.width/2
    page.update()


# -------------------------------
# StartUp Page
# -------------------------------

def main(main_page: ft.Page):
    main_page.title = "TeenyLauncher"
    main_page.window.width = 800
    main_page.window.height = 600
    main_page.window.min_width = 700
    main_page.window.min_height = 550
    main_page.vertical_alignment = ft.MainAxisAlignment.CENTER
    main_page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    main_page.decoration = bgImg
    
    global page
    page = main_page
    
    if config.EnabledBgImg:
        main_page.bgcolor = ft.Colors.TRANSPARENT
    main_page.theme_mode = ft.ThemeMode.DARK  if config.Theme.lower() == "dark" else ft.ThemeMode.LIGHT


    main_page.add(ft.Card(topCardRow),
             ft.Row([menuCard,
                     launchGameCard],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER),
             ft.Card(progressBarRow))


    main_page.on_resize = update_contents


    accounts_ui.updateAccounts(False)
    accounts_ui.updateRemoveAccounts(False)
    
    instances_ui.updateInstances(False)
    instances_ui.updateInstancesModify(False)
    instances_ui.updateRemoveInstances(False)
    instances_ui.modify_instance_name_updater()


    main_page.update()