import minecraft_launcher_lib, os, subprocess, tkinter

window = tkinter.Tk()
window.title("TeenyLauncher")
window.geometry("800x600")
window.config(bg="#FFFFFF")
window.iconbitmap("assets/icon.ico")
window.resizable(0,0)

options = tkinter.Frame(window, width=300, height=600)
options.place(x=500, y=0)
options.config(bg="#3D3D3D", )
options.pack()

nameText = tkinter.Label(options, text="Nombre de usuario")
nameText.grid(row=2,column=0, sticky="w", padx=50, pady=10)

nameSelect = tkinter.Entry(options)
nameSelect.grid(row=3, column=0, sticky="w", padx=50, pady=10)

versionText = tkinter.Label(options, text="Version de minecraft")
versionText.grid(row=0,column=0, sticky="w", padx=50, pady=10)

versionSelect = tkinter.Entry(options)
versionSelect.grid(row=1, column=0, sticky="w", padx=50, pady=10)

installTypeText = tkinter.Label(options, text="Tipo de instalacion")
installTypeText.grid(row=4,column=0, sticky="w", padx=50, pady=10)

installTypeSelect = tkinter.Entry(options)
installTypeSelect.grid(row=5, column=0, sticky="w", padx=50, pady=10)

window.mainloop()

user_window = os.environ["USERNAME"]
minecraft_directori = f"C:/Users/{user_window}/AppData/Roaming/.minecraftLauncher"

def instalar_minecraft(version):
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version,minecraft_directori)
        print(f'Se ha instalado la version {version}')
    else:
        print('No se ingreso ninguna contraseña')

def instalar_forge(version):
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    minecraft_launcher_lib.forge.install_forge_version(forge,minecraft_directori)
    print('Forge instalado')

def ejecutar_minecraft(nombre,vers):
    mine_user = nombre
    version = vers

    options = {
        'username': mine_user,
        'uuid' : '',
        'token': '',

        'jvArguments': ["-Xmx4G","-Xmx4G"], # 4G es para 4 de gigas de RAM
        'launcherVersion': "0.0.2"
    }

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version,minecraft_directori,options)
    subprocess.run(minecraft_command)

def menu():
    while True:

        versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)
        if len(versiones_instaladas) == 0:
            print('No tienes versiones instaladas')
        else:
            for ver in versiones_instaladas:
                print(ver['id'])

        print('Bienvenido al launcher de Minecraft')
        respuesta = int(input('Para instalar una version (0) \nPara instalar forge (1) \nPara ejecutar minecraft (2) \nPara para launcher (3)\n'))

        match respuesta:
            case 0:
                version = input('Que version: ')
                instalar_minecraft(version)
            case 1:
                version = input('Que version: ')
                instalar_forge(version)
            case 2:
                nombre = input('Tu nombre: ')
                version = input('Que version: ')
                ejecutar_minecraft(nombre,version)
            case 3:
                break