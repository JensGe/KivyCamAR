from kivy.uix.camera import Camera
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.vector import Vector

import kivy
import numpy as np
from math import floor
import cv2

from plyer import gravity

compass_x = 0
compass_y = 0
compass_z = 0
compass_angle_xy = 0
compass_angle_xz = 0
compass_angle_xz_avg = 0


class CustomCamera(Camera):
    angle = NumericProperty(0)
    bw = BooleanProperty(False)
    invert = BooleanProperty(False)
    edge = BooleanProperty(False)
    gravity_horizon = BooleanProperty(False)
    compass_sun = BooleanProperty(False)

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

        if self.edge:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            edges = cv2.Canny(image, 100, 200)
            image = cv2.cvtColor(edges, cv2.COLOR_BGR2RGBA)

        if self.invert:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            image = cv2.bitwise_not(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

        if self.gravity_horizon:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            width, height, channels = image.shape

            x, y, z = self.get_grav()

            horizon_start = (int(height/2-z*128-x*64), 0)
            horizon_end = (int(height/2-z*128+x*64), width)

            cv2.line(image, horizon_start, horizon_end, (0, 255, 0), 3)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)

        if self.compass_sun:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

            width, height, channels = image.shape

            x, y, z = self.get_grav()

            compass_sun_x = ((compass_angle_xz_avg - 180) * width * 39.334 / 360)
            compass_sun_y = height / 2 - z * 128

            compass_sun_point = (int(compass_sun_y), int(compass_sun_x))
            compass_sun_color = (0, 200, 255)
            compass_sun_size = 50
            compass_sun_thickness = -1
            cv2.circle(image, compass_sun_point, compass_sun_size, compass_sun_color, compass_sun_thickness)
            print('Sun X: %s, Y: %s, Grav X: %s, Y: %s Z: %s, Picture Width: %s, Height: %s, NorthXZ: %s' % (
                str(compass_sun_x), str(compass_sun_y), str(x), str(y), str(z), str(width), str(height), str(compass_angle_xz)
            ))

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
        if not self.sensorEnabled:
            gravity.enable()
            Clock.schedule_interval(self.get_gravity, 1 / 10.)
            self.sensorEnabled = True
        else:
            gravity.disable()
            Clock.unschedule(self.get_gravity)
            self.sensorEnabled = False

    def get_gravity(self, dt):
        val = gravity.gravity

        if not val == (None, None, None):
            x_str, y_str, z_str = str(round(val[0], 3)), str(round(val[1], 3)), str(round(val[2], 3))
            self.ids.toggle_grav_btn.text = "Gravity\nX: %s\nY: %s\nZ: %s" % (x_str, y_str, z_str)


class CompassInterface(BoxLayout):

    compass_angle_xz_history = [0] * 10

    facade = ObjectProperty()
    compass_enabled = BooleanProperty(False)

    def toggle_compass(self):
        if not self.compass_enabled:
            self.facade.enable()
            Clock.schedule_interval(self.get_field, 1 / 10.)
            self.compass_enabled = True
        else:
            self.facade.disable()
            Clock.unschedule(self.get_field)
            self.compass_enabled = False


    def get_field(self, dt):

        global compass_x
        global compass_y
        global compass_z
        global compass_angle_xy
        global compass_angle_xz
        global compass_angle_xz_avg

        if not self.facade.field == (None, None, None):
            compass_x, compass_y, compass_z = self.facade.field


            compass_angle_xy = Vector(compass_x, compass_y).angle((0, 1)) + 90
            if (compass_angle_xy % 360) - compass_angle_xy > 180: compass_angle_xy += 360
            elif (compass_angle_xy % 360) - compass_angle_xy < -180: compass_angle_xy -= 360
            compass_angle_xy += 360 * floor(compass_angle_xy / 360.)

            compass_angle_xz = Vector(compass_x, compass_z).angle((0, 1)) + 90
            if (compass_angle_xz % 360) - compass_angle_xz > 180: compass_angle_xz += 360
            elif (compass_angle_xz % 360) - compass_angle_xz < -180: compass_angle_xz -= 360
            compass_angle_xz += 360 * floor(compass_angle_xz / 360.)

            compass_angle_xz = Vector(compass_x, compass_z).angle((0, 1)) + 90
            if (compass_angle_xz % 360) - compass_angle_xz > 180: compass_angle_xz += 360
            elif (compass_angle_xz % 360) - compass_angle_xz < -180: compass_angle_xz -= 360
            compass_angle_xz += 360 * floor(compass_angle_xz / 360.)

            del self.compass_angle_xz_history[0]
            self.compass_angle_xz_history.append(compass_angle_xz)
            compass_angle_xz_avg = sum(self.compass_angle_xz_history) / len(self.compass_angle_xz_history)

            self.ids.compass_toggle_btn.text = "Compass\nXY: %s\nXZ: %s\nXZ': %s" % (
                str(round(compass_angle_xy, 2)),
                str(round(compass_angle_xz, 2)),
                str(round(compass_angle_xz_avg, 2))
            )


class CameraWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(orientation="vertical")

