import minecraft_launcher_lib, os, subprocess
import tkinter as tk

window = tk.Tk()
window.geometry('800x500')
window.title('TeenyLauncher')
window.resizable(0,0)
window.iconbitmap("assets/Icon.ico")

info = tk.Frame(window)
info.config(bg="#FFFFFF",width=600,height=500)
info.grid(row=0,column=0)

mineconf = tk.Frame(window)
mineconf.config(bg="#3D3D3D",width=200,height=500)
mineconf.grid(row=0,column=1)
mineconf.grid_propagate(False)

user = os.getenv('USERNAME')
if os.name == "nt":
    minecraft_directori = f"C:/Users/{user}/AppData/Roaming/.TeenyLauncher"
elif os.name == "posix":
    minecraft_directori = f"/home/{user}/.TeenyLauncher"

bt_ejecutar_minecraft = tk.Button(mineconf)
bt_instalar_versiones = tk.Button(mineconf)
bt_instalar_forge = tk.Button(mineconf)

label_nombre = tk.Label(mineconf,text='Nombre de usuario')
laber_ram = tk.Label(mineconf,text='Uso de ram en Gb')

entry_versiones = tk.Entry(mineconf)
entry_nombre = tk.Entry(mineconf)
entry_ram = tk.Entry(mineconf)

versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)

lista_versiones_instaladas = []
for versiones_instaladas in versiones_instaladas:
    lista_versiones_instaladas.append(versiones_instaladas['id'])

if len(lista_versiones_instaladas) != 0:
    vers = tk.StringVar(mineconf)
    vers.set(lista_versiones_instaladas[0])
elif len(lista_versiones_instaladas) == 0:
    vers = 'sin versiones instaladas'
    lista_versiones_instaladas.append('sin versiones instaladas')

versiones_menu_desplegable = tk.OptionMenu(mineconf, vers, *lista_versiones_instaladas)
versiones_menu_desplegable.config()

def instalar_minecraft():
    version = entry_versiones.get()
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version,minecraft_directori)
        print(f'Se ha instalado la version {version}')
    else:
        print('No se ingreso ninguna version')

def instalar_forge():
    version = entry_versiones.get()
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    minecraft_launcher_lib.forge.install_forge_version(forge,minecraft_directori)
    print('Forge instalado')

def ejecutar_minecraft():
    mine_user = entry_nombre.get()
    version = vers.get()
    ram = f"-Xmx{entry_ram.get()}G"

    options = {'username': mine_user,'uuid' : '','token': '','jvArguments': [ram,ram],'launcherVersion': "0.0.2"}

    window.destroy()
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version,minecraft_directori,options)
    subprocess.run(minecraft_command)

def instalar_versiones_normales():
    global entry_versiones
    ventana_versiones = tk.Toplevel(mineconf)
    entry_versiones = tk.Entry(ventana_versiones)
    entry_versiones.grid(row=0,column=0,pady=5,sticky=tk.W)

    bt_instalar_vers = tk.Button(ventana_versiones,command=instalar_minecraft,text='Instalar')
    bt_instalar_vers.grid(row=1,column=0,pady=5,sticky=tk.W)

def instalar_versiones_forge():
    global entry_versiones
    ventana_versiones = tk.Toplevel(mineconf)
    entry_versiones = tk.Entry(ventana_versiones)
    entry_versiones.grid(row=0,column=0,pady=5,sticky=tk.W)
    
    bt_instalar_vers = tk.Button(ventana_versiones,command=instalar_forge,text='Instalar')
    bt_instalar_vers.grid(row=1,column=0,pady=5,sticky=tk.W)

def menu():
    label_nombre.config(fg="#FFFFFF", font=("Antipasto Pro Extrabold", 15), background="#3D3D3D")
    label_nombre.grid(row=0,column=0,pady=5,sticky=tk.W)

    entry_nombre.grid(row=1,column=0,pady=5,sticky=tk.W)

    laber_ram.config(fg="#FFFFFF", font=("Antipasto Pro Extrabold", 15), background="#3D3D3D")
    laber_ram.grid(row=2,column=0,pady=5,sticky=tk.W)

    entry_ram.grid(row=3,column=0,pady=5,sticky=tk.W)
    
    bt_instalar_versiones.config(command=instalar_versiones_normales,text='Instalar versiones',fg="#FFFFFF", font=("Antipasto Pro Extrabold", 12), background="#2BC911")
    bt_instalar_versiones.grid(row=4,column=0,pady=5,sticky=tk.W)

    bt_instalar_forge.config(command=instalar_versiones_forge,text='Instalar forge',fg="#FFFFFF", font=("Antipasto Pro Extrabold", 12), background="#2BC911")
    bt_instalar_forge.grid(row=5,column=0,pady=5,sticky=tk.W)

    versiones_menu_desplegable.config(fg="#FFFFFF", font=(12), background="#2BC911")
    versiones_menu_desplegable.grid(row=6,column=0,pady=5,sticky=tk.W)
    
    bt_ejecutar_minecraft.config(command=ejecutar_minecraft,text='Iniciar',fg="#FFFFFF", font=("Antipasto Pro Extrabold", 12), background="#2BC911")
    bt_ejecutar_minecraft.grid(row=7,column=0,pady=5,sticky=tk.W)
    
    window.mainloop()

menu()