from entity import *



class Player(Entity) :
    def __init__(self, file_name, scaling, img_width, img_height, coords) :
        # Attention, bien indiquer la taille de l'image qui sera affichée !
        super().__init__(file_name, scaling, img_width, img_height, coords)
        
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
 
        # Fermeture du fichier
        f.close()
        
        
        # Position / Etat / Image de départ
        self.center_x = self.attributes["Init_x"] * MAP_SCALING
        self.init_x_pos = self.center_x
        
        ####### COMPLETER LES ORDONNEES ICI  ############

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
        ####### COMPLETER LES ORDONNEES ICI  ############
            
            
        ################################################################################
        ##################### ANIMATIONS ICI ###########################################
        ################################################################################

        # Appliquer la texture à utiliser (statut et indice)
        self.texture = self.textures[self.status][self.current_texture_indice]
       
        
               
        
        
            
        
            