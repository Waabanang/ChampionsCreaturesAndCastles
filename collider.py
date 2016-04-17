from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.clock import Clock

class Collider(Widget):
	def __init__(self, **kwargs):
		super(Collider, self).__init__(**kwargs)
	def update(self, dt):
		for widA in self.children:
			for widB in self.children:
				if self.collision_check(widA, widB):
					widA.on_collide(widB)
					widB.on_collide(widA)
	def collision_check(self, widA, widB):
		if widA is widB:
			return False
		if not(isinstance(widB, Collidable)) or not(isinstance(widA, Collidable)):
			return False
		else:
			return widA.collide_widget(widB)

class Collidable(Widget):
	is_dead = BooleanProperty(True)
	def __init__(self, **kwargs):
		super(Collidable, self).__init__(**kwargs)
		self.is_dead = False
		self.collidable = True
		self.is_solid = True
		self.bind(is_dead = self.clean_up_self_cb)
	def on_collide(self, other_widget):
		pass
	def destory(self):
		self.is_dead = True
	def clean_up_self_cb(self, instance, value):
		if value:
			self.parent.remove_widget(self)

class Damagable(Collidable):
	health = NumericProperty(1)
	def __init__(self, health, alignment, **kwargs):
		super(Damagable, self).__init__(**kwargs) 
		self.alignment = alignment

		self.health = health
		self.invunerable = False
		self.bind(health = self.health_check_cb)

	def health_check_cb(self, instance,  value):
		if value < 1:
			self.destory()

	def take_damage(self, damage):
		if not(self.invunerable):
			self.health -= damage
			self.invunerable = True
			Clock.schedule_once(self.restore, 1/30)


	def restore(self, dt):
		self.invunerable = False