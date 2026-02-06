from constants import *
import arcade
from PIL import Image
import tempfile, os, shutil
import json
from typing import Dict, List, Tuple



class Entity(arcade.Sprite):
    def __init__(self, file_name, scaling, img_width, img_height, coords, game):
        # Nouveau: ne pas utiliser l'ancien constructeur Sprite(file, x, y, w, h)
        super().__init__(scale=scaling)

        self.game = game
        self.file_name = file_name
        self.scaling = scaling
        self.img_width = img_width
        self.img_height = img_height

        # coords: dict {state: [(x,y), ...]}
        self.coords: Dict[int, List[Tuple[int, int]]] = coords
        self.textures: Dict[int, List[arcade.Texture]] = {}
        self.current_texture_indice = 0

        self.center_x = 0
        self.center_y = 0
        self.attributes = {}

        # Charger toutes les frames depuis la spritesheet
        self._temp_dir = tempfile.mkdtemp(prefix="rpg_frames_")
        sheet = Image.open(self.file_name).convert("RGBA")

        for key, frames_xy in self.coords.items():
            frames: List[arcade.Texture] = []
            rects = [(x, y, self.img_width, self.img_height) for (x, y) in frames_xy]
            for (x, y, w, h) in rects:
                region = sheet.crop((x, y, x + w, y + h))
                frame_path = os.path.join(
                    self._temp_dir, f"{os.path.basename(self.file_name)}_{key}_{x}_{y}.png"
                )
                region.save(frame_path, "PNG")
                tex = arcade.load_texture(frame_path)
                frames.append(tex)
            self.textures[key] = frames

        # Texture initiale (prend la première anim disponible)
        first_key = next(iter(self.textures.keys()))
        if self.textures[first_key]:
            self.texture = self.textures[first_key][0]

    def setup(self):
        # Compat: tout est déjà chargé dans __init__
        pass

    # Regénération des HP / mana etc.
    def regenerate(self) :
        return regen_tick(self, REGEN_PERIOD, REGEN_RATE)

    def attack(self, entity) :
        pass
    
    def update(self):
        pass

    def die(self) :
        pass
