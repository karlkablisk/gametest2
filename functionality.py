#functionality.py - handles all functionality and creation of settings
from PIL import Image
import io
import os
from urllib.parse import urlparse
import base64
import json


location_image = "https://hips.hearstapps.com/hmg-prod/images/bojnice-castle-1603142898.jpg"
location_name = "Default Location"

def get_image_or_placeholder(path, color="grey"):
    if isinstance(path, str):
        if os.path.exists(path) or bool(urlparse(path).netloc):
            return path
        else:
            img = Image.new('RGB', (100, 100), color=color)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            data_url = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
            return f"data:image/png;base64,{data_url}"

class Player:
    def __init__(self):
        self.image = get_image_or_placeholder("placeholder_player_image.png", "blue")
        self.name = "Player Name"
        self.stats = {"Health": 100, "Attack": 50, "Defense": 30, "Strength": 5, "Dexterity": 5, "Agility": 5, "Charisma": 5, "Luck": 5}
        self.inventory = []
        self.thought_cabinet = []
        self.equipment = {
            "Head": None,
            "Arms": None,
            "Legs": None,
            "Torso": None,
            "Neck": None,
            "Accessory1": None,
            "Accessory2": None,
        }

    def set_name(self, new_name):
        self.name = new_name

    def set_image(self, new_image):
        self.image = new_image

class Item:
    def __init__(self, image, name, modifier, modifies, description):
        self.image = get_image_or_placeholder(image, "green")
        self.name = name
        self.modifier = modifier
        self.modifies = modifies
        self.description = description

class Dialogue:
    def __init__(self):
        self.speakers = {}

    def add_speaker(self, name, image):
        self.speakers[name] = {"image": get_image_or_placeholder(image, "red"), "dialogues": []}

    def add_dialogue(self, name, text):
        if name in self.speakers:
            self.speakers[name]["dialogues"].append(text)

    def remove_speaker(self, name):
        if name in self.speakers:
            del self.speakers[name]

player = Player()
dialogue = Dialogue()

def save_settings():
    settings = {
        "player": {
            "image": player.image,
            "name": player.name,
            "stats": player.stats,
            "inventory": [item.__dict__ for item in player.inventory],
            "equipment": {key: (value.__dict__ if value else None) for key, value in player.equipment.items()},
            "thought_cabinet": player.thought_cabinet,
        },
        "dialogue": {
            "speakers": {key: {"image": value["image"], "dialogues": value["dialogues"]} for key, value in dialogue.speakers.items()},
        },
        "location": {
            "name": location_name,
            "image": location_image,
        }
    }
    with open('settings/settings.json', 'w') as f:
        json.dump(settings, f, indent=4)

def load_settings():
    with open('settings/settings.json', 'r') as f:
        settings = json.load(f)

    global player, dialogue, location_name, location_image
    
    player.image = settings["player"]["image"]
    player.name = settings["player"]["name"]
    player.stats = settings["player"]["stats"]
    player.inventory = [Item(**item) for item in settings["player"]["inventory"]]
    player.equipment = {key: (Item(**value) if value else None) for key, value in settings["player"]["equipment"].items()}
    player.thought_cabinet = settings["player"]["thought_cabinet"]

    dialogue.speakers = {key: {"image": value["image"], "dialogues": value["dialogues"]} for key, value in settings["dialogue"]["speakers"].items()}
    
    location_name = settings["location"]["name"]
    location_image = settings["location"]["image"]
