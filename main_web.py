if __name__ == '__main__':
    import flet as ft
    
    from scripts.configHandeler import configHandeler
    ConfigHandeler = configHandeler()
    
    from scripts.langHandeler import langHandeler
    LangHandeler = langHandeler()
    
    from scripts.jdkHandeler import jdkHandeler
    JdkHandeler = jdkHandeler()
    
    from scripts.instanceHandeler import instanceHandeler
    InstanceHandeler = instanceHandeler()
    
    from scripts.accountHandeler import accountHandeler
    AccountHandeler = accountHandeler()
    
    from scripts.mainGui import mainGui
    
    ft.app(mainGui, assets_dir=".", view=None, port=9892, host="0.0.0.0")
    ConfigHandeler.save_config()