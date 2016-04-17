from kivy.clock import Clock
from attacks import * 

class Action():
	def __init__(self):
		self.lock_time = 0
		self.cost = 0
	def take_action(self, actor):
		pass

class ExampleShoot(Action):
	def __init__(self):
		super(ExampleShoot, self).__init__()		
		self.lock_time = 1/20
		self.cost = 1
		self.state = 'attacking_light'

	def take_action(self, actor):
		direction = actor.last_dir
		origin_point = (actor.center_x, actor.center_y)
		new_bullet = BasicShot(direction, origin_point, actor.alignment)
		add_bullet(new_bullet, actor)
		return self.cost, self.lock_time, self.state

class ExampleBomb(Action):
	def __init__(self):
		super(ExampleBomb, self).__init__()
		self.lock_time = 1/10
		self.cost = 3
		self.state = 'attacking_heavy'

	def take_action(self, actor):
		direction = actor.last_dir
		origin_point = (actor.center_x, actor.center_y)
		new_bullet = BasicBomb(direction, origin_point, actor.alignment)
		add_bullet(new_bullet, actor)
		return self.cost, self.lock_time, self.state
class ExampleStrike(Action):
	def __init__(self, actor):
		super(ExampleStrike, self).__init__()
		self.lock_time = 1/2
		self.cost = 2
		self.state = 'attacking_heavy'
		self.strike_zone = BasicStrike(actor.center_x, actor.center_y, actor.alignment)
		actor.bind(parent = add_bullet_on_connect)
	def update(self, center, dt):
		self.strike_zone.update(center, dt)
	def take_action(self, actor):
		self.strike_zone.turn_on(actor.last_dir)
		return self.cost, self.lock_time, self.state

def add_bullet(bullet, actor):
	actor.parent.add_widget(bullet)
	actor.parent.parent.bullets.append(bullet)

def add_bullet_on_connect(instance, value):
	if not(isinstance(value, type(None))):
		value.add_widget(instance.current_character.actions[2].strike_zone.quad_w)
		value.add_widget(instance.current_character.actions[2].strike_zone.quad_a)
		value.add_widget(instance.current_character.actions[2].strike_zone.quad_s)
		value.add_widget(instance.current_character.actions[2].strike_zone.quad_d)



'''
def action_0(self, player, world):
	direction = player.last_dir
	origin_point = (player.center_x, player.center_y)
	self.real_energy -= 1
	new_bullet = BaseBullet(direction, origin_point, 'player')
	add_bullet(world, new_bullet)
def action_1(self, player, world):
	v_x, v_y = player.last_dir
	offset_x, offset_y = 0, 0
	if v_y == -1:
		offset_x, offset_y = -35, -30
	elif v_y == 1:
		offset_x, offset_y = -35, 35
	if v_x == -1:
		offset_x, offset_y = -40, -20
	elif v_x == 1:
		offset_x, offset_y = 15, -20
	origin_point = (player.center_x + offset_x, player.center_y + offset_y)
	self.real_energy -= 1
	new_bullet = MeleeBullet((v_x, v_y), origin_point, 'player')
	add_bullet(world, new_bullet)
	player.state = 'attacking'
	Clock.schedule_once(player.free_state, new_bullet.life_length)

def action_2(self, player, world):
	v_x, v_y = player.last_dir
	origin_point = (player.center_x, player.center_y)
	self.real_energy -= 3
	new_bullet = BombBullet((v_x, v_y), origin_point, 'player')
	add_bullet(world, new_bullet)

def add_bullet(world, bullet):
	world.add_widget(bullet)
	world.bullets.append(bullet)
	Clock.schedule_once(bullet.destroy, bullet.life_length)

'''