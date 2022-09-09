# Imports and Aesthetics
import pygame
from os import path, environ
from support import import_csv_layout, import_cut_graphics  # csv contents, cut_tiles
from settings import tile_size, screen_height, screen_width   #import screen aesthetics

# Tiles
from Tile import Tile, StaticTile, Crate, Coin, Palm
from decoration import Sky, Water, Clouds

# Enemy
from enemy import Enemy

#Player
from Player import Player
from ParticleEffects import ParticleEffect


class Level:
    def __init__(self, level_data, surface):
        # General Setup
        self.display_surface = surface
        self.world_shift = -8
        self.homedir = environ.get("HOME")
        self.subdir = 'Downloads/2 - Level'

        # Player
        player_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['player']))
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        self.current_x = None

        # Dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # Terrain Setup
        terrain_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['terrain']))
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #Grass Setup
        grass_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['grass']))
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # Crates
        crate_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['crates']))
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # Coins
        coin_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['coins']))
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # Foreground Palms
        fg_palm_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['fg_palms']))
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg_palms')

        # Background Palms
        bg_palm_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['bg_palms']))
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg_palms')

        # Enemy
        enemy_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['enemy']))
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

        # Bounds
        bound_layout = import_csv_layout(path.join(self.homedir, self.subdir, level_data['enemy_bound']))
        self.bound_layout_sprites = self.create_tile_group(bound_layout, 'enemy_bound')

        #Decorations
            #Sky
        self.sky = Sky(8)
            #Water: Throughout the level
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 50, level_width)
            #Clouds
        self.clouds = Clouds(400, level_width, 25)

    # Create and implement tile graphics
    def create_tile_group(self, layout, graphic):
        global sprite
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # Check my graphic
                        # Static
                    if graphic == 'terrain':
                        terrain_tile_list = import_cut_graphics(path.join(self.homedir, self.subdir, 'graphics/terrain/terrain_tiles.png'))   # tile sheet
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if graphic == 'grass':
                        grass_tile_list = import_cut_graphics(path.join(self.homedir, self.subdir, 'graphics/decoration/grass/grass.png'))
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if graphic == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if graphic == 'enemy_bound':
                        sprite = Tile(tile_size, x, y)

                        # Animated
                    if graphic == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, path.join(self.homedir, self.subdir, 'graphics/coins/gold'))

                        if val == '1':
                            sprite = Coin(tile_size, x, y, path.join(self.homedir, self.subdir, 'graphics/coins/silver'))

                    if graphic == 'fg_palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y, path.join(self.homedir, self.subdir, 'graphics/terrain/palm_small'), 40)
                        if val == '1':
                            sprite = Palm(tile_size, x, y, path.join(self.homedir, self.subdir, 'graphics/terrain/palm_large'), 72)

                    if graphic == "bg_palms":
                        sprite = Palm(tile_size, x, y, path.join(self.homedir, self.subdir, 'graphics/terrain/palm_bg'), 64)

                    if graphic == "enemy":
                        sprite = Enemy(tile_size, x, y,)

                    sprite_group.add(sprite)

        return sprite_group

    # Player Setup
    def player_setup(self, layout):
        global sprite
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load(path.join(self.homedir, self.subdir, 'graphics/character/hat.png')).convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    # Is the player on ground?
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    # Air initially, on the ground, no overlapping animation
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(10, -15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    # Collisions(Player)
    def horizontal_movement_collision(self):
        player = self.player.sprite   # Obtain my player
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            # Converts all sprites to images
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.collision_point = player.rect.left   # Find the collision point
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.collision_point = player.rect.right   # Find the collision point

        # Am I touching the left wall?
        if player.on_left and (player.rect.left < self.collision_point or player.direction.x >= 0):
            player.on_left = False

        if player.on_right and (player.rect.right > self.collision_point or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite   # Obtain my player
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                # If I am moving down
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                # If I am moving up
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        # Is the player jumping or falling?
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def scroll_x(self):
        # Setup
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        bound = screen_width / 4

        # Move the level with respect to the Player
        if player_x < bound and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - bound and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8


    # Does the enemy go off the platform or not?
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():      # A list of sprites
            # Taking my enemy, check with a series of bounds
            if pygame.sprite.spritecollide(enemy, self.bound_layout_sprites, False):
                enemy.reverse()

    #Create particles
    def create_jump_particles(self, pos):
        # Align the particle in middle
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)
   
    # Run the entire game
    def run(self):

        # Sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # Background Palms
        self.bg_palm_sprites.draw(self.display_surface)
        self.bg_palm_sprites.update(self.world_shift)

        # Terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # Enemy
        self.enemy_sprites.draw(self.display_surface)
        self.bound_layout_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.update(self.world_shift)

        # Crate
        self.crate_sprites.draw(self.display_surface)
        self.crate_sprites.update(self.world_shift)

        # Grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # Coins
        self.coin_sprites.draw(self.display_surface)
        self.coin_sprites.update(self.world_shift)

        #Foreground Palms
        self.fg_palm_sprites.draw(self.display_surface)
        self.fg_palm_sprites.update(self.world_shift)

        #Dust particles
        self.dust_sprite.draw(self.display_surface)
        self.dust_sprite.update(self.world_shift)

        # Player Initialization
        self.player.draw(self.display_surface)
        self.player.update()

            # States of Player
        self.horizontal_movement_collision()    # Running
        self.get_player_on_ground()     # Is the player on the ground initially before jumping?
        self.vertical_movement_collision()  #Jumping
        self.create_landing_dust()  # Check for a difference
        self.scroll_x()     # Move the player with respect to the level

            #Goals
        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift)

            # Water
        self.water.draw(self.display_surface, self.world_shift)






