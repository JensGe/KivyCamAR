#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from plyer import notification


class ScatterTextWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(ScatterTextWidget, self).__init__(**kwargs)

    def do_notify(self, text='Hello'):
        notification.notify(message=text, toast=True)


class SimpleKivyApp(App):
    def build(self):
        return ScatterTextWidget()

    def on_pause(self):
        return True


if __name__ == "__main__":
    SimpleKivyApp().run()
