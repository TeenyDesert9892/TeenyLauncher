import flet as ft
import minecraft_launcher_lib as mcll

from core import lang
from core import process

from services import instances

from ui import main_ui

# -------------------------------
# Instances Functions
# -------------------------------

# Resize the elements from the instances ui
def resize(event):
    instancesSelectDropdown.width = event.width/1.6
    instanceCardColumn.width = event.width/1.5
    instanceCardColumn.height = event.height/1.4
    instancesCard.width = event.width/1.6
    instancesCard.height = event.height/2.2

    addInstanceCardColumn.width = event.width/1.6
    addInstanceCardColumn.height = event.height/2.2
    addInstanceName.width = event.width/3.4
    addInstanceType.width = event.width/3.4
    addInstanceVersion.width = event.width/3.4
    addInstaceEngine.width = event.width/3.4
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

# The selector for the option to poform
def instancesPharagraph(menu):
    menus = {
        lang.Create_Instances_Title: addInstanceCardColumn,
        lang.Delete_Instances_Title: removeInstanceCardColumn,
        lang.Modify_Instances_Title: modifyInstancesCardColumn
    }
    
    instancesCard.content = menus[menu.data]
    instancesCard.update()

# Updates the dropdown versions fwom the install ui
def update_versions(event=None):
    version, version_list = instances.check_versions(addInstanceType.value, addInstanceVersion.value)
    
    version_list = [ft.dropdown.Option(opt) for opt in version_list]
    
    addInstanceVersion.value, addInstanceVersion.options = version, version_list
    
    if event:
        addInstanceVersion.update()
    update_versions_engines(True)

# Updates the dropdown engines from the install ui
def update_versions_engines(event=None):
    engine, engine_list = instances.check_engine_ver(addInstanceType.value)
    
    engine_list = [ft.dropdown.Option(opt) for opt in engine_list]
    
    addInstaceEngine.value, addInstaceEngine.options = engine, engine_list
    
    if event:
        addInstaceEngine.update()

# Updates the dropdown versions from the modify ui
def modify_versions(event=None):
    version, version_list = instances.check_versions(modifyInstancesType.value)
    
    version_list = [ft.dropdown.Option(opt) for opt in version_list]
    
    modifyInstancesVersion.value, modifyInstancesVersion.options = version, version_list
    
    if event:
        modifyInstancesVersion.update()
    modify_versions_engines(True)

# Updates the dropdown engines from the modify ui
def modify_versions_engines(event=None):
    engine, engine_list = instances.check_engine_ver(modifyInstancesType.value)
    
    engine_list = [ft.dropdown.Option(opt) for opt in engine_list]
    
    modifyInstancesEngine.value, modifyInstancesEngine.options = engine, engine_list
    
    if event:
        modifyInstancesEngine.update()

# Selector to update the necesary ui instaces dropdowns
def update_instances_displays(ins, modIns, remIns):
    updateInstances(ins)
    updateInstancesModify(modIns)
    updateRemoveInstances(remIns)

# Starts the instance modification process
def modify_version_start(event=None):
    process.add_process(instances.modify_instance,
                                modifyInstancesName.value,
                                modifyInstancesType.value,
                                modifyInstancesVersion.value,
                                modifyInstancesEngine.value)
    update_instances_displays(False, True, False)

# Starts the  installation of an instance
def start_instance_install(event=None):
    process.add_process(instances.install_instance,
                                addInstanceName.value,
                                addInstanceType.value,
                                addInstanceVersion.value,
                                addInstaceEngine.value)
    update_instances_displays(True, False, False)

# Starts the uninstallation of an instance
def start_instance_uninstall(event=None):
    process.add_process(instances.uninstall_instance,
                                removeInstancesDropdown.value)
    update_instances_displays(True, False, True)

# Updates the name of an instance name in the modify ui when changed
def modify_instance_name_updater(event=None):
    if modifyInstancesInstance.value != lang.Without_Versions:
        modifyInstancesName.value = modifyInstancesInstance.value
        if event:
            modifyInstancesName.update()

# Updates the name of an instance in the ui's
def modify_instance_name(event=None):
    instances.update_instance_name(modifyInstancesInstance.value,
                                    modifyInstancesName.value)
    update_instances_displays(True, False, False)

# Updates the instances dropdown from the main ui
def updateInstances(update):
    value, options = instances.check_instances()
    options = [ft.dropdown.Option(option) for option in options]
    
    main_ui.instancesDropdown.value, main_ui.instancesDropdown.options = value, options
    
    if update:
        main_ui.instancesDropdown.update()

# Updates the instances dropdown from the modify ui
def updateInstancesModify(update):
    value, options = instances.check_instances()
    options = [ft.dropdown.Option(option) for option in options]

    modifyInstancesInstance.value, modifyInstancesInstance.options = value, options
    
    if update:
        modifyInstancesInstance.update()

# Updates the instances dropdown from the remove ui
def updateRemoveInstances(update):
    value, options = instances.check_instances()
    options = [ft.dropdown.Option(option) for option in options]

    removeInstancesDropdown.value, removeInstancesDropdown.options = value, options
    
    if update:
        removeInstancesDropdown.update()


# -------------------------------
# Instances Variables
# -------------------------------


addInstanceName = ft.TextField(label=lang.Create_Instance_Name_Title)


addInstanceType = ft.Dropdown(
    lang.Default_Option,
    label=lang.Create_Instance_Type_Title,
    options=[ft.dropdown.Option("Vanilla"),
        ft.dropdown.Option("Snapshot"),
        ft.dropdown.Option("Forge"),
        ft.dropdown.Option("NeoForge"),
        ft.dropdown.Option("Fabric"),
        ft.dropdown.Option("Quilt")
    ],
    on_text_change=update_versions
)


addInstanceVersion = ft.Dropdown(
    label=lang.Create_Instance_Version_Title,
    on_text_change=update_versions_engines,
    
    options=[ft.dropdown.Option(opt["id"])
             for opt in mcll.utils.get_version_list()
             if opt["type"] == "release"]
)


addInstaceEngine = ft.Dropdown(
    label=lang.Create_Instance_Engin_Version_Title
)


addInstancesButton = ft.CupertinoFilledButton(
    lang.Create_Instance_Install_Button,
    icon=ft.Icons.ADD_BOX,
    on_click=start_instance_install
)


removeInstancesDropdown = ft.Dropdown(
    lang.Default_Option
)


removeInstancesButton = ft.CupertinoFilledButton(
    lang.Delete_Instances_Button,
    icon=ft.Icons.CANCEL,
    on_click=start_instance_uninstall
)


removeInstanceCardColumn = ft.Column(
    [
        removeInstancesDropdown,
        removeInstancesButton
    ],                        
    scroll=ft.ScrollMode.AUTO,                            
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER)


modifyInstancesInstance = ft.Dropdown(
    on_text_change=modify_instance_name_updater
)


modifyInstancesName = ft.TextField(
    text_size=16
)


modifyInstancesChangeName = ft.CupertinoFilledButton(
    lang.Modify_Instances_Name_Button,
    ft.Icons.EDIT,
    on_click=modify_instance_name
)


modifyInstancesType = ft.Dropdown(
    lang.Default_Option,
    options=[ft.dropdown.Option("Vanilla"),
        ft.dropdown.Option("Snapshot"),
        ft.dropdown.Option("Forge"),
        ft.dropdown.Option("Fabric"),
        ft.dropdown.Option("Fabric Snapshot"),
        ft.dropdown.Option("Quilt"),
        ft.dropdown.Option("Quilt Snapshot")],
    on_text_change=modify_versions)


modifyInstancesVersion = ft.Dropdown(
    on_text_change=modify_versions_engines
)


modifyInstancesEngine = ft.Dropdown()


modifyInstanceStartButton = ft.CupertinoFilledButton(
    lang.Modify_Instance_Change_Button,
    ft.Icons.CHANGE_CIRCLE,
    on_click=modify_version_start
)


modifyInstancesCardColumn = ft.Column(
    [
        modifyInstancesInstance,
        ft.Text(lang.Modify_Instance_Name_Title, size=16),
        ft.Row([
            modifyInstancesName,
            modifyInstancesChangeName
        ],
        alignment=ft.MainAxisAlignment.CENTER),
        ft.Text(
            lang.Modify_Instance_Type_Title,
            size=16
        ),
        modifyInstancesType,
        ft.Text(
            lang.Modify_Instance_Version_Title,
            size=16
        ),
        modifyInstancesVersion,
        ft.Text(
            lang.Modify_Instance_Engin_Version_Title,
            size=16
        ),
        modifyInstancesEngine,
        modifyInstanceStartButton],
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)


addInstanceCardColumn = ft.Column(
    [
        ft.Row([
            addInstanceName,
            addInstaceEngine
        ]),
        ft.Row([
            addInstanceType,
            addInstanceVersion
        ]),
        addInstancesButton
    ],
    scroll=ft.ScrollMode.AUTO,
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)


instancesCard = ft.Card(
    addInstanceCardColumn
)


instancesSelectDropdown = ft.Dropdown(
    lang.Default_Option,
    options=[
        ft.dropdown.Option(lang.Create_Instances_Title),
        ft.dropdown.Option(lang.Delete_Instances_Title),
        ft.dropdown.Option(lang.Modify_Instances_Title)],
    on_text_change=instancesPharagraph
)


instanceCardColumn = ft.Column(
    [
        ft.Text(lang.Instances_Title, size=36),
        instancesSelectDropdown,
        instancesCard
    ],
    scroll=ft.ScrollMode.AUTO,
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)
