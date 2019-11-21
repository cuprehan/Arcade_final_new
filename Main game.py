import arcade

WINDOW_WIDTH = 10000
WINDOW_HEIGHT = 1000
GAME_TITLE = "Adventure Game"


class AdventureGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        arcade.set_background_color(arcade.color.PICTON_BLUE)

    def setup(self):
        pass


def main():
    window = AdventureGame()
    window.setup()
    arcade.run()

if __name__ == '__main__':
    main()
