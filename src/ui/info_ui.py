import flet as ft

import os

from core import config
from core import lang

# -------------------------------
# Info Version changelog function
# -------------------------------

def resize(event):
    infoColumn.width = event.width/1.7
    infoColumn.height = event.height/2.5
    infoCard.width = event.width/1.7
    infoCard.height = event.height/2.5
    infoDropdown.width = event.width/1.6
    infoCardColumn.width = event.width/1.5
    infoCardColumn.height = event.height/1.4


def change_info(event):
    for file in os.scandir(config.get_assets_path()+'/changelog'):
        if file.name.replace('.txt', '') ==  event.data:
            infoVersionText.value = open(file.path, 'r', encoding='utf-8').read()
    infoVersionText.update()


# -------------------------------
# Info Variables
# -------------------------------


infoTextTitle = ft.Text('TeenyLauncher '+config.Version, size=48)


infoDropdown = ft.Dropdown(lang.Default_Option,
                            options=[ft.dropdown.Option(file.name.replace('.txt', ''))
                                    for file in os.scandir(config.get_assets_path()+'/changelog')],
                            on_text_change=change_info)


infoVersionText = ft.Text(open(config.get_assets_path()+'/changelog/V'+config.Version+'.txt', 'r').read())


infoColumn = ft.Column([infoVersionText],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.ALWAYS)


infoCard = ft.Card(infoColumn)


infoCardColumn = ft.Column([infoTextTitle, infoDropdown, infoCard],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER)