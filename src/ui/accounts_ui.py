import flet as ft

from core import config
from core import lang
from core import process

from services import accounts

from ui import main_ui

# -------------------------------
# Account Functions
# -------------------------------


def resize(event):
    accountDropdown.width = event.width/1.6
    accountCardColumn.width = event.width/1.5
    accountCardColumn.height = event.height/1.4
    accountsCard.width = event.width/1.6
    accountsCard.height = event.height/2.2

    addAccountColumn.width = event.width/1.6
    addAccountColumn.height = event.height/2.2
    addAccountType.width = event.width/1.7
    addAccountName.width = event.width/1.7
    addAccountPassword.width = event.width/1.7
    addAccountButton.width = event.width/1.7

    removeAccountColumn.width = event.width/1.6
    removeAccountColumn.height = event.height/2.2


def accountsParagraph(menu):
    menus = {lang.Add_Accounts_Title: addAccountColumn,
                lang.Delete_Accounts_Title: removeAccountColumn}
    accountsCard.content = menus[menu.data]
    accountsCard.update()
        
        
def update_account_displays(acc, accDel):
    updateAccounts(acc)
    updateRemoveAccounts(accDel)
        
        
def start_account_creation(event=None):
    process.add_process(accounts.add_account, 
                        addAccountType.value,
                        addAccountName.value,
                        addAccountPassword.value)
    update_account_displays(True, False)


def start_account_delete(event=None):
    process.add_process(accounts.del_account,
                                removeAccountDropdown.value)
    update_account_displays(True, True)


def updateAccounts(update):
    value, options = accounts.check_accounts()
    for i, option in enumerate(options):
        options[i] = ft.dropdown.Option(option)
    main_ui.accountsDropdown.value, main_ui.accountsDropdown.options = value, options

    if update:
        main_ui.accountsDropdown.update()


def updateRemoveAccounts(update):
    value, options = accounts.check_accounts()
    for i, option in enumerate(options):
        options[i] = ft.dropdown.Option(option)
    removeAccountDropdown.value, removeAccountDropdown.options = value, options
    
    if update:
        removeAccountDropdown.update()


# -------------------------------
# Account Variables
# -------------------------------


addAccountType = ft.Dropdown(lang.Default_Option,
                                options=[ft.dropdown.Option("Premiun"),
                                        ft.dropdown.Option("No Premiun")])

addAccountName = ft.TextField()


addAccountPassword = ft.TextField(password=True,
                                    can_reveal_password=True)


addAccountButton = ft.CupertinoFilledButton(lang.Add_Account_Button,
                                            icon=ft.Icons.ACCOUNT_BOX,
                                            on_click=start_account_creation)


addAccountColumn = ft.Column([addAccountType,
                                ft.Text(lang.Add_Account_Name, size=16),
                                addAccountName,
                                ft.Text(lang.Add_Account_Password, size=16),
                                addAccountPassword,
                                addAccountButton],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                scroll=ft.ScrollMode.AUTO)


removeAccountDropdown = ft.Dropdown(lang.Default_Option,
                                    options=[ft.dropdown.Option(account)
                                                for account in config.settings.Accounts])


removeAccountButton = ft.CupertinoFilledButton(lang.Delete_Account_Button,
                                                icon=ft.Icons.CANCEL,
                                                on_click=start_account_delete)


removeAccountColumn = ft.Column([removeAccountDropdown,
                                    removeAccountButton],
                                scroll=ft.ScrollMode.AUTO,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER)


accountDropdown = ft.Dropdown(lang.Add_Accounts_Title,
                                options=[ft.dropdown.Option(lang.Add_Accounts_Title),
                                        ft.dropdown.Option(lang.Delete_Accounts_Title)],
                                on_text_change=accountsParagraph)


accountsCard = ft.Card(addAccountColumn)


accountCardColumn = ft.Column([ft.Text(lang.Accounts_Title, size=36),
                                accountDropdown,
                                accountsCard],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER)