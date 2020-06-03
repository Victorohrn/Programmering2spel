import arcade
import os
import random
import math
from settings import * 



class TheGame(arcade.Window):  
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)

        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None
        self.shield_list = None

        
        self.enemy_textures = None

        
        self.game_state = GAME_PLAY

        
        self.player_sprite = None
        self.score = 0

        
        self.enemy_change_x = -ENEMY_SPEED

       
        self.set_mouse_visible(False)

        
        self.Difficulty = 0
        
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

        self.game_over = False
        #arcade.configure_logging()
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.pause = False
    def setup_level_one(self):
        
        self.enemy_textures = []
        texture = arcade.load_texture("./static/enemies.png", mirrored=True)
        self.enemy_textures.append(texture)
        texture = arcade.load_texture("./static/enemies.png")
        self.enemy_textures.append(texture)

        
        x_count = 14
        x_start = 420
        x_spacing = 90
        y_count = 6
        y_start = 800
        y_spacing = 50
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):

             
                enemy = arcade.Sprite()
                enemy.scale = SPRITE_SCALING_enemy
                enemy.texture = self.enemy_textures[1]

              
                enemy.center_x = x
                enemy.center_y = y

                #add later!!!
                self.enemy_list.append(enemy)
    def shield(self, x_start):
        shield_block_width = 1
        shield_block_height = 1
        shield_width_count = 1
        shield_height_count = 1

        if self.Difficulty == 1:
            shield_block_width = 5
            shield_block_height = 10
            shield_width_count = 20
            shield_height_count = 5

        elif self.Difficulty == 2:
            shield_block_width = 5
            shield_block_height = 5
            shield_width_count = 10
            shield_height_count = 2

        
        y_start = 150
        
        for x in range(x_start, x_start + shield_width_count * shield_block_width, shield_block_width):
            for y in range(y_start, y_start + shield_height_count * shield_block_height, shield_block_height):
                shield_sprite = arcade.SpriteSolidColor(shield_block_width, shield_block_height, arcade.color.GREEN)
                shield_sprite.center_x  = x
                shield_sprite.center_y = y
                self.shield_list.append(shield_sprite)

    def play(self):
        

        self.game_state = GAME_PLAY

        
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.shield_list = arcade.SpriteList(is_static=True)

        
        self.score = 0

     
        self.player_sprite = arcade.Sprite("./static/shooter.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH/2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)


        for x in range(250, 1670, 190):
            self.shield(x)

       
        arcade.set_background_color(arcade.color.BLACK)
        
        self.setup_level_one()
    def on_draw(self):
        arcade.start_render()
        """
        Huvudfunktion för utritningar av ALLA spelobjekt.
        Ordningen saker ritas på spelar stor roll.
        Ritar du exempelvis bakgrund sist, så är
        bakgrunden överst! Ordningen spelar roll.
      """
        if self.Difficulty != 0:
            self.enemy_list.draw()
            self.player_bullet_list.draw()
            self.enemy_bullet_list.draw()
            self.player_list.draw()
            self.shield_list.draw()

        if self.Difficulty == 0:
            arcade.draw_text(f"Press 1 for Normal\nPress 2 for Hard",  SCREEN_WIDTH / 2 - 175, 500, arcade.color.WHITE, 55 , 750)

        
        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text(f" ESC TO EXIT\n R to restart\n P to Pause", 1770, 20, arcade.color.WHITE, 14)
        # Draw game over if the game state is such
        
        if self.game_state == GAME_OVER:
            arcade.draw_text(f"GAME OVER", SCREEN_WIDTH / 2 - 175, 500, arcade.color.WHITE, 55 , 750)
            self.set_mouse_visible(True)
        if self.pause:
            arcade.draw_text(f"PAUSED", SCREEN_WIDTH / 2 - 175, 500, arcade.color.WHITE, 55 , 750)
            self.set_mouse_visible(True)
    def update_enemies(self):

        
        for enemy in self.enemy_list:
            enemy.center_x += self.enemy_change_x

        
        move_down = False
        for enemy in self.enemy_list:
            if enemy.right > RIGHT_ENEMY_BORDER and self.enemy_change_x > 0:
                self.enemy_change_x *= -1
                move_down = True
            if enemy.left < LEFT_ENEMY_BORDER and self.enemy_change_x < 0:
                self.enemy_change_x *= -1
                move_down = True

        
        if move_down:
        
            for enemy in self.enemy_list:
                
                enemy.center_y -= ENEMY_MOVE_DOWN_AMOUNT
                
                if self.enemy_change_x > 0:
                    enemy.texture = self.enemy_textures[0]
                else:
                    enemy.texture = self.enemy_textures[1]

        if enemy.center_y <= 75:
            self.game_state = GAME_OVER

    def allow_enemies_to_fire(self):
        """
        See if any enemies will fire this frame.
        """
        
        x_spawn = []
        for enemy in self.enemy_list:
            
            chance = 4 + len(self.enemy_list) * 4

            
            if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:
                
                bullet = arcade.Sprite("./static/Bullet.png", SPRITE_SCALING_LASER,)
                
              
                bullet.angle = 180

                bullet.change_x = random.randrange(-5,5,1) 
                """
                if bullet.change_x <=2:
                    bullet.angle = 150
                if bullet.change_x == 1:
                    bullet.angle = 170
                if bullet.change_x >=-2:
                    bullet.angle = 210
                if bullet.change_x ==-1:
                    bullet.angle = 190
                """
                bullet.change_y = -BULLET_SPEED
                
                
                bullet.center_x = enemy.center_x
                bullet.top = enemy.bottom

                self.enemy_bullet_list.append(bullet)

            
            x_spawn.append(enemy.center_x)

    def process_enemy_bullets(self):

        
        self.enemy_bullet_list.update()

        
        for bullet in self.enemy_bullet_list:
            
            hit_list = arcade.check_for_collision_with_list(bullet, self.shield_list)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list):
                self.game_state = GAME_OVER

            
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def process_player_bullets(self):

        
        self.player_bullet_list.update()

     
        for bullet in self.player_bullet_list:

            
            hit_list = arcade.check_for_collision_with_list(bullet, self.shield_list)
            
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

                # Hit Sound
                arcade.play_sound(self.hit_sound)

            
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            exit()

        if key == arcade.key.P:
            self.pause = not self.pause
            self.set_mouse_visible(False)
        if key == arcade.key.R:
            self.play()
            self.set_mouse_visible(False)
            
        if key == arcade.key.KEY_1:
            self.Difficulty = 1
            self.play()
            self.set_mouse_visible(False)
           
        if key == arcade.key.KEY_2:
            self.Difficulty = 2
            self.play()
            self.set_mouse_visible(False)
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """

        # Don't move the player if the game is over
        if self.game_state == GAME_OVER:
            return

        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """

        # Only allow the user so many bullets on screen at a time to prevent
        # them from spamming bullets.
        if len(self.player_bullet_list) < MAX_PLAYER_BULLETS:

            # Gunshot sound
            arcade.play_sound(self.gun_sound)

            # Create a bullet
            bullet = arcade.Sprite("./static/laser.png", SPRITE_SCALING_LASER)

            

            # Give the bullet a speed
            bullet.change_y = BULLET_SPEED

            # Position the bullet
            bullet.center_x = self.player_sprite.center_x
            bullet.bottom = self.player_sprite.top

            # Add the bullet to the appropriate lists
            self.player_bullet_list.append(bullet)

            if self.game_state == GAME_OVER:
                return

    def on_update(self, deltatime):
        """
        Huvudfunktion för uppdateringar av HELA spel-loopen.
        Placera all uppdatering av spellogik här
        Alltså här skriver du in ordning för när
        alla spelobjekt ska uppdateras.
        """
        if self.pause:
            return
            

        self.update_enemies()
        self.allow_enemies_to_fire()
        self.process_enemy_bullets()
        self.process_player_bullets()

        if len(self.enemy_list) == 0:
            self.setup_level_one()
      
