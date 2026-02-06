from entity import *



class Player(Entity) :
    def __init__(self, file_name, scaling, img_width, img_height, coords, game) :
        # Attention, bien indiquer la taille de l'image qui sera affichée !
        super().__init__(file_name, scaling, img_width, img_height, coords, game)
        
        self.status = 0  

        # Position / image de départ
        self.init_x_pos = 0 
        self.init_y_pos = 0

        # -- TP 2 : Ajout des actions -- 
        self.actions = None     # Dictionnaire des actions
        self.action_name = ""   # Nom de l'action menée en cours (attaque ici)
        # -- TP 2 : FIN --

        self.game = None
        self.gui = None  
        
        
        
        
       
    def setup(self) :
        # Chargement des textures
        super().setup()
        
        
        # Ouverture des fichiers JSON
        # -- TP 2 : Chargement des fichiers -- 
        # Chargement des caractéristiques du joueur
        with open(PLAYER_CAR_FILE, "r", encoding="utf-8") as f:
            data: dict = json.load(f)
        self.attributes = data["Player"]
 
       
        # Chargement des actions (fichier .json)
        with open(PLAYER_ACTION_FILE, "r", encoding="utf-8") as f:
            self.actions: dict = json.load(f)
        # -- TP 2 : FIN ---
        

        # Position / Etat / Image de départ
        self.center_x = self.attributes["Init_x"] * MAP_SCALING
        self.center_y = self.attributes["Init_y"] * MAP_SCALING
        self.init_x_pos = self.center_x
        self.init_y_pos = self.center_y
        self.status = 0 
        self.texture = self.textures[0][0]
    


    # Lien vers game et gui.
    def set_context(self, game, gui) :
        self.game = game
        self.gui = gui    


    def update(self) :
        # --- Animation d'attaque ---
        if self.status & ATTACK:

            # 1) Déterminer UNE direction valide
            if self.status & WALK_LEFT:
                direction = WALK_LEFT
            elif self.status & WALK_RIGHT:
                direction = WALK_RIGHT
            elif self.status & WALK_UP:
                direction = WALK_UP
            else:
                direction = WALK_DOWN

            # 2) Etat d'attaque correspondant dans le dictionnaire textures
            status_for_texture = direction + ATTACK  # ex: WALK_DOWN + ATTACK = ATTACK_DOWN

            last_index = len(self.textures[status_for_texture]) - 1
            self.current_texture_indice += 1

            # 3) Fin de l'attaque -> retour à la marche
            if self.current_texture_indice > last_index:
                self.status = direction              # on garde juste la direction de marche
                self.status &= ~ATTACK               # on enlève le bit ATTACK
                self.current_texture_indice = 0
                self.texture = self.textures[self.status][self.current_texture_indice]
            else:
                # 4) Attaque en cours -> pas de déplacement
                self.change_x, self.change_y = 0, 0
                self.texture = self.textures[status_for_texture][self.current_texture_indice]
                return
        # --- fin animation d'attaque ---


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
        if self.change_x < 0 and self.change_y == 0 and not self.status == WALK_LEFT :
            self.status = WALK_LEFT 
            self.current_texture_indice = -1
        elif self.change_x > 0 and self.change_y == 0 and not self.status == WALK_RIGHT :
            self.status = WALK_RIGHT 
            self.current_texture_indice = -1
        elif self.change_y < 0 and self.change_x == 0 and not self.status == WALK_DOWN :
            self.status = WALK_DOWN  
            self.current_texture_indice = -1
        elif self.change_y > 0 and self.change_x == 0 and not self.status == WALK_UP :
            self.status = WALK_UP
            self.current_texture_indice = -1
            

        # Image suivante sauf si l'on est à la fin de l'animation (retour au début)
        self.current_texture_indice += 1
        if self.current_texture_indice >= len(self.textures[self.status]) :
            self.current_texture_indice = 0
    
        self.texture = self.textures[self.status][self.current_texture_indice]


    # -- TP 2 : Mode attaque (à venir) --
    def attack(self, mob) :
        if mob.attributes["HitPoints"] <= 0:
            self.clicked_mob = None
    # -- TP 2 : FIN --
       
        
               
        
        
            
        
            