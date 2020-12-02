from kivy.config import Config

#change config of app for style
Config.set('kivy', 'exit_on_escape', 1) #!Set to 0

Config.set('graphics', 'window_state', 'maximized')

Config.set('graphics', 'resizable', 1)

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 100)
Config.set('graphics', 'top',  100)

Config.write()

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.core.window import Window
from kivy.uix.label import Label
#from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.graphics.transformation import Matrix
from kivy.clock import Clock

import os
import subprocess
import sys
import atexit

import newProjectClass
import actionBarClass
import loadDialogClass
import changeConfigClass
import scatterClass
import startScreenClass
import gridClass
import charts

import renderClass

import Global

workPath = ""

#main-app
class MyApp(App):
    title = "Weld prefing"
    icon = 'img/finalicon.png'
    window_state = "maximized"
    pass

#Window.clearcolor = (1, 1, 1, 1)

#Window.fullscreen = "auto"

#start programm
if __name__ == '__main__':
    MyApp().run()