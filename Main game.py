import arcade

WINDOW_WIDTH = 10000
WINDOW_HEIGHT = 1000
GAME_TITLE = "Adventure Game"

player_lev1 = arcade.load_texture("images/manP1.png")
player_lev2 = arcade.load_texture("images/simpson.png")
player_lev3 = arcade.load_texture("images/kid_on_skateboard.png")


class AdventureGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.levels_list = None
        arcade.set_background_color(arcade.color.PICTON_BLUE)

    def setup(self):
        self.levels_list = arcade.SpriteList

    def on_draw(self):
        pass


class P_lev1(arcade.Sprite):
    pass


class P_lev2(arcade.Sprite):
    pass


class P_lev3(arcade.Sprite):
    pass

def main():
    window = AdventureGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
