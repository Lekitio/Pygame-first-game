

#information about masks: Invisible pixels -> black, visible pixels -> White
#   pixel perfect collision and sillouettes

from settings import * #all, includes pygame
from player import Player
from sprites import *
from groups import AllSprites
# from enemies import Enemy1

from random import randint
from pytmx.util_pygame import load_pygame #this is from tiled

class Game:
    def __init__(self):
        # Setup
        pygame.init()
        self.main_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #from settings
        pygame.display.set_caption("Game name")
        self.clock = pygame.time.Clock() 
        self.running = True

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group() #this is a sprite method, ex of why we add to pygame.sprite.Sprite. Collision sprites will include walls
        self.enemy_collision_sprites = pygame.sprite.Group() #here i wills tore enemies so when collliding with things here you take dmg or do dmg
        self.enemy_sprites = pygame.sprite.Group()
        self.textboxes = pygame.sprite.Group()


        self.setup()

        # Sprites
        self.player = Player((WINDOW_WIDTH//2, WINDOW_HEIGHT//2), self.all_sprites, self.collision_sprites)
        
        texts_init(self)
    
        # Constants
        self.framerate = 120

        #level information, for future use if we make levels.
        # level = 0
        # enemy_level_list = [[("positionx", "positiony"), "image", ["Groups"]]]
        # for enemy_info in enemy_level_list[level]:
        #     Enemy1(enemy_info[0], enemy_info[2], enemy_info[3])
        #     #creates an enemy it's stores in enemy_sprites but but in a variable. Only care about colissions it think.
            #special enemies can have special variables, these are for.

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
            dt = self.clock.tick(self.framerate) / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.main_display.fill((176, 152, 164))

            
            # update
            self.all_sprites.update(dt)

            # draw
            self.all_sprites.draw(self.player.rect.center, dt)
            pygame.display.update()

            texts_update(self, dt)

        pygame.quit()
        
if __name__ == "__main__": #only if its called main we will run it
    
    if not pygame.IS_CE:
        print("This project uses the pygame-ce version of pygame and wont work otherwise.")
    else:
        game = Game()
        game.run()
