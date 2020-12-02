from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty

# kivy3
from kivy3 import Renderer, Scene, Vector3
from kivy3 import PerspectiveCamera

# geometry
from kivy3.extras.geometries import SphereGeometry, BoxGeometry
from kivy3 import Material, Mesh

import math

import calculationClass
import Global


class My3DScreen(Screen):
    layout = ObjectProperty()
    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def __init__(self, **kwargs):
        super(My3DScreen, self).__init__(**kwargs)

        self.look_at = Vector3(0, 0, -1)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        #root = FloatLayout()
        self.camera = PerspectiveCamera(75, 0.3, 1, 1000)
        self.radius = 10
        self.phi = 90
        self.theta = 0
        self._touches = []
        self.camera.pos.z = self.radius
        self.camera.look_at((0, 0, 0))
        #root = self.layout

    def make_3d(self, clock=None):

        #self.root = FloatLayout()
        self.renderer = Renderer()
        self.renderer.set_clear_color((.2, .2, .2, 1.))

        self.scene = Scene()

        #geometry = BoxGeometry(0.5, 0.5, 0.5)
        geometry = SphereGeometry(0.1)
        material = Material(color=(0., 0., 1.), diffuse=(1., 1., 0.),
            specular=(.35, .35, .35))

        """
        a = 5
        liste = []
        i = 0
        for z in range(-5, -35, -1):
            for x in range(-5, 5):
                liste.append(Mesh(geometry, material))
                liste[-1].pos.x = x
                liste[-1].pos.y = -i
                liste[-1].pos.z = z
                print(x, -i, z)
                self.scene.add(liste[-1])
            i+=1
        """
        #!erster test für errecnete Daten
        liste = []
        for z in range(0, int(Global.config["maxy"])):
        #for z in range(0, 10):
            #i = 0
            test = calculationClass.find_mistakes_along_x_axis(z)
            #print(test)
            for x, y, rad in calculationClass.find_mistakes_along_x_axis(z):
            #for x, y in [[1, 2], [2, 0], [2.314, 5], [3, 0], [3.123, 4]]:
            #for x, y in [[1, 2], [2, 0], [3, 0]]:
            #for x in [8.06158101842821, 4.06158101842821, 0.09813725490196079]:
            #for x in test[:][0]:
            #for line in test[:10]:
                #x = line[0]
                x = float(x)
                y = float(y)
                #x = 8.06158101842821
                #new_list.append([x, y, z, rad])
                rad = 1
                #y = 0
                z += 5
                liste.append(Mesh(geometry, material))
                #liste[-1].pos.x = x - 8
                liste[-1].pos.x = -z
                liste[-1].pos.y = y
                liste[-1].pos.z = x
                #print(x, y, z)
                self.scene.add(liste[-1])
                #i += 1

        self.renderer.render(self.scene, self.camera)

        self.renderer.bind(size=self._adjust_aspect)

        self.layout.add_widget(self.renderer)

        print(liste[0])
        print(liste[0].pos)
        #self.look_at = liste[0].pos


        #self.look_at.x = liste[0][0]
        #self.look_at.y = liste[0][1]
        #self.look_at.z = liste[0][2]
        #self.camera.look_at(self.look_at)
        #test = (liste[0][0], liste[0][1], liste[0][2])
        #a = tuple(liste[0].pos)
        #print(a)
        #self.camera.look_at(a)
        #self.look_at.x = liste[0].pos.x
        #self.look_at.y = liste[0].pos.y
        #self.look_at.z = liste[0].pos.z
        self.look_at = Vector3(0, 0, -1)

        #self.camera.look_at(self.look_at)

        #self.add_widget(self.root)
        print("here")
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.camera.pos.y += 0.2
            #self.look_at.y += 0.2
        elif keycode[1] == 's':
            self.camera.pos.y -= 0.2
            #self.look_at.y -= 0.2
        elif keycode[1] == 'a':
            self.camera.pos.x -= 0.2
            #self.look_at.x -= 0.2
        elif keycode[1] == 'd':
            self.camera.pos.x += 0.2
            #self.look_at.x += 0.2
        elif keycode[1] == '-':
            self.camera.pos.z += 0.2
            #self.look_at.z += 0.2
        elif keycode[1] == '+':
            self.camera.pos.z -= 0.2
            #self.look_at.z -= 0.2

        elif keycode[1] == 'up':
            self.look_at.y += 0.2
        elif keycode[1] == 'down':
            self.look_at.y -= 0.2
        elif keycode[1] == 'right':
            self.look_at.x += 0.2
        elif keycode[1] == 'left':
            self.look_at.x -= 0.2

        elif keycode[1] == "q":
            self.camera.rotation.y += 1

        self.camera.look_at(self.look_at)

    def define_rotate_angle(self, touch):
        theta_angle = (touch.dx / self.width) * -360
        phi_angle = -1 * (touch.dy / self.height) * 360
        return phi_angle, theta_angle

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                #self.look_at -= 0.2
                self.camera.pos -= 0.2
            elif touch.button == 'scrollup':
                #self.look_at += 0.2
                self.camera.pos += 0.2

        touch.grab(self)
        self._touches.append(touch)
        
        self.camera.look_at(self.look_at)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        self._touches.remove(touch)

    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                self.do_rotate(touch)
            elif len(self._touches) == 2:
                pass

    def do_rotate(self, touch):
        d_phi, d_theta = self.define_rotate_angle(touch)
        self.phi += d_phi
        self.theta += d_theta

        _phi = math.radians(self.phi)
        _theta = math.radians(self.theta)
        z = self.radius * math.cos(_theta) * math.sin(_phi)
        x = self.radius * math.sin(_theta) * math.sin(_phi)
        y = self.radius * math.cos(_phi)
        self.camera.pos = x, y, z
        self.camera.look_at((0, 0, 0))
    
    def on_enter(self, *args):
        super(My3DScreen, self).on_enter(*args)
        #self.remove_widget(self.renderer)
        #mat = Material()
        #box = BoxGeometry(0.5, 0.5, 0.5)
        #cube = Mesh(box, mat)
        #cube.pos.z = -4
        #self.scene.add(cube)
        Clock.schedule_once(self.make_3d)
        #self.renderer.render(self.scene, self.camera)
        #self.add_widget(self.renderer)