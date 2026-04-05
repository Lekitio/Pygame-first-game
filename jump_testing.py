import pygame
#I've downloaded the pygame-ce version (community edition)
#https://pypi.org/project/pygame-ce/

pygame.init()
# print("yay")
# print(pygame.version.ver)
WIDTH = HEIGHT = 300
display_main = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock()
running = True

GRAVITY = 700

all_sprites = pygame.sprite.Group()
class player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_frect(midbottom = (WIDTH//2, HEIGHT//2))
        self.direction = pygame.math.Vector2(0, 0)

        #Physics
        self.velocity = pygame.math.Vector2(0, 0)
        #Jumping physics
        self.on_ground = True
        self.jump_force = 600

        #jump cooldown
        self.can_jump = True
        self.last_jump_time = 0
        self.jump_cooldown = 100
        self.current_jump_time = 0
        self.landed = False #this isnt optimal
        self.jump_key = pygame.K_z
        self.jump_speed_cap = 600


    # def jump(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[self.jump_key]:
            
    #         self.velocity.y += GRAVITY
    #         self.direction.y -= self.velocity.y
        
    #     elif not keys[self.jump_key] and self.moving_up:
    #         self.velocity.y = 0
    #         self.direction.y =- GRAVITY

    def can_jump_cooldown(self):
        if not self.can_jump:
            self.current_jump_time = pygame.time.get_ticks()
            if self.current_jump_time >= self.last_jump_time + self.jump_cooldown:
                self.can_jump = True
    def jump(self, keys, delta_time):
        if keys[self.jump_key] and self.on_ground and self.can_jump:
            # self.rect.centery = 1
            self.velocity.y = -self.jump_force
            self.on_ground = False

        self.velocity.y += GRAVITY * delta_time #always affected by gravity
        
        
        # downwards
        if self.velocity.y > 0:
            self.velocity.y += 0.2 * GRAVITY * delta_time
            #why times delta_time here?
            
        #if släppa and upwards
        if not keys[self.jump_key] and self.velocity.y < 0:
            self.velocity.y *= 0.05


        # a speed cap
        self.velocity.y = min(self.jump_speed_cap, self.velocity.y)

        #set actions into place
        self.rect.centery += self.velocity.y * delta_time

        if self.rect.bottom >= HEIGHT:
            if self.on_ground == False:
                self.last_jump_time = pygame.time.get_ticks()
            self.rect.bottom = HEIGHT
            self.on_ground = True
            self.can_jump = False
            self.velocity.y = 0

        self.can_jump_cooldown()

    def update(self):
        keys = pygame.key.get_pressed()
        self.jump(keys, delta_time)
        

hanako = player(all_sprites)

while running:
    delta_time = clock.tick(60)/1000

    queue = pygame.event.get() 
    for event in queue:
        if event.type == pygame.QUIT:
            running = False
    
    #display stuff
    all_sprites.update()
    display_main.fill((71, 68, 72))
    all_sprites.draw(display_main)
    
    pygame.display.update()

pygame.quit()
