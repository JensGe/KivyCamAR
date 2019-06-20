from kivy.uix.camera import Camera
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

import kivy
import numpy as np
import cv2


class CustomCamera(Camera):
    angle = NumericProperty(0)
    bw = BooleanProperty(False)
    invert = BooleanProperty(False)
    edge = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(CustomCamera, self).__init__(**kwargs)

        self.isAndroid = kivy.platform == "android"
        if self.isAndroid:
            self.angle = -90

    def on_tex(self, *l):
        image = np.frombuffer(self.texture.pixels, dtype='uint8')
        image = image.reshape(self.texture.height, self.texture.width, -1)

        if self.edge:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            edges = cv2.Canny(image, 100, 200)
            image = cv2.cvtColor(edges, cv2.COLOR_BGR2RGBA)

        if self.bw:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)

        if self.invert:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            image = cv2.bitwise_not(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)


        numpy_data = image.tostring()
        self.texture.blit_buffer(numpy_data, bufferfmt="ubyte", colorfmt='rgba')
        super(CustomCamera, self).on_tex(self.texture)



class CameraWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(orientation="vertical")
