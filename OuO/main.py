from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition

from consts import colors, paths
from kivy.graphics import *

import time

from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.graphics.vertex_instructions import Rectangle, RoundedRectangle
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import Canvas
from kivy.properties import ObjectProperty

import hashlib
import json
import os
from datetime import datetime
import math as m
from kivy.uix.popup import Popup


class Card():
    def __init__(self, content: dict):
        
        self.init_from_dict(content)
        self.textview = AnchorLayout()

        # TODO make text view

    def init_from_dict(self, content: dict) -> None:

        self.faces = content["faces"]
        self.type = content["type"]
        self.proficiency = content["proficiency"]
        self.due = content["due"]

    def todict(self) -> dict:
        card = {}
        card["faces"] = self.faces
        card["type"]  = self.type
        card["proficiency"] = self.proficiency
        card["due"] = self.due
        return card


    def get_proficiency(self):
        return self.proficiency
    
    def set_proficiency(self, level):
        self.proficiency = level

    def mod_proficiency(self, level):
        if level == 0:
            self.proficiency /= 2
        elif level == 1:
            pass
        elif level == 2:
            self.proficiency *= 2
        elif level == 3:
            self.proficiency *= 3
        else:
            raise ValueError

    def get_due(self):
        return self.due

    def set_due(self, date):
        self.due = date

    def is_due(self) -> bool:
        if self.due != "New":
            if datetime.now() > self.due:
                return True
            else:
                return False
        else:
            return False

class Deck():
    def __init__(self, content: dict):

        self.textview = RelativeLayout()
        self.cardview = RelativeLayout()

        self.name = content["name"]
        self.pot = content["pot"]
        self.cards = content["cards"]
        self.importance = content["importance"]
        self.learning_rate = content["learning_rate"]

        self.whole = self.cards
        self.untouched = [self.cards[card] for card in self.cards if self.cards[card].get_due() == "New"]
        self.covered = [self.cards[card] for card in self.cards if self.cards[card].get_due() != "New"]
        self.due = [self.cards[card] for card in self.cards if self.cards[card].is_due()]

        self.anchors = Anchors()

        


        self.card_editor = RelativeLayout()

        self.card_editor.size_hint = (.7, .7)
        self.card_editor.pos_hint = {"center_x": .5, "center_y": .5}

        self.card_editor.anti_clickthrough = Button()
        self.card_editor.anti_clickthrough.size_hint = (None, None)
        self.card_editor.anti_clickthrough.size = (dp(10000), dp(10000))
        self.card_editor.anti_clickthrough.pos = (-5000, -5000)
        self.card_editor.anti_clickthrough.background_normal = ''
        self.card_editor.anti_clickthrough.background_color = (0, 0, 0, 0)
        self.card_editor.add_widget(self.card_editor.anti_clickthrough)

        
        self.card_editor.background_rectangle = BackgroundLGRAY()
        

        self.card_editor.add_widget(self.card_editor.background_rectangle)

        self.card_editor.anchors = Anchors()


        self.card_editor.title = Label()
        self.card_editor.title.text = "Add a Card"
        self.card_editor.title.size_hint = (1, None)
        self.card_editor.title.height = dp(50)
        self.card_editor.title.font_name = "Comfortaa"
        self.card_editor.title.color = colors.WHITE
        self.card_editor.title.pos_hint = {"center_x": .5, "center_y": .9}

        

        self.card_editor.escape = Button()
        self.card_editor.escape.on_press = self.close_card_edit
        self.card_editor.escape.text = "X"
        self.card_editor.escape.font_name = "ComfortaaBold"
        self.card_editor.escape.background_normal = ''
        self.card_editor.escape.background_color = colors.FLAME
        self.card_editor.escape.size_hint = (None, None)
        self.card_editor.escape.size = (dp(50), dp(50))

        self.card_editor.anchors.positions[2].add_widget(self.card_editor.escape)

        self.card_editor.confirm = Button()
        self.card_editor.confirm.on_press = self.create_card
        self.card_editor.confirm.text = u"\u2713"
        self.card_editor.confirm.font_name = "ArialUnicode"
        self.card_editor.confirm.background_normal = ''
        self.card_editor.confirm.background_color = colors.PGREEN
        self.card_editor.confirm.size_hint = (None, None)
        self.card_editor.confirm.size = (dp(50), dp(50))

        self.card_editor.anchors.positions[0].add_widget(self.card_editor.confirm)

        self.card_editor.face_inputs = BoxLayout()
        self.card_editor.face_inputs.orientation = "vertical"

        self.card_editor.faces = []

        self.make_input()
        self.make_input()
        self.make_input()

        self.card_editor.add_input_button = Button()
        self.card_editor.add_input_button.text = "Add another Face"
        self.card_editor.add_input_button.font_name = "ComfortaaBold"
        self.card_editor.add_input_button.background_normal = ''
        self.card_editor.add_input_button.background_color = colors.FLAME
        self.card_editor.add_input_button.size_hint = (None, None)
        self.card_editor.add_input_button.size = (dp(50), dp(50))
        self.card_editor.add_input_button.on_press = self.make_input
        
        self.reload_inputs()

        self.card_editor.add_widget(self.card_editor.title)
        self.card_editor.add_widget(self.card_editor.anchors.positions[0])
        self.card_editor.add_widget(self.card_editor.anchors.positions[2])
        self.card_editor.add_widget(self.card_editor.face_inputs)
        self.card_editor.add_widget(self.card_editor.add_input_button)



        self.untouchedlabel = Button()
        self.untouchedlabel.text = str(len(self.untouched))
        self.untouchedlabel.background_normal = ''
        self.untouchedlabel.background_color = colors.FLAME
        self.untouchedlabel.size_hint = (1/3, 1/3)
        self.untouchedlabel.font_size = min(self.untouchedlabel.height/6, self.untouchedlabel.width/6)

        self.duelabel = Button()
        self.duelabel.text = str(len(self.due))
        self.duelabel.background_normal = ''
        self.duelabel.background_color = colors.SGREEN
        self.duelabel.size_hint = (1/3, 1/3)
        self.duelabel.font_size = min(self.duelabel.height/6, self.duelabel.width/6)

        self.namelabel = Button()
        self.namelabel.text = self.name
        self.namelabel.background_normal = ''
        self.namelabel.background_color = colors.BLUE
        self.namelabel.size_hint = (1, 1/3)
        self.namelabel.color = colors.GRAY

        self.background = Button()
        self.background.background_normal = ''
        self.background.background_color = colors.WHITE
        self.background.text = ''
        self.background.on_press = self.open_card_edit

        self.anchors.positions[4].add_widget(self.background)
        self.anchors.add_widget(self.anchors.positions[4])

        self.anchors.positions[7].add_widget(self.namelabel)
        self.anchors.add_widget(self.anchors.positions[7])

        self.anchors.positions[0].add_widget(self.untouchedlabel)
        self.anchors.add_widget(self.anchors.positions[0])
        
        self.anchors.positions[2].add_widget(self.duelabel)
        self.anchors.add_widget(self.anchors.positions[2])

        self.cardview.add_widget(self.anchors)

    def fromdict(self, content: dict) -> None:
        self.name = content["name"]
        self.pot = content["pot"]
        self.cards = []

        for i in range(len(content["cards"])):
            self.cards[i] = Card(content["cards"][str(i)])
        
        self.importance = content["importance"]
        self.learning_rate = content["learning_rate"]
    
    def todict(self) -> dict:
        deck = {}
        deck["name"] = self.name
        deck["pot"] = self.pot

        deck["cards"] = []

        for i in range(len(self.cards)):
            deck["cards"][i] = self.cards[i].todict()
        
        deck["importance"] = self.importance
        deck["learning_rate"] = self.learning_rate
        return deck

    def make_input(self):
        index = len(self.card_editor.faces)
        self.card_editor.faces.append(TextInput())

        self.card_editor.faces[index].font_name = "Comfortaa"
        self.card_editor.faces[index].hint_text = f"Face {index + 1}"
        self.card_editor.faces[index].background_normal = ''
        self.card_editor.faces[index].background_color = colors.GRAY
        self.card_editor.faces[index].foreground_color = colors.WHITE
        self.card_editor.faces[index].size_hint = (.6, None)
        self.card_editor.faces[index].height = dp(50)
        self.card_editor.faces[index].multiline = False
        self.card_editor.faces[index].pos_hint = {"center_x":.4, "center_y":.5}

        self.reload_inputs()
        
    def reload_inputs(self):
        # for fa in self.card_editor.faces[:-1]:
        #     self.cardview.remove_widget(fa)
        
        for ba in self.card_editor.faces:
            try:
                self.card_editor.face_inputs.add_widget(ba)
            except:
                pass
                

    def add_card(self, content: Card) -> None:
        self.cards.append(content)

    def create_card(self):
        temp = {}
        # TODO
        self.add_card(temp)

    def open_card_edit(self):
        print("a")
        self.cardview.parent.parent.parent.add_widget(self.card_editor)

    def close_card_edit(self):
        self.card_editor.parent.remove_widget(self.card_editor)

class DecksMenu(RelativeLayout):
    def __init__(self, cards, setts, username, **kwargs):
        super().__init__(**kwargs)

        self.username = username

        self.acc_decks = [cards[card] for card in cards]

        self.acc_decks = [Deck(deck) for deck in self.acc_decks]
        
        self.acc_settings = setts

        self.cardWidth = 100
        self.spacingSize = 10
        self.paddingSize = 50

        Window.clearcolor = colors.GRAY

        self.scroll = ScrollView()

        self.scroll.size=(Window.width, Window.height)


        self.scroll.bar_color = colors.WHITE
        self.scroll.bar_width = dp(12)
        self.scroll.scroll_distance = dp(80)

        
        # * default oreintation is horizontal

        self.load()

        
        self.add_widget(self.scroll)

        self.bottom_buttons = BoxLayout()

        self.new_deck_button = Button()
        self.new_deck_button.text = "New Deck"
        self.new_deck_button.size_hint = (1, None)
        self.new_deck_button.height = dp(50)
        self.new_deck_button.on_press = self.goto_deck_adding


        self.stats_button = Button()
        self.stats_button.text = "Stats"
        self.stats_button.size_hint = (1, None)
        self.stats_button.height = dp(50)
        self.stats_button.on_press = self.goto_stats


        self.manage_button = Button()
        self.manage_button.text = "Manage"
        self.manage_button.size_hint = (1, None)
        self.manage_button.height = dp(50)

        self.bottom_buttons.add_widget(self.new_deck_button)
        self.bottom_buttons.add_widget(self.stats_button)
        self.bottom_buttons.add_widget(self.manage_button)

        self.add_widget(self.bottom_buttons)

        self.top_loc = StackLayout()
        self.top_loc.orientation = "rl-tb"

        self.top_buttons = BoxLayout()
        

        self.settings_button = Button()
        self.settings_button.text = "Settings"
        self.settings_button.size_hint = (None, None)
        self.settings_button.size = (dp(100), dp(50))
        self.settings_button.on_press = self.goto_settings


        self.search_button = Button()
        self.search_button.text = "Search"
        self.search_button.size_hint = (None, None)
        self.search_button.size = (dp(100), dp(50))

        self.top_bar = TextInput()
        self.top_bar.multiline = False
        self.top_bar.hint_text = "Search Query"
        self.top_bar.size_hint = (None, None)
        self.top_bar.height = dp(50)
        self.top_bar.width = dp(500)
        self.top_bar.background_normal = ''
        self.top_bar.background_color = colors.GRAY
        self.top_bar.foreground_color = colors.WHITE
        self.top_bar.font_name = "Comfortaa"
        self.top_bar.font_size = 40

        self.top_loc.add_widget(self.top_bar)
        self.top_loc.add_widget(self.search_button)
        self.top_loc.add_widget(self.settings_button)

        # self.top_loc.add_widget(self.top_buttons)

        self.add_widget(self.top_loc)

    def goto_settings(self):
        self.add_widget(SettingsPage())

    def goto_deck_adding(self):
        self.add_widget(DeckAddPage())

    def goto_stats(self):
        self.add_widget(StatsPage())
    
    def load(self):

        try:
            for deck in self.acc_decks[:-1]:
                self.boxes.remove_widget(deck.cardview)
        except AttributeError:
            pass
        
        try:
            self.scroll.remove_widget(self.boxes)
        except AttributeError:
            pass

        self.init_boxes()


        for deck in self.acc_decks:

            deck.cardview.size_hint = (None, None)
            deck.cardview.size = (dp(self.cardWidth), dp(self.cardWidth * 1.5))

            self.boxes.add_widget(deck.cardview)
    
    def init_boxes(self):
        self.boxes = StackLayout()

        self.boxes.bind(minimum_height=self.boxes.setter('height'))

        self.boxes.padding = dp(self.paddingSize)

        self.boxes.size_hint = (1, None)

        self.boxes.orientation = "lr-tb"
        self.boxes.spacing = dp(self.spacingSize)
        self.boxes.background_color = colors.PGREEN

        self.scroll.add_widget(self.boxes)


class SettingsPage(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7, .7)
        self.pos_hint = {"center_x": .5, "center_y": .5}


        self.anti_clickthrough = Button()
        self.anti_clickthrough.size_hint = (None, None)
        self.anti_clickthrough.size = (dp(10000), dp(10000))
        self.anti_clickthrough.pos = (-5000, -5000)
        self.anti_clickthrough.background_normal = ''
        self.anti_clickthrough.background_color = (0, 0, 0, 0)
        self.add_widget(self.anti_clickthrough)

        
        self.background_rectangle = BackgroundLGRAY()
        


        self.add_widget(self.background_rectangle)

        self.anchors = Anchors()

        self.title = Label()
        self.title.text = "Settings"
        self.title.size_hint = (1, None)
        self.title.height = dp(50)
        self.title.font_name = "Comfortaa"
        self.title.color = colors.WHITE
        self.title.pos_hint = {"center_x": .5, "center_y": .9}

        self.ouch = Label()
        self.ouch.text = "None at the moment, sorry"
        self.ouch.size_hint = (1, None)
        self.ouch.height = dp(50)
        self.ouch.font_name = "Comfortaa"
        self.ouch.color = colors.WHITE
        self.ouch.pos_hint = {"center_x": .5, "center_y": .5}

        self.escape = Button()
        self.escape.on_press = self.close
        self.escape.text = "X"
        self.escape.background_normal = ''
        self.escape.background_color = colors.FLAME
        self.escape.size_hint = (None, None)
        self.escape.size = (dp(50), dp(50))

        self.anchors.positions[2].add_widget(self.escape)

        self.add_widget(self.title)
        self.add_widget(self.ouch)
        self.add_widget(self.anchors.positions[2])
    
    def close(self):
        self.parent.remove_widget(self)


class DeckAddPage(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7, .7)
        self.pos_hint = {"center_x": .5, "center_y": .5}

        self.anti_clickthrough = Button()
        self.anti_clickthrough.size_hint = (None, None)
        self.anti_clickthrough.size = (dp(10000), dp(10000))
        self.anti_clickthrough.pos = (-5000, -5000)
        self.anti_clickthrough.background_normal = ''
        self.anti_clickthrough.background_color = (0, 0, 0, 0)
        self.add_widget(self.anti_clickthrough)
        
        self.background_rectangle = BackgroundLGRAY()
        


        self.add_widget(self.background_rectangle)

        self.anchors = Anchors()

        self.title = Label()
        self.title.text = "Add a Deck"
        self.title.size_hint = (1, None)
        self.title.height = dp(50)
        self.title.font_name = "Comfortaa"
        self.title.color = colors.WHITE
        self.title.pos_hint = {"center_x": .5, "center_y": .9}

        self.escape = Button()
        self.escape.on_press = self.close
        self.escape.text = "X"
        self.escape.font_name = "ComfortaaBold"
        self.escape.background_normal = ''
        self.escape.background_color = colors.FLAME
        self.escape.size_hint = (None, None)
        self.escape.size = (dp(50), dp(50))

        self.anchors.positions[2].add_widget(self.escape)

        self.confirm = Button()
        self.confirm.on_press = self.create_deck
        self.confirm.text = u"\u2713"
        self.confirm.font_name = "ArialUnicode"
        self.confirm.background_normal = ''
        self.confirm.background_color = colors.PGREEN
        self.confirm.size_hint = (None, None)
        self.confirm.size = (dp(50), dp(50))

        self.anchors.positions[0].add_widget(self.confirm)

        self.name = TextInput()
        self.name.font_name = "Comfortaa"
        self.name.hint_text = "deck name"
        self.name.background_normal = ''
        self.name.background_color = colors.GRAY
        self.name.foreground_color = colors.WHITE
        self.name.size_hint = (.6, None)
        self.name.height = dp(50)
        self.name.multiline = False
        self.name.pos_hint = {"center_x":.4, "center_y":.5}



        self.pot = CheckBox()

        self.pot.size_hint = (None, None)
        self.pot.size = (dp(20), dp(20))

        self.pot.bind(active=self.on_pot_active)

        self.pot.pos_hint = {"center_x":.8, "center_y":.5}

        self.pot_label = Label()
        self.pot_label.text = "Universal"
        self.pot_label.color = colors.WHITE
        self.pot_label.font_name = "ComfortaaBold"
        self.pot_label.size_hint = (.2, 1)
        self.pot_label.pos_hint = {"center_x":.9, "center_y":.5}
        self.pot_label.font_size = 20
        self.pot_label.size_hint = (None, None)
        self.pot_label.size = (dp(100), dp(100))
        self.pot_label.multiline = True

        self.pot_info = Label()
        self.pot_info.text = "The cards in this deck\nwill now appear when \nstudying other decks."
        self.pot_info.color = colors.WHITE
        self.pot_info.font_name = "Comfortaa"
        self.pot_info.size_hint = (.2, 1)
        self.is_pot = 0
        self.pot_info.opacity = self.is_pot

        self.pot_info.pos_hint = {"center_x":.85, "center_y":.4}
        self.pot_info.font_size = 16
        self.pot_info.size_hint = (None, None)
        self.pot_info.size = (dp(100), dp(100))
        self.pot_info.multiline = True

        self.add_widget(self.pot_info)


        self.add_widget(self.title)
        self.add_widget(self.pot)
        self.add_widget(self.pot_label)
        self.add_widget(self.name)
        self.add_widget(self.anchors.positions[2])
        self.add_widget(self.anchors.positions[0])

    def close(self):
        self.parent.remove_widget(self)
    
    def create_deck(self):
        print("WIP")
        newdeck = {}
        newdeck["name"] = self.name.text
        newdeck["pot"] = self.is_pot
        newdeck["cards"] = {}
        newdeck["importance"] = self.parent.acc_settings["importance"]
        newdeck["learning_rate"] = self.parent.acc_settings["learning_rate"]
        self.parent.acc_decks.append(Deck(newdeck)) #? FINE
        self.parent.load()
        self.close()
        
    
    def on_pot_active(self, checkbox, value):
        if value:
            self.is_pot = 1
            self.pot_info.opacity = self.is_pot
            print(1)
        else:
            self.is_pot = 0
            self.pot_info.opacity = self.is_pot
            print(0)
        


class StatsPage(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7, .7)
        self.pos_hint = {"center_x": .5, "center_y": .5}
        
        self.anti_clickthrough = Button()
        self.anti_clickthrough.size_hint = (None, None)
        self.anti_clickthrough.size = (dp(10000), dp(10000))
        self.anti_clickthrough.pos = (-5000, -5000)
        self.anti_clickthrough.background_normal = ''
        self.anti_clickthrough.background_color = (0, 0, 0, 0)
        self.add_widget(self.anti_clickthrough)

        self.background_rectangle = BackgroundLGRAY()
        


        self.add_widget(self.background_rectangle)

        self.anchors = Anchors()

        self.title = Label()
        self.title.text = "Study Statistics"
        self.title.size_hint = (1, None)
        self.title.height = dp(50)
        self.title.font_name = "Comfortaa"
        self.title.color = colors.WHITE
        self.title.pos_hint = {"center_x": .5, "center_y": .9}

        self.ouch = Label()
        self.ouch.text = "Not available at the moment, sorry"
        self.ouch.size_hint = (1, None)
        self.ouch.height = dp(50)
        self.ouch.font_name = "Comfortaa"
        self.ouch.color = colors.WHITE
        self.ouch.pos_hint = {"center_x": .5, "center_y": .5}

        self.escape = Button()
        self.escape.on_press = self.close
        self.escape.text = "X"
        self.escape.background_normal = ''
        self.escape.background_color = colors.FLAME
        self.escape.size_hint = (None, None)
        self.escape.size = (dp(50), dp(50))

        self.anchors.positions[2].add_widget(self.escape)

        self.add_widget(self.title)
        self.add_widget(self.ouch)
        self.add_widget(self.anchors.positions[2])

    def close(self):
        self.parent.remove_widget(self)


class Anchors(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.positions = []

        for i in range(9):
            self.positions.append(AnchorLayout())
        
        self.positions[0].anchor_y = "top"
        self.positions[0].anchor_x = "left"

        self.positions[1].anchor_y = "top"
        self.positions[1].anchor_x = "center"

        self.positions[2].anchor_y = "top"
        self.positions[2].anchor_x = "right"

        self.positions[3].anchor_y = "center"
        self.positions[3].anchor_x = "left"

        self.positions[4].anchor_y = "center"
        self.positions[4].anchor_x = "center"

        self.positions[5].anchor_y = "center"
        self.positions[5].anchor_x = "right"

        self.positions[6].anchor_y = "bottom"
        self.positions[6].anchor_x = "left"

        self.positions[7].anchor_y = "bottom"
        self.positions[7].anchor_x = "center"

        self.positions[8].anchor_y = "bottom"
        self.positions[8].anchor_x = "right"
        
class SmoothButton():
    pass

class LoginMenu(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        LabelBase.register(name='ComfortaaBold',
                           fn_regular='Resources/Fonts/Comfortaa-Bold.ttf')
        LabelBase.register(name='ComfortaaLight',
                           fn_regular='Resources/Fonts/Comfortaa-Light.ttf')
        LabelBase.register(name='Comfortaa',
                           fn_regular='Resources/Fonts/Comfortaa-Regular.ttf')
        LabelBase.register(name="ArialUnicode", fn_regular = 'Resources/Fonts/arial-unicode-ms.ttf')
        self.canvasex = BackgroundPGREEN()
        self.add_widget(self.canvasex)

        self.backgroundCustom = LoginBG()
        self.backgroundCustom.size_hint = (None, None)
        self.backgroundCustom.size = (dp(350), dp(210))
        self.backgroundCustom.pos_hint = {"center_x": .5, "center_y": .5}

        self.add_widget(self.backgroundCustom)

        self.loginbox = LoginBox()
        self.loginbox.pos_hint = {"center_x": .5, "center_y": .5}
        self.loginbox.size_hint = (None, None)
        self.loginbox.size = (dp(300), dp(170))

        self.result = Label()
        self.result.text= ""
        self.result.color= colors.FLAME
        self.result.opacity = 1
        self.result.font_name= "ComfortaaBold"
        self.result.size_hint= 1/2, 1/2
        self.result.font_size= self.width/3 if self.width < self.height else self.height/3
        self.result.pos_hint= {"center_x": .5, "center_y": .2}

        self.add_widget(self.result)

        self.add_widget(self.loginbox)


class BackgroundPGREEN(Widget):
    pass

class BackgroundGRAY(Widget):
    pass

class BackgroundLGRAY(Widget):
    pass

class LoginBox(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.anchor_x = "center"
        self.anchor_y = "center"

        self.passbox = Passthing()

        self.add_widget(self.passbox)

#  TODO: MAKE IT ACTUALLY LOG YOU IN WHEN LOGIN IS PRESSED
class Passthing(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.passloc = AnchorLayout()

        self.passloc.anchor_x = "right"
        self.passloc.anchor_y = "center"

        self.passbox = TextInput()
        self.passbox.multiline = False
        self.passbox.password = True
        self.passbox.hint_text = 'password'
        self.passbox.hint_text_color = colors.GRAY
        self.passbox.background_normal = ''
        self.passbox.background_color = colors.WHITE
        self.passbox.size_hint = (None, None)
        self.passbox.size = (dp(300), dp(50))
        self.passbox.pos_hint = {"center_x": .5, "bottom_y": .5}
        self.passbox.font_size = self.passbox.width/5 if self.passbox.width / \
            5 < self.passbox.height*.8 else self.passbox.height*.8
        self.passbox.on_text_validate = self.login

        self.passloc.add_widget(self.passbox)
        self.add_widget(self.passloc)

        self.userthing = AnchorLayout()
        self.userthing.anchor_y = "top"

        self.userbox = TextInput()
        self.userbox.focus = True
        self.userbox.multiline = False
        self.userbox.hint_text = 'username'
        self.userbox.hint_text_color = colors.GRAY
        self.userbox.background_normal = ''
        self.userbox.background_color = colors.WHITE
        self.userbox.size_hint = (None, None)
        self.userbox.size = (dp(300), dp(50))
        self.userbox.pos_hint = {"center_x": .5, "bottom_y": 0}
        self.userbox.font_size = self.userbox.width/5 if self.userbox.width / \
            5 < self.userbox.height*.8 else self.userbox.height*.8
        self.userbox.on_text_validate = self.nextbox

        self.userthing.add_widget(self.userbox)
        self.add_widget(self.userthing)

        self.button = Button()
        self.button.id = "reveal"
        self.button.text = "Reveal"
        self.button.background_normal = ''
        self.button.background_color = colors.SGREEN
        self.button.size_hint = (None, None)
        self.button.size = (dp(50), dp(50))
        self.button.on_press = self.pressed
        self.passloc.add_widget(self.button)

        self.loginbuttonsloc = AnchorLayout()
        self.loginbuttonsloc.anchor_y = "bottom"   
        self.loginbuttonsloc.anchor_x = "center"

        self.loginbuttons = FloatLayout()
        
        self.loginbuttons.pos_hint = {"center_x": .5, "center_y": -0.5}
        self.loginbuttons.size_hint = (None, None)
        self.loginbuttons.size = (dp(300), dp(40))

        self.loginbutton = Button()
        self.loginbutton.text = "Login"
        self.loginbutton.font_name = "Comfortaa"
        self.loginbutton.size_hint = (1/2, 1)
        self.loginbutton.pos_hint = {
            "center_x": .25, "center_y": .5}
        self.loginbutton.on_press = self.login

        self.registerbutton = Button()
        self.registerbutton.text = "Register"
        self.registerbutton.font_name = "Comfortaa"
        self.registerbutton.size_hint = (1/2, 1)
        self.registerbutton.pos_hint = {
            "center_x": .75, "center_y": .5}
        self.registerbutton.on_press = self.register

        self.loginbuttons.add_widget(self.loginbutton)
        self.loginbuttons.add_widget(self.registerbutton)

        self.loginbuttonsloc.add_widget(self.loginbuttons)
            
        self.add_widget(self.loginbuttonsloc)

    def nextbox(self):
        self.passbox.focus = True
        print("got theres")
        pass

    def login(self):
        username = self.userbox.text
        passhash = hashlib.sha256(self.passbox.text.encode()).hexdigest()

        if self.check_availability(username):
            time.sleep(.001)
            self.parent.parent.result.text = "Invalid Credentials"
        else:
            users = self.get_account_data()

            if users[username] == passhash:
                with open(f"data/users/{username}/cards.json") as f:
                    self.acc_decks = json.load(f)
                with open(f"data/users/{username}/settings.json") as b:
                    self.acc_settings = json.load(b)

                Window.add_widget(DecksMenu(self.acc_decks, self.acc_settings, username))
                Window.remove_widget(self.parent.parent)
            else:
                self.parent.parent.result.text = "Invalid Credentials"


    def register(self):

        username = self.userbox.text
        passhash = hashlib.sha256(self.passbox.text.encode()).hexdigest()

        print(username)
        print(passhash)

        if self.check_availability(username):
            self.open_account(username, passhash)
            self.login()
        else:
            print("ACCOUNT USERNAME TAKEN")
    
    def get_account_data(self) -> dict:
        with open("data/users.json", 'r') as f:
            users = json.load(f)
        return users
    
    def set_account_data(self, data: dict) -> None:
        with open("data/users.json", 'w') as f:
            json.dump(data, f)

    def check_availability(self, username: str) -> bool:
        usernames = self.get_account_data()

        if username in usernames:
            return False
        else:
            return True

    def open_account(self, username: str, passhash: str):
        usernames = self.get_account_data()

        usernames[username] = passhash

        self.set_account_data(usernames)

        path = os.path.join(paths.PARENT, username)

        os.mkdir(path)

        cardsfile = os.path.join(path, "cards.json")
        settingsfile = os.path.join(path, "settings.json")

        with open(cardsfile, 'w') as f:
            f.write("{}")
        
        with open(settingsfile, 'w') as f:
            f.write('{"importance": 1, "learning_rate": 1}')

    def pressed(self):
        print("Pressed")
        if(self.passbox.password == True):
            self.passbox.password = False
        else:
            self.passbox.password = True


class LoginBG(FloatLayout):
    pass


class OuO(App):
    
    def build(self):
        Window.bind(on_request_close=self.on_request_close)


    def on_request_close(self, *args):
        self.save()
        return False
    
    def save(self):
        """Open the pop-up with the name.

        :param title: title of the pop-up to open
        :type title: str
        :param text: main text of the pop-up to open
        :type text: str
        :rtype: None
        """
        save = {}
        for i in range(len(self._app_window.children[0].acc_decks)):
            save[i] = self._app_window.children[0].acc_decks[i].todict()
        
        with open(f"data/users/{self._app_window.children[0].username}/cards.json", "w") as f:
            json.dump(save, f)



if __name__ == '__main__':
    OuO().run()
