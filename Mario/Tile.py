import pygame, os
from math import floor
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft= (x, y))

    def update(self, x_shift):
        self.rect.x += x_shift

# Apply to different layers(terrain, grass)
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load(os.path.join(os.environ.get("HOME"), 'Downloads/2 - Level', 'graphics/terrain/crate.png')).convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft= (x, offset_y))


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]  # Start image

    # Change state of player
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[floor(self.frame_index)]


    # Updates
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift

class Coin(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center= (center_x, center_y))

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)





