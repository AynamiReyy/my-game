import arcade
from typing import Iterable, List


class Animation:
    """Utility to manage a list of textures as an animation.

    - paths: iterable of image paths that will be loaded with arcade.load_texture
    - frame_duration: seconds per frame
    - loop: whether to loop back to the first frame when finished
    - hold_last: if True, advance frames until the last and then keep showing the last
                 (useful for jump/crouch states where sprite should "hang" on last frame)
    """

    def __init__(self, paths: Iterable[str], frame_duration: float = 0.1, loop: bool = True, hold_last: bool = False):
        self.textures: List[arcade.Texture] = [arcade.load_texture(p) for p in paths]
        self.frame_duration = frame_duration
        self.loop = loop
        self.hold_last = hold_last

        # runtime state
        self._index = 0
        self._time = 0.0

    def reset(self) -> None:
        """Reset animation to the first frame and zero time."""
        self._index = 0
        self._time = 0.0

    def update(self, delta_time: float) -> None:
        """Advance the animation according to delta_time and current flags."""
        if not self.textures:
            return
        self._time += delta_time
        if self._time >= self.frame_duration:
            self._time = 0.0
            if self.loop:
                # loop around
                self._index = (self._index + 1) % len(self.textures)
            else:
                # non-looping: either hold the last, or advance until the last
                if self.hold_last:
                    if self._index < len(self.textures) - 1:
                        self._index += 1
                    # else keep showing last
                else:
                    # advance until last, then keep it
                    if self._index < len(self.textures) - 1:
                        self._index += 1

    def current(self):
        """Return current arcade.Texture or None if empty."""
        if not self.textures:
            return None
        return self.textures[self._index]
