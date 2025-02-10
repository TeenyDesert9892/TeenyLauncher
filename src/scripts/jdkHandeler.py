import jdk
import os
import glob


class jdkHandeler:
    def __init__(self, configHandeler):
        self.ConfigHandeler = configHandeler
    
    
    def get_jdk_version(self, game_version=float):
        if game_version >= 120.5:
            return "21"
        elif game_version >= 118:
            return "17"
        elif game_version >= 117:
            return "16"
        else:
            return "8"


    def get_jdk_client(self, game_version=float):
        jdk_version = self.get_jdk_version(game_version)

        if not os.path.exists(self.ConfigHandeler.Minecraft_Dir+"/jdks"):
            os.mkdir(self.ConfigHandeler.Minecraft_Dir+"/jdks")

        if game_version <= 116.5:
            try:
                return os.path.normpath(glob.glob(self.ConfigHandeler.Minecraft_Dir+'/jdks/jdk'+jdk_version+'*')[0])
            except:
                jdk.install(version=jdk_version,
                            operating_system=jdk.OperatingSystem.detect(),
                            arch=jdk.Architecture.detect(),
                            jre=True,
                            path=os.path.normpath(self.ConfigHandeler.Minecraft_Dir+'/jdks'),
                            vendor="Adoptium")
                return os.path.normpath(glob.glob(self.ConfigHandeler.Minecraft_Dir+'/jdks/jdk'+jdk_version+'*')[0])
        else:
            try:
                return os.path.normpath(glob.glob(self.ConfigHandeler.Minecraft_Dir+'/jdks/jdk-'+jdk_version+'*')[0])
            except:
                jdk.install(version=jdk_version,
                            operating_system=jdk.OperatingSystem.detect(),
                            arch=jdk.Architecture.detect(),
                            jre=True,
                            path=os.path.normpath(self.ConfigHandeler.Minecraft_Dir+'/jdks'),
                            vendor="Adoptium")
                return os.path.normpath(glob.glob(self.ConfigHandeler.Minecraft_Dir+'/jdks/jdk-'+jdk_version+'*')[0])