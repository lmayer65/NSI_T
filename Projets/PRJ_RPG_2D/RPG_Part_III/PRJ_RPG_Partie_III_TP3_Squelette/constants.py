import PIL.Image
import PIL
import arcade
import math
from random import randint, choice, random
from timer import *



##################################### MAP / ECRAN #################################################

# L'écran en général
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NSI_RPG"


# Map
MAP_FILE = "Maps/map.json"
MAP_SCALING = 2   # Mise à l'échelle souhaitée d'un tile
MAP_WIDTH = 1280  # Largeur de la carte
MAP_HEIGHT = 1280 # Hauteur de la carte
TILE_SIZE = 32    # Taille d'une tuile
PERFECT_COLLISION = True   # Collision au pixel près


########################################### ENTITIES ##########################################################

# Direction / Etat des monstres / joueur
WALK_DOWN, WALK_UP, WALK_RIGHT, WALK_LEFT = 1, 2, 4, 8
ATTACK_DOWN, ATTACK_UP, ATTACK_RIGHT, ATTACK_LEFT, ATTACK = 17, 18, 20, 24, 16
DEAD = 0

TARGET_IN_SIGHT = 60   # Angle du cône de vision (savoir si une cible est "devant" l'attaquant)
DEATH_DURATION = 4     # Durée de l'animation de la mort (secondes)
REGEN_PERIOD = 4       # Durée d'un cycle de regénération (secondes) 
REGEN_RATE = 4         # HP régénérés par cycle
COMBO_INTERVAL = 0.12  # délai entre 2 coups d’un même Repeat (en s)
MISS_RATE = 0.2        # Probabilité de rater une attaque (0.0 à 1.0) si pas précisé   


############################################ JOUEUR #########################################################

# Caractéristiques du joueur
PLAYER_WIDTH,PLAYER_HEIGHT = 32, 32
PLAYER_SCALING = 2
PLAYER_FILE = "Mobs/Player/player.png"  # Animations du joueur
PLAYER_CAR_FILE = "Mobs/Player/player.json"
PLAYER_ACTION_FILE = "Mobs/Player/warrior_actions.json"
PLAYER_LEVELING = { 1 : 0, 2 : 20, 3 : 300 } # XP nécessaire pour chaque niveau
    
PLAYER_WD_COORDS = [(0,0), (32,0), (64,0), (96,0)]
PLAYER_WU_COORDS = [(0,32), (32,32), (64,32), (96,32)]
PLAYER_WR_COORDS = [(0,64), (32,64), (64,64), (96,64)]
PLAYER_WL_COORDS = [(0,96), (32,96), (64,96), (96,96)]

PLAYER_AD_COORDS = [(0,128), (32,128), (64,128), (96,128)]
PLAYER_AU_COORDS = [(0,160), (32,160), (64,160), (96,160)]
PLAYER_AR_COORDS = [(0,192), (32,192), (64,192), (96,192)]
PLAYER_AL_COORDS = [(0,224), (32,224), (64,224), (96,224)]

# On ne tient compte que de l'animation de mort vers le bas pour l'instant
PLAYER_DD_COORDS = [(0,256), (32,256), (64,256), (96,256)]
PLAYER_DU_COORDS = []
PLAYER_DR_COORDS = []
PLAYER_DL_COORDS = []


# Permet de relier état du joueur et série de textures à afficher
PLAYER_SPRITE_COORDS = { WALK_DOWN : PLAYER_WD_COORDS, WALK_UP : PLAYER_WU_COORDS, WALK_RIGHT : PLAYER_WR_COORDS, 
                        WALK_LEFT : PLAYER_WL_COORDS, ATTACK_DOWN : PLAYER_AD_COORDS, ATTACK_UP : PLAYER_AU_COORDS, 
                        ATTACK_RIGHT : PLAYER_AR_COORDS, ATTACK_LEFT : PLAYER_AL_COORDS, DEAD : PLAYER_DD_COORDS  }
    

######################################## MOBS ################################################

# Durée d'aggo d'un monstre
AGGRO_DURATION = 20.0  # secondes de poursuite après avoir été touché
RUNNING = 3            # Facteur de vitesse en poursuite

# Caractéristiques d'un zombie
ZOMBIE_WIDTH,ZOMBIE_HEIGHT = 32, 32
ZOMBIE_SCALING = 2
ZOMBIE_FILE = "Mobs/Zombie/zombie.png"
ZOMBIE_CAR_FILE = "Mobs/Zombie/zombie.json"
    

ZOMBIE_WD_COORDS = [(0,0), (32,0), (64,0), (96,0), (128,0), (160,0), (192,0), (224,0), (256,0), (288, 0)]
ZOMBIE_WU_COORDS = [(0,32), (32,32), (64,32), (96,32), (128,32), (160,32), (192,32), (224,32), (256,32), (288,32)]
ZOMBIE_WR_COORDS = [(0,64), (32,64), (64,64), (96,64), (128,64), (160,64), (192,64), (224,64), (256,64), (288,64)]
ZOMBIE_WL_COORDS = [(0,96), (32,96), (64,96), (96,96), (128,96), (160,96), (192,96), (224,96), (256,96), (288,96)]

ZOMBIE_AD_COORDS = [(0,128), (32,128), (64,128), (96,128), (128,128), (160,128), (192,128), (224,128), (256,128)]
ZOMBIE_AU_COORDS = [(0,160), (32,160), (64,160), (96,160), (128,160), (160,160), (192,160), (224,160), (256,160)]
ZOMBIE_AR_COORDS = [(0,192), (32,192), (64,192), (96,192), (128,192), (160,192), (192,192), (224,192), (256,192)]
ZOMBIE_AL_COORDS = [(0,224), (32,224), (64,224), (96,224), (128,224), (160,224), (192,224), (224,224), (256,224)]

# On ne tient compte que de l'animation de mort vers le bas pour l'instant
ZOMBIE_DD_COORDS = [(0,256), (32,256), (64,256), (96,256), (128,256), (160,256), (192,256)]
ZOMBIE_DU_COORDS = []
ZOMBIE_DR_COORDS = []
ZOMBIE_DL_COORDS = []

ZOMBIE_SPRITE_COORDS = { WALK_DOWN : ZOMBIE_WD_COORDS, WALK_UP : ZOMBIE_WU_COORDS, WALK_RIGHT : ZOMBIE_WR_COORDS, 
                        WALK_LEFT : ZOMBIE_WL_COORDS, ATTACK_DOWN : ZOMBIE_AD_COORDS, ATTACK_UP : ZOMBIE_AU_COORDS, 
                        ATTACK_RIGHT : ZOMBIE_AR_COORDS, ATTACK_LEFT : ZOMBIE_AL_COORDS, DEAD : ZOMBIE_DD_COORDS  }



######################################### FLECHE #################################################

ARROW_WIDTH,ARROW_HEIGHT = 32, 32
ARROW_SCALING = 2
ARROW_SPEED    = 6  
ARROW_MAX_RANGE = 1000.0 
ARROW_FILE = "Mobs/Player/Arrow.png"    

ARROW_WD_COORDS = [(0,0), (32,0), (64,0), (96,0), (128,0), (160,0), (192,0), (224,0)]
ARROW_WU_COORDS = [(0,32), (32,32), (64,32), (96,32), (128,32), (160,32), (192,32), (224,0)]
ARROW_WR_COORDS = [(0,64), (32,64), (64,64), (96,64), (128,64), (160,64), (192,64), (224,64)]
ARROW_WL_COORDS = [(0,96), (32,96), (64,96), (96,96), (128,96), (160,96), (192,96), (224,96)]

ARROW_SPRITE_COORDS = { WALK_DOWN : ARROW_WD_COORDS, WALK_UP : ARROW_WU_COORDS, WALK_RIGHT : ARROW_WR_COORDS, 
                        WALK_LEFT : ARROW_WL_COORDS }


######################################### GUI ###################################################
    
# Caractéristiques du GUI
GUI_BOX_TEXTURE_FILE = "GUI/actions_player.png"
GUI_BOX_TEXTURE_CLICKED_FILE = "GUI/actions_player_clicked.png"
# Nombre d'emplacements de la barre d'actions
ACTIONBAR_SLOTS = 4


# Popups: valeurs par défaut (peuvent être réutilisées partout)
POPUP_DEFAULT_DURATION   = 0.9
POPUP_DEFAULT_RISE       = 40
POPUP_DEFAULT_SIZE       = 16

# Popups spécifiques (level up, nouvelles capacités etc.)
POPUP_LEVELUP_DURATION   = 9.0   
POPUP_LEVELUP_RISE       = 60
POPUP_LEVELUP_SIZE       = 20

##################################################################################################


#################################################################################################
####################### FONCTIONS UTILES ########################################################
#################################################################################################

def dir_from_vector(dx: float, dy: float) -> int:
    """Retourne le bit de direction cardinal selon l'axe dominant."""
    return (WALK_RIGHT if abs(dx) >= abs(dy) and dx >= 0 else
            WALK_LEFT  if abs(dx) >= abs(dy) and dx < 0  else
            WALK_UP    if dy >= 0 else
            WALK_DOWN)


# --- Direction → vecteur face ---
def _facing_vec(status):
    if status & WALK_RIGHT: return (1.0, 0.0)
    if status & WALK_LEFT:  return (-1.0, 0.0)
    if status & WALK_UP:    return (0.0, 1.0)
    if status & WALK_DOWN:  return (0.0, -1.0)
    return (0.0, 0.0)


# Version “arcade” simple : demi-plan + tolérance latérale
def target_in_front(attacker, target, lateral_tol=None):
    # tolérance latérale ≈ largeur de couloir (3/4 de tuile par défaut)
    if lateral_tol is None:
        lateral_tol = TILE_SIZE * 0.75

    dx = target.center_x - attacker.center_x
    dy = target.center_y - attacker.center_y

    if attacker.status & WALK_RIGHT:
        return dx >= 0 and abs(dy) <= lateral_tol
    if attacker.status & WALK_LEFT:
        return dx <= 0 and abs(dy) <= lateral_tol
    if attacker.status & WALK_UP:
        return dy >= 0 and abs(dx) <= lateral_tol
    if attacker.status & WALK_DOWN:
        return dy <= 0 and abs(dx) <= lateral_tol
    return True  # fallback

# Teste si la cible est dans un cône de demi-angle `half_deg` devant l’attaquant
def target_in_cone(attacker, target, half_deg=TARGET_IN_SIGHT):
    fx, fy = _facing_vec(attacker.status)
    vx = target.center_x - attacker.center_x
    vy = target.center_y - attacker.center_y

    # si superposés, considérer "devant"
    if vx == 0 and vy == 0:
        return True

    # cos(angle) = (v·f) / |v|
    dot = vx*fx + vy*fy
    norm_v = math.hypot(vx, vy)
    cos_angle = dot / norm_v
    cos_thresh = math.cos(math.radians(half_deg))
    return cos_angle >= cos_thresh


def ensure_attr(obj, name, default):
    if not hasattr(obj, name):
        setattr(obj, name, default)


def set_dir_towards(attacker, target):
    dx = target.center_x - attacker.center_x
    dy = target.center_y - attacker.center_y
    # enlever ATTACK si présent
    if attacker.status & ATTACK:
        attacker.status ^= ATTACK
    old_dir = attacker.status & (WALK_DOWN | WALK_UP | WALK_LEFT | WALK_RIGHT)
    if abs(dx) >= abs(dy):
        new_dir = WALK_RIGHT if dx >= 0 else WALK_LEFT
    else:
        new_dir = WALK_UP if dy >= 0 else WALK_DOWN
    attacker.status = (attacker.status & ~ (WALK_DOWN | WALK_UP | WALK_LEFT | WALK_RIGHT)) | new_dir
    return new_dir != old_dir


def in_attack_range(attacker, target):
    dx = attacker.center_x - target.center_x
    dy = attacker.center_y - target.center_y
    d2 = dx*dx + dy*dy
    rmin = int(attacker.attributes.get('Range_Min', 0))
    rmax = int(attacker.attributes.get('Range_Max', 30))
    return (d2 >= rmin*rmin) and (d2 <= rmax*rmax)


# Directions cardinales pour la texture
CARD_BITS = (WALK_RIGHT, WALK_LEFT, WALK_UP, WALK_DOWN)

def choose_facing_with_hysteresis(prev_dir, dx, dy, switch_ratio=1.25, stick_ratio=0.8):
    """
    - switch_ratio : il faut que l'axe dominant soit 1.25x plus fort pour changer d'orientation
    - stick_ratio  : si on venait d'un axe, on le garde tant qu'il reste >= 0.8x l'autre
    """
    adx, ady = abs(dx), abs(dy)
    # groupe précédent
    was_horiz = prev_dir in (WALK_RIGHT, WALK_LEFT)
    was_vert  = prev_dir in (WALK_UP, WALK_DOWN)

    # stickiness : si on était horizontal et que adx >= ady*stick_ratio -> rester horizontal
    if was_horiz and adx >= ady * stick_ratio:
        return WALK_RIGHT if dx >= 0 else WALK_LEFT
    if was_vert  and ady >= adx * stick_ratio:
        return WALK_UP if dy >= 0 else WALK_DOWN

    # sinon, bascule seulement si dominance claire
    if adx >= ady * switch_ratio:
        return WALK_RIGHT if dx >= 0 else WALK_LEFT
    if ady >= adx * switch_ratio:
        return WALK_UP if dy >= 0 else WALK_DOWN

    # sinon, ne change pas (stabilité)
    return prev_dir


# Niveau du joueur en fonction de son XP
def level_from_xp(xp: int) -> int:
    lvl = 1
    # PLAYER_LEVELING = {1:0, 2:100, 3:300, ...}
    for k, req in sorted(PLAYER_LEVELING.items()):
        if xp >= req:
            lvl = k
    return lvl


# Délimite une valeur entre deux bornes
def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v


# Regénération de PV
def regen_tick(entity, period: float, amount: int) -> bool:
    """
    Rend 'amount' PV à 'entity' au plus toutes les 'period' secondes.
    Retourne True si les PV ont changé (pour rafraîchir le GUI).
    """
    # ne régénère pas si mort
    if getattr(entity, "status", None) == 0:  # DEAD = 0
        return False

    # prépare les champs nécessaires
    if not hasattr(entity, "last_regen_time"):
        entity.last_regen_time = 0.0
    # max HP : player a souvent self.max_hitpoints ; pour les mobs on se base sur l'init
    max_hp = getattr(entity, "max_hitpoints", entity.attributes.get("MaxHitPoints",
             entity.attributes.get("HitPoints", 0)))
    if max_hp <= 0:
        return False

    now = time.time()
    if now - entity.last_regen_time < period:
        return False

    hp = int(entity.attributes.get("HitPoints", 0))
    if hp >= max_hp:
        return False

    new_hp = clamp(hp + int(amount), 0, int(max_hp))
    entity.attributes["HitPoints"] = new_hp
    entity.last_regen_time = now
    return new_hp != hp



# Réglages
CRIT_MIN_MULT = 1.10
CRIT_MAX_MULT = 2.10
BLOCK_REDUCE  = 0.70
PARRY_REDUCE  = 0.50

def _pct01(x):
    """10 -> 0.10 ; 0.10 -> 0.10 ; None -> 0.0"""
    if x is None:
        return 0.0
    return x / 100.0 if x > 1 else float(x)

def calculate_damage(attacker, action, defender,
                     *,
                     allow_block=True, allow_parry=True, allow_dodge=True, allow_miss=True,
                     block_reduces=False, parry_reduces=False,
                     glancing_min=0):
    """
    Ordre EQ : Block → Parry → Dodge → Miss → (Attack-Defense) → Crit.
    Retourne (damage:int, tag:str).
    """
    A = attacker.attributes
    D = defender.attributes

    # --- Lecture sûre des champs d'action ---
    if action is not None:
        act_hit   = float(action.get("Hit", 0))
        act_miss  = _pct01(action.get("Miss", 0))
        act_crit  = _pct01(action.get("Critical", 0))
        act_atk   = float(action.get("Attack", A.get("Attack", 0)))  # si pas présent, on fallback aux stats
    else:
        act_hit   = float(A.get("Hit", 0))
        act_miss  = 0.0
        act_crit  = _pct01(A.get("Critical", 0))
        act_atk   = float(A.get("Attack", 0))

    base_dmg = act_hit

    # --- Défenses AVANT précision ---
    if allow_block and float(D.get("Block", 0.0)) >= random():
        if block_reduces:
            base_dmg *= BLOCK_REDUCE
        else:
            return 0, "Block!"

    if allow_parry and float(D.get("Parry", 0.0)) >= random():
        if parry_reduces:
            base_dmg *= PARRY_REDUCE
        else:
            return 0, "Parry!"

    if allow_dodge and float(D.get("Dodge", 0.0)) >= random():
        return 0, "Dodge!"

    # --- Miss ---
    if allow_miss and act_miss >= random():
        return 0, "Miss!"

    # --- Scaling Attack - Defense (clamp [-90;+90]) ---
    dfn = float(D.get("Defense", 0))
    base_attack = max(-90.0, min(90.0, act_atk - dfn))
    scaled = base_dmg * (1.0 + base_attack / 100.0)

    # --- Critique ---
    tag = ""
    if act_crit >= random():
        scaled *= (CRIT_MIN_MULT + (CRIT_MAX_MULT - CRIT_MIN_MULT) * random())
        tag = "Critical!"

    # --- Plancher éventuel (glancing) ---
    if scaled < glancing_min:
        scaled = glancing_min

    dmg = max(0, int(math.floor(scaled)))
    return dmg, tag


def show_hit_feedback(game, defender, damage: int, tag: str = ""):
    TAG_COLOR = {
        "Critical!": arcade.color.GOLD,
        "Dodge!":    arcade.color.SILVER,
        "Parry!":    arcade.color.SILVER,
        "Block!":    arcade.color.SILVER,
        "Miss!":     arcade.color.SILVER,
        "Glancing!": arcade.color.LIGHT_GRAY,
    }

    # 1) dégâts chiffrés si > 0
    if damage > 0:
        game.gui.show_damage(defender, damage)

    # 2) tag (si présent) — sinon option “glancing” quand 0 sans tag
    if not tag and damage == 0:
        # si tu veux afficher quelque chose pour les *0 secs* non défensifs :
        # tag = "Glancing!"
        pass

    if tag:
        color = TAG_COLOR.get(tag, arcade.color.ORANGE)
        if tag == "Critical!":
            game.gui.show_info(defender, tag, color, duration=1.2, rise=50, size=16, debounce=0.0, dy=36)
        else:
            game.gui.show_info(defender, tag, color, duration=0.8, rise=40, size=14, debounce=0.2, dy=28)

