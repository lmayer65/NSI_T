# projectile.py
import math, time, arcade
from entity import Entity
from constants import *



class Arrow(Entity):
    """
    Flèche :
      - endommage UNIQUEMENT self.target
      - détruite si mur / hors carte / fin de portée / après impact
      - anim via self.textures[self.status][self.current_texture_indice]
    """
    def __init__(self, game, start_x, start_y, vx, vy,
                 damage: int, speed_px: float, max_range_px: float, owner, target, action_snapshot = None):
        super().__init__(ARROW_FILE, ARROW_SCALING, ARROW_WIDTH, ARROW_HEIGHT,
                         ARROW_SPRITE_COORDS, game)
        self.center_x, self.center_y = start_x, start_y
        self.vx, self.vy = float(vx), float(vy)
        self.damage = int(damage)
        self.speed_px = float(speed_px)
        self.remaining = float(max_range_px)
        self.owner = owner
        self.target = target
        self.consumed = False # Pour éviter les doublons d'impact
        self.attributes['Type'] = "Projectile"

        self.status = dir_from_vector(self.vx, self.vy)
        self.current_texture_indice = 0
        self.anim_tick = 0
        frames = self.textures.get(self.status, [])
        if frames:
            self.texture = frames[0]

        self.action_snapshot = dict(action_snapshot) if action_snapshot else None   # Pour le journal de combat
       



    def _refresh_dir_if_needed(self):
        nd = dir_from_vector(self.vx, self.vy)
        if nd != self.status:
            self.status = nd
            self.current_texture_indice = 0
            frames = self.textures.get(self.status, [])
            if frames:
                self.texture = frames[0]

    def _advance_animation(self):
        frames = self.textures.get(self.status, [])
        if not frames: return
        self.anim_tick = (self.anim_tick + 1) % 999999
        if self.anim_tick % 3 == 0:
            self.current_texture_indice = (self.current_texture_indice + 1) % len(frames)
            self.texture = frames[self.current_texture_indice]



    def update(self):
        # Si déjà utilisée
        if self.consumed :
            self.remove_from_sprite_lists()      # enlève de toutes les SpriteList Arcade

            # si tu as aussi une liste Python (ex: self.game.projectiles), enlève l’objet
            try:
                if hasattr(self.game, "projectiles") and self in self.game.projectiles:
                    self.game.projectiles.remove(self)
            except Exception:
                pass
            return


        # 1) mouvement + portée
        self.center_x += self.vx
        self.center_y += self.vy
        self.remaining -= math.hypot(self.vx, self.vy)
        if self.remaining <= 0:
            self.remove_from_sprite_lists(); return

        # 2) bornes carte
        if (self.center_x < 0 or self.center_y < 0 or
                self.center_x > MAP_WIDTH*MAP_SCALING or
                self.center_y > MAP_HEIGHT*MAP_SCALING):
            self.remove_from_sprite_lists() 
            return

        # 3) visuel
        self._refresh_dir_if_needed()
        self._advance_animation()

        # 4) murs → perdue
        if arcade.check_for_collision_with_lists(self, self.game.map.walls):
            self.game.gui.show_info(self, "Arrow lost!", arcade.color.SILVER,
                       duration=0.6, dy=16, debounce=0.0)
            self.consumed = True
            self.remove_from_sprite_lists()
            try:
                if hasattr(self.game, "projectiles") and self in self.game.projectiles:
                    self.game.projectiles.remove(self)
            except Exception:
                pass
            
            return

        # 5) impact uniquement sur LA cible
        tgt = self.target
        if not tgt or getattr(tgt, "status", 1) == DEAD:
            return
        sprites = getattr(self.game, "sprites_list", None)
        if sprites is not None and tgt not in sprites:
            return

        if arcade.check_for_collision(self, tgt):
            # Marquer consommée tout de suite pour éviter 2 impacts
            self.consumed = True

            try:
                # --- Calcul dégâts version projectile (pas de Miss/Dodge/Parry) ---
                if self.action_snapshot is not None:
                    dmg, tag = calculate_damage(
                        self.owner,
                        self.action_snapshot,  # ton snapshot minimal {"Hit","Miss","Critical"}
                        tgt,
                        allow_miss=True, allow_dodge=False, allow_parry=False,  
                        allow_block=True,  block_reduces=False,                  
                        glancing_min=0                                           
                    )           
                else:
                       # fallback très simple
                       dmg, tag = self.damage, ""

                # --- Appliquer / afficher d'abord les dégâts, puis le tag si présent ---
                if dmg > 0:
                    tgt.attributes['HitPoints'] -= dmg
                    self.game.gui.show_damage(tgt, dmg)  # <- le nombre (rouge/orange)
                if tag:
                    self.game.gui.show_info(
                        tgt, tag,
                        arcade.color.GOLD if "Crit" in tag else arcade.color.SILVER,
                        duration=0.9, rise=40, size=14, debounce=0.0
                    )

                # Aggro du mob sur le tireur
                tgt.target = self.owner
                tgt.aggro_until = time.time() + AGGRO_DURATION

                # --- Mort ? (afficher le ☠ APRES le nombre) ---
                if tgt.attributes.get('HitPoints', 1) <= 0:
                    self.game.gui.show_info(tgt, "☠", arcade.color.BONE, debounce=0.0)
                    # décocher si c'était la cible cliquée
                    if getattr(self.game.player, "clicked_mob", None) is tgt:
                        self.game.player.clicked_mob = None
                        self.game.gui.update()
                    if hasattr(tgt, "die"):
                        tgt.die()
                    # XP
                    if hasattr(self.owner, "add_xp"):
                        self.owner.add_xp(int(tgt.attributes.get('Experience', 0)))

            finally:
                # Retrait propre du projectile (SpriteList + éventuelle liste Python)
                self.remove_from_sprite_lists()
                try:
                    if hasattr(self.game, "projectiles") and self in self.game.projectiles:
                        self.game.projectiles.remove(self)
                except Exception:
                    pass

            return

