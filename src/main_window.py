if __name__ == '__main__':
    import flet as ft
    
    from scripts.configHandeler import configHandeler
    ConfigHandeler = configHandeler()
    
    from scripts.langHandeler import langHandeler
    LangHandeler = langHandeler()
    
    from scripts.jdkHandeler import jdkHandeler
    JdkHandeler = jdkHandeler()
    
    from scripts.processHandeler import processHandeler
    ProcessHandeler = processHandeler()
    
    from scripts.instanceHandeler import instanceHandeler
    InstanceHandeler = instanceHandeler()
    
    from scripts.accountHandeler import accountHandeler
    AccountHandeler = accountHandeler()
    
    from scripts import mainGui as MainGui
    
    ft.app(MainGui.gui)
    ConfigHandeler.save_config()