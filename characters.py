from kivy.uix.image import Image
def create_character(choice):
	return Warrior()

class Character_abst(Image):
	def __init__(self, **kwargs):
		super(Character_abst, self).__init__(**kwargs)
		self.asset_path = "path/to/character/assets"
		self.bind(parent = self.bind_animations_cb)

	def bind_animations_cb(self, character, parent):
		if not(parent is None):
			print("Character got parent")
			parent.bind(sprite_data = self.update_sprite_cb)
	def update_sprite_cb(self, player, sprite_data):
		facing, direction = sprite_data
		action = 'walking'
		if direction[0] == 0 and direction[1] == 0:
			action = 'standing'
		self.source = self.asset_path + action + facing[0] + '.gif'
		print("Source: " + self.source)

class Warrior(Image):
	def __init__(self, **kwargs):
		super(Warrior, self).__init__(size_hint = (1.0, 1.0),  pos_hint = {'bottom': 0}, allow_stretch = True)
		self.asset_path = './assets/characters/warrior/'
		self.source = self.asset_path + 'standing_u.gif'