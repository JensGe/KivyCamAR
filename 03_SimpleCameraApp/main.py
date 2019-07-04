#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder

from android.permissions import request_permission, Permission, check_permission

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (1280, 960)
        play: False
        keep_ratio: True
        allow_stretch: True
        canvas.before:  
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix
    ToggleButton:
        text: 'Camera On'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '96dp'
        state: 'down'
''')


class CameraClick(BoxLayout):
    pass

class TestCamera(App):
    def build(self):
        if not check_permission(Permission.CAMERA):
            print('Permission for Camera not accepted, will request now')
            request_permission(Permission.CAMERA)
        else:
            print('Permission OK')
        return CameraClick()


if __name__ == '__main__':
    TestCamera().run()
