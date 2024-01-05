import minecraft_launcher_lib
import os
import subprocess
import shutil
import __main__

user = os.getenv('USERNAME')
if os.name == "nt":
    minecraft_directori = f"C:/Users/{user}/AppData/Roaming/.TeenyLauncher"
elif os.name == "posix":
    minecraft_directori = f"/home/{user}/.TeenyLauncher"

def install_minecraft(version):
    minecraft_launcher_lib.install.install_minecraft_version(version,minecraft_directori)
    __main__.check_vers()
    __main__.message(f"La version de minecraft vanilla se ha instalado correctamente!")

def install_forge(version):
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    if not forge:
        __main__.message("Esta version no tiene soporte por parte de el equipo de Forge.")
    else:
        minecraft_launcher_lib.forge.install_forge_version(forge,minecraft_directori)
        __main__.check_vers()
        __main__.message("La version de minecraft forge se ha instalado correctamente!")

def install_fabric(version):
    if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(version):
        __main__.message("Esta version no tiene soporte por parte de el equipo de Fabric.")
    else:
        minecraft_launcher_lib.fabric.install_fabric(version, minecraft_directori)
        __main__.check_vers()
        __main__.message('La version de minecraft fabric se ha instalado correctamente!')

def install_quilt(version):
    if not minecraft_launcher_lib.quilt.is_minecraft_version_supported(version):
        __main__.message("Esta version no tiene soporte por parte de el equipo de Quilt.")
    else:
        minecraft_launcher_lib.quilt.install_quilt(version, minecraft_directori)
        __main__.check_vers()
        __main__.message("La version de minecraft quilt se ha instalado correctamente!")

def ejecutar_minecraft(version, ram):
    user = __main__.config[0]["Accounts"]["Default"]["Name"]
    online = __main__.config[0]["Accounts"]["Default"]["Online"]

    if ram != "":
        ram = "2"

    if online:
        uuid = __main__.config[0]["Accounts"]["Default"]["Uuid"]
        token = __main__.config[0]["Accounts"]["Default"]["Token"]
        options = {'username': user,'uuid' : uuid,'token': token,'jvArguments': [ram,ram],'launcherVersion': "1.0.0"}
    else:
        options = {'username': user,'uuid' : '','token': '','jvArguments': [ram,ram],'launcherVersion': "1.0.0"}

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)
    subprocess.run(minecraft_command)

def verif_ver(ver, type):
    if ver != "":
        if type == "Vanilla":
            install_minecraft(ver)
        elif type == "Forge":
            install_forge(ver)
        elif type == "Fabric":
            install_fabric(ver)
        elif type == "Quilt":
            install_quilt(ver)
        else:
            __main__.message("Selecciona un tipo de verion!")
    else:
        __main__.message("Introduce el numero de la version!")

def uninstall_minecraft_version(version):
    shutil.rmtree(minecraft_directori + '/versions/' + version)
    __main__.check_vers()
    __main__.message(f"La version {version} ha sido desinstalada con exito!")