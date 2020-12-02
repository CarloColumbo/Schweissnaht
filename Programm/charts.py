from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas,\
                                                NavigationToolbar2Kivy

import sys
import numpy as np
import matplotlib.pyplot as plt
import subprocess

import Global
import sliderClass

import time #!not needed

fore_color = 'white'

plt.rcParams["text.color"] = fore_color
plt.rcParams["axes.labelcolor"] = fore_color
plt.rcParams["xtick.color"] =  fore_color
plt.rcParams["ytick.color"] = fore_color

plt.style.use('dark_background')
plt.rc('grid', linestyle=":", color='gray')

class Testscan(Screen):
    file_name = ObjectProperty(None)
    my_graph = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Testscan, self).__init__(**kwargs)
        self.oldPlot = 0
        Clock.schedule_once(self.bindEvent)
    
    def bindEvent(self, clock):
        self.ids.slider.bind(on_release=self.changeTime)

    def changeTime(self, obj):
        self.time = int(obj.value)
        self.updateChart()


    #function to configurate the chart
    #TODO: read from config file
    def configChart(self, clock):
        self.xbounds = Global.config["scans"]
        self.ybounds = Global.config["maxx"]

        self.timeInterval = 14
        self.ids.slider.max = Global.config["ybounds"] - 1

    def popPlot(self):
        plot = subprocess.Popen([sys.executable, "plot.py"] + ["CScan", str(Global.path), str(self.time)])

    def updateChart(self, clock=0):

        self.data, self.X, self.Y = sqlPort.getValuesBySurfaceTest()

        fig, ax = plt.subplots(facecolor='black')

        my_mpl_kivy_widget = FigureCanvas(fig)

        ax.set_xlabel('x', fontsize=15)
        ax.set_ylabel('y', fontsize=15)

        CS = ax.contourf(self.X, self.Y, self.data)
        cbar = plt.colorbar(CS)

        cbar.set_label('amplidtude')

        nav2 = NavigationToolbar2Kivy(my_mpl_kivy_widget)

        self.my_box.clear_widgets()
        self.my_box.add_widget(nav2.actionbar)
        self.my_box.add_widget(my_mpl_kivy_widget)
    
    def on_enter(self):
        super(Testscan, self).on_enter()
        if(not Global.alreadyLoaded["Testscan"]):
            Global.alreadyLoaded["Testscan"] = True
            Clock.schedule_once(self.configChart)
            Clock.schedule_once(self.updateChart)

class Cscan(Screen):
    file_name = ObjectProperty(None)
    my_graph = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Cscan, self).__init__(**kwargs)
        self.oldPlot = 0
        Clock.schedule_once(self.bindEvent)
    
    def bindEvent(self, clock):
        self.ids.slider.bind(on_release=self.changeTime)

    def changeTime(self, obj):
        self.time = int(obj.value)
        self.updateChart()


    #function to configurate the chart
    #TODO: read from config file
    def configChart(self, clock):
        self.xbounds = Global.config["scans"]
        self.ybounds = Global.config["maxy"]

        self.timeInterval = 14
        self.ids.slider.max = Global.config["ybounds"] - 1
        self.ids.slider.value = 0

        self.time = 0

    def popPlot(self):
        plot = subprocess.Popen([sys.executable, "plot.py"] + ["CScan", str(Global.path), str(self.time)])

    def updateChart(self, clock=0):
        print(Global.array.shape)
        if Global.array.shape[0] <= 1:
            label = Label(text='Nicht genug Daten')
            self.my_box.clear_widgets()
            self.my_box.add_widget(label)
            return

        #self.data, self.X, self.Y = sqlPort.getValuesBySurface(self.time)
        self.data = np.sum(Global.array, 2) / Global.config["ybounds"]
        print(self.data)

        fig, ax = plt.subplots(facecolor='black')

        my_mpl_kivy_widget = FigureCanvas(fig)

        ax.set_xlabel('x', fontsize=15)
        ax.set_ylabel('y', fontsize=15)

        #CS = ax.contourf(self.X, self.Y, self.data)
        CS = ax.contourf(self.data)
        cbar = plt.colorbar(CS)

        cbar.set_label('amplidtude')

        nav2 = NavigationToolbar2Kivy(my_mpl_kivy_widget)

        self.my_box.clear_widgets()
        self.my_box.add_widget(nav2.actionbar)
        self.my_box.add_widget(my_mpl_kivy_widget)
    
    def on_enter(self):
        super(Cscan, self).on_enter()
        if(not Global.alreadyLoaded["CScan"]):
            Global.alreadyLoaded["CScan"] = True
            Clock.schedule_once(self.configChart)
            Clock.schedule_once(self.updateChart)

#class for the B-Scans
class Bscan2(Screen):
    file_name = ObjectProperty(None)
    my_graph = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Bscan2, self).__init__(**kwargs)
        self.oldPlot = 0
        Clock.schedule_once(self.bindEvent)
    
    def bindEvent(self, clock):
        self.ids.slider.bind(on_release=self.changeLine)

    #function to configurate the chart
    #TODO: read from config file
    def configChart(self, clock):
        self.xbounds = Global.config["scans"]
        self.ybounds = Global.config["ybounds"]

        self.timeInterval = 14

        self.maxLine = Global.config["scans"]
        self.ids.slider.max = self.maxLine
        self.ids.slider.value = 0

        self.numberOfLine = 0

    def changeLine(self, obj):
        self.numberOfLine = int(obj.value)
        self.updateChart(0)

    def updateChart(self, clock):
        plt.figure(1)

        self.data, self.X, self.Y = sqlPort.getValuesByLine2(self.numberOfLine)

        fig, ax = plt.subplots(facecolor='black')

        my_mpl_kivy_widget = FigureCanvas(fig)

        ax.set_xlabel('x', fontsize=15)
        ax.set_ylabel('time', fontsize=15)

        CS = ax.contourf(self.X, self.Y, self.data)
        cbar = plt.colorbar(CS)

        cbar.set_label('amplidtude')

        nav1 = NavigationToolbar2Kivy(my_mpl_kivy_widget)

        self.my_box.clear_widgets()
        self.my_box.add_widget(nav1.actionbar)
        self.my_box.add_widget(my_mpl_kivy_widget)
    
    def popPlot(self, scanType):
        plot = subprocess.Popen([sys.executable, "plot.py"] + [scanType, str(Global.path), str(self.numberOfLine)])

    def on_enter(self):
        super(Bscan2, self).on_enter()
        if(not Global.alreadyLoaded["BScan2"]):
            Global.alreadyLoaded["BScan2"] = True
            Clock.schedule_once(self.configChart)
            Clock.schedule_once(self.updateChart)

#class for the B-Scans
class Bscan(Screen):
    file_name = ObjectProperty(None)
    my_graph = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Bscan, self).__init__(**kwargs)
        self.oldPlot = 0
        Clock.schedule_once(self.bindEvent)
    
    def bindEvent(self, clock):
        self.ids.slider.bind(on_release=self.changeLine)

    #function to configurate the chart
    #TODO: read from config file
    def configChart(self, clock):
        self.xbounds = Global.config["scans"]
        self.ybounds = Global.config["ybounds"]

        self.timeInterval = 14

        self.maxLine = Global.config["maxy"]
        self.ids.slider.max = self.maxLine - 1
        self.ids.slider.value = 0

        self.numberOfLine = 0

    def changeLine(self, obj):
        self.numberOfLine = int(obj.value)
        self.updateChart(0)

    def updateChart(self, clock):
        plt.figure(1)

        self.Y = np.arange(0, Global.config["scans"])
        self.X = np.arange(0, Global.config["ybounds"])
        self.data = Global.array[self.numberOfLine]

        fig, ax = plt.subplots(facecolor='black')

        my_mpl_kivy_widget = FigureCanvas(fig)

        ax.set_xlabel('x', fontsize=15)
        ax.set_ylabel('time', fontsize=15)

        CS = ax.contourf(np.transpose(self.data))
        cbar = plt.colorbar(CS)

        cbar.set_label('amplidtude')

        nav1 = NavigationToolbar2Kivy(my_mpl_kivy_widget)

        self.my_box.clear_widgets()
        self.my_box.add_widget(nav1.actionbar)
        self.my_box.add_widget(my_mpl_kivy_widget)
    
    def popPlot(self, scanType):
        plot = subprocess.Popen([sys.executable, "plot.py"] + [scanType, str(Global.path), str(self.numberOfLine)])

    def on_enter(self):
        super(Bscan, self).on_enter()
        if(not Global.alreadyLoaded["BScan"]):
            Global.alreadyLoaded["BScan"] = True
            Clock.schedule_once(self.configChart)
            Clock.schedule_once(self.updateChart)


#class for the A-Scans
class Ascan(Screen):

    def __init__(self, **kwargs):
        super(Ascan, self).__init__(**kwargs)
        self.oldPlot = 0
        self.X, self.Y = 0, 0

    #function to configurate the chart
    #TODO: read from config file
    def configChart(self, clock):
        self.xbounds = Global.config["scans"]
        self.ybounds = Global.config["ybounds"]

    #sets label text to number of a-scan
    def updateLabel(self, clock=0):
        self.ids.pos_y.text = str(self.Y)
        self.ids.pos_x.text = str(self.X)

    #calls next line in array
    def nextPosition(self):
        self.X += 1
        self.updateChart()
    
    #calls previous line in array
    def previousPosition(self):
        self.X -= 1
        self.updateChart()

    def inputNumberOfPosition(self):
        self.X = int(self.ids.pos_x.text)
        self.Y = int(self.ids.pos_y.text)
        self.updateChart()

    def getPosPara(self):
        if(self.X >= Global.config["scans"]):
            self.Y += int(self.X // Global.config["scans"])
            self.X %= int(Global.config["scans"])
            #self.X = int(self.X)
        elif(self.X < 0 and self.Y > 0):
            self.Y -= 1
            self.X = int(Global.config["scans"] - 1)
        elif(self.X < 0 or self.Y < 0):
            self.X, self.Y = 0, 0
        if(self.Y > Global.config["maxy"] - 1):
            self.Y = int(Global.config["maxy"]) - 1

    #updates the chart
    def updateChart(self, clock=0):
        start_time = time.time()
        self.getPosPara()
        self.updateLabel()
        plt.figure(1)

        print(self.X, self.Y)

        self.data = Global.array[self.Y, self.X]

        fig, ax = plt.subplots(facecolor='black')

        my_mpl_kivy_widget = FigureCanvas(fig)

        ax.set_xlabel('time in 14/1024 \u03BCs', fontsize=15)
        ax.set_ylabel('amplitude', fontsize=15)

        print("Here1", time.time() - start_time)
        start_time = time.time()
       
        major_ticks_x = np.arange(0, 1020, 100)
        major_ticks_y = np.arange(0, 1020, 100)
        minor_ticks = np.arange(0, 1020, 10)

        print("Here2", time.time() - start_time)
        start_time = time.time()

        ax.set_xticks(major_ticks_x)
        #ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(major_ticks_y)
        #ax.set_yticks(minor_ticks, minor=True)
        print("Here3", time.time() - start_time)
        start_time = time.time()

        ax.grid()

        CS = ax.plot(self.data)

        nav1 = NavigationToolbar2Kivy(my_mpl_kivy_widget)

        self.my_box.clear_widgets()
        self.my_box.add_widget(nav1.actionbar)
        self.my_box.add_widget(my_mpl_kivy_widget)

    def on_enter(self):
        super(Ascan, self).on_enter()
        if(not Global.alreadyLoaded["AScan"]):
            Global.alreadyLoaded["AScan"] = True
            Clock.schedule_once(self.configChart)
            Clock.schedule_once(self.updateChart)

