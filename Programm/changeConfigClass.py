from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import numpy as np
import Global

class NewTextInput(TextInput):
    def __init__(self, **kwargs):
        super(NewTextInput, self).__init__(**kwargs)

class ChangeConfig(FloatLayout):
    cancel = ObjectProperty(None)
    change = ObjectProperty(None)
    config_box = ObjectProperty(None)
    
    def load(self):
        string = ""
        for child in self.config_box.children:
            text_input, label = child.children
            string += label.text + "&" + text_input.text + "\n"
        with open(Global.path + "/config.txt", "w") as writer:
            writer.write(string)
        #Global.renew_config()
        Global.get_config()
        self.change("StartScreen")
        self.change("WeldFigure")
        self.cancel()

    def renew_config():
        x = Global.config["scans"] * Global.config["maxy"]
        print(Global.config)
        Global.get_config()
        print(Global.config)
        print(Global.array.shape)
        new_x = int(x / Global.config["scans"])
        print(x, new_x)
        #array.reshape((new_x, int(config["scans"]), int(config["ybounds"])))

        array = np.reshape(array, (66, 100, 1024))
        print(array.shape)
        np.save(Global.path + "/measure.npy", array)


    def __init__(self, **kwargs):
        super(ChangeConfig, self).__init__(**kwargs)

        Clock.schedule_once(self.insertConfigData)

    def insertConfigData(self, clock=0):
        dic = Global.config
        number = len(dic)
        for row in dic:
            newBox = BoxLayout(orientation="horizontal")
            text = Label(text=row, font_size=newBox.height*0.3)
            config_input = NewTextInput(text=str(dic[row]))
            newBox.add_widget(text)
            newBox.add_widget(config_input)
            self.config_box.add_widget(newBox)