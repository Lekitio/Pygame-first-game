from settings import *

class Enemy1(pygame.sprite.Sprite): # pygame.sprite.Sprite is so i can add it to a group and use built in collision handling later
    def __init__(self, pos, image, groups, wall_collision_sprites, player, health = 20):
        super().__init__(groups) #to call a method from a parent class, which is the stuff in the parenthesis??
        #initialiser
        # self.image = pygame.image.load() 
        #temp
        self.image = pygame.surface((100, 100)) #temp "image" before we fix actual character
        self.image.fill((51, 61, 41)) 

        self.rect = self.image.get_frect(bottomleft = (450, 300)) 
        self.hitbox_rect = self.rect.infalte(0, 0) #currently not making it any skinnier, playtest to find out

        self.health = health #uh lets start with this ig?


    def move(self):

    # def collision(self):
        #idea, check if its touching player -> do dmg
        #check if its touching player weapon -> get damaged
        #extra:
        #check for wall or floor

    
    def update(self, dt):
        self.move()

