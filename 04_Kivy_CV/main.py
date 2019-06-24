from kivy.app import App
from custom_camera.custom_camera import CameraWidget, CustomCamera

from kivy.base import Builder

from android.permissions import request_permission, Permission, check_permission


Builder.load_file("custom_camera/custom_camera.kv")

class TestCamera(App):

    def build(self):

        if not check_permission(Permission.CAMERA):
            print('Permission for Camera not accepted, will request now')
            request_permission(Permission.CAMERA)
        else:
            print('Permission OK')

        camera = CameraWidget()
        return camera


TestCamera().run()
