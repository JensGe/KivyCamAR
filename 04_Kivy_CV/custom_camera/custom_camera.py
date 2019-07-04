from kivy.uix.camera import Camera
from kivy.properties import BooleanProperty, NumericProperty
from image_processing.image_processing import face_detection
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import kivy
import numpy as np
import cv2

from android.permissions import request_permission, Permission, check_permission

class CustomCamera(Camera):
    detectFaces = BooleanProperty(False)
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super(CustomCamera, self).__init__(**kwargs)

        self.isAndroid = kivy.platform == "android"
        if self.isAndroid:
            self.angle = -90

    def change_index(self, *args):
        new_index = 1 if self.index == 0 else 0
        self._camera._set_index(new_index)
        self.index = new_index
        self.angle = -90 if self.index == 0 else 90


    def on_tex(self, *l):
        image = np.frombuffer(self.texture.pixels, dtype='uint8')
        image = image.reshape(self.texture.height, self.texture.width, -1)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

        if self.detectFaces:
            image, faceRect = face_detection(image, (0, 255, 0, 255), self.angle)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
        numpy_data = image.tostring()
        self.texture.blit_buffer(numpy_data, bufferfmt="ubyte", colorfmt='rgba')
        super(CustomCamera, self).on_tex(self.texture)

    def get_cameras_count(self):
        cameras = 1
        if self.isAndroid:
            cameras = self._camera.get_camera_count()
        return cameras

    def toggle_camera(self):
        if not check_permission(Permission.CAMERA):
            request_permission(Permission.CAMERA)
        else:
            self.play = not self.play


class CameraWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(CameraWidget, self).__init__(orientation="vertical")
        if self.ids['camera'].get_cameras_count() > 1:
            self.ids['buttons'].add_widget(Button(text="Change Camera", on_press=self.ids['camera'].change_index))
