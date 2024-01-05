import os
import pickle

file = "assets/config.pkl"

def save_config(var):
    with open(file, 'wb') as pklfile:
        pickle.dump(var, pklfile)

def load_config():
    with open(file, 'rb') as pklfile:
        variable = pickle.load(pklfile)
    return variable

def check_config():
    if not os.path.exists("Main/assets/config.pkl"):
        default_config = [{"Accounts":{"Default":{"Name": "User","Online": False,}}},{"Launcher":{"Color": "dark"}}]
        save_config(default_config)