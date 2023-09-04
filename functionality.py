from PIL import Image
import io

def generate_placeholder_image(color="grey"):
    img = Image.new('RGB', (100, 100), color=color)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

class Player:
    def __init__(self):
        self.image = "placeholder_player_image.png"
        self.stats = {"Health": 100, "Attack": 50, "Defense": 30}
        self.inventory = []
        self.equipment = {
            "Head": None,
            "Arms": None,
            "Legs": None,
            "Torso": None,
            "Neck": None,
            "Accessory1": None,
            "Accessory2": None,
        }
        
class Item:
    def __init__(self, image, name, modifier, modifies, description):
        self.image = image
        self.name = name
        self.modifier = modifier
        self.modifies = modifies
        self.description = description
        
class Dialogue:
    def __init__(self):
        self.speakers = {}

    def add_speaker(self, name, image):
        self.speakers[name] = {"image": image, "dialogues": []}

    def add_dialogue(self, name, text):
        if name in self.speakers:
            self.speakers[name]["dialogues"].append(text)

    def remove_speaker(self, name):
        if name in self.speakers:
            del self.speakers[name]

player = Player()
dialogue = Dialogue()
