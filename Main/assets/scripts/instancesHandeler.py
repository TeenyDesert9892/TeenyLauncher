import os
import json
import shutil
import platform
import subprocess
import minecraft_launcher_lib as mllb

from __main__ import configHandeler
from __main__ import jdkHandeler

config = configHandeler.config
lang = configHandeler.lang
minecraft_directory = configHandeler.minecraft_directory


def install_instance(name, type, ver, mod, setStatus, setProgress, setMax, msg):
    def save_version(typ, version, jar):
        with open(minecraft_directory+'/'+name+'/'+name+'.json', 'w') as file:
            json.dump({"Type": typ, "Version": version, "Jar": jar}, file, indent=4)
            file.close()

    callback = {"setStatus": setStatus, "setProgress": setProgress, "setMax": setMax}

    alreadyExistsName = False

    for dir in os.scandir(minecraft_directory):
        if name == dir.name:
            alreadyExistsName = True

    if alreadyExistsName:
        msg(lang.Install_Version_Already_Exsists)
        return

    if name == "":
        msg(lang.Install_Version_Without_Name)
        return

    if ver == "":
        msg(lang.Install_Version_Not_Selected)
        return

    if type == "Vanilla" or type == "Snapshot":
        try:
            mllb.install.install_minecraft_version(versionid=ver,
                                                   minecraft_directory=str(f"{minecraft_directory}/{name}"),
                                                   callback=callback)
            save_version(type, ver, ver)

            msg(lang.Install_Vanilla_Version_Success)

        except:
            msg(lang.Install_Vanilla_Version_Failure)

            if os.path.exists(str(f"{minecraft_directory}/{name}")):
                shutil.rmtree(str(f"{minecraft_directory}/{name}"))
            return

    elif type == "Forge":
        try:
            mllb.forge.install_forge_version(versionid=mod,
                                             path=str(f"{minecraft_directory}/{name}"),
                                             callback=callback)
            save_version(type, ver, mod.replace("-", "-forge-"))

            msg(lang.Install_Forge_Version_Success)

        except:
            msg(lang.Install_Forge_Version_Failure)

            if os.path.exists(str(f"{minecraft_directory}/{name}")):
                shutil.rmtree(str(f"{minecraft_directory}/{name}"))
            return

    elif type == "Fabric" or type == "Fabric Snapshot":
        try:
            mllb.fabric.install_fabric(minecraft_version=ver,
                                       minecraft_directory=str(f"{minecraft_directory}/{name}"),
                                       loader_version=mod,
                                       callback=callback)
            save_version(type, ver, str(f"fabric-loader-{mod}-{ver}"))

            msg(lang.Install_Fabric_Version_Success)

        except:
            msg(lang.Install_Fabric_Version_Failure)

            if os.path.exists(str(f"{minecraft_directory}/{name}")):
                shutil.rmtree(str(f"{minecraft_directory}/{name}"))
            return

    elif type == "Quilt" or type == "Quilt Snapshot":
        try:
            mllb.quilt.install_quilt(minecraft_version=ver,
                                     minecraft_directory=str(f"{minecraft_directory}/{name}"),
                                     loader_version=mod,
                                     callback=callback)
            save_version(type, ver, str(f"quilt-loader-{mod}-{ver}"))

            msg(lang.Install_Quilt_Version_Success)

        except:
            msg(lang.Install_Quilt_Version_Failure)

            if os.path.exists(str(f"{minecraft_directory}/{name}")):
                shutil.rmtree(str(f"{minecraft_directory}/{name}"))
            return

    else:
        msg(lang.Install_Version_Type_Not_Selected)
        return

    shutil.rmtree(f"{minecraft_directory}/{name}/runtime")


def uninstall_instance(version, setStatus, setProgress, setMax, msg):
    try:
        setMax(1)
        setProgress(0)
        setStatus("Uninstalling instance: "+version)

        shutil.rmtree(minecraft_directory+'/'+version)

        setProgress(1)

        msg(lang.Delete_Instance_Success)
    except:
        msg(lang.Delete_Instance_Failure)


def check_instances():
    versions = ""
    installed_version_list = []

    for installed_version in os.scandir(minecraft_directory):
        if installed_version.name != "launcher_config.pkl" and installed_version.name != "minecraft_directory.txt" and installed_version.name != "jdks":
            installed_version_list.append(installed_version.name)

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
    versions = {}
    first_ver = ""
    first = True

    if type == "Vanilla" or type == "Forge":
        for version in mllb.utils.get_version_list():
            if version["type"] == "release":
                versions[version["id"]] = version["id"]
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Snapshot":
        for version in mllb.utils.get_version_list():
            if version["type"] == "snapshot":
                versions[version["id"]] = version["id"]
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Fabric":
        for version in mllb.utils.get_version_list():
            if mllb.fabric.is_minecraft_version_supported(version["id"]) and version["type"] == "release":
                versions[version["id"]] = version["id"]
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Fabric Snapshot":
        for version in mllb.utils.get_version_list():
            if mllb.fabric.is_minecraft_version_supported(version["id"]) and version["type"] == "snapshot":
                versions[version["id"]] = version["id"]
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Quilt":
        for version in mllb.utils.get_version_list():
            if mllb.quilt.is_minecraft_version_supported(version["id"]) and version["type"] == "release":
                versions[version["id"]] = version["id"]
                if first:
                    first_ver = version["id"]
                    first = False

    elif type == "Quilt Snapshot":
        for version in mllb.utils.get_version_list():
            if mllb.quilt.is_minecraft_version_supported(version["id"]) and version["type"] == "snapshot":
                versions[version["id"]] = version["id"]
                if first:
                    first_ver = version["id"]
                    first = False

    new_versions = []
    for ver in versions:
        new_versions.append(ver)

    return first_ver, new_versions


def check_engine_ver(ver, engine_type):
    engines = {}
    first_engine = ""
    first = True
    if engine_type == "Forge":
        for version in mllb.forge.list_forge_versions():
            if version.startswith(ver):
                engines[version] = version
                if first:
                    first_engine = version
                    first = False

    elif engine_type == "Fabric" or engine_type == "Fabric Snapshot":
        for version in mllb.fabric.get_all_loader_versions():
            engines[version["version"]] = version["version"]
            if first:
                first_engine = version["version"]
                first = False

    elif engine_type == "Quilt" or engine_type == "Quilt Snapshot":
        for version in mllb.quilt.get_all_loader_versions():
            engines[version["version"]] = version["version"]
            if first:
                first_engine = version["version"]
                first = False

    new_engines = []
    for engine in engines:
        new_engines.append(engine)

    return first_engine, new_engines

def run_instance(version, username, msg):
    if username == lang.Without_Accounts:
        msg(lang.Without_Accounts_To_Play)
        return
    
    if version == lang.Without_Versions:
        msg(lang.Without_Versions_To_Play)
        return

    ram = '-Xmx'+str(config.RamAmount)+'M'

    options = {'username': username,
               'uuid': config.Accounts[username]["Uuid"],
               'token': config.Accounts[username]["Token"],
               'jvArguments': '['+ram+', '+ram+']',
               'launcherVersion': config.Version}

    file = open(minecraft_directory+'/'+version+'/'+version+'.json', 'r')
    fileData = json.load(file)
    file.close()

    minecraft_command = mllb.command.get_minecraft_command(fileData["Jar"], minecraft_directory+'/'+version, options)
    try:
        if platform.system() == "Windows":
            minecraft_command[0] = os.path.normpath(jdkHandeler.get_jdk_client(float(fileData['Version'].replace(".", "", 1)))+"/bin/java.exe")
        else:
            minecraft_command[0] = os.path.normpath(jdkHandeler.get_jdk_client(float(fileData['Version'].replace(".", "", 1))) + "/bin/java")
    except:
        msg(lang.Incompatible_JDK)
        return

    subprocess.run(minecraft_command)


def open_instances_folder(e=None):
    if os.name == "nt":
        os.startfile(minecraft_directory)
    elif os.name == "posix":
        os.system('xdg-open '+minecraft_directory)