#!/usr/bin/env python
import sys
import random
import argparse
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import ListProperty
from kivy.animation import Animation

class Pattern(Image):
    def __init__(self, **kwargs):
        super(Pattern, self).__init__(**kwargs)
        # defaults
        self.patternsize = 4
        self.patterntype = 'CHQ'
        self.bgcolor = (0,0,0)
        self.fgcolor = (1,1,1)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
        self.draw_pattern(self.patterntype, self.patternsize)

    def draw_pattern(self, ptype, psize):
        if ptype == 'VER':
            self.draw_verlines(psize)
        elif ptype == 'HOR':
            self.draw_horlines(psize)
        elif ptype == 'RND':
            self.draw_random(psize)
        else:
            self.draw_chequerboard(psize)

    def draw_horlines(self, psize):
        self.size_x, self.size_y = self.size
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
            Color(rgb=self.fgcolor)
            for n in range(0, self.size_y, psize * 2):
                Rectangle(size=(self.size_x, psize), pos=(0, n))

    def draw_verlines(self, psize):
        self.size_x, self.size_y = self.size
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
            Color(rgb=self.fgcolor)
            for n in range(0, self.size_x, psize * 2):
                Rectangle(size=(psize, self.size_y), pos=(n, 0))

    def draw_chequerboard(self, psize):
        increment = psize * 2
        size_x, size_y = self.size
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
            Color(rgb=self.fgcolor)
            for v in range(0, size_y, increment):
                for h in range(0, size_x, increment):
                    Rectangle(size=(psize, psize), pos=(h, v))
                    Rectangle(size=(psize, psize), pos=(h + psize, v + psize))

    def draw_random(self, psize):
        increment = psize * 2
        rndvar = psize / 2
        size_x, size_y = self.size
        self.canvas.clear()
        with self.canvas:
            Color(rgb=self.bgcolor)
            Rectangle(size=self.size, pos=self.pos)
            Color(rgb=self.fgcolor)
            for v in range(0, size_y, increment):
                for h in range(0, size_x, increment):
                    Rectangle(size=(psize, psize), pos=(h + random.randint(-rndvar, rndvar), v + random.randint(-rndvar, rndvar)))
                    Rectangle(size=(psize, psize), pos=(h + psize + random.randint(-rndvar, rndvar), v + psize + random.randint(-rndvar, rndvar)))



class SchlierenPGApp(App):
    def increase_size(self, instance):
        self.output.patternsize += 1
        self.size.text = str(self.output.patternsize)
        self.output.draw_pattern(self.output.patterntype, self.output.patternsize)

    def decrease_size(self, instance):
        self.output.patternsize -= 1
        if self.output.patternsize < 1:
            self.output.patternsize = 1
        self.size.text = str(self.output.patternsize)
        self.output.draw_pattern(self.output.patterntype, self.output.patternsize)

    def set_pattern(self, instance, value):
        self.output.patterntype = value
        self.output.draw_pattern(self.output.patterntype, self.output.patternsize)

    def toggle_controlbar(self, instance, value):
        if value == 'down':
            self.hide.start(self.controlbar)
        else:
            self.show.start(self.controlbar)

    def build(self):

        # the individual elements
        self.output = Pattern()
        self.controlbar = BoxLayout(pos_hint={'right':0.5, 'y':0}, size_hint_x=0.5, size_hint_y=0.1)
        self.bigger = Button(text='+')
        self.smaller = Button(text='-')
        self.size = Button(text=str(self.output.patternsize))
        self.choose_pattern = Spinner(text='CHQ', values=['CHQ', 'HOR', 'VER', 'RND'])
        self.showbar = ToggleButton(text='<-')

        # the layout
        self.controlbar.add_widget(self.bigger)
        self.controlbar.add_widget(self.size)
        self.controlbar.add_widget(self.smaller)
        self.controlbar.add_widget(self.choose_pattern)
        self.controlbar.add_widget(self.showbar)
        self.mainscreen = FloatLayout()
        self.mainscreen.add_widget(self.output)
        self.mainscreen.add_widget(self.controlbar)

        # the controlbar animation
        self.show = Animation(pos_hint={'right':0.5}, opacity=1.0)
        self.hide = Animation(pos_hint={'right':0.1}, opacity=0.2)

        # the command line parser
        parser = argparse.ArgumentParser(description='Schlieren Imaging Pattern Generator')
        parser.add_argument('-n', '--no_controlbar', action='store_true', help='hide controlbar')
        parser.add_argument('-p', '--pattern_type', default=self.choose_pattern.text, help='pattern type (CHQ, HOR, VER, RND)')
        parser.add_argument('-s', '--pattern_size', default=str(self.output.patternsize), help='pattern size')
        self.args = parser.parse_args(sys.argv[2:])

        # apply command line parameters
        if self.args.no_controlbar:
            self.controlbar.pos_hint={'right':-1}
        self.choose_pattern.text = self.args.pattern_type
        self.output.patterntype = self.args.pattern_type
        self.output.patternsize = int(self.args.pattern_size)
        self.size.text = str(self.output.patternsize)

        # the events
        self.bigger.bind(on_release=self.increase_size)
        self.smaller.bind(on_release=self.decrease_size)
        self.choose_pattern.bind(text=self.set_pattern)
        self.showbar.bind(state=self.toggle_controlbar)

        return self.mainscreen


if __name__ == "__main__":
    SchlierenPGApp().run()
