# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:25:31 2019

@author: Jeroen VdS
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class HoofdScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        
        for i in range(25, 45):
            self.add_widget(Label(text="{} Abcde".format(i), font_size=i))



class font_app(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def build(self):
        scherm = HoofdScherm()
        return scherm

if __name__ == "__main__":
    font_app().run()