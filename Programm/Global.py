import numpy as np

path = r"C:\Users\karlm\Desktop\Semi\Programm\Version21\test"
config = {}
array = np.array([])
alreadyLoaded = {"WeldFigure": False, "AScan": False, "BScan": False, "BScan2": False, "CScan": False, "Testscan": False}

def get_config():
    for e in alreadyLoaded:
        alreadyLoaded[e] = False
    with open(path + "/config.txt", "r") as reader:
        for line in reader.read().splitlines():
            option, value = line.split("&")
            config[option] = float(value)

def make_array():
    global array
    array = np.load(path + "/measure.npy")

def changePath(new):
    global path
    path = new
    get_config()
    make_array()
