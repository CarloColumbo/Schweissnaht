from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

import loadDialogClass
import Global

class StartScreen(Screen):
    def loadProject(self):
        content = loadDialogClass.LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Select file", content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()
    def dismiss_popup(self):
        self.popup.dismiss()

    #loads the Path which is choosen by filedialog
    def load(self, path, filename):
        Global.changePath(path)
        self.popup.dismiss()
        self.parent.current = "WeldFigure" #!Wrong