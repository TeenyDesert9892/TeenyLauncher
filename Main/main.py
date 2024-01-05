import customtkinter as ctk
import minecraft_launcher_lib
from scripts import configpkl, mcfunctios

print("This code was made by TeenyDesert9892")

configpkl.check_config()
config = configpkl.load_config()
launcher = config[1]["Launcher"]["Color"]

ctk.set_appearance_mode(launcher)
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.geometry("800x500")
window.iconbitmap("assets/Icon.ico")
window.title("Teeny Launcher")
window.resizable(width=False, height=False)

info = ctk.CTkFrame(master=window, width=500,height=480)
mineconf = ctk.CTkFrame(master=window, width=260,height=480)

acount_display = ctk.CTkOptionMenu(master=mineconf)
entry_ram = ctk.CTkEntry(master=mineconf)

installVersions = ctk.CTkButton(master=mineconf)
uninstallVersions = ctk.CTkButton(master=mineconf)

versions_display = ctk.CTkOptionMenu(master=mineconf)
updateVersions = ctk.CTkButton(master=mineconf)
iniciar_minecraft = ctk.CTkButton(master=mineconf)

def check_vers():
    vers = ctk.StringVar()
    lista_versiones_instaladas = []
    versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(mcfunctios.minecraft_directori)

    for version_instalada in versiones_instaladas:
        lista_versiones_instaladas.append(version_instalada['id'])

    if len(lista_versiones_instaladas) != 0:
        vers.set(lista_versiones_instaladas[0])
    elif len(lista_versiones_instaladas) == 0:
        vers.set('Sin versiones instaladas')
        lista_versiones_instaladas.append('Sin versiones instaladas')
    versions_display.configure(variable=vers, values=lista_versiones_instaladas)

def message(msg):
    winmsg = ctk.CTk()
    winmsg.geometry("300x200")
    winmsg.iconbitmap("assets/Icon.ico")
    winmsg.title("Mensaje")
    winmsg.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winmsg, width=280, height=140)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    msgtxt = ctk.CTkLabel(master=frame, text=msg, font=("", 16),wraplength=280)
    msgtxt.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    msgbtn = ctk.CTkButton(master=winmsg,text="Ok", font=("", 16),command=winmsg.destroy)
    msgbtn.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    winmsg.mainloop()

def install_versions():
    winins = ctk.CTk()
    winins.geometry("300x200")
    winins.iconbitmap("assets/Icon.ico")
    winins.title("Instalar versiones")
    winins.resizable(width=False, height=False)

    frame = ctk.CTkFrame(master=winins, width=280, height=180)
    frame.grid_propagate(False)
    frame.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    ver_name = ctk.CTkEntry(master=frame)
    ver_name.configure(placeholder_text="Numero de la version", font=("",16))
    ver_name.grid(row=0, column=0, pady=5, padx=5, sticky="nswe")

    ver_types = ["Vanilla", "Forge", "Fabric", "Quilt"]
    def_ver_type = ctk.StringVar(value="Selecciona el tipo e version")

    type_display = ctk.CTkOptionMenu(master=frame,values=ver_types,variable=def_ver_type)
    type_display.configure(font=("", 16))
    type_display.grid(row=1, column=0, pady=5, padx=5, sticky="nswe")

    install_button = ctk.CTkButton(master=frame)
    install_button.configure(text="Instalar", font=("", 16), command=lambda: mcfunctios.verif_ver(ver_name.get(), type_display.get()))
    install_button.grid(row=2, column=0, pady=5, padx=5, sticky="nswe")

    winins.mainloop()

def uninstall_versions():
    winuns = ctk.CTk()
    winuns.geometry("300x200")
    winuns.iconbitmap("assets/Icon.ico")
    winuns.title("Desinstalar versiones")
    winuns.resizable(width=False, height=False)

    display = ctk.CTkOptionMenu(master=winuns,font=("",16))
    display.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    button = ctk.CTkButton(master=winuns,text="Desinstalar",font=("", 24),command=lambda: mcfunctios.uninstall_minecraft_version(display.get()))
    button.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    vers = ctk.StringVar()
    lista_versiones_instaladas = []

    versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(mcfunctios.minecraft_directori)

    for version_instalada in versiones_instaladas:
        lista_versiones_instaladas.append(version_instalada['id'])

    if len(lista_versiones_instaladas) != 0:
        vers.set(lista_versiones_instaladas[0])
    elif len(lista_versiones_instaladas) == 0:
        vers.set('Sin versiones instaladas')
        lista_versiones_instaladas.append('Sin versiones instaladas')

    display.configure(variable=vers, values=lista_versiones_instaladas)

    winuns.mainloop()

def menu():
    info.grid_propagate(False)
    info.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")

    mineconf.grid_propagate(False)
    mineconf.grid(row=0, column=1, pady=10, padx=10, sticky="nswe")

    title = ctk.CTkLabel(master=mineconf, text="Configuracion Minecraft", font=("", 24))
    title.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    acount_display.configure(font=("",16))
    acount_display.grid(row=1, column=0, pady=5, padx=5, sticky="we")

    entry_ram.configure(placeholder_text="Uso de ram",font=("",16))
    entry_ram.grid(row=2, column=0, pady=5, padx=5, sticky="we")

    installVersions.configure(text="Instalar versiones de Minecraft", font=("", 16), command=install_versions)
    installVersions.grid(row=3, column=0, pady=5, padx=5, sticky="we")

    uninstallVersions.configure(text="Desinstalar versiones de Minecraft", font=("", 16), command=uninstall_versions)
    uninstallVersions.grid(row=4, column=0, pady=5, padx=5, sticky="we")

    versions_display.configure(font=("",16))
    versions_display.grid(row=5, column=0, pady=5, padx=5, sticky="we")

    iniciar_minecraft.configure(text="Inicar Minecraft", font=("", 16), command=lambda: mcfunctios.ejecutar_minecraft(versions_display.get(), f"-Xmx{entry_ram.get()}G"))
    iniciar_minecraft.grid(row=6, column=0, pady=5, padx=5, sticky="we")

    window.mainloop()

if __name__ == "__main__":
    check_vers()
    menu()