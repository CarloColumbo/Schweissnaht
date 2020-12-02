import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

import Global

#TODO: read config

def plotBScan2D():

    data = Global.array[line_number]

    fig, ax = plt.subplots()

    ax.set_title('2D BScan of line %i' % line_number)

    ax.tick_params(axis='x')
    ax.tick_params(axis='y')

    CS = ax.contourf(np.transpose(data))

    cbar = fig.colorbar(CS)
    cbar.ax.set_ylabel('amplitude')

    canvas = fig.canvas
    plt.show()

def plotBScan3D():

    Z = Global.array[line_number]
    #X = np.arange(0, Global.config["scans"])
    #Y = np.arange(0, Global.config["ybounds"])
    Y = np.arange(0, Global.config["scans"])
    X = np.arange(0, Global.config["ybounds"])

    fig = plt.figure(figsize=plt.figaspect(2.))
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    ax.set_title('3D BScan of line %i' % line_number)

    ax.tick_params(axis='x')
    ax.tick_params(axis='y')

    X, Y = np.meshgrid(X, Y)
    Z = Z.reshape(X.shape)

    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    #ax.plot_surface(data, rstride=8, cstride=8, alpha=0.3)
    plt.show()

def plotCScan():
    if Global.array.ndim < 4:
        return

    #data, X, Y = sqlPort.getValuesBySurface(time)
    data = np.sum(Global.array, 2) / Global.config["ybounds"]

    fig, ax = plt.subplots()

    ax.set_title('CScan of time %i' % time)

    ax.tick_params(axis='x')
    ax.tick_params(axis='y')

    CS = ax.contourf(data)

    cbar = fig.colorbar(CS)
    cbar.ax.set_ylabel('amplitude')

    plt.show()


scanType = sys.argv[1]
Global.path = sys.argv[2]
Global.get_config()
Global.make_array()

if(scanType == "2D"):
    line_number = int(sys.argv[3])
    plotBScan2D()
elif(scanType == "3D"):
    line_number = int(sys.argv[3])
    plotBScan3D()
elif(scanType == "CScan"):
    time = int(sys.argv[3])
    plotCScan()
else:
    print("Not Implemented")