import arcade

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750
GAME_TITLE = "Adventure Game"

CHARACTER_SCALING = 1

LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 50
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class AdventureGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.levels_list = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.color.PICTON_BLUE)

    def setup(self):
        self.player_sprite = arcade.Sprite("images/caveman.png", .5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.food_list = arcade.SpriteList()
        self.food_coordinates = [[800, 400]]
        self.wall_list = arcade.SpriteList()
        for coordinate in self.food_coordinates:
            food = arcade.Sprite("images/food.png", .25)
            food.position = coordinate
            self.food_list.append(food)
        coordinate_list = [[100, 96],
                           [500, 196],
                           [900, 96],
                           [1300, 96],
                           [1700, 196],
                           [2100, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images/prehistoric_wall.png", 1)
            wall.position = coordinate
            self.wall_list.append(wall)
        self.spike_list = arcade.SpriteList()
        self.spike_coordinates = [[1300, 200]]
        for coordinate in self.spike_coordinates:
            spike = arcade.Sprite("images/spike.png", .3)
            spike.position = coordinate
            self.spike_list.append(spike)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, 0.5)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.food_list.draw()
        self.spike_list.draw()
        self.player_sprite.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = 15
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -15
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 15

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()

        food_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.food_list)

        # Loop through each food we hit (if any) and remove it
        for food in food_hit_list:
            food.remove_from_sprite_lists()

        # --- Manage Scrolling ---
        # Track if we need to change the viewport
        changed = False
        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + WINDOW_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right + right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + WINDOW_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                WINDOW_WIDTH + self.view_left,
                                self.view_bottom,
                                WINDOW_HEIGHT + self.view_bottom)

#class P_lev1(arcade.Sprite):
#    def __init__(self):
#        super().__init__("images/manP1.png")

class P_lev1(arcade.Sprite):
    def __init__(self, **kwargs):
        self.SPEED = 15
        self.JUMP_HEIGHT = 15
        self.HEALTH = 2
        super().__init__(kwargs)

class P_lev2(arcade.Sprite):
    def __init__(self, **kwargs):
        self.SPEED = 20
        self.JUMP_HEIGHT = 20
        self.HEALTH = 4
        super().__init__(kwargs)

class P_lev3(arcade.Sprite):
    def __init__(self, **kwargs):
        self.SPEED = 25
        self.JUMP_HEIGHT = 25
        self.HEALTH = 6
        super().__init__(kwargs)

def main():
    window = AdventureGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
