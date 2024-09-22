import minecraft_launcher_lib as mllb

from __main__ import configHandeler

config = configHandeler.config
lang = configHandeler.lang


def add_account(type, name, pasword, setStatus, setProgress, setMax, msg):

    for account in config.Accounts:
        if account == name:
            msg(lang.Add_Account_Name_Already_Exsists)
            return

    if name == "":
        msg(lang.Add_Account_Name_Remaining)
        return

    if type == "Premium":
        if pasword == "":
            msg(lang.Add_Account_Password_Remaining)
            return

        setMax(1)
        setProgress(0)
        setStatus(f"Adding {name} premiun account")
        
        msg("This function is disabled untill I am able to make it work")
        return

        try:
            client_id = "" # azure app
            redirect_url = "" # azure app

            login_url, state, code_verifier = mllb.microsoft_account.get_secure_login_data(client_id, redirect_url)

            print(f"Please open {login_url} in your browser and copy the url you are redirected into the prompt below.")
            code_url = input()

            try:
                auth_code = mllb.microsoft_account.parse_auth_code_url(code_url, state)
            except AssertionError:
                print("States do not match!")
                return
            except KeyError:
                print("Url not valid")
                return

            mllb.microsoft_account.complete_login(client_id, None, redirect_url, auth_code, code_verifier)

            setProgress(1)

            msg(lang.Add_Account_Premium_Success)

        except:
            msg(lang.Add_Account_Premium_Failure)

    elif type == "No Premiun":
        setMax(1)
        setProgress(0)
        setStatus(f"Creating {name} no premiun account")

        try:
            config.Accounts[name] = {'Uuid': mllb.utils.uuid.uuid4(), 'Token': '0'}

            setProgress(1)

            msg(lang.Add_Account_No_Premium_Success)
        except:
            msg(lang.Add_Account_No_Premium_Failure)
    else:
        msg(lang.Add_Account_No_Type_Selected)


def del_account(removedAccount, setStatus, setProgress, setMax, msg):
    setMax(1)
    setProgress(0)
    setStatus(f"Deleting {removedAccount} account")

    try:
        newAccounts = {}
        for account in config.Accounts:
            if account != removedAccount:
                newAccounts[account] = {'Uuid': config.Accounts[account]["Uuid"],
                                            'Token': config.Accounts[account]["Token"]}
        config.Accounts = newAccounts

        setProgress(1)

        msg(lang.Delete_Account_Success)
    except:
        msg(lang.Delete_Account_Failure)


def check_accounts():
    accounts = ""
    list_added_accounts = []

    for account_added in config.Accounts:
        list_added_accounts.append(account_added)

    if len(list_added_accounts) != 0:
        if config.DefaultAccount == "" or config.DefaultAccount == lang.Without_Accounts:
            config.DefaultAccount = list_added_accounts[0]
        is_added = False

        for account_added in list_added_accounts:
            if config.DefaultAccount == account_added:
                is_added = True

        if not is_added:
            config.DefaultAccount = list_added_accounts[0]
        accounts = config.DefaultAccount

    elif len(list_added_accounts) == 0:
        accounts = lang.Without_Accounts
        list_added_accounts.append(lang.Without_Accounts)

    return accounts, list_added_accounts