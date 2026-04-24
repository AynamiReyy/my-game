import arcade

from game_src.constants import TextureGroup
from Creatures.Scott.animation import Animation


class Scott(arcade.Sprite):
    JUMP_VELOCITY = 600.0
    GRAVITY = 1200.0
    MOVE_SPEED = 5
    MAX_JUMPS = 2
    FRAME_DURATION = 0.1

    def __init__(self, *image_paths: str):
        super().__init__(image_paths[0])
        self.change_x = 0
        self.change_y = 0
        self.platform_list: arcade.SpriteList | None = None
        # Create Animation objects for each state. Using the helper keeps logic
        # consistent and makes it easy to modify behaviour (looping/holding) per-state.
        # frame_duration is shared by default; you can pass different values if needed.
        self.anim_crouch = Animation(TextureGroup.CROUCH, frame_duration=self.FRAME_DURATION, loop=False, hold_last=True)
        self.anim_jump = Animation(TextureGroup.JUMP, frame_duration=self.FRAME_DURATION, loop=False, hold_last=True)
        self.anim_forward = Animation(TextureGroup.WALK_FORWARD, frame_duration=self.FRAME_DURATION, loop=True)
        self.anim_back = Animation(TextureGroup.WALK_BACKWARD, frame_duration=self.FRAME_DURATION, loop=True)
        self.anim_idle = Animation(TextureGroup.IDLE, frame_duration=self.FRAME_DURATION, loop=True)

        # runtime animation pointer
        self._current_animation: Animation | None = self.anim_idle
        # start with idle texture
        self.texture = self._current_animation.current()
        self._animation_time = 0.0
        self.jump_count = 0
        self.is_crouching = False
        self.ground_y = 300
        self._current_state = "idle"

    def jump(self):
        if self.jump_count < self.MAX_JUMPS:
            self.change_y = self.JUMP_VELOCITY
            self.jump_count += 1
            self.is_crouching = False

    def crouch(self, crouching: bool):
        if self.jump_count > 0:
            return
        self.is_crouching = crouching
        if crouching:
            self.change_y = 0

    def update(self, delta_time: float = 0):
        self.center_x += self.change_x * self.MOVE_SPEED

        if self.is_crouching:
            self.change_y = 0
        else:
            self.change_y -= self.GRAVITY * delta_time
            self.center_y += self.change_y * delta_time

        if self.platform_list is not None:
            self._resolve_platforms(delta_time)
        elif not self.is_crouching and self.center_y <= self.ground_y:
            self.center_y = self.ground_y
            self.change_y = 0
            self.jump_count = 0

        self._update_animation(delta_time)

    def _overlaps_platform_x(self, platform: arcade.Sprite) -> bool:
        return platform.left < self.right and platform.right > self.left

    def _resolve_platforms(self, delta_time: float) -> None:
        """Платформы только снизу (как односторонние). Без sweep легко «пролетать» сквозь тайл за кадр."""
        if not self.platform_list or len(self.platform_list) == 0:
            return
        if self.change_y > 0:
            return

        scale = max(abs(self.scale_x), abs(self.scale_y), 1.0)
        slack_y = max(8.0 * scale, abs(self.change_y) * delta_time + 4.0 * scale)
        prev_bottom = self.bottom - self.change_y * delta_time

        candidates: list[arcade.Sprite] = []
        for platform in self.platform_list:
            if not self._overlaps_platform_x(platform):
                continue
            top = platform.top
            if self.top <= top:
                continue
            if prev_bottom >= top - 2.0 * scale and self.bottom <= top + slack_y:
                candidates.append(platform)

        if candidates:
            best = max(candidates, key=lambda p: p.top)
            self.bottom = best.top
            if self.change_y < 0:
                self.change_y = 0
            self.jump_count = 0

    def _update_animation(self, delta_time: float):
        # Choose animation based on state
        if self.is_crouching:
            anim = self.anim_crouch
            state = "crouch"
        elif self.jump_count > 0:
            anim = self.anim_jump
            state = "jump"
        elif self.change_x != 0:
            anim = self.anim_forward if self.change_x > 0 else self.anim_back
            state = "walk"
        else:
            anim = self.anim_idle
            state = "idle"

        # If animation changed, reset the new one so it starts from frame 0
        if anim is not self._current_animation:
            anim.reset()
            self._current_animation = anim
            self._current_state = state

        # Update the currently selected animation and apply its texture
        self._current_animation.update(delta_time)
        tex = self._current_animation.current()
        if tex is not None:
            self.texture = tex

    def _set_state(self, state: str):
        if self._current_state != state:
            self.cur_texture_index = 0
            self._current_state = state
