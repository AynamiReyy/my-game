import arcade

from settings.config.config import load_settings, toggle_fullscreen
from settings.view_src.controls_view import ControlsView


class SettingsView(arcade.View):
    OPTIONS = [
        ("Полноэкранный режим", "fullscreen"),
        ("Управление", "controls"),
        ("Назад", None),
    ]

    def __init__(self, pause_view):
        super().__init__()
        self.pause_view = pause_view
        self.selected = 0
        self.settings = load_settings()

    @property
    def game_view(self):
        return self.pause_view.game_view

    def on_draw(self):
        self.game_view.on_draw()

        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width, 0, self.window.height, (0, 0, 0, 200),
        )

        arcade.draw_text(
            "Настройки",
            self.window.width / 2,
            self.window.height / 2 + 120,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )

        start_y = self.window.height / 2 + 40
        for i, (label, key) in enumerate(self.OPTIONS):
            if key == "fullscreen":
                value = "✓" if self.settings.get(key, False) else "✗"
                text = f"{label}: {value}"
            else:
                text = label
            color = arcade.color.YELLOW if i == self.selected else arcade.color.WHITE
            arcade.draw_text(
                text,
                self.window.width / 2,
                start_y - i * 40,
                color,
                20,
                anchor_x="center",
            )

        arcade.draw_text(
            "↑/↓ — навигация    Enter — выбрать    ESC — назад",
            self.window.width / 2,
            self.window.height / 2 - 120,
            arcade.color.GRAY,
            14,
            anchor_x="center",
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.selected = max(0, self.selected - 1)
            return
        if symbol == arcade.key.DOWN:
            self.selected = min(len(self.OPTIONS) - 1, self.selected + 1)
            return
        if symbol in (arcade.key.ENTER, arcade.key.RETURN):
            self._handle_selection()
            return
        if symbol == arcade.key.ESCAPE:
            self.game_view.reload_controls()
            self.window.show_view(self.pause_view)

    def _handle_selection(self):
        _, key = self.OPTIONS[self.selected]
        if key is None:
            self.window.show_view(self.pause_view)
            return
        if key == "fullscreen":
            toggle_fullscreen(self.settings)
            try:
                self.window.set_fullscreen(self.settings["fullscreen"])
            except Exception:
                pass
        elif key == "controls":
            self.window.show_view(ControlsView(self))