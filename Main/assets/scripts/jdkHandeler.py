import jdk
import os
import glob

from __main__ import configHandeler

minecraft_directory = configHandeler.get_launcher_path()

def get_jdk_version(game_version=float):
    if game_version >= 120.5:
        return "21"
    elif game_version >= 118:
        return "17"
    elif game_version >= 117:
        return "16"
    else:
        return "8"


def get_jdk_client(game_version=float):
    jdk_version = get_jdk_version(game_version)

    if not os.path.exists(minecraft_directory+"/jdks"):
        os.mkdir(minecraft_directory+"/jdks")

    if game_version <= 116.5:
        try:
            return os.path.normpath(glob.glob(minecraft_directory+'/jdks/jdk'+jdk_version+'*')[0])
        except:
            jdk.install(version=jdk_version,
                        operating_system=jdk.OperatingSystem.detect(),
                        arch=jdk.Architecture.detect(),
                        jre=True,
                        path=os.path.normpath(minecraft_directory+'/jdks'),
                        vendor="Adoptium")
            return os.path.normpath(glob.glob(minecraft_directory+'/jdks/jdk'+jdk_version+'*')[0])
    else:
        try:
            return os.path.normpath(glob.glob(minecraft_directory+'/jdks/jdk-'+jdk_version+'*')[0])
        except:
            jdk.install(version=jdk_version,
                        operating_system=jdk.OperatingSystem.detect(),
                        arch=jdk.Architecture.detect(),
                        jre=True,
                        path=os.path.normpath(minecraft_directory+'/jdks'),
                        vendor="Adoptium")
            return os.path.normpath(glob.glob(minecraft_directory+'/jdks/jdk-'+jdk_version+'*')[0])