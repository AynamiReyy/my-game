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
    """Groups of texture file paths used by the player and other sprites.

    Keep paths relative to project root. This centralised list makes it easy
    to find and change character frames (walk/jump/crouch/idle).
    """
    CROUCH = [
        "Creatures/Scott/texture_for_animation/crouch/croach-1.png",
        "Creatures/Scott/texture_for_animation/crouch/crouch-2.png",
        "Creatures/Scott/texture_for_animation/crouch/crouch-3.png",
        "Creatures/Scott/texture_for_animation/crouch/crouch-4.png",
    ]
    JUMP = [
        "Creatures/Scott/texture_for_animation/jump/jump-1.png",
        "Creatures/Scott/texture_for_animation/jump/jump-2.png",
        "Creatures/Scott/texture_for_animation/jump/jump-3.png",
        "Creatures/Scott/texture_for_animation/jump/jump-4.png",
    ]
    WALK_FORWARD = [
        "Creatures/Scott/texture_for_animation/walk/walk-1.png",
        "Creatures/Scott/texture_for_animation/walk/walk-2.png",
        "Creatures/Scott/texture_for_animation/walk/walk-3.png",
        "Creatures/Scott/texture_for_animation/walk/walk-4.png",
    ]
    WALK_BACKWARD = [
        "Creatures/Scott/texture_for_animation/walk_back/walk-1-back.png",
        "Creatures/Scott/texture_for_animation/walk_back/walk-2-back.png",
        "Creatures/Scott/texture_for_animation/walk_back/walk-3-back.png",
        "Creatures/Scott/texture_for_animation/walk_back/walk-4-back.png",
    ]
    # Idle / no-move animation frames (small breathing/idle animation)
    IDLE = [
        "Creatures/Scott/texture_for_animation/no_move_animation/no_move_1.png",
        "Creatures/Scott/texture_for_animation/no_move_animation/no_move_2.png",
        "Creatures/Scott/texture_for_animation/no_move_animation/no_move_3.png",
        "Creatures/Scott/texture_for_animation/no_move_animation/no_move_4.png",
    ]

    @classmethod
    def all(cls) -> list[str]:
        # Include IDLE frames too so they are available for preloading if needed
        return cls.CROUCH + cls.JUMP + cls.WALK_FORWARD + cls.WALK_BACKWARD + cls.IDLE


BG_PATH: Final[str] = "game/textureBackground/background.png"
GROUND_Y: Final[int] = 300

TMX_MAP_PATH: Final[str] = "location_first/yong_uil.tmx"
MAP_TILE_WIDTH: Final[int] = 32
MAP_TILE_HEIGHT: Final[int] = 32
MAP_WIDTH_TILES: Final[int] = 30
MAP_HEIGHT_TILES: Final[int] = 20