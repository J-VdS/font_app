# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:25:31 2019

@author: Jeroen VdS
"""
import os
import sys
from random import randint

#algemeen
import kivy
from kivy.app import App
from kivy.clock import Clock
#core
from kivy.core.window import Window
#achtergrond
from kivy.graphics import Color, Rectangle
#uix elementen
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView


#ToDo: aanpasbaar door de gebruiker
COLS = 2
ROWS = 4

kivy.require("1.10.1") #vw voor de versie

class HoofdScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        
        for i in range(25, 45):
            self.add_widget(Label(text="{} Abcde".format(i), font_size=i))

class ProductScreen(GridLayout):
    '''
        knoppen
        knop ('<', '>') en in het midden textinput voor aantal
        label met paginanr
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        
        self.paginaNr = 0
        self.prods = []
        self.prods_knoppen = []
        self.mode = 1
        self.mode_type = -1 #{-1: alles, 0: is eerste type in DATA.get_types()}
        
        topgrid = GridLayout(size_hint_y=0.1, cols=2, rows=1)
        #paginaNr:
        self.paginaNr_label = Label(
                text=f"Pagina {self.paginaNr+1}",
                size_hint_y=0.1,
                font_size=36)
        topgrid.add_widget(self.paginaNr_label)
        
        knop = Button(text="SORT", size_hint_x=0.25, font_size=22)
        knop.bind(on_press=self.type_sort)
        topgrid.add_widget(knop)
        self.add_widget(topgrid)
        
        #knopjes
        self.knopLayout = GridLayout(cols=COLS, padding=[10, 5], spacing=[15, 10])
        for _ in range(COLS*ROWS):
            self.prods_knoppen.append(Button(
                    text="spaghetti groenten normaal", halign="center",
                    font_size=38, markup=True,
                    background_normal = '',
                    background_color = (0,0.2,1,1)))
            self.prods_knoppen[-1].bind(on_press=self.klik, width=self._update_text_width)
            self.knopLayout.add_widget(self.prods_knoppen[-1])
            
        
        self.min_knop = Button(text="[b]-[/b]",
                               font_size=24, 
                               markup=True,
                               background_color = (0.5, 0.5, 0.5,1),
                               background_normal='',
                               size_hint_y=0.5)
        self.min_knop.bind(on_press=self.switch_mode)
        self.knopLayout.add_widget(self.min_knop)
        
        self.plus_knop = Button(text="[b]+[/b]",
                                font_size=24,
                                markup=True,
                                background_color=(0.8,0.8,0,1),
                                background_normal='',
                                size_hint_y=0.5)
        self.plus_knop.bind(on_press=self.switch_mode)
        self.knopLayout.add_widget(self.plus_knop)
        
        knop = Button(text="[b]<-[/b]",
                      font_size=24,
                      markup=True,
                      size_hint_y=0.5)
        knop.bind(on_press=self.switch_page)
        self.knopLayout.add_widget(knop)
        
        knop = Button(text="[b]->[/b]",
                      font_size=24,
                      markup=True,
                      size_hint_y=0.5)
        knop.bind(on_press=self.switch_page)
        self.knopLayout.add_widget(knop)
        
        self.add_widget(self.knopLayout)
        
        knop = Button(
                text="Huidige bestelling...",
                background_color=(0.1,0.7,0.3,1),
                background_normal='', #om donkere tint te vermijden
                size_hint_y=0.15,
                font_size=36)
        knop.bind(on_press=self.zie_huidig)
        self.add_widget(knop)
        
        
    def zie_huidig(self, _):
        pass
        
                
    def klik(self, instance, load_backup=False):
        pass

    
    def switch_mode(self, instance):
        if instance.text == "[b]+[/b]":
            self.mode = 1
            self.plus_knop.background_color = (0.8,0.8,0,1)
            self.min_knop.background_color = (0.5, 0.5, 0.5,1)
        else:
            self.mode = -1
            self.plus_knop.background_color = (0.5, 0.5, 0.5,1)
            self.min_knop.background_color = (0.8,0.8,0,1)
        
    
    def switch_page(self, instance):
        pass
    

    #knoppen
    def _update_text_width(self, instance, _):
        instance.text_size = (instance.width * .9, None)
        
        
    def type_selected(self, *_):       
        #close popup
        self.tpopup.dismiss()
        del self.tpopup
    
    
    #sorteren
    def type_sort(self, *_):
        self.tpopup = Popup(title="sorteren", width=Window.size[0]*0.4, size_hint_x=None)
        layout = GridLayout(cols=1)
        
        select_layout = GridLayout(cols=2)
        
        select_layout.add_widget(Label(text="alles", font_size=38))
        self._type_checkboxes = [CheckBox(group="select_type", size_hint_x=0.4, active=True)]
        select_layout.add_widget(self._type_checkboxes[-1])
        
        for type in ["gerechten", "dranken", "divers", "dessert"]:
            select_layout.add_widget(Label(text=type, font_size=38))
            self._type_checkboxes.append(CheckBox(group="select_type", size_hint_x=0.4))
            select_layout.add_widget(self._type_checkboxes[-1])
        
        layout.add_widget(select_layout)
        
        
        knop = Button(text="select",width=Window.size[0]*.75, font_size=22, size_hint_y=0.25)
        knop.bind(on_press=self.type_selected)
        layout.add_widget(knop)
        
        self.tpopup.add_widget(layout)                        
        self.tpopup.open()
                

class font_app(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def build(self):
        scherm = ProductScreen()
        return scherm

if __name__ == "__main__":
    font_app().run()