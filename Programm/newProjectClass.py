from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from functools import partial
from kivy.clock import Clock

import os
import time as t
import threading

import createDatabase
import loadDialogClass
import Global

save_path = ""
file_path = ""

class Progress(Popup):
    def __init__(self, title, **kwargs):
        super(Progress, self).__init__(**kwargs)
        self.title = title


class NewProjectFirstStep(Screen):

    def __init__(self, **kwargs):
        super(NewProjectFirstStep, self).__init__()
        self.file_path = ""
        self.save_path = ""
    
    #show the file-chooser with content of LoadDialog-Class as popup
    def show_load(self, orderType):
        self.orderType = orderType
        content = loadDialogClass.LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Select file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    #loads the Path which is choosen by filedialog
    def load(self, path, filename):
        if(self.orderType == "select"):
            self.file_choose_button.text = path
            self.file_path = path
        elif(self.orderType == "save"):
            self.save_choose_button.text = path
            self.save_path = path
        self.dismiss_popup()
    
    #standard popup cancel option
    def dismiss_popup(self):
        self._popup.dismiss()

    def nextStep(self):
        global save_path, file_path
        if(os.path.isdir(self.save_path) and os.path.isdir(self.file_path) and self.ids.name_input.text != ""):
            self.projectName = self.ids.name_input.text
            save_path = self.save_path + "/" + self.projectName
            if(not os.path.isdir(save_path)):
                file_path = self.file_path
                self.parent.current = "NewProjectSecondStep"
            else:
                save_path = ""
                showError("The project name \n you choose exists already")               
                

class NewProjectSecondStep(Screen):

    def __init__(self, **kwargs):
        super(NewProjectSecondStep, self).__init__(**kwargs)
        self.popup = Progress("Progress")

    def checkAngleValue(self, other):
        try:
            if(float(other.text) >= 85 ):
                showError("The angle can not be \n over 85 degrees")
                other.text = "85"
        except ValueError:
            if(other.text != ""):
                showError("The angle must be a float value")
                other.text = "85"

    def doit_in_thread(self):
        self.popup.open()
        threading.Thread(target=partial(self.makeProject)).start()

    def makeProject(self):
        config = [self.ids[i].text for i in self.ids]
        
        if ("" not in config):
            xbounds = int(config[3])
            os.mkdir(save_path)

            progress, text = 40, "Fill database"
            Clock.schedule_once(partial(self.do_update, progress, text))

            createDatabase.fill(save_path, file_path, xbounds)

            createDatabase.makeConfig(save_path, config)

            progress, text = 70, "Calculating"
            Clock.schedule_once(partial(self.do_update, progress, text))

            t.sleep(4)

            self.popup.dismiss()
            
            Global.changePath(save_path)

            self.parent.current = "WeldFigure"

        else:
            self.popup.dismiss()
            showError("incorrect input")

    def do_update(self, value, text, *args):
        self.popup.ids.progress.value = value
        self.popup.ids.progress_text.text = text


def showError(error):
    popup = Popup(title='Error',
        content=Label(text=error),
        size_hint=(None, None), size=(200, 200))
    popup.open()

    
