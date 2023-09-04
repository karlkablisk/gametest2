from PIL import Image
import io
import os
from urllib.parse import urlparse
import base64


location_name = "Default Location"

def get_image_or_placeholder(path, color="grey", height=None):
    if isinstance(path, str):
        if os.path.exists(path) or bool(urlparse(path).netloc):
            if height:
                img = Image.open(path)
                width = int((height / img.height) * img.width)
                img = img.resize((width, height), Image.ANTIALIAS)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                data_url = base64.b64encode(img_byte_arr.getvalue()).decode('ascii')
                return f"data:image/png;base64,{data_url}"
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
