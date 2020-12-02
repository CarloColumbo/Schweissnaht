from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

import Global

#TODO: choose directions from other drives than c
#?Better to use kivy_garden.filebrowser???
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    def is_dir(self, path):
        return os.path.isdir(path)
