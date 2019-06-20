from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.lang import Builder
from custom_camera.custom_camera import CameraWidget

from android.permissions import request_permission, Permission, check_permission



Builder.load_file('custom_camera/custom_camera.kv')


class TestCamera(App):
    def build(self):
        if not check_permission(Permission.CAMERA):
            print('Permission for Camera not accepted, will request now')
            request_permission(Permission.CAMERA)
        else:
            print('Permission OK')

        return CameraWidget()

    def on_pause(self):
        return True


if __name__ == '__main__':
    TestCamera().run()
