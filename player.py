from kivy.core.window import Window
from kivy.uix.layout import Layout
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import ReferenceListProperty
from kivy.clock import Clock
from kivy.uix.image import Image

from math import ceil

from characters import create_character

class Player(Layout):
	width, height = NumericProperty(64), NumericProperty(64)

	#The player always has to be facing one of eight direction to know where to shoot
	#But the player can also be moving or not in any of eight (possibly different) directions
	#So 'facing' is responsible for the former, and direction is the latter
	#Both functions are updated through the request_move, and release_move methods
	d_x, d_y = NumericProperty(0), NumericProperty(0)
	direction = ReferenceListProperty(d_x, d_y)
	facing = StringProperty('u')

	sprite_data = ReferenceListProperty(facing, direction)

	active_character = ObjectProperty()

	strafe_locked = BooleanProperty(False)

	def __init__(self, characters, **kwargs):
		super(Player, self).__init__(**kwargs)

		self.facing_options = {'u':(0,-1), 'd':(0,1), 'l':(1,0), 'r':(-1,0), 'ur':(1, -1), 'ul':(-1,-1), 'dr':(1,1), 'dl':(-1, 1)}
		self.characters = [create_character(characters[0]), create_character(characters[1]), create_character(characters[2])]

		self.active_character = self.characters[0]
		self.add_widget(self.active_character)

		self.crosshairs = Image(size_hint = (1.0, 1.0), source = './assets/player/crosshairs_normal_u.png', allow_stretch = True)
		self.add_widget(self.crosshairs)
		self.bind(facing = self.update_crosshairs_cb)

	'''
	The following functions are those that can be called by the controller
	'''
	def request_move(self, choice):
		if choice == 'up':
			self.d_y = -1
		elif choice == 'down':
			self.d_y = 1
		elif choice == 'right':
			self.d_x = -1
		elif choice == 'left':
			self.d_x = 1

		for k, v in self.facing_options.items():
			if self.d_x == v[0] and self.d_y == v[1]:
				self.facing = k

	def release_move(self, choice):
		if choice == 'up' or choice == 'down':
			self.d_y = 0
		elif choice == 'left' or choice == 'right':
			self.d_x = 0
		if self.d_y == 0 and self.d_x == 0:
			pass
		else:
			for k, v in self.facing_options.items():
				if self.d_x == v[0] and self.d_y == v[1]:
					self.facing = k

	'''
	Any update logic that needs to get done can be done here (recharging)
	'''
	def update(self, dt):
		self.x += (300 * dt) * self.d_x
		self.y += (300 * dt) * self.d_y
	def update_crosshairs_cb(self, player, facing):
		player.crosshairs.source = './assets/player/crosshairs_normal_' + facing + '.png'

