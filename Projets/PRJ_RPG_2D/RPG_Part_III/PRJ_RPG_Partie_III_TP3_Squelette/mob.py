from entity import *




class Mob(Entity) :
    def __init__(self, file_name, scaling, img_width, img_height, coords, game) :
        # Attention, bien indiquer la taille de l'image qui sera affichée !
        super().__init__(file_name, scaling, img_width, img_height, coords, game)
        
        self.status = 0  
        
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
        self.center_y = y_pos * MAP_SCALING
        self.init_x_pos = self.center_x
        self.init_y_pos = self.center_y
        

           
    def setup(self) :
        # Chargement des textures
        super().setup()
        
        
        # Ouverture du fichier JSON file
        # Chargement des caractéristiques du joueur
        f = open(ZOMBIE_CAR_FILE)
        data = json.load(f)
        
        for key,value in data[self.attributes['Name']].items():
            self.attributes[key] = value
 
        # Fermeture du fichier
        f.close()
        
        self.status = WALK_DOWN
        self.current_texture_indice = 0
        self.texture = self.textures[self.status][0]

        
        
    # Mise à jour du mob    
    def update(self) :
        # --- TP1 AJOUT — Gestion de la mort (DEATH_DOWN) ---
        if self.status == DEAD :
            # On "tick" l’anim pour garder ta logique "toutes les 5 ticks on avance une frame"
            self.current_count_tick_move += 1
            if not self.current_count_tick_move % 5:
                self.current_texture_indice += 1

            # Si on a dépassé la dernière frame de l'anim de mort → on supprime le mob
            last_index = len(self.textures[self.status]) - 1
            if self.current_texture_indice >= last_index:
                # On fige visuellement sur la dernière frame puis on retire
                self.texture = self.textures[self.status][last_index]
                self.remove_from_sprite_lists()
                return

            # Sinon on affiche la frame courante de DEATH et on ne bouge pas
            self.change_x, self.change_y = 0, 0
            self.texture = self.textures[self.status][self.current_texture_indice]
            return
        # --- TP1 : FIN ---

        # Animation
        # Divise par 5 la vitesse d'animation
        if not self.current_count_tick_move % 5 :
            self.current_texture_indice += 1
        
        # Si l'indice courant dépasse le nombre d'images de l'animation courante,
        # on revient à la texture de départ
        if self.current_texture_indice >= len(self.textures[self.status]) :
            self.current_texture_indice = 0
        
        # Déplacement du monstre (jusqu'au bout du compteur initialisé)
        if self.current_count_tick_move < self.init_count_tick_move :
            if self.status == WALK_DOWN :
                self.change_y = -0.5
            elif self.status == WALK_UP :
                self.change_y = 0.5
            elif self.status == WALK_LEFT :
                self.change_x = -0.5
            elif self.status == WALK_RIGHT :
                self.change_x = 0.5
            
            
            self.center_x += self.change_x
            self.center_y += self.change_y
            
            self.current_count_tick_move += 1 
        
        # Déplacement aléatoire et réinitialisation des attributs
        else :
            self.current_count_tick_move = 0
            self.status = choice([WALK_DOWN, WALK_UP, WALK_LEFT, WALK_RIGHT])
            self.current_texture_indice = 0
            self.init_count_tick_move = randint(50,200)
            
                
        # Si changement de type de déplacement
        if self.change_x < 0 and self.status != WALK_LEFT :
             self.status = WALK_LEFT            
        elif self.change_x > 0 and self.status != WALK_RIGHT :
             self.status = WALK_RIGHT              
        elif self.change_y < 0 and self.status != WALK_DOWN :
             self.status = WALK_DOWN     
        elif self.change_y > 0 and self.status != WALK_UP :
             self.status = WALK_UP
        
        
        # Mise à zéro du déplacement et de la texture en cours
        self.change_x, self.change_y = 0,0                
        self.texture = self.textures[self.status][self.current_texture_indice]


    # -- TP 2 : Mode attaque (à venir) --
    def attack(self, mob) :
        pass
    # -- TP 2 : FIN --
            
        
        