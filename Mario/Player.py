import pygame
import os
from math import floor
# Access each folder's contents
from support import import_folder

# Influenced by the level map
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]  # Start with the first image
        self.rect = self.image.get_rect(topleft = pos)

        #Dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # Control Speed of the Player
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # Player Status
        self.status = 'idle'
        self.facing_right = True    # Direction the player faces

        # Collisions
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    # Understand Player Status
    def import_character_assets(self):
        main_path = os.environ.get("HOME") + '/PycharmProjects/Super Mario/'
        character_path = 'graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = main_path + character_path + animation
            self.animations[animation] = import_folder(full_path)


    def import_dust_run_particles(self):
        main_path = os.environ.get("HOME") + '/PycharmProjects/Super Mario/'
        particle_path = main_path + 'graphics/character/dust_particles/run'
        self.dust_run_particles = import_folder(particle_path)


    # Switch the Animation
    def animate(self):
        animation = self.animations[self.status]

        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Check player direction
        image = animation[floor(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # Update the rect with its current status
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        # On Ceiling:
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    # Dust particles
    def run_dust_animation(self):
         if self.status == 'run' and self.on_ground:
             self.dust_frame_index += self.dust_animation_speed
             if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

             dust_particle = self.dust_run_particles[floor(self.dust_frame_index)]

             if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(5, 10)
                self.display_surface.blit(dust_particle, pos)
             else:
                 pos = self.rect.bottomright - pygame.math.Vector2(5, 10)
                 self.display_surface.blit(dust_particle, pos)


    # Key Presses, Player Movement
    def get_input(self):
        keys = pygame.key.get_pressed()

        # Player Speed
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    # Understand player state
    def get_status(self):
        # Compare the y coordinates
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        # Running or idling
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'


    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
