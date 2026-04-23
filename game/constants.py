import arcade
from typing import Final


KEY_UP = arcade.key.UP
KEY_DOWN = arcade.key.DOWN
KEY_LEFT = arcade.key.LEFT
KEY_RIGHT = arcade.key.RIGHT
KEY_ENTER = arcade.key.ENTER
KEY_ESCAPE = arcade.key.ESCAPE

KEY_NAMES: Final[dict[int, str]] = {
    arcade.key.UP: "Вверх",
    arcade.key.DOWN: "Вниз",
    arcade.key.LEFT: "Влево",
    arcade.key.RIGHT: "Вправо",
    arcade.key.SPACE: "Пробел",
    arcade.key.ENTER: "Enter",
    arcade.key.ESCAPE: "Esc",
    arcade.key.W: "W",
    arcade.key.A: "A",
    arcade.key.S: "S",
    arcade.key.D: "D",
}


class TextureGroup:
    CROUCH = [
        "Creatures/Scott/crouch/croach-1.png",
        "Creatures/Scott/crouch/crouch-2.png",
        "Creatures/Scott/crouch/crouch-3.png",
        "Creatures/Scott/crouch/crouch-4.png",
    ]
    JUMP = [
        "Creatures/Scott/jump/jump-1.png",
        "Creatures/Scott/jump/jump-2.png",
        "Creatures/Scott/jump/jump-3.png",
        "Creatures/Scott/jump/jump-4.png",
    ]
    WALK_FORWARD = [
        "Creatures/Scott/walk/walk-1.png",
        "Creatures/Scott/walk/walk-2.png",
        "Creatures/Scott/walk/walk-3.png",
        "Creatures/Scott/walk/walk-4.png",
    ]
    WALK_BACKWARD = [
        "Creatures/Scott/walk/walk-1-back.png",
        "Creatures/Scott/walk/walk-2-back.png",
        "Creatures/Scott/walk/walk-3-back.png",
        "Creatures/Scott/walk/walk-4-back.png",
    ]
    IDLE = [WALK_FORWARD[0]]

    @classmethod
    def all(cls) -> list[str]:
        return cls.CROUCH + cls.JUMP + cls.WALK_FORWARD + cls.WALK_BACKWARD


BG_PATH: Final[str] = "game/textureBackground/background.png"
GROUND_Y: Final[int] = 300
