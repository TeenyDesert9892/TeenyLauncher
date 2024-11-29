import os
import pickle
import shutil
import platform
import subprocess
import minecraft_launcher_lib as mllb

from __main__ import ConfigHandeler
from __main__ import LangHandeler
from __main__ import JdkHandeler

class instanceHandeler:
    def __init__(self):
        pass
    
    
    def do_install(self, name, type, ver, mod, callback):
        if type == "Vanilla" or type == "Snapshot":
            try:
                mllb.install.install_minecraft_version(versionid=ver,
                                                    minecraft_directory=ConfigHandeler.Minecraft_Dir+'/'+name,
                                                    callback=callback)
                ConfigHandeler.update_config_add_instances(name, type, ver, ver, True)

                return LangHandeler.Delete_Instance_Success

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                return LangHandeler.Delete_Instance_Failure
                

        elif type == "Forge":
            try:
                mllb.forge.install_forge_version(versionid=mod,
                                                path=ConfigHandeler.Minecraft_Dir+'/'+name,
                                                callback=callback)
                
                ConfigHandeler.update_config_add_instances(name, type, ver, mod.replace("-", "-forge-"), True)

                return LangHandeler.Delete_Instance_Success

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                return LangHandeler.Delete_Instance_Failure

        elif type == "Fabric" or type == "Fabric Snapshot":
            try:
                mllb.fabric.install_fabric(minecraft_version=ver,
                                        minecraft_directory=ConfigHandeler.Minecraft_Dir+'/'+name,
                                        loader_version=mod,
                                        callback=callback)
                
                ConfigHandeler.update_config_add_instances(name, type, ver, f'fabric-loader-{mod}-{ver}', True)

                return LangHandeler.Delete_Instance_Success

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                return LangHandeler.Delete_Instance_Failure

        elif type == "Quilt" or type == "Quilt Snapshot":
            try:
                mllb.quilt.install_quilt(minecraft_version=ver,
                                        minecraft_directory=ConfigHandeler.Minecraft_Dir+'/'+name,
                                        loader_version=mod,
                                        callback=callback)
                
                ConfigHandeler.update_config_add_instances(name, type, ver, f'quilt-loader-{mod}-{ver}', True)

                return LangHandeler.Delete_Instance_Success

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                return LangHandeler.Delete_Instance_Failure

    def install_instance(self, name, type, ver, mod, callback):

        alreadyExistsName = False

        if len(ConfigHandeler.Instances) != 0:
            for instance in ConfigHandeler.Instances:
                if instance == name:
                    alreadyExistsName = True

        if alreadyExistsName:
            return LangHandeler.Install_Version_Already_Exsists

        if name == "":
            return LangHandeler.Install_Version_Without_Name
        
        if type == "":
            return LangHandeler.Install_Version_Type_Not_Selected

        if ver == "":
            return LangHandeler.Install_Version_Not_Selected

        return self.do_install(name, type, ver, mod, callback)


    def modify_instance(self, name, type, ver, mod, callback):
        for version in os.scandir(ConfigHandeler.Minecraft_Dir+'/'+name+'/versions'):
            shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name+'/versions/'+version.name)
        return self.install_instance(name, type, ver, mod, callback)


    def uninstall_instance(self, versionName, setStatus, setProgress, setMax):
        try:
            setMax(1)
            setProgress(0)
            setStatus("Uninstalling instance: "+versionName)
            
            ConfigHandeler.update_config_remove_instances(versionName)
            
            shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+versionName)
            
            setProgress(1)

            return LangHandeler.Delete_Instance_Success
        except:
            return LangHandeler.Delete_Instance_Failure


    def check_instance_folders(self):
        folder_list = []
        installed_version_list = []
        coincidence = False
            
        for folder in os.scandir(ConfigHandeler.Minecraft_Dir):
            if folder.is_dir == True:
                folder_list.append(folder.name)
        
        for folder in folder_list:
            for installed_version in ConfigHandeler.Instances:
                if installed_version == folder:
                    installed_version_list.append(installed_version)
                    coincidence = True
                    continue
            else:
                if not coincidence:
                    for file in os.scandir(ConfigHandeler.Minecraft_Dir+'/'+folder):
                        if file.name == 'instance_data.pkl':
                            with open(ConfigHandeler.Minecraft_Dir+'/'+folder+'/instance_data.pkl', 'rb') as data:
                                file_data = pickle.load(data)
                                data.close()
                                
                                installed_version_list.append(file.name)
                                ConfigHandeler.update_config_add_instances(file_data['Name'],
                                                                        file_data['Type'],
                                                                        file_data['Version'],
                                                                        file_data['Jar'])
                                
                            coincidence = True
                            continue
        else:
            if not coincidence:
                ConfigHandeler.update_config_remove_instances(installed_version_list)
                
        return installed_version_list


    def check_instances(self):
        versions = ""
        installed_version_list = self.check_instance_folders()
        
        if len(installed_version_list) != 0:
            if ConfigHandeler.DefaultInstance == "" or ConfigHandeler.DefaultInstance == LangHandeler.Without_Versions:
                ConfigHandeler.DefaultInstance = installed_version_list[0]
            is_installed = False

            for installed_version in installed_version_list:
                if ConfigHandeler.DefaultInstance == installed_version:
                    is_installed = True

            if not is_installed:
                ConfigHandeler.DefaultInstance = installed_version_list[0]
            versions = ConfigHandeler.DefaultInstance

        elif len(installed_version_list) == 0:
            versions = LangHandeler.Without_Versions
            installed_version_list.append(LangHandeler.Without_Versions)

        return versions, installed_version_list


    def check_versions(self, type):
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


    def check_engine_ver(self, ver, engine_type):
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


    def run_instance(self, versionName, username, msg):
        if username == LangHandeler.Without_Accounts:
            msg(LangHandeler.Without_Accounts_To_Play)
            return
        
        if versionName == LangHandeler.Without_Versions:
            msg(LangHandeler.Without_Versions_To_Play)
            return
        
        ConfigHandeler.save_config()

        ram = '-Xmx'+str(ConfigHandeler.RamAmount)+'M'

        options = {'username': username,
                'uuid': ConfigHandeler.Accounts[username]["Uuid"],
                'token': ConfigHandeler.Accounts[username]["Token"],
                'jvArguments': '['+ram+', '+ram+']',
                'launcherVersion': ConfigHandeler.Version}

        minecraft_command = mllb.command.get_minecraft_command(ConfigHandeler.Instances[versionName]['Jar'], ConfigHandeler.Minecraft_Dir+'/'+versionName, options)
        try:
            if platform.system() == "Windows":
                minecraft_command[0] = os.path.normpath(JdkHandeler.get_jdk_client(float(ConfigHandeler.Instances[versionName]['Version'].replace(".", "", 1)))+"/bin/java.exe")
            else:
                minecraft_command[0] = os.path.normpath(JdkHandeler.get_jdk_client(float(ConfigHandeler.Instances[versionName]['Version'].replace(".", "", 1))) + "/bin/java")
        except:
            msg(LangHandeler.Incompatible_JDK)
            return

        subprocess.run(minecraft_command)


    def open_instances_folder(self, e=None):
        if os.name == "nt":
            os.startfile(ConfigHandeler.Minecraft_Dir)
        elif os.name == "posix":
            os.system('xdg-open '+ConfigHandeler.Minecraft_Dir)