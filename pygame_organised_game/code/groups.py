from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2(0, 0)

    def draw(self, target_pos): #customised drawing method
        #overrides the self.all_sprites.draw(self.main_display) function
        self.offset.x = -target_pos[0] + (WINDOW_WIDTH//2)
        self.offset.y = -target_pos[1] + (WINDOW_HEIGHT//2)
        for sprite in self: #all the sprites excisting in this class
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)