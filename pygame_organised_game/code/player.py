
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((40, 60))
        self.rect = self.image.get_frect(bottomleft = (10, ground.top))
        