import arcade

from settings.config.config import load_controls, set_control_scheme, load_settings
from game_src.constants import KEY_NAMES


class ControlsView(arcade.View):
    ACTIONS = [
        ("Раскладка", "scheme", True, ""),
        ("Влево", "left", False, "движение влево"),
        ("Вправо", "right", False, "движение вправо"),
        ("Прыжок", "jump", False, "прыжок"),
        ("Присесть", "crouch", False, "присесть"),
    ]

    def __init__(self, settings_view):
        super().__init__()
        self.settings_view = settings_view
        self.selected = 0

    def on_show_view(self):
        self.controls = load_controls()
        self.settings = load_settings()

    @property
    def game_view(self):
        return self.settings_view.game_view

    def on_draw(self):
        self.game_view.on_draw()

        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width, 0, self.window.height, (0, 0, 0, 220),
        )

        arcade.draw_text(
            "Управление",
            self.window.width / 2,
            self.window.height / 2 + 140,
            arcade.color.WHITE,
            36,
            anchor_x="center",
        )

        start_y = self.window.height / 2 + 60

        for i, (label, action, selectable, description) in enumerate(self.ACTIONS):
            if action == "scheme":
                scheme = self.settings.get("control_scheme", "arrows")
                key_text = f"Раскладка: {'WASD' if scheme == 'wasd' else 'Стрелки'}"
            else:
                key_code = self.controls.get(action)
                if key_code is None:
                    key_code = arcade.key.UP if action == "jump" else arcade.key.DOWN
                key_text = KEY_NAMES.get(key_code, f"Key({key_code})")

            is_selected = i == self.selected and selectable
            color = arcade.color.YELLOW if is_selected else arcade.color.WHITE
            text = f"{key_text}" if not description else f"{key_text}  —  {description}"
            
            arcade.draw_text(
                text,
                self.window.width / 2,
                start_y - i * 50,
                color,
                20,
                anchor_x="center",
            )

        arcade.draw_text(
            "Включите английскую раскладку для управления",
            self.window.width / 2,
            self.window.height / 2 - 200,
            arcade.color.GRAY,
            14,
            anchor_x="center",
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP:
            self.selected = max(0, self.selected - 1)
            return
        if symbol == arcade.key.DOWN:
            self.selected = min(len(self.ACTIONS) - 1, self.selected + 1)
            return
        if symbol in (arcade.key.ENTER, arcade.key.RETURN):
            _, action, selectable, _ = self.ACTIONS[self.selected]
            if action == "scheme":
                current = self.settings.get("control_scheme", "arrows")
                new_scheme = "wasd" if current == "arrows" else "arrows"
                set_control_scheme(new_scheme)
                self.settings = load_settings()
                self.controls = load_controls()
            return
        if symbol == arcade.key.ESCAPE:
            self.game_view.reload_controls()
            self.window.show_view(self.settings_view)