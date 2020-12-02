from kivy.uix.actionbar import ActionBar
from kivy.uix.popup import Popup

import os
import platform

import loadDialogClass
import changeConfigClass
import Global

class MyActionBar(ActionBar):

    def changeTitle(self):
        self.ids.showed_title.title = Global.path

    def loadNewProject(self):
        content = loadDialogClass.LoadDialog(load=self.actionBarLoad, cancel=self.dismiss_popup)
        self.popup = Popup(title="Select file", content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def changeConfig(self):
        content = changeConfigClass.ChangeConfig(cancel=self.dismiss_popup, change=self.changeView)
        self.popup = Popup(title="Change the config", content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()
    
    def actionBarLoad(self, path, filename):
        Global.changePath(path)
        self.popup.dismiss()
        self.changeView("Ascan")
        self.changeView("WeldFigure")

    def changeView(self, view):
        self.parent.parent.parent.current = view

    def openPDF(self, filename):
        if(platform.system() == "Windows"):
            cmd = 'start pdf/' + filename + '.pdf'
        else:
            cmd = 'xpdf pdf/' + filename + '.pdf'
        help = os.system(cmd)

    def dismiss_popup(self):
        self.popup.dismiss()