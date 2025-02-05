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
    
    
    def saveInstance(self, name, type, ver, jar):
        with open(ConfigHandeler.Minecraft_Dir+'/'+name+'/instance_data.pkl', 'wb') as file:
            pickle.dump({'Name': name, 'Type': type, 'Ver': ver, 'Jar': jar}, file)
            file.close()
    
    
    def do_install(self, name, type, ver, mod, callback):
        if type == "Vanilla" or type == "Snapshot":
            try:
                mllb.install.install_minecraft_version(versionid=ver,
                                                    minecraft_directory=ConfigHandeler.Minecraft_Dir+'/'+name,
                                                    callback=callback)
                self.saveInstance(name, type, ver, ver)
                ConfigHandeler.send_message(LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                ConfigHandeler.send_message(LangHandeler.Create_Instance_Failure)
                

        elif type == "Forge":
            try:
                mllb.forge.install_forge_version(versionid=mod,
                                                path=ConfigHandeler.Minecraft_Dir+'/'+name,
                                                callback=callback)
                
                self.saveInstance(name, type, ver, mod.replace("-", "-forge-"))

                ConfigHandeler.send_message(LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                ConfigHandeler.send_message(LangHandeler.Create_Instance_Failure)

        elif type == "Fabric" or type == "Fabric Snapshot":
            try:
                mllb.fabric.install_fabric(minecraft_version=ver,
                                        minecraft_directory=ConfigHandeler.Minecraft_Dir+'/'+name,
                                        loader_version=mod,
                                        callback=callback)
                
                self.saveInstance(name, type, ver, f'fabric-loader-{mod}-{ver}')

                ConfigHandeler.send_message(LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                ConfigHandeler.send_message(LangHandeler.Create_Instance_Failure)

        elif type == "Quilt" or type == "Quilt Snapshot":
            try:
                mllb.quilt.install_quilt(minecraft_version=ver,
                                        minecraft_directory=ConfigHandeler.Minecraft_Dir+'/'+name,
                                        loader_version=mod,
                                        callback=callback)
                
                self.saveInstance(name, type, ver, f'quilt-loader-{mod}-{ver}')

                ConfigHandeler.send_message(LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name)
                ConfigHandeler.send_message(LangHandeler.Create_Instance_Failure)
        
        shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name+'/runtime')


    def install_instance(self, name, type, ver, mod, callback):
        for instance in os.scandir(ConfigHandeler.Minecraft_Dir):
            if instance.name == name:
                ConfigHandeler.send_message(LangHandeler.Install_Version_Already_Exsists)

        if name == "":
            ConfigHandeler.send_message(LangHandeler.Install_Version_Without_Name)
            return
        
        if type == "":
            ConfigHandeler.send_message(LangHandeler.Install_Version_Type_Not_Selected)
            return

        if ver == "":
            ConfigHandeler.send_message(LangHandeler.Install_Version_Not_Selected)
            return

        return self.do_install(name, type, ver, mod, callback)


    def get_instance_data(self, name):
        with open(ConfigHandeler.Minecraft_Dir+'/'+name+'/instance_data.pkl', 'rb') as file:
            fileData = pickle.load(file)
            file.close()
        return fileData


    def update_instance_name(self, oldName, name):
        os.rename(ConfigHandeler.Minecraft_Dir+'/'+oldName, ConfigHandeler.Minecraft_Dir+'/'+name)


    def modify_instance(self, name, type, ver, mod, callback):
        for version in os.scandir(ConfigHandeler.Minecraft_Dir+'/'+name+'/versions'):
            shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+name+'/versions/'+version.name)
        
        return self.do_install(name, type, ver, mod, callback)


    def uninstall_instance(self, versionName, callback):
        try:
            callback.setMax(1)
            callback.setProgress(0)
            callback.setStatus("Uninstalling instance: "+versionName)
            
            shutil.rmtree(ConfigHandeler.Minecraft_Dir+'/'+versionName)
            
            callback.setProgress(1)

            ConfigHandeler.send_message(LangHandeler.Delete_Instance_Success)
        except:
            ConfigHandeler.send_message(LangHandeler.Delete_Instance_Failure)


    def check_instance_folders(self):
        installed_version_list = []
            
        for folder in os.scandir(ConfigHandeler.Minecraft_Dir):
            if folder.is_dir():
                for file in os.scandir(ConfigHandeler.Minecraft_Dir+'/'+folder.name):
                        if file.name == 'instance_data.pkl':
                            installed_version_list.append(folder.name)
        
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


    def check_engine_ver(self, ver, engine_type):
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


    def run_instance(self, versionName, username):
               
        if username == LangHandeler.Without_Accounts:
            ConfigHandeler.send_message(LangHandeler.Without_Accounts_To_Play)
            return
        
        if versionName == LangHandeler.Without_Versions:
            ConfigHandeler.send_message(LangHandeler.Without_Versions_To_Play)
            return
        
        ConfigHandeler.save_config()

        ram = '-Xmx'+str(ConfigHandeler.RamAmount)+'M'

        options = {'username': username,
                'uuid': ConfigHandeler.Accounts[username]["Uuid"],
                'token': ConfigHandeler.Accounts[username]["Token"],
                'jvArguments': '['+ram+', '+ram+']',
                'launcherVersion': ConfigHandeler.Version}
        
        instanceData = self.get_instance_data(versionName)

        minecraft_command = mllb.command.get_minecraft_command(instanceData['Jar'], ConfigHandeler.Minecraft_Dir+'/'+versionName, options)
        try:
            if os.name == "nt":
                minecraft_command[0] = os.path.normpath(JdkHandeler.get_jdk_client(float(instanceData['Ver'].replace(".", "", 1)))+"/bin/java.exe")
            else:
                minecraft_command[0] = os.path.normpath(JdkHandeler.get_jdk_client(float(instanceData['Ver'].replace(".", "", 1))) + "/bin/java")
        except:
            ConfigHandeler.send_message(LangHandeler.Incompatible_JDK)
            return
        subprocess.run(minecraft_command)


    def open_instances_folder(self, e=None):
        if os.name == "nt":
            os.startfile(ConfigHandeler.Minecraft_Dir)
        elif os.name == "posix":
            os.system('xdg-open '+ConfigHandeler.Minecraft_Dir)