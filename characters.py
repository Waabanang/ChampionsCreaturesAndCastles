#from actions import *
from kivy.clock import Clock

from actions import *

class TemplateCharacter():

	def __init__(self, player):
		self.speed = 100
		self.max_health = 3
		self.real_health = self.max_health
		self.max_energy = 10
		self.real_energy = self.max_energy
		self.recharge_rate = 1/2 #in fractions of a second
		self.source_base = './assets/tmp_character/' #needs to be path to image, later though
		self.actions = [ExampleShoot(), ExampleBomb(), ExampleStrike(player)]
	def update(self, player, dt):
		self.actions[2].update((player.center_x, player.center_y), dt)