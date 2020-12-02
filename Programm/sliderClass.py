from kivy.uix.slider import Slider

#https://gist.github.com/hchandad/b71ed0e977e6d345bcb8
class MySlider(Slider):

    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        super(MySlider, self).__init__(**kwargs)

    def on_release(self):
        pass

    def on_touch_up(self, touch):
        super(MySlider, self).on_touch_up(touch)
        if touch.grab_current == self:
            self.dispatch('on_release')
            return True