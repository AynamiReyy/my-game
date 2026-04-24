import json
from pathlib import Path
import arcade


SETTINGS_FILE = Path("settings/settings.json")

ARROW_CONTROLS = {
    "left": arcade.key.LEFT,
    "right": arcade.key.RIGHT,
    "jump": arcade.key.UP,
    "crouch": arcade.key.DOWN,
    "pause": arcade.key.ESCAPE,
}

WASD_CONTROLS = {
    "left": arcade.key.A,
    "right": arcade.key.D,
    "jump": arcade.key.W,
    "crouch": arcade.key.S,
    "pause": arcade.key.ESCAPE,
}


def load_settings() -> dict:
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"fullscreen": False, "control_scheme": "arrows"}


def save_settings(settings: dict) -> bool:
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def toggle_fullscreen(settings: dict) -> bool:
    settings["fullscreen"] = not settings.get("fullscreen", False)
    save_settings(settings)
    return settings["fullscreen"]


def load_controls() -> dict:
    settings = load_settings()
    scheme = settings.get("control_scheme", "arrows")
    return WASD_CONTROLS.copy() if scheme == "wasd" else ARROW_CONTROLS.copy()


def save_controls(controls: dict) -> bool:
    settings = load_settings()
    settings["controls"] = {k: v for k, v in controls.items() if v is not None}
    return save_settings(settings)


def set_control_scheme(scheme: str) -> bool:
    settings = load_settings()
    settings["control_scheme"] = scheme
    return save_settings(settings)
