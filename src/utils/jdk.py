import jdk
import os
import glob

from core import config

def get_jdk_version(self, game_version: float):
    if game_version >= 120.5:
        return "21"
    elif game_version >= 118:
        return "17"
    elif game_version >= 117:
        return "16"
    else:
        return "8"


def get_jdk_client(self, game_version: float):
    jdk_version = self.get_jdk_version(game_version)

    if not os.path.exists(config.Minecraft_Dir+"/jdks"):
        os.mkdir(config.Minecraft_Dir+"/jdks")

    if game_version < 117:
        try:
            os.path.normpath(glob.glob(config.Minecraft_Dir+'/jdks/jdk'+jdk_version+'*')[0])
        except:
            jdk.install(version=jdk_version,
                        jre=True,
                        path=os.path.normpath(config.Minecraft_Dir+'/jdks'),
                        vendor="Adoptium")
        return os.path.normpath(glob.glob(config.Minecraft_Dir+'/jdks/jdk'+jdk_version+'*')[0])
    else:
        try:
            os.path.normpath(glob.glob(config.Minecraft_Dir+'/jdks/jdk-'+jdk_version+'*')[0])
        except:
            jdk.install(version=jdk_version,
                        jre=True,
                        path=os.path.normpath(config.Minecraft_Dir+'/jdks'),
                        vendor="Adoptium")
        return os.path.normpath(glob.glob(config.Minecraft_Dir+'/jdks/jdk-'+jdk_version+'*')[0])