import pickle
import icecream
def save_config(variable, nombre_archivo):
    with open(nombre_archivo, 'wb') as file:
        pickle.dump(variable, file)

mi_variable = "Guardame en un archivo"
save_config(mi_variable, "Main/assets/ejemplo.pkl")

def load_config(nombre_archivo):
    with open(nombre_archivo, 'rb') as file:
        variable = pickle.load(file)
    return variable

tu_variable = load_config("Main/assets/ejemplo.pkl")
print(tu_variable)