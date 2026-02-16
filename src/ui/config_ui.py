from minecraft_launcher_lib import utils
import flet as ft

import os

from core import config
from core import lang

from services import instances

from utils import utils

from ui import main_ui

# -------------------------------
# Config Functions
# -------------------------------


def resize(event):
    configDropdown.width = event.width/1.6
    configCardColumn.width = event.width/1.5
    configCardColumn.height = event.height/1.4
    configCard.width = event.width/1.6
    configCard.height = event.height/2.2
    configDropdown.width = event.width/1.6

    normalConfigCardColumn.width = event.width/1.6
    normalConfigCardColumn.height = event.height/2.2
    languajeConfigDropdown.width = event.width/1.6
    themeConfigDropdown.width = event.width/1.6

    advancedConfigCardColumn.width = event.width/1.6
    advancedConfigCardColumn.height = event.height/2.2
    ramConfigSlider.width = event.width/2.35
    ramConfigRow.spacing = event.width/50
    minecraftDirectoryConfigTextField.width = event.width/2.4
    minecraftFirectoryConfigButton.width = event.width/5.5
    openFolderConfigCuppertinoFilledButton.width = event.width/1.6


def configPharagraph(menu):
    menus = {lang.Launcher_Config_Title: normalConfigCardColumn,
                lang.Advanced_Config_Title: advancedConfigCardColumn}
    configCard.content = menus[menu.data]
    configCard.update()


def langChange(dropdown):
    config.update_config_lang(dropdown.data)
    main_ui.Message("To apply the languaje changes you need to restart the launcher")


def themeChange(dropdown):
    config.update_config_theme(dropdown.data)
    main_ui.bgImg.image = ft.DecorationImage(utils.get_assets_path()+main_ui.backgroundImages[dropdown.data],
                                        fit=ft.BoxFit.COVER)
    main_ui.page.theme_mode = ft.ThemeMode.DARK  if dropdown.data.lower() == "dark" else ft.ThemeMode.LIGHT
    main_ui.page.update()


def imageChange(checkBox):
    if checkBox.data == "true":
        main_ui.page.bgcolor = ft.Colors.TRANSPARENT
        config.settings.EnabledBgImg = True
    else:
        main_ui.page.bgcolor = ft.Colors.GREY
        config.settings.EnabledBgImg = False
    main_ui.page.update()


def closeOnPlayChange(checkBox):
    if checkBox.data == "true":
        config.settings.CloseOnPlay = True
    else:
        config.settings.CloseOnPlay = False
    main_ui.page.update()


def ramTextValueEdit(event=None):
    ramConfigShow.value = str(int(ramConfigSlider.value))+'MB'
    config.update_config_ram(ramConfigSlider.value)
    ramConfigShow.update()


def addRam(event=None):
    if ramConfigSlider.value < utils.get_ram():
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


languajeConfigDropdown = ft.Dropdown(lang.Default_Option,
                                        options=[ft.dropdown.Option(option.name.replace(".json", ""))
                                                for option in os.scandir(utils.get_assets_path()+'/lang')
                                                if option.name != "Example.json"],
                                        on_text_change=langChange)


themeConfigDropdown = ft.Dropdown(lang.Default_Option,
                                    options=[ft.dropdown.Option("Light"),
                                            ft.dropdown.Option("Dark")],
                                    on_text_change=themeChange)


normalConfigCardColumn = ft.Column([ft.Text(lang.Launcher_Config_Title, size=36),
                                    ft.Text(lang.Launcher_Config_Lang_Title, size=16),
                                    languajeConfigDropdown,
                                    ft.Text(lang.Launcher_Config_Theme_Title, size=16),
                                    themeConfigDropdown,
                                    ft.Switch(lang.Launcher_Config_Img, value=config.settings.EnabledBgImg, on_change=imageChange),
                                    ft.Switch(lang.Launcher_Config_On_Close, value=config.settings.CloseOnPlay, on_change=closeOnPlayChange)],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    scroll=ft.ScrollMode.AUTO)


ramConfigSlider = ft.Slider(value=config.settings.RamAmount,
                            min=128,
                            max=utils.get_ram(),
                            divisions=int(utils.get_ram()/32)-4,
                            on_change=ramTextValueEdit,
                            on_change_start=ramTextValueEdit,
                            on_change_end=ramTextValueEdit)


ramConfigShow = ft.Text(str(config.settings.RamAmount)+'MB', size=12)


ramConfigRow = ft.Row([ramConfigSlider,
                        ft.Row([ft.IconButton(ft.Icons.REMOVE, on_click=removeRam),
                                ramConfigShow,
                                ft.IconButton(ft.Icons.ADD, on_click=addRam)])],
                        alignment=ft.MainAxisAlignment.CENTER)


minecraftDirectoryConfigTextField = ft.TextField(config.settings.Minecraft_Dir)


minecraftFirectoryConfigButton = ft.CupertinoFilledButton(lang.Advanced_Config_Minecraft_Directory,
                                                            on_click=lambda event: config.update_config_dir(minecraftDirectoryConfigTextField.value))


openFolderConfigCuppertinoFilledButton = ft.CupertinoFilledButton(lang.Advanced_Config_Open_Versions_Folder,
                                                                    ft.Icons.FOLDER,
                                                                    on_click=instances.open_instances_folder)


advancedConfigCardColumn = ft.Column([ft.Text(lang.Advanced_Config_Title, size=36),
                                        ft.Text(lang.Advanced_Config_Ram_Title, size=16),
                                        ramConfigRow,
                                        ft.Text(lang.Advanced_Config_Folder_Title, size=16),
                                        ft.Row([minecraftDirectoryConfigTextField,
                                                minecraftFirectoryConfigButton],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                        openFolderConfigCuppertinoFilledButton],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        scroll=ft.ScrollMode.AUTO)


configCard = ft.Card(normalConfigCardColumn)


configDropdown = ft.Dropdown(lang.Default_Option,
                                options=[ft.dropdown.Option(lang.Launcher_Config_Title),
                                        ft.dropdown.Option(lang.Advanced_Config_Title)],
                                on_text_change=configPharagraph)


configCardColumn = ft.Column([ft.Text(lang.Config_Title, size=36),
                                configDropdown,
                                configCard],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER)