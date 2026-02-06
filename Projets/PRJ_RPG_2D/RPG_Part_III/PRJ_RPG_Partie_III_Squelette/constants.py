import arcade
from random import randint


# L'écran en général
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NSI_RPG"


# Map
MAP_FILE = "Maps/map.json"
MAP_SCALING = 2   # Mise à l'échelle souhaitée d'un tile
MAP_WIDTH = 1280  # Largeur de la carte
MAP_HEIGHT = 1280 # Hauteur de la carte


# Caractéristiques du joueur
PLAYER_WIDTH,PLAYER_HEIGHT = 32, 32
PLAYER_SCALING = 2
PLAYER_FILE = "assets/Player/player.png"
PLAYER_CARACTERISTICS_FILE = "assets/Player/player.json"

# Indices des animations du joueur
### NE PAS CHANGER ###
PLAYER_WALK_DOWN, PLAYER_WALK_LEFT, PLAYER_WALK_RIGHT,PLAYER_WALK_UP = 0, 1, 2, 3
PLAYER_ATTACK_DOWN, PLAYER_ATTACK_LEFT, PLAYER_ATTACK_RIGHT, PLAYER_ATTACK_UP = 4, 5, 6, 7

# Coordonnées des images de chaque animation du joueur
### A COMPLETER / MODIFIER si autre image ###
PLAYER_WD_COORDS = [(0,0), (32,0), (64,0), (96,0)]        # Marche vers le bas
PLAYER_WU_COORDS = [(0,32), (32,32), (64,32), (96,32)]    # Marche vers la droite
PLAYER_WR_COORDS = [(0,64), (32,64), (64,64), (96,64)]    # Marche vers le haut
PLAYER_WL_COORDS = [(0,96), (32,96), (64,96), (96,96)]    # Marche vers la gauche

PLAYER_AD_COORDS = [(6,128), (38,128), (70,128), (102,128)]  # Attaque vers la droite
PLAYER_AU_COORDS = [(6,160), (38,160), (70,160), (102,160)]  # Attaque vers le haut
PLAYER_AR_COORDS = [(6,192), (38,192), (70,192), (102,192)]  # Attaque vers la droite
PLAYER_AL_COORDS = [(6,224), (38,224), (70,224), (102,224)]  # Attaque vers la gauche


# Regroupement des coordonnées précédentes dans une liste
### NE PAS CHANGER ###
PLAYER_SPRITE_COORDS = [PLAYER_WD_COORDS, PLAYER_WL_COORDS, PLAYER_WR_COORDS, PLAYER_WU_COORDS, \
        PLAYER_AD_COORDS, PLAYER_AL_COORDS, PLAYER_AR_COORDS, PLAYER_AU_COORDS  ]
    

# Caractéristiques d'un orc zombie
ZOMBIE_WIDTH,ZOMBIE_HEIGHT = 32, 32
ZOMBIE_SCALING = 2
ZOMBIE_FILE = "assets/Mobs/zombie.png"
ZOMBIE_CARACTERISTICS_FILE = "assets/Mobs/zombie.json"
    
WALK_DOWN, WALK_LEFT, WALK_RIGHT, WALK_UP = 0, 1, 2, 3
ATTACK_DOWN, ATTACK_LEFT, ATTACK_RIGHT, ATTACK_UP = 4, 5, 6, 7


# Coordonnées des images de chaque animation du joueur
### A COMPLETER / MODIFIER si autre image ###
ZOMBIE_WD_COORDS = [(0,0), (32,0), (64,0), (96,0), (128,0), (160,0), (192,0), (224,0), (256,0)]
ZOMBIE_WU_COORDS = [(0,32), (32,32), (64,32), (96,32), (128,32), (160,32), (192,32), (224,32), (256,32)]
ZOMBIE_WR_COORDS = [(0,64), (32,64), (64,64), (96,64), (128,64), (160,64), (192,64), (224,64), (256,64)]
ZOMBIE_WL_COORDS = [(0,96), (32,96), (64,96), (96,96), (128,96), (160,96), (192,96), (224,96), (256,96)]

ZOMBIE_AD_COORDS = [(0,128), (32,128), (64,128), (96,128), (128,128), (160,128), (192,128), (224,128), (256,128)]
ZOMBIE_AU_COORDS = [(0,160), (32,160), (64,160), (96,160), (128,160), (160,160), (192,160), (224,160), (256,160)]
ZOMBIE_AR_COORDS = [(0,192), (32,192), (64,192), (96,192), (128,192), (160,192), (192,192), (224,192), (256,192)]
ZOMBIE_AL_COORDS = [(0,224), (32,224), (64,224), (96,224), (128,224), (160,224), (192,224), (224,224), (256,224)]


ZOMBIE_SPRITE_COORDS = [ZOMBIE_WD_COORDS, ZOMBIE_WL_COORDS, ZOMBIE_WR_COORDS, ZOMBIE_WU_COORDS, \
        ZOMBIE_AD_COORDS, ZOMBIE_AL_COORDS, ZOMBIE_AR_COORDS,ZOMBIE_AU_COORDS ]



# === TP1 AJOUT (GUI Actions + XP + DEATH timing) ===
# Icônes de la barre d'actions (à créer si pas présents)
GUI_ACTIONS_SPRITE      = "assets/GUI/actions_player.png"
GUI_ACTIONS_SPRITE_DOWN = "assets/GUI/actions_player_clicked.png"

# Barre d'actions (icônes uniquement, pas de clavier)
ACTIONBAR_SLOTS = 6
ACTIONBAR_BINDINGS = {
    0: "attack_0",  # défini dans warrior_actions.json
}

# Test pédagogique : gain d'XP quand un zombie meurt par clic (TP)
XP_PER_ZOMBIE = 5

# Durée (approx.) de l'animation de mort avant disparition
DEATH_DURATION = 0.9
