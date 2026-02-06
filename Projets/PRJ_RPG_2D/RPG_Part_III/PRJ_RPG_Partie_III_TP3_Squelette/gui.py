import arcade
import arcade.gui
from constants import *

# -- TP 2 : Ajout d'import --
from PIL import Image
import tempfile, os
from timer import Timer
# -- TP 2 : FIN --


class QuitButton(arcade.gui.UIFlatButton):
    def set_window(self, game):
        self.game = game

    def on_click(self, event):
        self.game.close()



# Boutons d'action (icônes)
# -- TP 2 : Classe liant icône / action du joueur --
class ActionButton(arcade.gui.UITextureButton):
    
    def set_window(self, game):
        self.game = game
    
    def set_name(self, text):
        self.name = text

    def on_click(self, event: arcade.gui.UIMousePressEvent):
        if self.game.gui.active:
            return

        if self.game.clicked_mob is None:
            return
    

        self.game.player.status |= ATTACK
        self.game.player.action_name = self.name
        self.game.player.current_texture_indice = -1
        self.game.player.attack(self.game.clicked_mob)
        self.game.gui.active = True
        self.game.gui.setup_clicked_mob(self.game.clicked_mob)
        self.game.player_timer = Timer(self.game.player.actions[self.name]["Cooldown"])
        self.game.player_timer.start()
# -- TP 2 : FIN --




class Gui:
    def __init__(self, game):
        self.game = game

        # UIManager unique, activé
        if not hasattr(self.game, "manager") or self.game.manager is None:
            self.game.manager = arcade.gui.UIManager()
        self.game.manager.enable()

        self.anchor = None  # UIAnchorLayout
        self.menu_bar = None
        self.player_box = None
        self.clicked_mob_box = None

        # -- TP 2 : Création des textures --
        self.actions_player_textures = []
        self.actions_player_textures_clicked = []
        self.create_textures() 
        self.active = True # Icônes actives ?
        # -- TP 2 : FIN --



    # -- TP 2 : Génération des textures --
    def create_textures(self):
        # génère ACTIONBAR_SLOTS rectangles 32x32 sur la rangée y=98 (ajuste 98 si besoin)
        rects = [(i * 32, 98, 32, 32) for i in range(ACTIONBAR_SLOTS)]

        # charge les spritesheets
        img_normal = Image.open(GUI_BOX_TEXTURE_FILE).convert("RGBA")
        img_clicked = Image.open(GUI_BOX_TEXTURE_CLICKED_FILE).convert("RGBA")

        # Variable temporaire
        self._tmp_icon_files = []

        # NORMAL
        for i, (x, y, w, h) in enumerate(rects):
            crop = img_normal.crop((x, y, x + w, y + h))
            tmp = tempfile.NamedTemporaryFile(prefix=f"act_norm_{i}_", suffix=".png", delete=False)
            crop.save(tmp.name)
            tmp.close()
            self._tmp_icon_files.append(tmp.name)
            tex = arcade.load_texture(tmp.name)
            self.actions_player_textures.append(tex)

        # CLICKED
        for i, (x, y, w, h) in enumerate(rects):
            crop = img_clicked.crop((x, y, x + w, y + h))
            tmp = tempfile.NamedTemporaryFile(prefix=f"act_click_{i}_", suffix=".png", delete=False)
            crop.save(tmp.name)
            tmp.close()
            self._tmp_icon_files.append(tmp.name)
            tex = arcade.load_texture(tmp.name)
            self.actions_player_textures_clicked.append(tex)

    # -- TP 2 : FIN --


    # ---------- Widgets composés ----------

    def create_game_menu(self):
        self.menu_bar = arcade.gui.UIBoxLayout(vertical=False)

        quit_button = QuitButton(text="Quit", width=50)
        quit_button.set_window(self.game)
        self.menu_bar.add(quit_button)

        # ancrer en bas/droite
        self.anchor.add(child=self.menu_bar, anchor_x="right", anchor_y="bottom")


    def create_player_box(self):
        self.player_box = arcade.gui.UIBoxLayout(vertical=False)

        player_texture_button = arcade.gui.UITextureButton(
            texture=self.game.player.textures[0][0],
            width=40,
            height=68,
        )
        self.player_box.add(player_texture_button)

        v_box_2 = arcade.gui.UIBoxLayout()
        hp_label_1 = arcade.gui.UILabel(text="Name = " + str(self.game.player.attributes["Name"]))
        hp_label_2 = arcade.gui.UILabel(text="HitPoints = " + str(self.game.player.attributes["HitPoints"]))
        hp_label_3 = arcade.gui.UILabel(text="XP = " + str(self.game.player.attributes["Experience"]))
        v_box_2.add(hp_label_1)
        v_box_2.add(hp_label_2)
        v_box_2.add(hp_label_3)
        self.player_box.add(v_box_2)


    def create_clicked_mob_box(self, clicked_mob):
        self.clicked_mob_box = arcade.gui.UIBoxLayout(vertical=False)

        mob_texture_button = arcade.gui.UITextureButton(
            texture=clicked_mob.textures[0][0],
            width=40,
            height=68,
        )
        self.clicked_mob_box.add(mob_texture_button)

        v_box_2 = arcade.gui.UIBoxLayout()
        hp_label_1 = arcade.gui.UILabel(text="Name = " + str(clicked_mob.attributes["Name"]))
        hp_label_2 = arcade.gui.UILabel(text="HitPoints = " + str(clicked_mob.attributes["HitPoints"]))
        v_box_2.add(hp_label_1)
        v_box_2.add(hp_label_2)
        self.clicked_mob_box.add(v_box_2)


    # -- TP 3 : Fenêtre d'action sans ennemi de ciblé --
    def create_no_mob_box(self):
        """
        Box affichée lorsqu'aucun ennemi n'est sélectionné
        """
        self.no_mob_box = arcade.gui.UIBoxLayout(vertical=True, width=200)

        label = arcade.gui.UILabel(
            text="Nothing selected",
            font_size=14,
            align="center",
            text_color=arcade.color.WHITE
        )

        self.no_mob_box.add(label)
    # -- TP 3 : FIN --

    
    # -- TP 2 : Fenêtre d'actions (icônes) --
    def create_action_box(self):
        self.action_player_box = arcade.gui.UIBoxLayout(vertical=False)
        textures = self.actions_player_textures_clicked if self.active else self.actions_player_textures

        player_level = player_level = self.game.player.attributes['Level']

        for i in range(ACTIONBAR_SLOTS):
            # Nom d'action à partir de "attack_i"
            action_name = f"attack_{i}"

            action_def = self.game.player.actions.get(action_name)
            if not action_def:
                continue  # pas définie dans le JSON => pas d'icône

            required_level = action_def['Level']
            if player_level < required_level:
                continue  # pas affichée si niveau insuffisant

            # Sécurité : si on a plus de slots que de textures chargées
            if i >= len(textures):
                break

            btn = ActionButton(texture=textures[i], width=50, height=50)
            btn.set_window(self.game)
            btn.set_name(action_name)
            self.action_player_box.add(btn)

        self.anchor.add(child=self.action_player_box, anchor_x="left", anchor_y="bottom")


    # ---------- Scènes GUI ----------

    def setup(self):
        # Réinitialise proprement l’UI
        self.game.manager.clear()

        # Layout d’ancrage racine
        self.anchor = self.game.manager.add(arcade.gui.UIAnchorLayout())

        # Menu
        self.create_game_menu()

        # Box joueur
        self.create_player_box()

        # Boite d'actions
        # -- TP 2 : Création des icones --
        self.create_action_box()
        # -- TP 2 : FIN --

        # Regroupe en haut à gauche
        mobs_box = arcade.gui.UIBoxLayout(vertical=False)
        mobs_box.add(self.player_box)

        # -- TP 3 : Affichage par défaut sans mob sélectionné --
        # Affiche "aucun ennemi sélectionné" par défaut
        self.create_no_mob_box()
        mobs_box.add(self.no_mob_box)
        # -- TP 3 : Fin --

        self.anchor.add(child=mobs_box, anchor_x="left", anchor_y="top")


    def setup_clicked_mob(self, clicked_mob):
        # Réinitialise et reconstruit
        self.game.manager.clear()
        self.anchor = self.game.manager.add(arcade.gui.UIAnchorLayout())

        # Menu
        self.create_game_menu()

        # Box joueur
        self.create_player_box()

        mobs_box = arcade.gui.UIBoxLayout(vertical=False)
        mobs_box.add(self.player_box)

        # -- TP 3 : Affichage des infos du mob cliqué s'il existe seulement--
        # Box mob seulement si un mob est sélectionné sinon box vid
        if clicked_mob is not None:
            self.create_clicked_mob_box(clicked_mob)
            mobs_box.add(self.clicked_mob_box)
        else:
            self.create_no_mob_box()
            mobs_box.add(self.no_mob_box)
        # -- TP 3 : Fin --


        self.anchor.add(child=mobs_box, anchor_x="left", anchor_y="top")

        # Boite d'actions
        self.create_action_box()


    # -- TP 2 : Mise à jour du GUI --
    #def update(self) :
    #    self.setup()
    # -- TP 2 : Fin --

    # -- TP 3 : update du GUI selon mob cliqué --
    def update(self):
        if self.game.clicked_mob is None:
            self.setup()
        else:
            self.setup_clicked_mob(self.game.clicked_mob)
    #-- TP 3 : FIN --

        
       
    def draw(self):
        self.game.manager.draw()
