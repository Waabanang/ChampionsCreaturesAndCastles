import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.config import Config
from functools import partial
from kivy.uix.checkbox import CheckBox

from player import Player
from scene import Scene
from controller import Controller


Config.set('graphics','resizable',0) #don't make the app re-sizeable
Window.clearcolor = (0,0,0,1.0) #this fixes drawing issues on some phones

selected_chars = []
selected_level = ""


class Game(FloatLayout):
    '''
    The main widget class that contains the game, the game loop and runs everything
    '''

    def __init__(self, **kwargs):
        super(Game, self).__init__(size = (10000, 10000))
        self.player = Player(selected_chars)
        self.scene = Scene(selected_level, size = self.size)
        self.scene.add_widget(self.player)
        self.add_widget(self.scene)
        self.controller = Controller(self.player)
        
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self,dt):
        '''
        This update function is the main update function for the game
        All of the game logic has its origin here
        dt - The change in time between updates of the game logic
        '''
        self.player.update(dt)

class SplashScreen(Screen):
    '''
    Opening Splash screen
    '''
    pass

class GameScreen(Screen):
    '''
    Screen where game is played
    '''
    def on_enter(self):
        self.game = Game()

        self.camera = ScrollView()
        
        self.camera.add_widget(self.game)
        self.add_widget(self.camera)
        self.camera.do_scroll = True

        self.game.player.bind(pos=self.scroll_to_player_cb)

    def scroll_to_player_cb(self, player, pos):
        self.camera.x, self.camera.y = -(player.x - Window.width/2), -(player.y - Window.height/2)

class CharSelectScreen(Screen):
    def on_enter(self):
        global selected_chars
    def select_character(self, choice):
        global selected_chars
        if choice in selected_chars:
            selected_chars.remove(choice)
            print(choice + " removed from party")
        elif len(selected_chars) < 3:
            selected_chars.append(choice)
            print(choice + " added to party")
        print("You have " + str(len(selected_chars)) + " in your party")
    def go_to_level_select(self):
        if len(selected_chars) == 3:
            self.parent.current = 'level_select_screen'
        else:
            print("You need at least 3 party members. You have " + str(len(selected_chars)) + " party members.")

class LevelSelectScreen(Screen):
    def on_enter(self):
        global selected_level
    def select_level(self, choice):
        global selected_level
        selected_level = choice
        print("You have selected " + selected_level)
    def start_game(self):
        if len(selected_level) > 0:
            self.parent.current = 'game_screen'
        
class MainApp(App):
    screen_manager = ObjectProperty(None)
    ''' 
    The root widget canvas upon which the game is drawn
    Because this named ClientApp, the kv file needs to be client.kv
    '''
    def build(self):
        MainApp.screen_manager = ScreenManager()

        ss = SplashScreen(name='splash_screen')
        gs = GameScreen(name='game_screen')
        ls = LevelSelectScreen(name = 'level_select_screen')
        cs = CharSelectScreen(name = 'character_select_screen')

 
        self.screen_manager.add_widget(ss)
        self.screen_manager.add_widget(gs)
        self.screen_manager.add_widget(ls)
        self.screen_manager.add_widget(cs)

        self.screen_manager
        return self.screen_manager



if __name__ == '__main__' :
    MainApp().run()