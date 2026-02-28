import json
import minecraft_launcher_lib as mcll

import os
import shutil
import subprocess

from ui import main_ui

from core import config
from core import lang

from utils import jdk
    
def saveInstance(name, type, ver, jar):
    with open(config.settings.Minecraft_Dir+'/'+name+'/instance_data.json', 'w') as file:
        json.dump({'Name': name, 'Type': type, 'Ver': ver, 'Jar': jar}, file, indent=4)
        file.close()


def do_install(name, type, ver, mod):
    main_ui.callback.setMax(1)
    main_ui.callback.setProgress(0)
    main_ui.callback.setStatus("Installing java...")
    java = jdk.get_jdk_client(float(ver.replace(".", "", 1)))
    main_ui.callback.setProgress(1)
    
    if type == "Vanilla" or type == "Snapshot":
        try:
            mcll.install.install_minecraft_version(
                versionid=ver,
                minecraft_directory=config.settings.Minecraft_Dir+'/'+name,
                callback=mcll.types.CallbackDict(
                    setStatus = main_ui.callback.setStatus,
                    setProgress = main_ui.callback.setProgress,
                    setMax = main_ui.callback.setMax
                )
            )
            
            saveInstance(name, type, ver, ver)
            main_ui.Message(lang.Create_Instance_Success)

        except Exception as e:
            shutil.rmtree(config.settings.Minecraft_Dir+'\\'+name)
            main_ui.Message(lang.Create_Instance_Failure+"\n\n Error: "+str(e))
    
    elif type == "Forge" or type == "NeoForge":
        try:
            installation = mcll.mod_loader.get_mod_loader(type.lower())
            installation.install(
                minecraft_version=ver,
                loader_version=mod,
                minecraft_directory=config.settings.Minecraft_Dir+'/'+name,
                java=java,
                callback=mcll.types.CallbackDict(
                    setStatus = main_ui.callback.setStatus,
                    setProgress = main_ui.callback.setProgress,
                    setMax = main_ui.callback.setMax
                )
            )
                            

            saveInstance(name, type, ver, mod.replace("-", f"-{type.lower()}-", 1))
            main_ui.Message(lang.Create_Instance_Success)

        except Exception as e:
            shutil.rmtree(config.settings.Minecraft_Dir+'\\'+name)
            main_ui.Message(lang.Create_Instance_Failure+"\n\n Error: "+str(e))
        
    elif type == "Fabric" or type == "Quilt":
        try:
            installation = mcll.mod_loader.get_mod_loader(type.lower())
            installation.install(
                minecraft_version=ver,
                loader_version=mod,
                minecraft_directory=config.settings.Minecraft_Dir+'/'+name,
                java=java,
                callback=mcll.types.CallbackDict(
                    setStatus = main_ui.callback.setStatus,
                    setProgress = main_ui.callback.setProgress,
                    setMax = main_ui.callback.setMax
                )
            )
            
            saveInstance(name, type, ver, f"{type.lower()}-loader-{mod}-{ver}")
            main_ui.Message(lang.Create_Instance_Success)

        except Exception as e:
            shutil.rmtree(config.settings.Minecraft_Dir+'\\'+name)
            main_ui.Message(lang.Create_Instance_Failure+"\n\n Error: "+str(e))
            
    else:
        pass


def install_instance(name, type, ver, mod):
    for instance in os.scandir(config.settings.Minecraft_Dir):
        if instance.name == name:
            main_ui.Message(lang.Install_Version_Already_Exsists)

    if name == "":
        main_ui.Message(lang.Install_Version_Without_Name)
        return
    
    if type == "":
        main_ui.Message(lang.Install_Version_Type_Not_Selected)
        return

    if ver == "":
        main_ui.Message(lang.Install_Version_Not_Selected)
        return

    return do_install(name, type, ver, mod)


def get_instance_data(name):
    with open(config.settings.Minecraft_Dir+'/'+name+'/instance_data.json', 'r') as file:
        fileData = json.load(file)
        file.close()
        
    return fileData


def update_instance_name(oldName, name):
    os.rename(config.settings.Minecraft_Dir+'/'+oldName, config.settings.Minecraft_Dir+'/'+name)


def modify_instance(name, type, ver, mod):
    for version in os.scandir(config.settings.Minecraft_Dir+'/'+name+'/versions'):
        shutil.rmtree(config.settings.Minecraft_Dir+'/'+name+'/versions/'+version.name)
    
    return do_install(name, type, ver, mod)


def uninstall_instance(versionName):
    try:
        main_ui.callback.setMax(1)
        main_ui.callback.setProgress(0)
        main_ui.callback.setStatus("Uninstalling instance: "+versionName)
        
        shutil.rmtree(config.settings.Minecraft_Dir+'/'+versionName)

        main_ui.callback.setProgress(1)
        main_ui.Message(lang.Delete_Instance_Success)
    except Exception as e:
        main_ui.Message(lang.Delete_Instance_Failure)


def check_instance_folders():
    installed_version_list = []
        
    for folder in os.scandir(config.settings.Minecraft_Dir):
        if folder.is_dir():
            for file in os.scandir(config.settings.Minecraft_Dir+'/'+folder.name):
                    if file.name == 'instance_data.json':
                        installed_version_list.append(folder.name)
    
    return installed_version_list


def check_instances():
    versions = ""
    installed_version_list = check_instance_folders()
    
    if len(installed_version_list) != 0:
        if config.settings.DefaultInstance == "" or config.settings.DefaultInstance == lang.Without_Versions:
            config.DefaultInstance = installed_version_list[0]
        is_installed = False

        for installed_version in installed_version_list:
            if config.settings.DefaultInstance == installed_version:
                is_installed = True

        if not is_installed:
            config.settings.DefaultInstance = installed_version_list[0]
        versions = config.settings.DefaultInstance

    elif len(installed_version_list) == 0:
        versions = lang.Without_Versions
        installed_version_list.append(lang.Without_Versions)

    return versions, installed_version_list


def check_versions(type: str, version: str):
    if type == "Vanilla":
        versions = [ver["id"] for ver in mcll.utils.get_version_list() if ver["type"] == "release"]
        first_ver = versions[0]
        
    elif type == "Snapshot":
        versions = [ver["id"] for ver in mcll.utils.get_version_list() if ver["type"] == "snapshot"]
        first_ver = versions[0]
        
    elif type in ["Forge", "NeoForge", "Fabric", "Quilt"]:
        mod_loader = mcll.mod_loader.get_mod_loader(type.lower())
        versions = mod_loader.get_loader_versions(version, False)
        first_ver = versions[0]
        
    else:
        first_ver = ""
        versions = []
        
    
    return first_ver, versions


def check_engine_ver(type: str):   
    try: mod_loader = mcll.mod_loader.get_mod_loader(type.lower())
    except Exception as e: mod_loader = ""
    
    if mod_loader != "":
        engines = mod_loader.get_minecraft_versions(False)
        first_engine = engines[0]
        
    else:
        first_engine = ""
        engines = []
    
    return first_engine, engines


def run_instance(versionName, username):
            
    if username == lang.Without_Accounts:
        main_ui.Message(lang.Without_Accounts_To_Play)
        return
    
    if versionName == lang.Without_Versions:
        main_ui.Message(lang.Without_Versions_To_Play)
        return
    
    config.save_config()

    options = mcll.types.MinecraftOptions()
    
    options['username'] = username
    options['uuid'] = config.settings.Accounts[username]["Uuid"]
    options['token'] = config.settings.Accounts[username]["Token"]
    options['jvmArguments'] = ['-Xmx'+str(config.settings.RamAmount)+'M']
    options['launcherVersion'] = config.Version
    
    instanceData = get_instance_data(versionName)

    minecraft_command = mcll.command.get_minecraft_command(instanceData['Jar'], config.settings.Minecraft_Dir+'/'+versionName, options)
    
    try:
        if os.name == "nt":
            minecraft_command[0] = os.path.normpath(jdk.get_jdk_client(float(instanceData['Ver'].replace(".", "", 1)))+"/bin/java.exe")
            
        else:
            minecraft_command[0] = os.path.normpath(jdk.get_jdk_client(float(instanceData['Ver'].replace(".", "", 1))) + "/bin/java")
            
    except Exception as e:
        main_ui.Message(lang.Incompatible_JDK+"\n\n Error: "+str(e))
        return
    
    subprocess.run(minecraft_command)


def open_instances_folder(e=None):
    if os.name == "nt":
        os.startfile(config.settings.Minecraft_Dir)
        
    elif os.name == "posix":
        os.system('xdg-open '+config.settings.Minecraft_Dir)
