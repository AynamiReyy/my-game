import json
import tkinter as tk

import arcade

from game_src.Game import MyGame


def get_screen_size() -> tuple[int, int]:
    root = tk.Tk()
    size = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    return size


def load_settings() -> dict:
    try:
        with open("settings/settings.json") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"fullscreen": False}


SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()
SETTINGS = load_settings()


def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Drawing Example")
    if SETTINGS.get("fullscreen", False):
        window.set_fullscreen(True)

    window.show_view(MyGame())
    arcade.run()


if __name__ == "__main__":
    main()