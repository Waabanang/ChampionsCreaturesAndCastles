from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ReferenceListProperty
from kivy.clock import Clock
from kivy.uix.image import Image

from math import ceil

from characters import create_character

class Player(FloatLayout):
	width, height = NumericProperty(64), NumericProperty(64)
	x, y  = NumericProperty(0), NumericProperty(0)
	dir_x, dir_y = NumericProperty(0), NumericProperty(0)
	direction = ReferenceListProperty(dir_x, dir_y)
	active_character = ObjectProperty()

	def __init__(self, characters, **kwargs):
		super(Player, self).__init__(**kwargs)
		self.characters = [create_character(characters[0]), create_character(characters[1]), create_character(characters[2])]
		self.active_character = self.characters[0]
	'''
	The following functions are those that can be called by the controller
	'''
	#option is for which action, can be 0-2 (we'll do modulo so it actually can be whatever)
	def take_action(self, option):
		pass
	def change_directions(self, direction):
		pass
	'''
	Any update logic that needs to get done can be done here (recharging)
	'''
	def update(self, dt):
		self.x += (self.current_character.speed * dt) * self.dir_x
		self.y += (self.current_character.speed * dt) * self.dir_y
		self.current_character.update(self, dt)
