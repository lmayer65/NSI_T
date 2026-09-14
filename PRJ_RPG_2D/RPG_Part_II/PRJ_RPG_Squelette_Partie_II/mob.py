from entity import *




class Mob(Entity) :
    def __init__(self, file_name, scaling, img_width, img_height, coords) :
        # Attention, bien indiquer la taille de l'image qui sera affichée !
        super().__init__(file_name, scaling, img_width, img_height, coords)
        
        # Position / Image de départ
        self.init_x_pos = 0
        self.init_y_pos = 0
        
        # Compteur pour le nombre de déplacement
        self.init_count_tick_move = randint(50,200)
        self.current_count_tick_move = 0
        
        
        
    def set_name(self, name) :
        self.attributes['Name'] = name
        
    def set_init_position(self, x_pos, y_pos):
        self.center_x = x_pos * MAP_SCALING
        self.init_x_pos = self.center_x
        
        ####### COMPLETER LES ORDONNEES ICI  ############
        

           
    def setup(self) :
        # Chargement des textures
        super().setup()
        
        
        # Ouverture du fichier JSON file
        # Chargement des caractéristiques du joueur
        f = open(MOB_CARACTERISTICS_FILE)
        data = json.load(f)
        
        for key,value in data[self.attributes['Name']].items():
            self.attributes[key] = value
 
        # Fermeture du fichier
        f.close()
        
        self.status = 0 
        self.current_texture_indice = 0
        self.texture = self.textures[0][0]
        
        
        
    def update(self) :

        ################################################################################
        ##################### ANIMATIONS ICI ###########################################
        ################################################################################
        
        
        # Mise à zéro du déplacement et de la texture en cours
        self.change_x, self.change_y = 0,0                
        self.texture = self.textures[self.status][self.current_texture_indice]
            
        
        