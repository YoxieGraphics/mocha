import os
import json
from pathlib import Path

# settings directory and file
SETTINGS_DIR = Path.home() / 'mocha-downloader'
SETTINGS_FILE = SETTINGS_DIR / 'settings.json'

# bruhhhhhhhhh
SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

def save_settings(gui):
    settings = {
        'url': gui.url_input.text(),
        'output_type': 'video' if gui.video_radio.isChecked() else 'audio',
        'location': gui.location_input.text(),
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def load_settings(gui):
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            gui.url_input.setText(settings.get('url', ''))
            if settings.get('output_type', 'video') == 'video':
                gui.video_radio.setChecked(True)
            else:
                gui.audio_radio.setChecked(True)
            gui.location_input.setText(settings.get('location', ''))
