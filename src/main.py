import flet as ft

from ui import main_ui


if __name__ == '__main__':
    ft.run(main_ui.main)
    
    from core import config
    config.save_config()