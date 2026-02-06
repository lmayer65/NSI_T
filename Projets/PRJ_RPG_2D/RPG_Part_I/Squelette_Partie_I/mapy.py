from constants import*
import arcade



class Map :
    def __init__(self, game) :
        self.tile_map = None  # Future carte du jeu
        self.game = game      # Permet d'accéder à tous les éléments du jeu
        
        
    def setup(self) :
        # Traitement des calques à collisions.
        layers_options = {
            "ground_collide1" : {"use_spatial_hash": True },
            "nature_collide2" : {"use_spatial_hash": True },
            "house_collide2" : {"use_spatial_hash": True }
        }
        
        # Charge la map en format .json
        self.tile_map = arcade.load_tilemap(MAP_FILE, MAP_SCALING, layers_options)
        

    def set_collisions(self) :
        # Indique les calques à collision
        self.walls = [self.game.scene["ground_collide1"],self.game.scene["nature_collide2"], \
                 self.game.scene["house_collide2"]]
        
        
