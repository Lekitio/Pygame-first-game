import pygame
from os.path import join
from random import randint

pygame.init()
#"gets pygame started up"

## Pygame display info: https://www.pygame.org/docs/ref/display.html#pygame.display.init
WIDTH = 900
HEIGHT = 600
main_display = pygame.display.set_mode((WIDTH, HEIGHT)) 
#this creates a screen, set_mode specifically

pygame.display.set_caption("Game name")
#this gives the window a name

#importing all images
japanese_pillar_1_surf = pygame.image.load(join("images", "Japanese_rock_pillar1.png")).convert_alpha()

clock = pygame.time.Clock() #caps the framerate, Otherwise it runs infinitely fast


GRAVITY = 700

def in_frame_checker(name, HEIGHT, WIDTH):
    if name.rect.bottom >= HEIGHT:
        name.rect.bottom = HEIGHT
    if name.rect.top <= 0:
        name.rect.top = 0 #gets rid of pesky bugs
    if name.rect.right >= WIDTH:
        name.rect.right = WIDTH
    if name.rect.left <= 0:
        name.rect.left = 0
    
#making groups/classes/sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        #this is like refering that you have parents I guess?
        #parent in this case is group
        w = 40
        h = 60
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_frect(bottomleft = (10, ground.top))
        # self.velocity = pygame.math.Vector2(1, 0) #defult
        self.speed = 300

        #Physics
        self.velocity = pygame.math.Vector2(1, 1)
        #Jumping physics
        self.on_ground = True
        self.jump_force = 400

        #Jump
        self.can_jump = True
        self.last_jump_time = 0
        self.jump_cooldown = 100
        self.current_jump_time = 0
        self.landed = False #this isnt optimal
        self.jump_key = pygame.K_z
        self.jump_speed_cap = 600
        self.jump_velocity_multiplier = 0.3
        self.groundy = ground.top

        #Slash
        self.can_slash = True
        self.last_slash_time = 0
        self.cooldown_slash = 1000

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
            self.velocity.y += self.jump_velocity_multiplier * GRAVITY * delta_time
            #why times delta_time here?
            
        #if släppa and upwards
        if not keys[self.jump_key] and self.velocity.y < 0:
            self.velocity.y *= 0.05

        # a speed cap
        self.velocity.y = min(self.jump_speed_cap, self.velocity.y)

        #set actions into place
        self.rect.centery += self.velocity.y * delta_time

        if self.rect.bottom >= self.groundy:
            if self.on_ground == False:
                self.last_jump_time = pygame.time.get_ticks()
            self.rect.bottom = self.groundy
            self.on_ground = True
            self.can_jump = False
            self.velocity.y = 0

        self.can_jump_cooldown()

    def slash_timer(self):
        if not self.can_slash:
            current_slash_time = pygame.time.get_ticks()
            if current_slash_time > self.last_slash_time + self.cooldown_slash:
                self.can_slash = True
            
    def update(self):
        #update() will run this
        keys = pygame.key.get_pressed() #this is a dictionary of all the keys
        self.velocity.x = keys[pygame.K_RIGHT]-keys[pygame.K_LEFT] #this jsut turns True -> 1, crazy
        self.rect.centerx += self.velocity.x * self.speed * delta_time #can control speed
        self.rect.centery += self.velocity.y * delta_time
        in_frame_checker(player, HEIGHT, WIDTH) #makes sure its in frame

        #Getting inputs
        # jumping mechanism
        self.jump(keys, delta_time)

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_slash:
            print("pew")
            self.can_slash = False
            self.last_slash_time = pygame.time.get_ticks()
        self.slash_timer()


class Object1(pygame.sprite.Sprite):
    def __init__(self, image, group):
        super().__init__(group)
        #question if you grandparent gets updated then do you also update
        # self.image = pygame.image.load(join("images", "Japanese_rock_pillar1.png")).convert_alpha()
        #import every time, inefficient time
        
        self.image = image

        self.image = pygame.transform.scale(self.image, (100, 150))
        #bahahahhahaha you can squish the import
        # self.rect = self.image.get_bounding_rect() This is what i should use honestly OR just fix the art from the beginning
        self.rect = self.image.get_frect(midbottom = (randint(0, WIDTH), ground.top + 30))
        # its currently transparent so i need to move it down, hardcoded



all_sprites = pygame.sprite.Group()
#holds and manages all sprites, grandparent

grey = (71, 68, 72) #colors the screen main_display.fill(grey). But i wanna do it constantly so into the game

#Makes the floor rectangle
floor_color = (45, 35, 46)
ground = pygame.Rect(0, 400, 900, 500)

#creating objects, order matter.
#   created first -> gets covered. 
japanese_pillar_1_sprites = pygame.sprite.Group() #more organised, usually for usually gonna get acessed but not as often as ex, player. Stuff
for i in range(10):
    Object1(japanese_pillar_1_surf, (all_sprites, japanese_pillar_1_sprites))
player = Player(all_sprites)

# pygame.FRect((0, 520), (900, 300))
#FRects are rectangles but with decimals -> more precise #Rectangles can give you acess to a bunch of useful points of the rectangle -> less math #for storing coordinates
#convertion for higher framerate, .convert() if no transparency, .convert_alpha() if transparent pixels

frames = 60
running = True
while running:
    delta_time = clock.tick(frames)/1000
    # print(clock.get_fps())
#to make sure everyone moves the same speed and not make one persons game much faster cause they got more frame    # -> math and delta_time (how long time (ms) to render one frame)

    #getting all sprites up to date
    all_sprites.update()

    #making display
    main_display.fill(grey)
    # pygame.Surface.blit(ground)
    pygame.draw.rect(main_display, floor_color, ground) #i draw rect here but define rect outside

    #event loop
    queue = pygame.event.get() #gets event from queue (takes every input as a list then clears all input)
    for event in queue: #in here you check for all input
        if event.type == pygame.QUIT:
            running = False
           

    all_sprites.draw(main_display)
#.update() - updates every spite, inbyggd in sprite to appear or something #.draw() blit the sprite images #gets everything in the group to appear i guess


    #Test colission #sprite and rect check manualspritecollide(single, lst, dokill)
    
    collided = pygame.sprite.spritecollide(player, japanese_pillar_1_sprites, False)
    for pillar in collided:
        pygame.draw.rect(main_display, floor_color, pygame.FRect(pillar.rect.centerx-10, pillar.rect.top-30, 30, 30))
        #hardcoding position fixes

    pygame.display.update()
    #updates background every loop


pygame.quit()