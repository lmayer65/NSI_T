from map import *
from player import *
from mob import *
from gui import *
import arcade



# Classe de base du jeu
class My_Game(arcade.Window):  # Hérite de la classe `Window`
    def __init__(self):
        # Création de la fenêtre 
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
          
        self.map = None
       
        self.scene = None
        self.physics_engine = None
        self.camera = None
        
        self.player = None
        self.mobs = []
        self.sprites_list = None
        
        self.gui = None


    def setup(self):
        # Couleur de fond de la map.
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        
        # Création de la caméra
        self.camera = arcade.Camera2D()
        self.camera.match_window()

        
        # Création de la map
        self.map = Map(self)
        self.map.setup()
        self.scene = arcade.Scene.from_tilemap(self.map.tile_map)
        
        # Liste des mobs à afficher
        self.sprites_list = arcade.SpriteList()
        
        
        # Création du joueur
        ###### A COMPLETER #########
        
                   
        # Création de 15 orcs zombies (par exemple)
        ###### A COMPLETER #########
       


        # Création du moteur physique (déplacement et collision du joueur)
        if self.player != None :
            self.map.set_collisions()
        
        
        # Création de l'IHM
        self.gui = Gui(self)
        self.gui.setup()
        
        
        
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.camera.match_window()

    
    def on_key_press(self, key, modifiers):
        if self.player == None :
            return

        # Mouvements du joueur
        if key == arcade.key.LEFT :
            self.player.change_x = -self.player.attributes["Speed"]

        ########## A COMPLETER ICI ###########
        
        
        
    def on_key_release(self, key, modifiers):
        if self.player == None :
            return

        # Fin de mouvement du joueur
        if key == arcade.key.LEFT :
            self.player.change_x = 0

        ########## A COMPLETER ICI ###########
        
             
    
    def on_mouse_press(self, x, y, button, modifiers) :
        if self.player == None or self.gui == None :
            return

        # Attention à transformer les coordonnées relatives en coordonnées absolues
        new_x = self.player.center_x + x - SCREEN_WIDTH/2
        new_y = self.player.center_y + y - SCREEN_HEIGHT/2
        
        # Liste de sprites cliqués
        clicked_mob = arcade.get_sprites_at_point((new_x, new_y), self.sprites_list)
        
        # 0n seul sprite au mieux de choisi dans ce type de jeu
        if len(clicked_mob) > 0 :
            # Ajout des caractéristiques du mob cliqué
            self.gui.add_clicked_mob(clicked_mob[0])
        else :
            # Sinon, IHM de base
            self.gui.setup()
      
        
      
    def on_update(self, delta_time):
        # Déplace le joueur, gère les collisions avec les objets de la map
        if self.physics_engine != None :
            self.physics_engine.update() 
        
         
        # Mise à jour du joueur
        if self.player != None :
            self.player.update()
        
        # Mise à jour des mobs
        for mob in self.mobs :
            mob.update()
       
        
        # Positionne la caméra sur le joueur
        self.center_camera_to_player()
      
    

    # Permet de centrer la caméra sur le joueur
    def center_camera_to_player(self):
        # Camera2D se centre en position monde directement
        if self.camera != None and self.player != None:
            self.camera.position = (self.player.center_x, self.player.center_y)     
      
        
      
    def on_draw(self):
        # Efface l'écran
        self.clear()
        
        # Activation de la caméra
        if self.camera != None :
            self.camera.use()

        # Affichage de la scène (map)
        if self.scene != None :
            self.scene.draw()
        
        # Affichage des mobs
        if self.sprites_list != None :
            self.sprites_list.draw()
        
        # Affichage de l'IHM
        if self.gui != None :
            self.gui.draw()
        

        



# Fonction principale
def main():
    window = My_Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()