import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

'''
to-do
'''
from controller import Controller 
from scene import Scene 
from player import Player

from kivy.config import Config
Config.set('graphics','resizable',0) #don't make the app re-sizeable
Window.clearcolor = (0,0,0,1.) #this fixes drawing issues on some phones

class Game(Widget):
    '''
    The main widget class that contains the game, the game loop and runs everything
    '''
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        player = Player()
        self.controller = Controller(player)
        self.scene = Scene(player)
        self.add_widget(self.scene)

 
    def update(self,dt):
        '''
        This update function is the main update function for the game
        All of the game logic has its origin here
        dt - The change in time between updates of the game logic
        '''
        self.scene.update(dt)

class MainApp(App):
    ''' 
    The root widget canvas upon which the game is drawn
    Because this named ClientApp, the kv file needs to be client.kv
    '''
    def build(self):
        parent = Widget() #this is an empty holder for buttons, etc
        app = Game()        
        #Start the game clock (runs update function once every (1/60) seconds
        Clock.schedule_interval(app.update, 1.0/60.0) 
        parent.add_widget(app) #use this hierarchy to make it easy to deal w/buttons
        return parent

if __name__ == '__main__' :
    MainApp().run()