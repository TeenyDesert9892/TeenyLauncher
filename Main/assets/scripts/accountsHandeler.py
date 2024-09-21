import minecraft_launcher_lib as mllb
import random

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
        

        try:
            auth_response = mllb.microsoft_types.MinecraftAuthenticateResponse(username=name, roles=[], access_token="", token_type="", expires_in=1)
            auth_token = mllb.microsoft_account.authenticate_with_minecraft(name, pasword)
            profile = mllb.microsoft_account.get_profile(access_token=auth_token)
            store_info = mllb.microsoft_account.get_store_information(access_token=auth_token)

            print(auth_response)
            print(auth_token)
            print(profile)
            print(store_info)

            setProgress(1)

            msg(lang.Add_Account_Premium_Success)

        except:
            msg(lang.Add_Account_Premium_Failure)

    elif type == "No Premiun":
        setMax(1)
        setProgress(0)
        setStatus(f"Creating {name} no premiun account")

        try:
            uuid = ""

            def create_chain(lenghth):
                chain = ""
                for i in range(0, lenghth):
                    num = random.randint(0, 15)
                    chain += str(dec_to_hex(num))
                return chain

            def dec_to_hex(num):
                letters = ["a", "b", "c", "d", "e", "f"]
                if num >= 0 and num <= 9:
                    return str(num)
                else:
                    return letters[num-10]

            uuid += create_chain(8)
            uuid += "-"

            for i in range(0, 3):
                uuid += create_chain(4)
                uuid += "-"

            uuid += create_chain(12)

            config.Accounts[name] = {'Uuid': uuid, 'Token': '0'}

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