from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.image import Image


from collider import Collidable
from collider import Damagable

def orient_image(direction):
	if direction[1] == 1:
		print(direction)
		return 'w', (1, 2)
	elif direction[0] == -1:
		return 'a', (2, 1)
	elif direction[1] == -1:
		return 's', (1, 2)
	elif direction[0] == 1:
		return 'd', (2, 1)
	return "error"


class Bullet(Collidable):
	diameter  =  NumericProperty(10)
	def __init__(self, direction, origin_point, alignment, **kwargs):
		super(Bullet, self).__init__(**kwargs)
		self.alignment = alignment
		self.dir_x, self.dir_y = direction
		self.x, self.y = self.center_x, self.center_y = origin_point
		self.size = (self.diameter, self.diameter)
		self.is_dead = False #gets flipped to false when the bullet needs to be removed

		self.speed = 0
		self.damage = 0
		self.life_length = 1 #time in seconds that the bullet should be around
	def update(self, dt):
		self.x += (self.speed * dt) * self.dir_x
		self.y += (self.speed * dt) * self.dir_y
	def on_collide(self, other_widget):
		if isinstance(other_widget, Bullet):
			pass
		elif isinstance(other_widget, Damagable) and self.alignment != other_widget.alignment:
			other_widget.take_damage(self.damage)
			self.destroy()
	def destroy(self, dt=0):
		self.is_dead = True

class BasicShot(Bullet):
	def __init__(self, direction, origin_point, alignment, **kwargs):
		super(BasicShot, self).__init__(direction, origin_point, alignment, **kwargs)
		self.speed = 200
		self.damage = 1
		self.life_length = 1
		Clock.schedule_once(self.destroy, self.life_length)

		image_orientation, image_size = orient_image(direction)
		self.sprite = Image(source = './assets/basicshot/bullet_' + image_orientation + '.gif', size = (self.diameter * image_size[0], self.diameter * image_size[1]))
		self.sprite.anim_delay = 1/20
		self.sprite.x, self.sprite.y = self.x-(self.width*3/4), self.y-(self.height*3/4)
		self.add_widget(self.sprite)

	def update(self, dt):
		self.x += (self.speed * dt) * self.dir_x
		self.y += (self.speed * dt) * self.dir_y
		self.sprite.x, self.sprite.y = self.center_x-(self.diameter/2), self.center_y-(self.diameter/2)
		if self.dir_x >0:
			self.sprite.x -= self.diameter
		elif self.dir_y >0:
			self.sprite.y -= self.diameter

class BasicBomb(Bullet):
	diameter = NumericProperty(100)
	def __init__(self, direction, origin_point, alignment, **kwargs):
		super(BasicBomb, self).__init__(direction, origin_point, alignment, **kwargs)
		self.exploding = False
		self.speed = 0
		self.damage = 3
		self.life_length = 3 #time in seconds that the bullet should be around
		Clock.schedule_once(self.destroy, self.life_length)

		self.sprite = Image(source = './assets/basicbomb/bomb.gif', size = (self.diameter, self.diameter))
		self.sprite.anim_delay = 1/20
		self.sprite.x, self.sprite.y = self.x, self.y
		self.add_widget(self.sprite)
	def update(self, dt):
		pass
	def on_collide(self, other_widget):
		if isinstance(other_widget, Damagable) and self.exploding:
			other_widget.take_damage(self.damage)
	def destroy(self, dt=0):
		self.sprite.source = './assets/basicbomb/explosion.gif'
		self.exploding = True
		Clock.schedule_once(self.actually_destroy, 1/5)
	def actually_destroy(self, dt=0):
		self.is_dead = True

class StrikeQuad(Collidable):
	rgb = ListProperty([0, 255, 0])
	def __init__(self, direction, alignment, **kwargs):
		super(StrikeQuad, self).__init__(**kwargs)
		self.on = False
		self.direction = direction
		self.alignment = alignment

		self.damage = 0
	def on_collide(self, other_widget):
		if self.on and (isinstance(other_widget, Damagable) and other_widget.alignment != self.alignment):
			other_widget.take_damage(self.damage)
		if self.on and isinstance(other_widget, Bullet):
			other_widget.destroy()
	def turn_on(self, dt=0):
		self.rgb = (255, 0, 0)
		self.on = True
	def turn_off(self, dt=0):
		self.rgb = (0, 255, 0)
		self.on = False


class BasicQuad(StrikeQuad):
	def __init__(self, direction, alignment, **kwargs):
		super(BasicQuad, self).__init__(direction, alignment, **kwargs)
		self.sprite = Image()
		self.damage = 2
	def turn_on(self, dt=0):
		self.sprite = Image(source = './assets/basicstrike/strike_' + orient_image(self.direction)[0]  + '.gif', size = self.size)
		self.sprite.pos = self.pos
		self.add_widget(self.sprite)
		self.on = True
		self.on = True
	def turn_off(self, dt=0):
		self.clear_widgets()
		self.on = False

class StrikeZone():
	def __init__(self, center_x, center_y, alignment, long_side, short_side, **kwargs):
		self.center_x = center_x
		self.center_y = center_y
		self.alignment = alignment
		self.long_side = long_side
		self.short_side = short_side
		self.duration = 1/2

		self.quad_w = StrikeQuad((0, 1), alignment, size = (self.long_side, self.short_side), pos = (center_x-(self.long_side/2), center_y + 24))
		self.quad_a = StrikeQuad((-1, 0), alignment, size = (self.short_side, self.long_side), pos = (center_x-(17+self.short_side), center_y - (self.long_side/2)))
		self.quad_s = StrikeQuad((0, -1), alignment, size = (self.long_side, self.short_side), pos = (center_x-(self.long_side/2), center_y - (24 + self.short_side)))
		self.quad_d = StrikeQuad((1, 0), alignment, size = (self.short_side, self.long_side), pos = (center_x+17, center_y - (self.long_side/2)))
		self.dir_x, self.dir_y = 0, 0

		self.length = 1 #time in seconds that the bullet should be around
	def update(self, center, dt):
		self.center_x, self.center_y = center
		self.quad_w.x, self.quad_w.y = self.center_x-(self.long_side/2), self.center_y + 24
		self.quad_a.x, self.quad_a.y = self.center_x-(17+self.short_side), self.center_y - (self.long_side/2)
		self.quad_s.x, self.quad_s.y = self.center_x-(self.long_side/2), self.center_y - (24 + self.short_side)
		self.quad_d.x, self.quad_d.y = self.center_x+17, self.center_y - (self.long_side/2)
	def turn_on(self, direction):
		if direction[1] == 1:
			self.quad_w.turn_on()
		elif direction[0] == -1:
			self.quad_a.turn_on()
		elif direction[1] == -1:
			self.quad_s.turn_on()
		elif direction[0] == 1:
			self.quad_d.turn_on()
		Clock.schedule_once(self.turn_off, self.duration)

	def turn_off(self, dt=0):
		self.quad_w.turn_off()
		self.quad_a.turn_off()
		self.quad_s.turn_off()
		self.quad_d.turn_off()

class BasicStrike(StrikeZone):
	def __init__(self, center_x, center_y, alignment, **kwargs):
		super(BasicStrike, self).__init__(center_x, center_y, alignment, 48, 20, **kwargs)

		self.quad_w = BasicQuad((0, 1),alignment, size = (self.long_side, self.short_side), pos = (center_x-(self.long_side/2), center_y + 24))
		self.quad_a = BasicQuad((-1, 0), alignment, size = (self.short_side, self.long_side), pos = (center_x-(17+self.short_side), center_y - (self.long_side/2)))
		self.quad_s = BasicQuad((0, -1), alignment, size = (self.long_side, self.short_side), pos = (center_x-(self.long_side/2), center_y - (24 + self.short_side)))
		self.quad_d = BasicQuad((1, 0), alignment, size = (self.short_side, self.long_side), pos = (center_x+17, center_y - (self.long_side/2)))

		self.dir_x, self.dir_y = 0, 0
	def turn_on(self, direction):
		if direction[1] == 1:
			self.quad_w.turn_on() 
		elif direction[0] == -1:
			self.quad_a.turn_on()
		elif direction[1] == -1:
			self.quad_s.turn_on()
		elif direction[0] == 1:
			self.quad_d.turn_on()
		Clock.schedule_once(self.turn_off, self.duration)
	def update(self, center, dt):
		self.center_x, self.center_y = center
		self.quad_w.x, self.quad_w.y = self.center_x-(self.long_side/2), self.center_y + 24
		self.quad_a.x, self.quad_a.y = self.center_x-(17+self.short_side), self.center_y - (self.long_side/2)
		self.quad_s.x, self.quad_s.y = self.center_x-(self.long_side/2), self.center_y - (24 + self.short_side)
		self.quad_d.x, self.quad_d.y = self.center_x+17, self.center_y - (self.long_side/2)
		self.quad_w.sprite.x, self.quad_w.sprite.y = self.quad_w.x, self.quad_w.y
		self.quad_a.sprite.x, self.quad_a.sprite.y = self.quad_a.x, self.quad_a.y
		self.quad_s.sprite.x, self.quad_s.sprite.y = self.quad_s.x, self.quad_s.y
		self.quad_d.sprite.x, self.quad_d.sprite.y = self.quad_d.x, self.quad_d.y





