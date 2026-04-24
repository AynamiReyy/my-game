import arcade
from arcade.tilemap import TileMap, load_tilemap
from pyglet.math import Vec2

from Creatures.Scott.Scott import Scott
from game_src.constants import (
    MAP_HEIGHT_TILES,
    MAP_TILE_HEIGHT,
    MAP_TILE_WIDTH,
    MAP_WIDTH_TILES,
    TextureGroup,
    TMX_MAP_PATH,
)
from settings.config.config import load_controls
from settings.view_src.pause_view import PauseView


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.tile_map: TileMap | None = None
        self._map_scale = 1.0
        self.world_camera = arcade.Camera2D()
        self.ui_camera = arcade.Camera2D()
        self._hud: arcade.Text | None = None
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
        if self.tile_map is None:
            self._load_tile_map()
        self._sync_cameras()

    def _world_map_size(self) -> tuple[float, float]:
        return (
            MAP_WIDTH_TILES * MAP_TILE_WIDTH * self._map_scale,
            MAP_HEIGHT_TILES * MAP_TILE_HEIGHT * self._map_scale,
        )

    def _sync_cameras(self) -> None:
        self.world_camera.match_window()
        self.ui_camera.match_window(position=True)
        self._rebuild_hud_text()
        self._clamp_world_camera_to_map()

    def _rebuild_hud_text(self) -> None:
        self._hud = arcade.Text(
            "ESC — пауза    ←/→ — движение    ↑ — прыжок",
            12,
            self.window.height - 8,
            arcade.color.WHITE,
            14,
            anchor_y="top",
        )

    def _clamp_axis(self, center: float, half_visible: float, world_size: float) -> float:
        if world_size <= 2 * half_visible:
            return world_size / 2
        return max(half_visible, min(center, world_size - half_visible))

    def _clamp_world_camera_to_map(self) -> None:
        if self.tile_map is None:
            return
        mw, mh = self._world_map_size()
        half_w = self.world_camera.width / 2
        half_h = self.world_camera.height / 2
        px, py = self.player.position
        self.world_camera.position = (
            self._clamp_axis(px, half_w, mw),
            self._clamp_axis(py, half_h, mh),
        )

    def on_resize(self, width: int, height: int) -> bool | None:
        if self.tile_map is not None:
            self._sync_cameras()
        return None

    def _load_tile_map(self) -> None:
        map_w = MAP_WIDTH_TILES * MAP_TILE_WIDTH
        map_h = MAP_HEIGHT_TILES * MAP_TILE_HEIGHT
        self._map_scale = min(self.window.width / map_w, self.window.height / map_h)
        layer_options = {"Flor": {"use_spatial_hash": True}}
        self.tile_map = load_tilemap(
            TMX_MAP_PATH,
            scaling=self._map_scale,
            offset=Vec2(0, 0),
            layer_options=layer_options,
        )
        self.player.platform_list = self.tile_map.sprite_lists["Flor"]
        flor = self.tile_map.sprite_lists["Flor"]
        lowest = min(flor, key=lambda s: s.center_y)
        # Масштаб как у тайлов — иначе на большом экране спрайт крошечный и «теряется» на карте.
        self.player.scale = self._map_scale
        mw = map_w * self._map_scale
        self.player.center_x = mw * 0.2
        self.player.bottom = lowest.top + 1

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
        if self.tile_map is not None:
            self.world_camera.use()
            for sprite_list in self.tile_map.sprite_lists.values():
                sprite_list.draw()
            self.player_list.draw()
        self.ui_camera.use()
        if self._hud is not None:
            self._hud.draw()

    def on_update(self, delta_time):
        if self.paused:
            return

        self.player.change_x = 0
        if self.controls.get("left", arcade.key.LEFT) in self.pressed_keys:
            self.player.change_x = -1
        elif self.controls.get("right", arcade.key.RIGHT) in self.pressed_keys:
            self.player.change_x = 1

        self.player_list.update(delta_time)
        pad = 8 * self._map_scale
        half_w = self.player.width / 2
        mw, _ = self._world_map_size()
        self.player.center_x = min(max(self.player.center_x, half_w + pad), mw - half_w - pad)
        self._clamp_world_camera_to_map()

    def resume(self):
        self.paused = False
        self.pressed_keys.clear()
        self.reload_controls()