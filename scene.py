from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window

#from enemies import *

class Scene(Widget):
	def __init__(self, **kwargs):
		super(Scene, self).__init__(**kwargs)
		pass


	def update(self,dt):
		'''
		I only want objects that are on screen to update
		'''
		pass

	'''
	for update and gross collider localization I need to determine which objects are on screen
	'''
	def find_onscreen(self):
		pass
