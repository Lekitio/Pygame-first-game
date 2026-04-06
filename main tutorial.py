import pygame
from os.path import join
from random import randint


#making groups/classes/sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        #this is like refering that you have parents I guess?
        #parent in this case is group

        self.init_display()
        self.init_movement()
        self.init_jump()
        self.init_slash()

    #clean init
    def init_movement(self):
        self.speed = 300
        self.velocity = pygame.math.Vector2(1, 1)

    def init_display(self):
        w = 40
        h = 60
        # self.image = pygame.Surface((w, h))
        self.image = pygame.transform.smoothscale_by(pygame.image.load(join("images", "playerdeafult5.png")).convert_alpha(), 0.2)
        self.rect = self.image.get_frect(bottomleft = (10, ground.top))
        self.mask = pygame.mask.from_surface(self.image)
        
    def init_slash(self):
        self.can_slash = True
        self.last_slash_time = 0
        self.cooldown_slash = 1000

    def init_jump(self):
        #variables ig?
        self.can_jump = True
        self.current_jump_time = 0
        self.last_jump_time = 0
        self.on_ground = True

        #constants
        self.jump_force = 800
        self.jump_key = pygame.K_z
        self.jump_cooldown = 100
        self.jump_speed_cap = 600
        self.jump_velocity_multiplier = 0.6

        #pos
        self.groundy = ground.top

    #methods
    def in_frame_checker(self, HEIGHT, WIDTH):
        # @staticmethod uh i forgot how to use this nvm i dont need anymore
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0 #gets rid of pesky bugs
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        
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
            self.velocity.y *= 0.1

        # a speed cap
        self.velocity.y = min(self.jump_speed_cap, self.velocity.y)

    def jump_collision_control(self):
        if self.rect.bottom > self.groundy:
            #Reason for this being below move and > rather than >= is because otherwise i will be below the ground when jumping -> if will be true -> fell directly -> no jumping. 
            if self.on_ground == False:
                self.last_jump_time = pygame.time.get_ticks()
                AnimatedDustLanding(land_dust_animation, (player.rect.centerx, player.rect.top+10), all_sprites, 0.1)

            self.rect.bottom = self.groundy
            self.on_ground = True
            self.velocity.y = 0
            #Timer 
            self.can_jump = False
        self.can_jump_cooldown()
    
    def slash_timer(self):
        if not self.can_slash:
            current_slash_time = pygame.time.get_ticks()
            if current_slash_time > self.last_slash_time + self.cooldown_slash:
                self.can_slash = True
            
    def update(self, delta_time):
        #update() will run this
        keys = pygame.key.get_pressed() #this is a dictionary of all the keys
        
        self.velocity.x = keys[pygame.K_RIGHT]-keys[pygame.K_LEFT] #this jsut turns True -> 1, crazy
        
        #Getting inputs
        # jumping mechanism
        self.jump(keys, delta_time)
        
        self.rect.centerx += self.velocity.x * self.speed * delta_time #can control speed
        self.rect.centery += self.velocity.y * delta_time #confsuion, i have one in jump too

        #collision controll + jump cooldown
        self.jump_collision_control()

        # print(self.velocity.y, delta_time)
        self.in_frame_checker(HEIGHT, WIDTH) #makes sure its in frame

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_slash:
            print("pew")
            self.can_slash = False
            self.last_slash_time = pygame.time.get_ticks()
        self.slash_timer()


class GameObjects(pygame.sprite.Sprite): #this means that GameObjects is a child of sprite, can do sprite stuff
    def __init__(self, image, pos, groups, scale=None, scale_by=None):
        super().__init__(groups)
        if scale:
            self.image = pygame.transform.scale(image, scale)
        elif scale_by:
            self.image = pygame.transform.scale_by(image, scale_by)
        else:
            self.image = image #dont change it
        self.rect = self.image.get_frect(midbottom = pos)

class Object1(GameObjects):
    def __init__(self, image, groups):
        pos = (randint(0, WIDTH), ground.top + 30)
        super().__init__(image, pos, groups, scale=(100, 150))
        #question if you grandparent gets updated then do you also update # self.image = pygame.image.load(join("images", "Japanese_rock_pillar1.png")).convert_alpha() #import every time, inefficient time # self.image = pygame.transform.scale(image, (100, 150)) #bahahahhahaha you can squish the import # self.rect = self.image.get_bounding_rect() This is what i should use honestly OR just fix the art from the beginning # self.rect = self.image.get_frect(midbottom = (randint(0, WIDTH), ground.top + 30)) # its currently transparent so i need to move it down, hardcoded
        
        #masks
        #so it doesnt float anymore
        # self.mask = pygame.mask.from_surface(self.image) #returns type mask
        # mask_surf = mask.to_surface()
        # mask_surf.set_colorkey((0,0,0)) #gets rid of all black pixels good for flashes :D
        # self.image = mask_surf #so spooky

class Fog(GameObjects): #Since its so similar i can jst call to a parent class
    def __init__(self, image, groups):
        pos = (randint(0, WIDTH), randint(100, ground.top + 30))
        super().__init__(image, pos, groups, scale_by=0.1) #calling parent
        
        self.velocity = pygame.math.Vector2(1, 0)
        self.speed = randint(1, 5)
        # self.image = pygame.mask.from_surface(self.image).to_surface(), doesnt work on semi transparent objects

    def update(self, delta_time):
        if self.rect.left > WIDTH:
            self.kill()
            # print("death")
        self.rect.x += self.velocity.x * delta_time * self.speed

class AnimatedDustLanding(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups, scale_by=False):
        super().__init__(groups)
        self.frames = frames
        self.frame_i = 0
        # self.image = pygame.transform.scale_by(self.frames[self.frame_i], scale_by)
        self.image = self.frames[self.frame_i]
        self.rect = self.image.get_frect(center = pos)

        #time
        self.animation_speed = 20
        self.frame_timer = 0

    def update(self, delta_time):

        self.frame_i += 20*delta_time #dont ask me why the index grows by not one I am jsut as confused
        print(self.frame_i, self.image)
        if self.frame_i < len(self.frames):
            self.image = self.frames[int(self.frame_i)]
        else:
            self.kill() #when done kill the animation



def collision_pillar(sprite_group):
    #Test colission #sprite and rect check manualspritecollide(single, lst, dokill)
    collided = pygame.sprite.spritecollide(player, sprite_group, False) #you can specify if mask or not collide in fourth parameter. Mask very hardware intensive! pygame.sprite.collide_mask
    for pillar in collided:
        pygame.draw.rect(main_display, floor_color, pygame.FRect(pillar.rect.centerx-10, pillar.rect.top-30, 30, 30))

#mandatory stuff
pygame.init()
#"gets pygame started up"

#initial display # Pygame display info: https://www.pygame.org/docs/ref/display.html#pygame.display.init
WIDTH, HEIGHT = 900, 600
main_display = pygame.display.set_mode((WIDTH, HEIGHT)) 
#this creates a screen, set_mode specifically

pygame.display.set_caption("Game name")
#this gives the window a name
clock = pygame.time.Clock() #caps the framerate, Otherwise it runs infinitely fast

#importing all images
japanese_pillar_1_surf = pygame.image.load(join("images", "Japanese_rock_pillar1.png")).convert_alpha()
fog_nr_1_surf = pygame.image.load(join("images", "fog_nr_1.png")).convert_alpha()
land_dust_animation = [pygame.image.load(join("images", "Landing_dust_animation", f"{i}.png")).convert_alpha() for i in range(1, 7)]
font = pygame.font.Font(join("images", "times.ttf"), 50)
text_surf = font.render("Text", True, "red")
#you could import sounds pygame.mixer.Sound(filename)

#editing the imports
for i in range(6):
    land_dust_animation[i] = pygame.transform.scale_by(land_dust_animation[i], 0.1)
#sound.set_volume(0.5) #half sound

#constant
GRAVITY = 1300
#colors
grey = (71, 68, 72) #colors the screen main_display.fill(grey). But i wanna do it constantly so into the game
floor_color = (45, 35, 46)

#displays and blocks and surfces
#Makes the floor rectangle
ground = pygame.Rect(0, 400, 900, 500)

#sprite creating&grouping
all_sprites = pygame.sprite.Group()#holds and manages all sprites, grandparent/super()
japanese_pillar_1_sprites = pygame.sprite.Group() #more organised, usually for usually gonna get acessed but not as often as ex, player. Stuff
all_fog_sprites = pygame.sprite.Group()

#creating objects, order matter. created first -> gets covered. 
for i in range(10):
    Object1(japanese_pillar_1_surf, (all_sprites, japanese_pillar_1_sprites))
player = Player(all_sprites)

for i in range(10):
    Fog(fog_nr_1_surf, (all_sprites, all_fog_sprites))



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
    all_sprites.update(delta_time)

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
    collision_pillar(japanese_pillar_1_sprites)
    # pygame.display.draw(main_display, font)
    # main_display.blit(fog_1)
    main_display.blit(text_surf)
    pygame.display.update()
    #updates background every loop


pygame.quit()