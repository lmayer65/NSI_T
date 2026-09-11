from mapy import *
from constants import*
import arcade



# Classe de base du jeu
class My_Game(arcade.Window):  # Hérite de la classe `Window`
    def __init__(self):
        # Création de la fenêtre 
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        self.map = None    # Instance de la classe `Map`
        self.scene = None  # Mise à jour et affichage de la carte
        

    # Chargement, mise en route des éléments du jeu
    def setup(self):
        # Couleur de fond de la map.
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
        # Création de la map
        self.map = Map(self)
        self.map.setup()
        self.scene = arcade.Scene.from_tilemap(self.map.tile_map)
        self.map.set_collisions()
        
       
      
    # Affichage des éléments 
    # ATTENTIONà l'ordre des instructions
    def on_draw(self):
        # Efface l'écran
        self.clear()     

        # Affichage de la scène (map)
        self.scene.draw()
        
       
        


# Fonction principale
# ATTENTION : NE PAS CHANGER
def main():
    window = My_Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()