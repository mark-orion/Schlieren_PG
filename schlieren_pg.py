#!/usr/bin/env python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import ListProperty

class Pattern(Image):
    def __init__(self, **kwargs):
        super(Pattern, self).__init__(**kwargs)
        self.bgcolor = (0,0,0)
        self.fgcolor = (0.5,0.5,0.5)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
        self.draw_chequerboard(2)

    def draw_horlines(self, linesize):
        self.size_x, self.size_y = self.size
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
            Color(rgb=self.fgcolor)
            for n in range(0, self.size_y, linesize * 2):
                Rectangle(size=(self.size_x, linesize), pos=(0, n))

    def draw_verlines(self, linesize):
        self.size_x, self.size_y = self.size
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
            Color(rgb=self.fgcolor)
            for n in range(0, self.size_x, linesize * 2):
                Rectangle(size=(linesize, self.size_y), pos=(n, 0))

    def draw_chequerboard(self, fieldsize):
        increment = fieldsize * 2
        size_x, size_y = self.size
        size_x = size_x - fieldsize
        size_y = size_y - fieldsize
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
            Color(rgb=self.fgcolor)
            for v in range(0, size_y, increment):
                for h in range(0, size_x, increment):
                    Rectangle(size=(fieldsize, fieldsize), pos=(h, v))
                    Rectangle(size=(fieldsize, fieldsize), pos=(h + fieldsize, v + fieldsize))



class SchlierenPGApp(App):
    def build(self):
        # the individual elements
        output = Pattern()
        controlbar = BoxLayout(pos_hint={'x':0, 'y':0}, size_hint_x=0.5, size_hint_y=0.1)
        bigger = Button(text='+')
        smaller = Button(text='-')
        size = Label()
        choose_pattern = Spinner(text='CHQ', values=['CHQ', 'HOR', 'VER', 'RND'])
        showbar = ToggleButton(text='<-')

        # the layout
        controlbar.add_widget(bigger)
        controlbar.add_widget(size)
        controlbar.add_widget(smaller)
        controlbar.add_widget(choose_pattern)
        controlbar.add_widget(showbar)
        mainscreen = FloatLayout()
        mainscreen.add_widget(output)
        mainscreen.add_widget(controlbar)
        return mainscreen

if __name__ == "__main__":
    SchlierenPGApp().run()
