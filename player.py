from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ReferenceListProperty
from kivy.clock import Clock
from kivy.uix.image import Image

from math import ceil

from characters import TemplateCharacter
from collider import Damagable

class Player(Damagable):
	width, height = NumericProperty(32), NumericProperty(48)
	x, y  = NumericProperty(0), NumericProperty(0)
	dir_x, dir_y = NumericProperty(0), NumericProperty(0)
	direction = ReferenceListProperty(dir_x, dir_y)
	source = StringProperty("")

	def __init__(self, **kwargs):
		super(Player, self).__init__(1, 'player', **kwargs)
		self.state = 'free'
		self.x, self.y  = self.center_x, self.center_y
		self.dir_x, self.dir_y = 0, 0
		self.last_dir = (0, -1)
		self.current_character = TemplateCharacter(self)
		self.sprite = Image(source = self.current_character.source_base + 'walk_s.gif', size = (48*2, 32*2))
		self.sprite.x, self.sprite.y = self.x, self.y
		self.add_widget(self.sprite)
		self.max_health = self.current_character.max_health
		self.health = self.max_health
		Clock.schedule_interval(self.recharge, self.current_character.recharge_rate)

		self.bind(direction=self.is_moving)
	'''
	The following functions are those that can be called by the controller
	'''
	#option is for which action, can be 0-2 (we'll do modulo so it actually can be whatever)
	def take_action(self, option):
		if not ('add_widget' in self.state) and self.current_character.real_energy > 0:
			cost, delay, state = self.current_character.actions[option].take_action(self)
			self.current_character.real_energy -= cost
			self.state = state
			Clock.schedule_once(self.set_ready, delay)
	'''
	Any update logic that needs to get done can be done here (recharging)
	'''
	def update(self, dt):
		if self.state != 'attacking_heavy':
			self.x += (self.current_character.speed * dt) * self.dir_x
			self.y += (self.current_character.speed * dt) * self.dir_y
		self.sprite.x, self.sprite.y = self.x - self.width, (self.y + self.sprite.height/2) - self.height
		self.current_character.update(self, dt)
	def recharge(self, dt):
		if self.current_character.real_energy < self.current_character.max_energy:
			self.current_character.real_energy += 1
	'''
	The following functions are responsible for changing the state of the player
	'''
	def set_ready(self, dt = 0):
		if (self.dir_x, self.dir_y) != (0, 0):
			self.state = 'moving'
		else:
			self.state = 'free'
	def is_moving(self, instance, value):
		if value[0] == -1:
			self.sprite.source = self.current_character.source_base + 'walk_a.gif'
			self.state = 'moving' 
			self.sprite.anim_delay = 0.25
		elif value[1] == -1:
			self.sprite.source = self.current_character.source_base + 'walk_s.gif'
			self.state = 'moving'
			self.sprite.anim_delay = 0.25
		elif value[0] == 1:
			self.sprite.source = self.current_character.source_base + 'walk_d.gif'
			self.state = 'moving'
			self.sprite.anim_delay = 0.25
		elif value[1] == 1: 
			self.sprite.source = self.current_character.source_base + 'walk_w.gif'
			self.state = 'moving'
			self.sprite.anim_delay = 0.25
		else:
			self.set_ready()
			self.sprite.anim_delay = -1
'''
class Damagable(Collidable):
	health = NumericProperty(1)
	def __init__(self, health, alignment, **kwargs):
		super(Damagable, self).__init__(**kwargs) 
		self.alignment = alignment

		self.health = health
		self.invunerable = False
		self.bind(self.health = health_check_cb)

	def health_check_cb(self, instance, value):
		if self.health < 1:
			self.destory()

	def take_damage(self, damage):
		if not(self.invunerable):
			self.actual_health -= damage
			self.invunerable = True
			Clock.schedule_once(self.restore, 1/30)

	def restore(self, dt):
		self.invunerable = False
'''
