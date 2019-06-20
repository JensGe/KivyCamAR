from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty

import random


class ScatterTextWidget(BoxLayout):
    text_colour = ObjectProperty([1, 0, 0, 1])

    def __init__(self, **kwargs):
        super(ScatterTextWidget, self).__init__(**kwargs)

    def change_label_colour(self, *args):
        colour = [random.random() for i in range(3)] + [1]
        self.text_colour = colour


class SimpleKivyApp(App):
    def build(self):
        return ScatterTextWidget()


if __name__ == "__main__":
    SimpleKivyApp().run()

