from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Color, Ellipse, Line, Rectangle

import numpy as np

import Global
import calculationClass

proportion_text = StringProperty("Proportion: ")

first_check = ObjectProperty(None)
second_check = ObjectProperty(None)
third_check = ObjectProperty(None)

percentage = ObjectProperty(None)

#Object in which the Canvas will be drawed
class Grid(Widget):
    property_text = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.angle_of_welt, self.height_of_welt = 80, 500
        self.grid_size = 10
        #Clock.schedule_once(self.orderSize)
        Clock.schedule_once(self.drawMainBody)
        Clock.schedule_once(self.draw_grid)

    def configCanvas(self):
        self.angle_of_welt = 90 - Global.config["angle"]
        height = Global.config["height"]
        self.updateCanvas(height)

    #updates Canvas to draw
    def updateCanvas(self, height):
        self.alignCanvas()
        #self.height_of_welt = 500
        self.height_of_welt = Global.config["height"] * 100

        f = lambda x: (self.parent.width/2) - (x/np.tan((np.pi*self.angle_of_welt)/180))
        while(f(self.height_of_welt) < 20):
            self.height_of_welt -= 5

        self.size_comparissen = round(height / (self.height_of_welt/100), 4)

        Clock.schedule_once(self.updateLabel)
        self.drawMainBody(0)
        self.draw_grid(0)

    def updateLabel(self, clock=0):
        self.parent.parent.parent.parent.parent.proportion_text = "Proportion: 1: {}".format(self.size_comparissen)

    #draws welt without errors
    def drawMainBody(self, clock=0):
        self.canvas.after.clear()

        with self.canvas.after:
            Color(1, 1, 1, 1)

            width = 2

            height = 40
            heightWelt = self.height_of_welt
            add_left = 40
            self.add_right = self.parent.width - add_left
            self.add_bottom = self.parent.y + self.grid_size*10

            middle = (self.add_right+add_left)/2
            self.middle = middle
            add_x = (self.height_of_welt/np.tan((np.pi*self.angle_of_welt)/180))
            new_x_1 = middle - add_x
            new_x_2 = middle + add_x

            start = new_x_1 - heightWelt
            end = new_x_2 + heightWelt
            if(start < 0):
                start = 0
                end = self.parent.width

            Line(points=[start, self.add_bottom, end, self.add_bottom], width=width)
            Line(points=[start, self.add_bottom + self.height_of_welt, new_x_1, self.add_bottom + self.height_of_welt], width=width)
            Line(points=[new_x_2, self.add_bottom + self.height_of_welt, end, self.add_bottom + self.height_of_welt], width=width)
            
            Line(points=[middle, self.add_bottom, new_x_1, self.add_bottom + self.height_of_welt], width=width)
            Line(points=[middle, self.add_bottom, new_x_2, self.add_bottom + self.height_of_welt], width=width)
            
            Line(ellipse=[new_x_1, self.add_bottom + self.height_of_welt - height/2, 2*add_x, 40, -90, 90], width=width)

    #draws background of canvas, but is copied
    def draw_grid(self, asdf=0):
        self.canvas.before.clear()
        with self.canvas.before:
            
            #draw background
            Color(0.616, 0.639, 0.667, mode='rgb')
            Rectangle(size=self.parent.size)

            #draw grid
            #grid_size = 10

            Color(0.576, 0.600, 0.627, mode='rgb')

            x_length, y_length = [int(abs(i)) for i in self.parent.size]

            for i in range(0,x_length, self.grid_size):
                Line(points=[i, 0, i, y_length])

            for i in range(0,y_length, self.grid_size):
                Line(points=[0, i, x_length, i])

            Color(0.537, 0.557, 0.580, mode='rgb')

            for i in range(0,x_length, self.grid_size*10):
                Line(points=[i, 0, i, y_length], width=1.05)

            for i in range(0,y_length, self.grid_size*10):
                Line(points=[0, i, x_length, i], width=1.05)
    
    #Todo: self size than container
    def orderSize(self, clock):
        #print(self.parent.parent.parent)
        #self.size = self.parent.parent.parent.size
        print("self")

    #aligns canvas
    def alignCanvas(self):
        self.parent.scale = 1
        #self.parent.height = self.parent.parent.height
        self.parent.pos = self.parent.parent.pos
        #self.parent.size = (500, 500)

    def drawMistakes(self, obj):
        self.configCanvas()
        self.draw_grid()
        y = int(obj.value)
        increase = self.height_of_welt / Global.config["height"]
        polygons = calculationClass.find_mistakes_along_x_axis(
            y, 
            self.middle / increase, 
            first_check.active, 
            second_check.active,
            third_check.active,
            float(percentage.text)
        )

        self.circles = []
        for e in polygons:
           self.drawCircle(e)
        #    break
        #self.drawCircle(polygons[2])
        #print(self.circles)
        #self.drawPolygone()
        pass

    def drawPolygone(self):
        for i in range(0, len(self.circles)-1, 2):
            with self.canvas.after:
                Line(points=self.circles[i]+self.circles[i+1], color="red")

    def drawCircle(self, points):
        increase = self.height_of_welt / Global.config["height"]
        #print(increase)
        points[1] *= increase
        #print(points)
        points[1] += self.add_bottom
        #print(points)
        #points[0] = self.middle - points[0] * increase

        points[0] *= increase

        points[2] *= increase
        #points[0] += self.add_right
        #print(points)
        with self.canvas.after:
            line = Line(circle=points, color="red")
            self.circles.append(points[:2])

class WeldFigure(Screen):
    #overwrites the layout of FloatLayout and makes minsize
    proportion_label = ObjectProperty(None)
    #global proportion_text
    proportion_text = StringProperty("Proportion: ")

    def on_enter(self):
        super(WeldFigure, self).on_enter()
        if(not Global.alreadyLoaded["WeldFigure"]):
            Global.alreadyLoaded["WeldFigure"] = True
            Clock.schedule_once(self.after__init__)

    def after__init__(self, clock):
        global first_check, second_check, third_check, percentage
        first_check = self.first_check
        second_check = self.second_check
        third_check = self.third_check
        #percentage = self.percentage_slider
        percentage = self.input

        self.ids.my_canvas.ids.grid.configCanvas()
        self.ids.slider.max = Global.config['maxy'] - 1 #?maxx
        self.ids.slider.bind(on_release=self.ids.my_canvas.ids.grid.drawMistakes)

        #self.percentage_slider.max = 500
        #self.percentage_slider.min = 0
        
        self.first_check.bind(active=self.on_active_checkbox_other)
        self.second_check.bind(active=self.on_active_checkbox_other)
        self.third_check.bind(active=self.on_active_checkbox)
        self.ids.my_canvas.ids.grid.drawMistakes(self.ids.slider)

    def on_active_checkbox(self, checkbox, value):
        if value:
            self.first_check.active = False
            self.second_check.active = False

    def on_active_checkbox_other(self, checkbox, value):
        if value:
            self.third_check.active = False