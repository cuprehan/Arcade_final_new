import arcade

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750
GAME_TITLE = "Adventure Game"

CHARACTER_SCALING = 1

GRAVITY = .5
LEFT_VIEWPORT_MARGIN = 150
RIGHT_VIEWPORT_MARGIN = 50
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class AdventureGame(arcade.Window):
    #the window for the game
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.levels_list = None

        # Used to keep track of our scrolling
        # step 5 of scrolling tutorial on arcade.academy
        self.view_bottom = 0
        self.view_left = 0

        arcade.set_background_color(arcade.color.PICTON_BLUE)

    def setup(self):
        self.HAS_KEY = False
        self.game_status = " "
        self.player_sprite = P_lev1()
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.food_list = arcade.SpriteList()
        self.food_coordinates = [
                                 [100, 400],
                                 [500, 400],
                                 [1400, 400],
                                 [1800, 400],
                                 [900, 400]
                                ]

        food_number = 1
        for coordinate in self.food_coordinates:
            food = arcade.Sprite("images/food"+str(food_number)+".png", .25)
            food_number = food_number + 1
            if(food_number > 3):
                food_number = 1
            food.position = coordinate
            self.food_list.append(food)

        self.wall_list = arcade.SpriteList()
        coordinate_list1 = [[100, 96],
                           [500, 196],
                           [900, 96],
                            [900, 500],
                           [1300, 96],
                            [1500,150],
                           [2100, 96],
                           [2500, 96],
                           [2900, 96]]

        for coordinate in coordinate_list1:
            # Add a crate on the ground
            wall = arcade.Sprite("images/prehistoric_wall.png", 1)
            wall.position = coordinate
            self.wall_list.append(wall)

        coordinate_list2 = [[1700, 196]]
        for coordinate in coordinate_list2:
            tall_wall = arcade.Sprite("images/tall_wall.png", 1)
            tall_wall.position = coordinate
            self.wall_list.append(tall_wall)

        self.spike_list = arcade.SpriteList()
        spike_coordinates = [[1300, 200],
                             [1500,250]]
        for coordinate in spike_coordinates:
            spike = arcade.Sprite("images/fire.png", .5)
            spike.position = coordinate
            self.spike_list.append(spike)

        self.key_list = arcade.SpriteList()
        key_coordinates = [[2300, 600]]
        for coordinate in key_coordinates:
            key = arcade.Sprite("images/torch.png", .3)
            key.position = coordinate
            self.key_list.append(key)

        self.door_list = arcade.SpriteList()
        self.door_coordinates = [[2500, 300]]
        for coordinate in self.door_coordinates:
            door = arcade.Sprite("images/cave.png", 1)
            door.position = coordinate
            self.door_list.append(door)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.food_list.draw()
        self.spike_list.draw()
        self.key_list.draw()
        self.door_list.draw()
        self.player_sprite.draw()
        health_text = f"Health: {self.player_sprite.HEALTH}"
        arcade.draw_text(health_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.RED, 18)

        game_text = self.game_status
        arcade.draw_text(game_text, 400 + self.view_left, 400 + self.view_bottom,
                         arcade.csscolor.RED, 26)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed.
        Code from arcade.academy"""
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = self.player_sprite.JUMP_HEIGHT
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -self.player_sprite.SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = self.player_sprite.SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()

        self.health_change = False

        food_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.food_list)
        # Loop through each food we hit (if any) and remove it
        for food in food_hit_list:
            food.remove_from_sprite_lists()
            self.player_sprite.HEALTH = self.player_sprite.HEALTH + 1
            self.health_change = True

        key_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.key_list)
        for key in key_hit_list:
            key.remove_from_sprite_lists()
            temp_sprite = P_key()
            temp_sprite.HEALTH = self.player_sprite.HEALTH
            temp_sprite.position = self.player_sprite.position
            self.player_sprite = temp_sprite
            self.HAS_KEY = True
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        spike_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.spike_list)
        # Loop through spike hits and remove the health score
        for spike in spike_hit_list:
            spike.remove_from_sprite_lists()
            self.player_sprite.HEALTH = self.player_sprite.HEALTH - 3
            self.health_change = True



        door_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.door_list)
        # Look if the character entered the door
        for door in door_hit_list:
            if self.HAS_KEY:
                self.game_status = "YOU WON!"

        if(self.player_sprite.center_y) < 100:
            self.player_sprite.center_x = 100
            self.player_sprite.center_y = 100
            self.game_status = "Game OVER!"

        if(self.health_change):
            if(self.player_sprite.HEALTH >= 6):
                temp_sprite = P_lev3()
                temp_sprite.HEALTH = self.player_sprite.HEALTH
                temp_sprite.position = self.player_sprite.position
                self.player_sprite = temp_sprite
            elif(self.player_sprite.HEALTH >= 4):
                temp_sprite = P_lev2()
                temp_sprite.HEALTH = self.player_sprite.HEALTH
                temp_sprite.position = self.player_sprite.position
                self.player_sprite = temp_sprite
            elif(self.player_sprite.HEALTH < 4 and self.player_sprite.HEALTH > 0):
                temp_sprite = P_lev1()
                temp_sprite.HEALTH = self.player_sprite.HEALTH
                temp_sprite.position = self.player_sprite.position
                self.player_sprite = temp_sprite
            elif(self.player_sprite.HEALTH <= 0):
                # this is death, end of game
                self.game_status = "Game OVER!"

            self.health_change = False
            #if the new sprite object was created we have to create new platformer with that character
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        # --- Manage Scrolling ---
        # Track if we need to change the viewport
        # scrolling code from arcade.academy
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


class P_lev1(arcade.Sprite):
    # Equivalent to the player being level 1. Starting sprite.
    def __init__(self):
        self.SPEED = 15
        self.JUMP_HEIGHT = 12
        self.HEALTH = 2
        super().__init__("images/caveman.png", .5)

class P_lev2(arcade.Sprite):
    # Equivalent to the player leveling up to level 2. Speed and jump height increased.
    def __init__(self):
        self.SPEED = 20
        self.JUMP_HEIGHT = 17
        self.HEALTH = 4
        super().__init__("images/caveman2.png", 1.25)

class P_lev3(arcade.Sprite):
    # Equivalent to the player leveling up to level 3. Speed and jump height increased.
    def __init__(self):
        self.SPEED = 25
        self.JUMP_HEIGHT = 20
        self.HEALTH = 6
        super().__init__("images/caveman1.png", .5)

class P_key(arcade.Sprite):
    # class received after obtaining the torch to win the game.
    def __init__(self):
        self.SPEED = 25
        self.JUMP_HEIGHT = 20
        self.HEALTH = 6
        super().__init__("images/caveman3.png", 1.25)

def main():
    window = AdventureGame()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()

