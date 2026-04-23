import arcade

from game.constants import TextureGroup


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

        self.frames_crouch = [arcade.load_texture(p) for p in TextureGroup.CROUCH]
        self.frames_jump = [arcade.load_texture(p) for p in TextureGroup.JUMP]
        self.frames_forward = [arcade.load_texture(p) for p in TextureGroup.WALK_FORWARD]
        self.frames_back = [arcade.load_texture(p) for p in TextureGroup.WALK_BACKWARD]

        self.cur_texture_index = 0
        self.texture = self.frames_crouch[0]
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
            if self.center_y <= self.ground_y:
                self.center_y = self.ground_y
                self.change_y = 0
                self.jump_count = 0

        self._update_animation(delta_time)

    def _update_animation(self, delta_time: float):
        if self.is_crouching:
            frames = self.frames_crouch
            self._set_state("crouch")
        elif self.jump_count > 0:
            frames = self.frames_jump
            self._set_state("jump")
        elif self.change_x != 0:
            frames = self.frames_forward if self.change_x > 0 else self.frames_back
            self._set_state("walk")
        else:
            frames = [self.frames_forward[0]]
            self._set_state("idle")

        self._animation_time += delta_time
        if self._animation_time >= self.FRAME_DURATION:
            self._animation_time = 0.0
            if self._current_state == "walk" or self.cur_texture_index < len(frames) - 1:
                self.cur_texture_index = (self.cur_texture_index + 1) % len(frames)
        self.texture = frames[self.cur_texture_index]

    def _set_state(self, state: str):
        if self._current_state != state:
            self.cur_texture_index = 0
            self._current_state = state
