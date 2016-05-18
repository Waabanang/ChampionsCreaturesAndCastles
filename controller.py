from kivy.uix.widget import Widget
from kivy.core.window import Window
from player import Player

class Controller(Widget):
    def __init__(self, player, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self.player = player


    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard

        if keycode[1] == 'w':
            self.player.request_move('up')
        elif keycode[1] == 'a':
            self.player.request_move('left')
        elif keycode[1] == 's':
            self.player.request_move('down')
        elif keycode[1] == 'd':
            self.player.request_move('right')

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'w':
            self.player.release_move('up')
        elif keycode[1] == 'a':
            self.player.release_move('left')
        elif keycode[1] == 's':
            self.player.release_move('down')
        elif keycode[1] == 'd':
            self.player.release_move('right')