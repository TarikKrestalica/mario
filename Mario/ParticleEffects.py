import pygame, os, math
from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        # Main directory
        self.homedir = '/Users/tarikkrestalica/PycharmProjects/Super Mario'
        self.particle_path = 'graphics/character/dust_particles'
        # Speed of animation
        self.frame_index = 0
        self.animation_speed = 0.6

        #Type of animation
        if type == 'jump':
            self.frames = import_folder(os.path.join(self.homedir, self.particle_path, type))
        if type == 'land':
            self.frames = import_folder(os.path.join(self.homedir, self.particle_path, type))

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    # Play through the animation
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[math.floor(self.frame_index)]


    # Animate, have the particle shift with level
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift