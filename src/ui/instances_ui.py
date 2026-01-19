import flet as ft

from core import lang
from core import process

from services import instances

from ui import main_ui

# -------------------------------
# Instances Functions
# -------------------------------


def resize(event):
    instancesSelectDropdown.width = event.width/1.6
    instanceCardColumn.width = event.width/1.5
    instanceCardColumn.height = event.height/1.4
    instancesCard.width = event.width/1.6
    instancesCard.height = event.height/2.2

    addInstanceCardColumn.width = event.width/1.6
    addInstanceCardColumn.height = event.height/2.2
    addInstanceName.width = event.width/1.7
    addInstanceType.width = event.width/1.7
    addInstanceVersion.width = event.width/1.7
    addInstaceEngine.width = event.width/1.7
    addInstancesButton.width = event.width/1.7

    removeInstanceCardColumn.width = event.width/1.6
    removeInstanceCardColumn.height = event.height/2.2
    removeInstancesDropdown.width = event.width/1.7
    removeInstancesButton.width = event.width/1.7
    
    modifyInstancesCardColumn.width = event.width/1.6
    modifyInstancesCardColumn.width = event.width/2.2
    modifyInstancesInstance.width = event.width/1.7
    modifyInstancesName.width = event.width/2.4
    modifyInstancesChangeName.width = event.width/5.5
    modifyInstancesType.width = event.width/1.7
    modifyInstancesVersion.width = event.width/1.7
    modifyInstancesEngine.width = event.width/1.7
    modifyInstanceStartButton.width = event.width/1.7


def instancesPharagraph(menu):
    menus = {lang.Create_Instances_Title: addInstanceCardColumn,
                lang.Delete_Instances_Title: removeInstanceCardColumn,
                lang.Modify_Instances_Title: modifyInstancesCardColumn}
    instancesCard.content = menus[menu.data]
    instancesCard.update()


def update_versions(event=None):
    version, version_list = instances.check_versions(addInstanceType.value)
    for i, ver in enumerate(version_list):
        version_list[i] = ft.dropdown.Option(ver)
    addInstanceVersion.value, addInstanceVersion.options = version, version_list
    
    if event:
        addInstanceVersion.update()
    update_versions_engines(True)


def update_versions_engines(event=None):
    engine, engine_list = instances.check_engine_ver(addInstanceVersion.value, addInstanceType.value)
    for i, eng in enumerate(engine_list):
        engine_list[i] = ft.dropdown.Option(eng)
    addInstaceEngine.value, addInstaceEngine.options = engine, engine_list
    
    if event:
        addInstaceEngine.update()


def modify_versions(event=None):
    version, version_list = instances.check_versions(modifyInstancesType.value)
    for i, ver in enumerate(version_list):
        version_list[i] = ft.dropdown.Option(ver)
    modifyInstancesVersion.value, modifyInstancesVersion.options = version, version_list
    
    if event:
        modifyInstancesVersion.update()
    modify_versions_engines(True)


def modify_versions_engines(event=None):
    engine, engine_list = instances.check_engine_ver(modifyInstancesVersion.value, modifyInstancesType.value)
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
    process.add_process(instances.modify_instance,
                                modifyInstancesName.value,
                                modifyInstancesType.value,
                                modifyInstancesVersion.value,
                                modifyInstancesEngine.value)
    update_instances_displays(False, True, False)


def start_instance_install(event=None):
    process.add_process(instances.install_instance,
                                addInstanceName.value,
                                addInstanceType.value,
                                addInstanceVersion.value,
                                addInstaceEngine.value)
    update_instances_displays(True, False, False)


def start_instance_uninstall(event=None):
    process.add_process(instances.uninstall_instance,
                                removeInstancesDropdown.value)
    update_instances_displays(True, False, True)


def modify_instance_name_updater(event=None):
    if modifyInstancesInstance.value != lang.Without_Versions:
        modifyInstancesName.value = modifyInstancesInstance.value
        if event:
            modifyInstancesName.update()


def modify_instance_name(event=None):
    instances.update_instance_name(modifyInstancesInstance.value,
                                            modifyInstancesName.value)
    update_instances_displays(True, False, False)


def updateInstances(update):
    value, options = instances.check_instances()
    for i, option in enumerate(options):
        options[i] = ft.dropdown.Option(option)
    
    main_ui.instancesDropdown.value, main_ui.instancesDropdown.options = value, options
    if update:
        main_ui.instancesDropdown.update()


def updateInstancesModify(update):
    value, options = instances.check_instances()
    for i, option in enumerate(options):
        options[i] = ft.dropdown.Option(option)

    modifyInstancesInstance.value, modifyInstancesInstance.options = value, options
    if update:
        modifyInstancesInstance.update()


def updateRemoveInstances(update):
    value, options = instances.check_instances()
    for i, option in enumerate(options):
        options[i] = ft.dropdown.Option(option)

    removeInstancesDropdown.value, removeInstancesDropdown.options = value, options
    if update:
        removeInstancesDropdown.update()


# -------------------------------
# Instances Variables
# -------------------------------


addInstanceName = ft.TextField()


addInstanceType = ft.Dropdown(lang.Default_Option,
                                options=[ft.dropdown.Option("Vanilla"),
                                        ft.dropdown.Option("Snapshot"),
                                        ft.dropdown.Option("Forge"),
                                        ft.dropdown.Option("Fabric"),
                                        ft.dropdown.Option("Fabric Snapshot"),
                                        ft.dropdown.Option("Quilt"),
                                        ft.dropdown.Option("Quilt Snapshot")],
                                on_text_change=update_versions)


addInstanceVersion = ft.Dropdown(on_text_change=update_versions_engines)


addInstaceEngine = ft.Dropdown()


addInstancesButton = ft.CupertinoFilledButton(lang.Create_Instance_Install_Button,
                                                icon=ft.Icons.ADD_BOX,
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
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)


removeInstancesDropdown = ft.Dropdown(lang.Default_Option)


removeInstancesButton = ft.CupertinoFilledButton(lang.Delete_Instances_Button,
                                                    icon=ft.Icons.CANCEL,
                                                    on_click=start_instance_uninstall)


removeInstanceCardColumn = ft.Column([removeInstancesDropdown,
                                        removeInstancesButton],
                                        scroll=ft.ScrollMode.AUTO,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER)


modifyInstancesInstance = ft.Dropdown(on_text_change=modify_instance_name_updater)


modifyInstancesName = ft.TextField(text_size=16)


modifyInstancesChangeName = ft.CupertinoFilledButton(lang.Modify_Instances_Name_Button,
                                                        ft.Icons.EDIT,
                                                        on_click=modify_instance_name)


modifyInstancesType = ft.Dropdown(lang.Default_Option,
                                    options=[ft.dropdown.Option("Vanilla"),
                                            ft.dropdown.Option("Snapshot"),
                                            ft.dropdown.Option("Forge"),
                                            ft.dropdown.Option("Fabric"),
                                            ft.dropdown.Option("Fabric Snapshot"),
                                            ft.dropdown.Option("Quilt"),
                                            ft.dropdown.Option("Quilt Snapshot")],
                                    on_text_change=modify_versions)


modifyInstancesVersion = ft.Dropdown(on_text_change=modify_versions_engines)


modifyInstancesEngine = ft.Dropdown()


modifyInstanceStartButton = ft.CupertinoFilledButton(lang.Modify_Instance_Change_Button,
                                                        ft.Icons.CHANGE_CIRCLE,
                                                        on_click=modify_version_start)


modifyInstancesCardColumn = ft.Column([modifyInstancesInstance,
                                        ft.Text(lang.Modify_Instance_Name_Title, size=16),
                                        ft.Row([modifyInstancesName,
                                                modifyInstancesChangeName],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Text(lang.Modify_Instance_Type_Title, size=16),
                                        modifyInstancesType,
                                        ft.Text(lang.Modify_Instance_Version_Title, size=16),
                                        modifyInstancesVersion,
                                        ft.Text(lang.Modify_Instance_Engin_Version_Title, size=16),
                                        modifyInstancesEngine,
                                        modifyInstanceStartButton],
                                        scroll=ft.ScrollMode.AUTO,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER)


instancesCard = ft.Card(addInstanceCardColumn)


instancesSelectDropdown = ft.Dropdown(lang.Default_Option,
                                        options=[ft.dropdown.Option(lang.Create_Instances_Title),
                                                ft.dropdown.Option(lang.Delete_Instances_Title),
                                                ft.dropdown.Option(lang.Modify_Instances_Title)],
                                        on_text_change=instancesPharagraph)


instanceCardColumn = ft.Column([ft.Text(lang.Instances_Title, size=36),
                                instancesSelectDropdown,
                                instancesCard],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
