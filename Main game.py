import arcade

WINDOW_WIDTH = 10000
WINDOW_HEIGHT = 750
GAME_TITLE = "Adventure Game"

CHARACTER_SCALING = 1


class AdventureGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.levels_list = None
        arcade.set_background_color(arcade.color.PICTON_BLUE)

    def setup(self):
        self.player_sprite = arcade.Sprite("images/caveman.png", .5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.wall_list = arcade.SpriteList()
        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images/prehistoric_wall.png", 1)
            wall.position = coordinate
            self.wall_list.append(wall)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, 1)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.player_sprite.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -5
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 5

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()


#class P_lev1(arcade.Sprite):
#    def __init__(self):
#        super().__init__("images/manP1.png")



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
