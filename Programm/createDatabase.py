import sqlite3
import time as t###
from os import listdir
from os.path import isfile, join

import numpy as np

ybounds = 0
maxy = 0


def fill(path, file_path, scans_per_run):
    global ybounds
    global maxy

    def sortByLen(val):
        return len(val)
    files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    files.sort(key=sortByLen)

    with open(file_path + "/" + files[0]) as reader:
        ybounds = len(reader.read().splitlines())
    
    maxy = len(files) // scans_per_run

    array = np.zeros((maxy, scans_per_run, ybounds))

    start_time = t.time()
    for i in range(maxy * scans_per_run):
        x = i % scans_per_run
        y = i // scans_per_run
        if y % 2 == 1:
            x = scans_per_run - x - 1
        with open(file_path + "/" + files[i]) as reader:
            content = reader.read().splitlines()
            data = [abs(int(line)) for a, line in enumerate(content)]
            for i, e in enumerate(data):
                array[y, x, i] = e

    np.save(path + "/measure.npy", array)
    print(t.time() - start_time)

"""
def fill(path, file_path, scans_per_run):
    global ybounds
    global maxy

    def sortByLen(val):
        return len(val)
    files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    files.sort(key=sortByLen)

    with open(file_path + "/" + files[0]) as reader:
        ybounds = len(reader.read().splitlines())
    
    maxy = len(files) // scans_per_run

    array = np.zeros((scans_per_run, maxy, ybounds))

    start_time = t.time()
    for i in range(maxy * scans_per_run):
        y = i % scans_per_run
        x = i // scans_per_run
        if x % 2 == 1:
            y = scans_per_run - x - 1
        with open(file_path + "/" + files[i]) as reader:
            content = reader.read().splitlines()
            data = [abs(int(line)) for a, line in enumerate(content)]
            for i, e in enumerate(data):
                array[y, x, i] = e

    np.save(path + "/measure.npy", array)
    print(t.time() - start_time)


def fill(path, file_path, scans_per_run):
    global ybounds
    global maxy

    def sortByLen(val):
        return len(val)
    files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    files.sort(key=sortByLen)

    with open(file_path + "/" + files[0]) as reader:
        ybounds = len(reader.read().splitlines())
    
    maxy = len(files) // scans_per_run

    array = np.zeros((maxy, scans_per_run, ybounds))

    start_time = t.time()
    for i in range(maxy * scans_per_run):
        y = i % maxy
        x = i // maxy
        if y % 2 == 1:
            y = maxy - y - 1
        with open(file_path + "/" + files[i]) as reader:
            content = reader.read().splitlines()
            data = [abs(int(line)) for a, line in enumerate(content)]
            for i, e in enumerate(data):
                array[y, x, i] = e

    np.save(path + "/measure.npy", array)
    print(t.time() - start_time)
"""

def makeConfig(path, config):
    configType = ["angle", "height", "interval", "scans", "distance"]
    #configType = ["angle", "height", "interval"]
    string = ""

    for t, v in zip(configType, config):
        string += str(t) + "&" + str(v) + "\n"

    string += "ybounds&" + str(ybounds) + "\n"
    string += "maxy&" + str(maxy) + "\n"

    #string += "maxy&" + str(maxy) + "\n"
    #string += "scans&" + str(config[3]) + "\n"


    with open(path + "/config.txt", "w") as writer:
        writer.write(string)


