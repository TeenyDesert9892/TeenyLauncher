import os
import pickle
import shutil
import platform
import subprocess
import minecraft_launcher_lib as mllb

class instanceHandeler:
    def __init__(self, configHandeler, langHandeler, jdkHandeler):
        self.ConfigHandeler = configHandeler
        self.LangHandeler = langHandeler
        self.JdkHandeler = jdkHandeler
    
    
    def saveInstance(self, name, type, ver, jar):
        with open(self.ConfigHandeler.Minecraft_Dir+'/'+name+'/instance_data.pkl', 'wb') as file:
            pickle.dump({'Name': name, 'Type': type, 'Ver': ver, 'Jar': jar}, file)
            file.close()
    
    
    def do_install(self, name, type, ver, mod, callback):
        if type == "Vanilla" or type == "Snapshot":
            try:
                mllb.install.install_minecraft_version(versionid=ver,
                                                    minecraft_directory=self.ConfigHandeler.Minecraft_Dir+'/'+name,
                                                    callback=callback)
                self.saveInstance(name, type, ver, ver)
                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(self.ConfigHandeler.Minecraft_Dir+'/'+name)
                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Failure)
                

        elif type == "Forge":
            try:
                mllb.forge.install_forge_version(versionid=mod,
                                                path=self.ConfigHandeler.Minecraft_Dir+'/'+name,
                                                callback=callback)
                
                self.saveInstance(name, type, ver, mod.replace("-", "-forge-"))

                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(self.ConfigHandeler.Minecraft_Dir+'/'+name)
                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Failure)

        elif type == "Fabric" or type == "Fabric Snapshot":
            try:
                mllb.fabric.install_fabric(minecraft_version=ver,
                                        minecraft_directory=self.ConfigHandeler.Minecraft_Dir+'/'+name,
                                        loader_version=mod,
                                        callback=callback)
                
                self.saveInstance(name, type, ver, f'fabric-loader-{mod}-{ver}')

                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(self.ConfigHandeler.Minecraft_Dir+'/'+name)
                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Failure)

        elif type == "Quilt" or type == "Quilt Snapshot":
            try:
                mllb.quilt.install_quilt(minecraft_version=ver,
                                        minecraft_directory=self.ConfigHandeler.Minecraft_Dir+'/'+name,
                                        loader_version=mod,
                                        callback=callback)
                
                self.saveInstance(name, type, ver, f'quilt-loader-{mod}-{ver}')

                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Success)

            except:
                shutil.rmtree(self.ConfigHandeler.Minecraft_Dir+'/'+name)
                self.ConfigHandeler.send_message(self.LangHandeler.Create_Instance_Failure)
        
        shutil.rmtree(self.ConfigHandeler.Minecraft_Dir+'/'+name+'/runtime')


    def install_instance(self, name, type, ver, mod, callback):
        for instance in os.scandir(self.ConfigHandeler.Minecraft_Dir):
            if instance.name == name:
                self.ConfigHandeler.send_message(self.LangHandeler.Install_Version_Already_Exsists)

        if name == "":
            self.ConfigHandeler.send_message(self.LangHandeler.Install_Version_Without_Name)
            return
        
        if type == "":
            self.ConfigHandeler.send_message(self.LangHandeler.Install_Version_Type_Not_Selected)
            return

        if ver == "":
            self.ConfigHandeler.send_message(self.LangHandeler.Install_Version_Not_Selected)
            return

        return self.do_install(name, type, ver, mod, callback)


    def get_instance_data(self, name):
        with open(self.ConfigHandeler.Minecraft_Dir+'/'+name+'/instance_data.pkl', 'rb') as file:
            fileData = pickle.load(file)
            file.close()
        return fileData


    def update_instance_name(self, oldName, name):
        os.rename(self.ConfigHandeler.Minecraft_Dir+'/'+oldName, self.ConfigHandeler.Minecraft_Dir+'/'+name)


    def modify_instance(self, name, type, ver, mod, callback):
        for version in os.scandir(self.ConfigHandeler.Minecraft_Dir+'/'+name+'/versions'):
            shutil.rmtree(self.ConfigHandeler.Minecraft_Dir+'/'+name+'/versions/'+version.name)
        
        return self.do_install(name, type, ver, mod, callback)


    def uninstall_instance(self, versionName, callback):
        try:
            callback.setMax(1)
            callback.setProgress(0)
            callback.setStatus("Uninstalling instance: "+versionName)
            
            shutil.rmtree(self.ConfigHandeler.Minecraft_Dir+'/'+versionName)
            
            callback.setProgress(1)

            self.ConfigHandeler.send_message(self.LangHandeler.Delete_Instance_Success)
        except:
            self.ConfigHandeler.send_message(self.LangHandeler.Delete_Instance_Failure)


    def check_instance_folders(self):
        installed_version_list = []
            
        for folder in os.scandir(self.ConfigHandeler.Minecraft_Dir):
            if folder.is_dir():
                for file in os.scandir(self.ConfigHandeler.Minecraft_Dir+'/'+folder.name):
                        if file.name == 'instance_data.pkl':
                            installed_version_list.append(folder.name)
        
        return installed_version_list


    def check_instances(self):
        versions = ""
        installed_version_list = self.check_instance_folders()
        
        if len(installed_version_list) != 0:
            if self.ConfigHandeler.DefaultInstance == "" or self.ConfigHandeler.DefaultInstance == self.LangHandeler.Without_Versions:
                self.ConfigHandeler.DefaultInstance = installed_version_list[0]
            is_installed = False

            for installed_version in installed_version_list:
                if self.ConfigHandeler.DefaultInstance == installed_version:
                    is_installed = True

            if not is_installed:
                self.ConfigHandeler.DefaultInstance = installed_version_list[0]
            versions = self.ConfigHandeler.DefaultInstance

        elif len(installed_version_list) == 0:
            versions = self.LangHandeler.Without_Versions
            installed_version_list.append(self.LangHandeler.Without_Versions)

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
               
        if username == self.LangHandeler.Without_Accounts:
            self.ConfigHandeler.send_message(self.LangHandeler.Without_Accounts_To_Play)
            return
        
        if versionName == self.LangHandeler.Without_Versions:
            self.ConfigHandeler.send_message(self.LangHandeler.Without_Versions_To_Play)
            return
        
        self.ConfigHandeler.save_config()

        ram = '-Xmx'+str(self.ConfigHandeler.RamAmount)+'M'

        options = {'username': username,
                'uuid': self.ConfigHandeler.Accounts[username]["Uuid"],
                'token': self.ConfigHandeler.Accounts[username]["Token"],
                'jvArguments': '['+ram+', '+ram+']',
                'launcherVersion': self.ConfigHandeler.Version}
        
        instanceData = self.get_instance_data(versionName)

        minecraft_command = mllb.command.get_minecraft_command(instanceData['Jar'],self.ConfigHandeler.Minecraft_Dir+'/'+versionName, options)
        try:
            if os.name == "nt":
                minecraft_command[0] = os.path.normpath(self.JdkHandeler.get_jdk_client(float(instanceData['Ver'].replace(".", "", 1)))+"/bin/java.exe")
            else:
                minecraft_command[0] = os.path.normpath(JdkHandeler.get_jdk_client(float(instanceData['Ver'].replace(".", "", 1))) + "/bin/java")
        except:
            self.ConfigHandeler.send_message(self.LangHandeler.Incompatible_JDK)
            return
        subprocess.run(minecraft_command)


    def open_instances_folder(self, e=None):
        if os.name == "nt":
            os.startfile(self.ConfigHandeler.Minecraft_Dir)
        elif os.name == "posix":
            os.system('xdg-open '+ConfigHandeler.Minecraft_Dir)