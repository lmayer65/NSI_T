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
        self.clicked_mob = None
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
        self.player = Player(PLAYER_FILE, PLAYER_SCALING, PLAYER_WIDTH, \
                             PLAYER_HEIGHT, PLAYER_SPRITE_COORDS)

        # Ajout du joueur dans la list de mobs à afficher
        # ATTENTION : avant l'appel au setup(), plantage sinon !!
        self.sprites_list.append(self.player) 
        self.player.setup()
        
                   
        # Création de 15 orcs zombies (par exemple)
        for i in range(15) :
            zombi_orc = Mob(ZOMBIE_FILE, ZOMBIE_SCALING, ZOMBIE_WIDTH, \
                             ZOMBIE_HEIGHT, ZOMBIE_SPRITE_COORDS)
            zombi_orc.set_name("Zombie")
            zombi_orc.set_init_position(randint(400,800),randint(400,800))
            self.mobs.append(zombi_orc)
            
        # ATTENTION : avant l'appel au setup(), plantage sinon !!
        for mob in self.mobs :
            self.sprites_list.append(mob)
            mob.setup()
       


        # Création du moteur physique (déplacement et collision du joueur)
        self.map.set_collisions()
        
        
        # Création de l'IHM
        self.gui = Gui(self)
        self.gui.setup()
        
        
    """    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        if self.camera is not None :
            self.camera.match_window()"""

    
    def on_key_press(self, key, modifiers):
        # Mouvements du joueur
        if key == arcade.key.LEFT :
            self.player.change_x = -self.player.attributes["Speed"]
        elif key == arcade.key.RIGHT :
            self.player.change_x = self.player.attributes["Speed"]
        elif key == arcade.key.UP :
            self.player.change_y = self.player.attributes["Speed"]
        elif key == arcade.key.DOWN :
            self.player.change_y = -self.player.attributes["Speed"]
        
        
    def on_key_release(self, key, modifiers):
        # Fin de mouvement du joueur
        if key == arcade.key.LEFT :
            self.player.change_x = 0
        elif key == arcade.key.RIGHT :
            self.player.change_x = 0
        elif key == arcade.key.UP :
             self.player.change_y = 0
        elif key == arcade.key.DOWN :
             self.player.change_y = 0
             
    
    def on_mouse_press(self, x, y, button, modifiers) :
        # Attention à transformer les coordonnées relatives en coordonnées absolues
        new_x = self.player.center_x + x - SCREEN_WIDTH/2
        new_y = self.player.center_y + y - SCREEN_HEIGHT/2
        
        # Liste de sprites cliqués
        clicked_mobs = arcade.get_sprites_at_point((new_x, new_y), self.sprites_list)
        
        # Un seul sprite au mieux de choisi dans ce type de jeu (on écarte le joueur))
        if len(clicked_mobs) > 0 :
            # Ajout des caractéristiques du mob cliqué
            self.gui.add_clicked_mob(clicked_mobs[0])
            self.clicked_mob = clicked_mobs[0]
        else :
            # Mise à jour du GUI
            self.gui.update()
      

      
    def on_update(self, delta_time):  
        # Déplace le joueur, gère les collisions avec les objets de la map
        self.physics_engine.update() 
            
        # Mise à jour du joueur
        self.player.update()
        

        # Mise à jour des mobs
        for mob in self.mobs:
            mob.update()   # ou la signature que tu utilises
       
        
        # Positionne la caméra sur le joueur
        self.center_camera_to_player()
      
    
    # Permet de centrer la caméra sur le joueur
    def center_camera_to_player(self):
        # Camera2D se centre en position monde directement
        self.camera.position = (self.player.center_x, self.player.center_y)     
      
        
      
    def on_draw(self):
        # Efface l'écran
        self.clear()
        
        # Activation de la caméra
        self.camera.use()

        # Affichage de la scène (map)
        self.scene.draw()
        
        # Affichage des mobs
        self.sprites_list.draw()
        
        # Affichage de l'IHM
        self.gui.draw()
        

        



# Fonction principale
def main():
    window = My_Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()