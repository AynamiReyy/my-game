import arcade

from Creatures.Scott.Scott import Scott
from game.constants import TextureGroup, BG_PATH
from settings.config import load_controls
from settings.pause_view import PauseView


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture(BG_PATH)
        self.player = Scott(*TextureGroup.all())
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.paused = False
        self.controls = load_controls()
        self.pressed_keys: set[int] = set()

    def reload_controls(self):
        self.controls = load_controls()

    def on_show_view(self):
        self.reload_controls()
        self.window.set_mouse_visible(False)
        self.player.center_x = self.window.width / 2
        self.player.center_y = self.window.height / 2

    def on_key_press(self, symbol, modifiers):
        if self.paused:
            return
        self.pressed_keys.add(symbol)

        if symbol == self.controls.get("pause", arcade.key.ESCAPE):
            self._toggle_pause()
        elif symbol == self.controls.get("jump", arcade.key.UP):
            self.player.jump()
        elif symbol == self.controls.get("crouch", arcade.key.DOWN):
            self.player.crouch(True)

    def on_key_release(self, symbol, modifiers):
        if self.paused:
            return
        self.pressed_keys.discard(symbol)
        if symbol == self.controls.get("crouch", arcade.key.DOWN):
            self.player.crouch(False)

    def _toggle_pause(self):
        self.paused = True
        self.pressed_keys.clear()
        self.window.show_view(PauseView(self))

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            rect=arcade.Rect.from_kwargs(x=0, y=0, width=self.width, height=self.height)
        )
        self.player_list.draw()

    def on_update(self, delta_time):
        if self.paused:
            return

        self.player.change_x = 0
        if self.controls.get("left", arcade.key.LEFT) in self.pressed_keys:
            self.player.change_x = -1
        elif self.controls.get("right", arcade.key.RIGHT) in self.pressed_keys:
            self.player.change_x = 1

        self.player_list.update(delta_time)

    def resume(self):
        self.paused = False
        self.pressed_keys.clear()
        self.reload_controls()
