from settings import *

class AllSprites(pygame.sprite.Group): #lowkey this is fixing cam
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface() #ref to current display
        self.offset = pygame.Vector2(0, 0) #how far camera moves

    def draw(self, target_pos, dt): #customised drawing method
        target_x = -target_pos[0] + WINDOW_WIDTH/2
        target_y = -target_pos[1] + WINDOW_HEIGHT/2

        #overrides the self.all_sprites.draw(self.main_display) function
        smooth = 10
        # if self.offset.x - (self.offset.x - target_x)*0.005 < self.offset.x overshooting is slightly annoying...
        self.offset.x -= (self.offset.x - target_x)*smooth*dt
        self.offset.y -= (self.offset.y - target_y)*smooth*dt

        for sprite in self: #all the sprites excisting in this class
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)