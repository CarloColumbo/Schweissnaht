from kivy.uix.scatter import Scatter

#Scatter to zoom and translate
class CustomScatter(Scatter):

    #*copied from https://groups.google.com/forum/#!topic/kivy-users/gyS2EqOk_Mw
    #to click menu and not canvas
    def collide_point(self, x, y):
        x0, y0 = self.to_local(self.x, self.y)
        x1, y1 = self.to_local(self.right, self.top)
        if (x > x0 and x < x1 and y > y0 and y < y1):
            return True
        else:
            return False
    
    #*copied from https://github.com/melissadale/Learning-Kivy/blob/master/ZoomPanning/zoom.py
    #TODO: Zoom by mouseposition
    #function for zooming and translation
    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        self.prev_x = touch.x
        self.prev_y = touch.y

        if (touch.is_mouse_scrolling):
            if (touch.button == 'scrolldown'):
                ## zoom in
                if self.scale < 100:
                    self.scale = self.scale * 1.1
                    #self.pos = (self.x * 1.1, self.y * 1.1)

            elif (touch.button == 'scrollup'):
                ## zoom out
                if self.scale > 0.1:
                    self.scale = self.scale * 0.8
                    #self.pos = (self.x * 0.8, self.y * 0.8)
        
        # if the touch isnt on the widget we do nothing
        #? What is that????
        if not self.do_collide_after_children:
            if not self.collide_point(x, y):
                return False

        if not self.do_translation_x and \
                not self.do_translation_y and \
                not self.do_scale:
            return False

        touch.grab(self)
        self._touches.append(touch)
        self._last_touch_pos[touch] = touch.pos

        return True