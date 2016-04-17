from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window

from collider import Collider
'''
to-do
'''
#from enemies import *

class Scene(Widget):
	def __init__(self, player,  **kwargs):
		super(Scene, self).__init__(**kwargs)
		self.collider = Collider()
		self.add_widget(self.collider)
		self.player = player
		self.collider.add_widget(self.player)
		self.bullets = []
		self.HEALTH = Label(text= "Health: " + str(self.player.health), pos = (0,Window.height-100))
		self.ENERGY = Label(text= "Energy: " + str(self.player.current_character.real_energy), pos = (0,Window.height-130))
		self.STATE = Label(text= "State: " + self.player.state, pos = (0,Window.height-160))
		self.add_widget(self.HEALTH)
		self.add_widget(self.ENERGY)
		self.add_widget(self.STATE)


	def update(self,dt):
		'''
		This update function is the main update function for the game
		All of the game logic has its origin here
		dt - The change in time between updates of the game logic
		'''
		for bullet in self.bullets:
			bullet.update(dt)
		self.player.update(dt)
		self.HEALTH.text = "Health: " + str(self.player.health)
		self.ENERGY.text= "Energy: " + str(self.player.current_character.real_energy)
		self.STATE.text = "State: " + self.player.state
		self.collider.update(dt)