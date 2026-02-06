from entity import *



class Player(Entity) :
    def __init__(self, file_name, scaling, img_width, img_height, coords) :
        # Attention, bien indiquer la taille de l'image qui sera affichée !
        super().__init__(file_name, scaling, img_width, img_height, coords)
        
        self.status = 0  
        self.xp = 0   # expérience du joueur
        
        # Position / image de départ
        self.init_x_pos = 0 
        self.init_y_pos = 0
        
        
        
       
    def setup(self) :
        # Chargement des textures
        super().setup()
        
        
        # Ouverture du fichier JSON file
        # Chargement des caractéristiques du joueur
        f = open(PLAYER_CARACTERISTICS_FILE)
        data = json.load(f)
        
        for key,value in data["Player"].items():
            self.attributes[key] = value

        # Expérience initiale du joueur
        self.xp = self.attributes["Experience"]
 
        # Fermeture du fichier
        f.close()
        
        
        # Position / Etat / Image de départ
        self.center_x = self.attributes["Init_x"] * MAP_SCALING
        self.center_y = self.attributes["Init_y"] * MAP_SCALING
        self.init_x_pos = self.center_x
        self.init_y_pos = self.center_y
        self.status = 0 
        self.texture = self.textures[0][0]
    

   
    def update(self) :
        # Le joueur doit rester sur la map
        # Les abscisses, ne pas dépasser la largeur de la map
        if self.center_x < 0 :
            self.center_x = 0        
        elif self.center_x > MAP_WIDTH * MAP_SCALING :
            self.center_x = MAP_WIDTH * MAP_SCALING 
            
        # Puis les ordonnées, ne pas dépasser la hauteur de la map
        if self.center_y < 0 :
            self.center_y = 0        
        elif self.center_y  > MAP_HEIGHT * MAP_SCALING :
            self.center_y = MAP_HEIGHT * MAP_SCALING 
            
            
        # Animation
        # Si le joueur ne bouge pas, pas d'animation
        if not self.change_x and not self.change_y :
            return
    
            
        # Si changement de type de déplacement
        if self.change_x < 0 and self.change_y == 0 and not self.status == PLAYER_WALK_LEFT :
            self.status = PLAYER_WALK_LEFT 
            self.current_texture_indice = -1
        elif self.change_x > 0 and self.change_y == 0 and not self.status == PLAYER_WALK_RIGHT :
            self.status = PLAYER_WALK_RIGHT 
            self.current_texture_indice = -1
        elif self.change_y < 0 and self.change_x == 0 and not self.status == PLAYER_WALK_DOWN :
            self.status = PLAYER_WALK_DOWN  
            self.current_texture_indice = -1
        elif self.change_y > 0 and self.change_x == 0 and not self.status == PLAYER_WALK_UP :
            self.status = PLAYER_WALK_UP
            self.current_texture_indice = -1
            

        # Image suivante sauf si l'on est à la fin de l'animation (retour au début)
        self.current_texture_indice += 1
        if self.current_texture_indice >= len(self.textures[self.status]) :
            self.current_texture_indice = 0
    
        self.texture = self.textures[self.status][self.current_texture_indice]
       
        
               
        
        
            
        
            