import minecraft_launcher_lib as mllb

import os
import pickle
import shutil
import subprocess

from ui import main_ui

from core import config
from core import lang

from utils import jdk
    
def saveInstance(name, type, ver, jar):
    with open(config.Minecraft_Dir+'/'+name+'/instance_data.pkl', 'wb') as file:
        pickle.dump({'Name': name, 'Type': type, 'Ver': ver, 'Jar': jar}, file)
        file.close()


def do_install(name, type, ver, mod, callback):
    callback.setMax(1)
    callback.setProgress(0)
    callback.setStatus("Installing java...")
    java = jdk.get_jdk_client(float(ver.replace(".", "", 1)))
    callback.setProgress(1)
    
    if type == "Vanilla" or type == "Snapshot":
        try:
            mllb.install.install_minecraft_version(versionid=ver,
                                                    minecraft_directory=config.Minecraft_Dir+'/'+name,
                                                    callback={'setStatus': callback.setStatus,
                                                                'setProgress': callback.setProgress,
                                                                'setMax': callback.setMax})
            
            saveInstance(name, type, ver, ver)
            main_ui.Message(lang.Create_Instance_Success)

        except Exception as e:
            shutil.rmtree(config.Minecraft_Dir+'/'+name)
            main_ui.Message(lang.Create_Instance_Failure+"\n\n Error: "+str(e))
            

    elif type == "Forge":
        try:
            mllb.forge.install_forge_version(versionid=mod,
                                                path=config.Minecraft_Dir+'/'+name,
                                                java=java,
                                                callback={'setStatus': callback.setStatus,
                                                        'setProgress': callback.setProgress,
                                                        'setMax': callback.setMax})
            
            saveInstance(name, type, ver, mod.replace("-", "-forge-", 1))

            main_ui.Message(lang.Create_Instance_Success)

        except Exception as e:
            shutil.rmtree(config.Minecraft_Dir+'/'+name)
            main_ui.Message(lang.Create_Instance_Failure+"\n\n Error: "+str(e))

    elif type == "Fabric" or type == "Fabric Snapshot":
        try:
            mllb.fabric.install_fabric(minecraft_version=ver,
                                        minecraft_directory=config.Minecraft_Dir+'/'+name,
                                        loader_version=mod,
                                        java=java,
                                        callback={'setStatus': callback.setStatus,
                                                    'setProgress': callback.setProgress,
                                                    'setMax': callback.setMax})
            
            saveInstance(name, type, ver, f'fabric-loader-{mod}-{ver}')

            main_ui.Message(lang.Create_Instance_Success)

        except Exception as e:
            shutil.rmtree(config.Minecraft_Dir+'/'+name)
            main_ui.Message(lang.Create_Instance_Failure+"\n\n Error: "+str(e))

    elif type == "Quilt" or type == "Quilt Snapshot":
        try:
            mllb.quilt.install_quilt(minecraft_version=ver,
                                    minecraft_directory=config.Minecraft_Dir+'/'+name,
                                    loader_version=mod,
                                    java=java,
                                    callback={'setStatus': callback.setStatus,
                                                'setProgress': callback.setProgress,
                                                'setMax': callback.setMax})

            saveInstance(name, type, ver, f'quilt-loader-{mod}-{ver}')
            main_ui.Message(lang.Create_Instance_Success)

        except Exception as e:
            shutil.rmtree(config.Minecraft_Dir+'/'+name)
            main_ui.Message(lang.Create_Instance_Failure+"\n\n Error: "+str(e))


def install_instance(name, type, ver, mod, callback):
    for instance in os.scandir(config.Minecraft_Dir):
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

    return do_install(name, type, ver, mod, callback)


def get_instance_data(name):
    with open(config.Minecraft_Dir+'/'+name+'/instance_data.pkl', 'rb') as file:
        fileData = pickle.load(file)
        file.close()
    return fileData


def update_instance_name(oldName, name):
    os.rename(config.Minecraft_Dir+'/'+oldName, config.Minecraft_Dir+'/'+name)


def modify_instance(name, type, ver, mod, callback):
    for version in os.scandir(config.Minecraft_Dir+'/'+name+'/versions'):
        shutil.rmtree(config.Minecraft_Dir+'/'+name+'/versions/'+version.name)
    
    return do_install(name, type, ver, mod, callback)


def uninstall_instance(versionName, callback):
    try:
        callback.setMax(1)
        callback.setProgress(0)
        callback.setStatus("Uninstalling instance: "+versionName)
        
        shutil.rmtree(config.Minecraft_Dir+'/'+versionName)
        
        callback.setProgress(1)

        main_ui.Message(lang.Delete_Instance_Success)
    except Exception as e:
        main_ui.Message(lang.Delete_Instance_Failure)


def check_instance_folders():
    installed_version_list = []
        
    for folder in os.scandir(config.Minecraft_Dir):
        if folder.is_dir():
            for file in os.scandir(config.Minecraft_Dir+'/'+folder.name):
                    if file.name == 'instance_data.pkl':
                        installed_version_list.append(folder.name)
    
    return installed_version_list


def check_instances():
    versions = ""
    installed_version_list = check_instance_folders()
    
    if len(installed_version_list) != 0:
        if config.DefaultInstance == "" or config.DefaultInstance == lang.Without_Versions:
            config.DefaultInstance = installed_version_list[0]
        is_installed = False

        for installed_version in installed_version_list:
            if config.DefaultInstance == installed_version:
                is_installed = True

        if not is_installed:
            config.DefaultInstance = installed_version_list[0]
        versions = config.DefaultInstance

    elif len(installed_version_list) == 0:
        versions = lang.Without_Versions
        installed_version_list.append(lang.Without_Versions)

    return versions, installed_version_list


def check_versions(type):
    versions = []
    first_ver = ""
    first = True

    if type == "Vanilla" or type == "Forge":
        for version in mllb.utils.get_version_list():
            if version["type"] == "release":
                versions.append(version["id"])
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Snapshot":
        for version in mllb.utils.get_version_list():
            if version["type"] == "snapshot":
                versions.append(version["id"])
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Fabric":
        for version in mllb.utils.get_version_list():
            if mllb.fabric.is_minecraft_version_supported(version["id"]) and version["type"] == "release":
                versions.append(version["id"])
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Fabric Snapshot":
        for version in mllb.utils.get_version_list():
            if mllb.fabric.is_minecraft_version_supported(version["id"]) and version["type"] == "snapshot":
                versions.append(version["id"])
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Quilt":
        for version in mllb.utils.get_version_list():
            if mllb.quilt.is_minecraft_version_supported(version["id"]) and version["type"] == "release":
                versions.append(version["id"])
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Quilt Snapshot":
        for version in mllb.utils.get_version_list():
            if mllb.quilt.is_minecraft_version_supported(version["id"]) and version["type"] == "snapshot":
                versions.append(version["id"])
                if first:
                    first_ver = version["id"]
                    first = False

    return first_ver, versions


def check_engine_ver(ver, engine_type):
    engines = []
    first_engine = ""
    first = True
    
    if engine_type == "Forge":
        for version in mllb.forge.list_forge_versions():
            if version.startswith(ver):
                engines.append(version)
                if first:
                    first_engine = version
                    first = False

    elif engine_type == "Fabric" or engine_type == "Fabric Snapshot":
        for version in mllb.fabric.get_all_loader_versions():
            engines.append(version["version"])
            if first:
                first_engine = version["version"]
                first = False

    elif engine_type == "Quilt" or engine_type == "Quilt Snapshot":
        for version in mllb.quilt.get_all_loader_versions():
            engines.append(version["version"])
            if first:
                first_engine = version["version"]
                first = False

    return first_engine, engines


def run_instance(versionName, username):
            
    if username == lang.Without_Accounts:
        main_ui.Message(lang.Without_Accounts_To_Play)
        return
    
    if versionName == lang.Without_Versions:
        main_ui.Message(lang.Without_Versions_To_Play)
        return
    
    config.save_config()

    options = mllb.types.MinecraftOptions()
    
    options['username'] = username
    options['uuid'] = config.Accounts[username]["Uuid"]
    options['token'] = config.Accounts[username]["Token"]
    options['jvmArguments'] = ['-Xmx'+str(config.RamAmount)+'M']
    options['launcherVersion'] = config.Version
    
    instanceData = get_instance_data(versionName)

    minecraft_command = mllb.command.get_minecraft_command(instanceData['Jar'], config.Minecraft_Dir+'/'+versionName, options)
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
        os.startfile(config.Minecraft_Dir)
    elif os.name == "posix":
        os.system('xdg-open '+config.Minecraft_Dir)