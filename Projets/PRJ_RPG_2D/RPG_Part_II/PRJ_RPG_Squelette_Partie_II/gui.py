import arcade
import arcade.gui
from constants import *


class QuitButton(arcade.gui.UIFlatButton):
    def set_window(self, game):
        self.game = game

    def on_click(self, event):
        self.game.close()


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

    # ---------- Widgets composés ----------

    def create_game_menu(self):
        self.menu_bar = arcade.gui.UIBoxLayout(vertical=False)

        quit_button = QuitButton(text="Quit", width=50)
        quit_button.set_window(self.game)
        self.menu_bar.add(quit_button)

        # ancrer en bas/droite
        self.anchor.add(child=self.menu_bar, anchor_x="right", anchor_y="bottom")


    def create_player_box(self):
        if self.game.player == None :
            return

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
        v_box_2.add(hp_label_1)
        v_box_2.add(hp_label_2)
        self.player_box.add(v_box_2)


    def create_clicked_mob_box(self, clicked_mob):
        if clicked_mob == None :
            return

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

    # ---------- Scènes GUI ----------

    def setup(self):
        # Réinitialise proprement l’UI
        self.game.manager.clear()

        # Layout d’ancrage racine
        self.anchor = self.game.manager.add(arcade.gui.UIAnchorLayout())

        # Menu
        self.create_game_menu()

        # Box joueur
        if self.game.player == None :
            return

        self.create_player_box()

        # Regroupe en haut à gauche
        mobs_box = arcade.gui.UIBoxLayout(vertical=False)
        mobs_box.add(self.player_box)
        self.anchor.add(child=mobs_box, anchor_x="left", anchor_y="top")


    def add_clicked_mob(self, clicked_mob):
        if clicked_mob == None :
            return

        # Réinitialise et reconstruit
        self.game.manager.clear()
        self.anchor = self.game.manager.add(arcade.gui.UIAnchorLayout())

        # Menu
        self.create_game_menu()

        # Box joueur + mob cliqué
        if self.game.player == None :
            return

        self.create_player_box()
        self.create_clicked_mob_box(clicked_mob)

        mobs_box = arcade.gui.UIBoxLayout(vertical=False)
        mobs_box.add(self.player_box)
        mobs_box.add(self.clicked_mob_box)
        self.anchor.add(child=mobs_box, anchor_x="left", anchor_y="top")

    # ---------- Draw ----------

    def draw(self):
        self.game.manager.draw()
