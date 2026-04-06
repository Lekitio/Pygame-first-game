

#information about masks: Invisible pixels -> black, visible pixels -> White
#   pixel perfect collision and sillouettes

from settings import * #all, includes pygame
from player import Player
from sprites import *
from groups import AllSprites

from random import randint
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        #Setup
        pygame.init()
        self.main_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #from settings
        pygame.display.set_caption("Game name")
        self.clock = pygame.time.Clock() 
        self.running = True

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # Sprites
        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), self.all_sprites, self.collision_sprites)
        
    
    def setup(self):
        the_map = load_pygame(join("Tiles", "Map3", "main_map.tmx"))
        # the_map = load_pygame(join("Tiles", "Map2.tmx"))
        # for obj in the_map.get_layer_by_name("object1 or something liek that"): THIS IS JUST FOR OBJECTS
        #     print(obj.x, obj.y, obj.image)
            # CollisionSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites]) #pos, surf, groups

        for x, y, image in the_map.get_layer_by_name("Ground_main").tiles():
            CollisionSprite((x*TILE_SIZE, y*TILE_SIZE), image, [self.all_sprites, self.collision_sprites])
            # pygame.Surface.blit(self.main_display, image, )

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.main_display.fill((176, 152, 164))

            
            # update
            self.all_sprites.update(dt)

            # draw
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()
        
if __name__ == "__main__": #only if its called main we will run it
    game = Game()
    game.run()
