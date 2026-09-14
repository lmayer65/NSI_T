import arcade
from random import randint


# L'écran en général
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NSI_RPG"



# Map
######### A COMPLETER / MODIFIER si autre map #########
MAP_FILE = "Maps/map.json"
MAP_SCALING = 2   # Mise à l'échelle souhaitée d'un tile
MAP_WIDTH = 1280  # Largeur de la carte
MAP_HEIGHT = 1280 # Hauteur de la carte



# Caractéristiques du joueur
######### A COMPLETER / MODIFIER si autre joueur #########
PLAYER_WIDTH,PLAYER_HEIGHT = 16, 32
PLAYER_SCALING = 2
PLAYER_FILE = "Mobs/player.png"
PLAYER_CARACTERISTICS_FILE = "Mobs/player.json"


# Indices des animations du joueur
### NE PAS CHANGER ###
PLAYER_WALK_DOWN, PLAYER_WALK_LEFT, PLAYER_WALK_RIGHT,PLAYER_WALK_UP = 0, 1, 2, 3
PLAYER_ATTACK_DOWN, PLAYER_ATTACK_LEFT, PLAYER_ATTACK_RIGHT, PLAYER_ATTACK_UP = 4, 5, 6, 7


# Coordonnées des images de chaque animation du joueur
######### A COMPLETER / MODIFIER si autre image #########
PLAYER_WD_COORDS = [(0,0), (16,0), (32,0), (48,0)]        # Marche vers le bas
PLAYER_WR_COORDS = [(0,32)]    # Marche vers la droite
PLAYER_WU_COORDS = [(0,64)]    # Marche vers le haut
PLAYER_WL_COORDS = [(0,96)]    # Marche vers la gauche

PLAYER_AD_COORDS = [(6,128), (38,128), (70,128), (102,128)]  # Attaque vers la droite
PLAYER_AU_COORDS = [(6,160)]  # Attaque vers le haut
PLAYER_AR_COORDS = [(6,192)]  # Attaque vers la droite
PLAYER_AL_COORDS = [(6,224)]  # Attaque vers la gauche

# Regroupement des coordonnées précédentes dans une liste
### NE PAS CHANGER ###
PLAYER_SPRITE_COORDS = [PLAYER_WD_COORDS, PLAYER_WL_COORDS, PLAYER_WR_COORDS, PLAYER_WU_COORDS, \
        PLAYER_AD_COORDS, PLAYER_AL_COORDS, PLAYER_AR_COORDS, PLAYER_AU_COORDS  ]
    



# Caractéristiques d'un orc zombie
######### A COMPLETER / MODIFIER si autre image #########
ORC_WIDTH,ORC_HEIGHT = 32, 32
ORC_SCALING = 2
ORC_FILE = "Mobs/zombie.png"
MOB_CARACTERISTICS_FILE = "Mobs/mob.json"
    

WALK_DOWN, WALK_LEFT, WALK_RIGHT, WALK_UP = 0, 1, 2, 3
ATTACK_DOWN, ATTACK_LEFT, ATTACK_RIGHT, ATTACK_UP = 4, 5, 6, 7

# Coordonnées des images de chaque animation du joueur
######### A COMPLETER / MODIFIER si autre image #########
ORC_WD_COORDS = [(0,0)]
ORC_WU_COORDS = [(0,32)]
ORC_WR_COORDS = [(0,64)]
ORC_WL_COORDS = [(0,96)]

ORC_AD_COORDS = [(0,128)]
ORC_AU_COORDS = [(0,160)]
ORC_AR_COORDS = [(0,192)]
ORC_AL_COORDS = [(0,224)]

ORC_SPRITE_COORDS = [ORC_WD_COORDS, ORC_WL_COORDS, ORC_WR_COORDS, ORC_WU_COORDS, \
        ORC_AD_COORDS, ORC_AL_COORDS, ORC_AR_COORDS, ORC_AU_COORDS  ]
