import arcade

from settings.config import load_controls
from settings.settings_view import SettingsView


class PauseView(arcade.View):
    MENU_ITEMS = [
        ("Продолжить", "resume"),
        ("Настройки", "settings"),
        ("Выйти", "exit"),
    ]

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.selected = 0
        self._header_y: float = 0.0
        self._start_y: float = 0.0

    def on_show_view(self):
        self.controls = load_controls()
        self.window.set_mouse_visible(False)
        h = self.window.height
        self._header_y = h / 2 + 100
        self._start_y = h / 2 + 40

    def on_draw(self):
        self.game_view.on_draw()

        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width, 0, self.window.height, (0, 0, 0, 180),
        )

        arcade.draw_text(
            "Пауза",
            self.window.width / 2,
            self._header_y,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )

        for i, (label, _) in enumerate(self.MENU_ITEMS):
            color = arcade.color.YELLOW if i == self.selected else arcade.color.WHITE
            arcade.draw_text(
                label,
                self.window.width / 2,
                self._start_y - i * 40,
                color,
                24,
                anchor_x="center",
            )

        arcade.draw_text(
            "↑/↓ — навигация    Enter — выбрать    ESC — вернуться",
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
            self.selected = min(len(self.MENU_ITEMS) - 1, self.selected + 1)
            return
        if symbol in (arcade.key.ENTER, arcade.key.RETURN):
            self._handle_selection()
            return
        if symbol == self.controls.get("pause", arcade.key.ESCAPE):
            self._resume_game()

    def _handle_selection(self):
        action = self.MENU_ITEMS[self.selected][1]
        if action == "resume":
            self._resume_game()
        elif action == "settings":
            self.window.show_view(SettingsView(self))
        elif action == "exit":
            self.window.close()

    def _resume_game(self):
        self.game_view.resume()
        self.window.show_view(self.game_view)
