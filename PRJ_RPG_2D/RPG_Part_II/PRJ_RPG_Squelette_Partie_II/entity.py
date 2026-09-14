import arcade
import json
from PIL import Image
import tempfile, os
from typing import List, Tuple
from constants import *




class Entity(arcade.Sprite):
    def __init__(self, file_name: str, scaling: float,
                 img_width: int, img_height: int,
                 coords: List[List[Tuple[int, int]]]):
        # coords = [[(x,y), ...],  # anim 0
        #           [(x,y), ...],  # anim 1
        #           ...]
        super().__init__(scale=scaling)

        self.file_name = file_name
        self.scaling = scaling
        self.img_width = img_width
        self.img_height = img_height
        self.coords = coords

        # État commun utilisé par Player
        self.textures: List[List[arcade.Texture]] = []
        self.current_texture_indice = 0
        self.status = 0
        self.attributes = {}

        # Position par défaut (si ton code l'attend)
        self.center_x = 0
        self.center_y = 0

        # ---- Construction des textures à partir de la spritesheet ----
        # Dossier temporaire pour stocker les frames découpées
        self._temp_dir = tempfile.mkdtemp(prefix="rpg_frames_")

        # Ouvre une seule fois la spritesheet
        sheet = Image.open(self.file_name).convert("RGBA")

        # Construit: List[List[arcade.Texture]]
        for anim in self.coords:
            frames = []
            for (x, y) in anim:
                # Découpe (x, y, x+w, y+h)
                region = sheet.crop((x, y, x + self.img_width, y + self.img_height))
                # Sauvegarde en PNG temporaire puis charge via arcade.load_texture (1 arg)
                frame_path = os.path.join(
                    self._temp_dir, f"{os.path.basename(self.file_name)}_{x}_{y}.png"
                )
                region.save(frame_path, format="PNG")
                tex = arcade.load_texture(frame_path)
                frames.append(tex)
            self.textures.append(frames)

        # Texture initiale
        if self.textures and self.textures[0]:
            self.texture = self.textures[0][0]



    def setup(self):
        # Compatibilité avec l'ancien code : on a déjà tout chargé dans __init__
        pass

    def update(self):
        pass
