from kivy.uix.camera import Camera
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import kivy
import numpy as np
import cv2

from plyer import gravity


class CustomCamera(Camera):
    angle = NumericProperty(0)
    bw = BooleanProperty(False)
    invert = BooleanProperty(False)
    edge = BooleanProperty(False)
    horizon = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(CustomCamera, self).__init__(**kwargs)

        self.isAndroid = kivy.platform == "android"
        if self.isAndroid:
            self.angle = -90

    def on_tex(self, *l):
        image = np.frombuffer(self.texture.pixels, dtype='uint8')
        image = image.reshape(self.texture.height, self.texture.width, -1)

        if self.bw:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)

        if self.invert:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            image = cv2.bitwise_not(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

        if self.edge:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            edges = cv2.Canny(image, 100, 200)
            image = cv2.cvtColor(edges, cv2.COLOR_BGR2RGBA)

        if self.horizon:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            width, height, channels = image.shape

            x, y, z = self.get_grav()

            horizon_start = (int(height/2-z*128-x*64), 0)
            horizon_end = (int(height/2-z*128+x*64), width)

            cv2.line(image, horizon_start, horizon_end, (255, 255, 255), 3)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)



        numpy_data = image.tostring()
        self.texture.blit_buffer(numpy_data, bufferfmt="ubyte", colorfmt='rgba')
        super(CustomCamera, self).on_tex(self.texture)

    def get_grav(self):
        return gravity.gravity


class GravityInterface(BoxLayout):
    def __init__(self, **kwargs):
        super(GravityInterface, self).__init__(**kwargs)
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                gravity.enable()
                Clock.schedule_interval(self.get_gravity, 1 / 10.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Gravity Sensor"
            else:
                gravity.disable()
                Clock.unschedule(self.get_gravity)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Gravity Sensor"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Gravity sensor is not implemented " \
                     "for your platform"
            self.ids.status.text = status

    def get_gravity(self, dt):
        val = gravity.gravity

        if not val == (None, None, None):
            self.ids.x_label.text = "X: " + str(round(val[0], 3))
            self.ids.y_label.text = "Y: " + str(round(val[1], 3))
            self.ids.z_label.text = "Z: " + str(round(val[2], 3))


class CameraWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(orientation="vertical")
