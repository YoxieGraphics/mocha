import os
import json

SETTINGS_FILE = 'settings.json'

def save_settings(gui):
    settings = {
        'url': gui.url_input.text(),
        'output_type': 'video' if gui.video_radio.isChecked() else 'audio',
        'location': gui.location_input.text(),
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)

def load_settings(gui):
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            gui.url_input.setText(settings.get('url', ''))
            if settings.get('output_type', 'video') == 'video':
                gui.video_radio.setChecked(True)
            else:
                gui.audio_radio.setChecked(True)
            gui.location_input.setText(settings.get('location', ''))
