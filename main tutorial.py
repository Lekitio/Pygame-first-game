import pygame
from os.path import join
from random import randint

pygame.init()
#"gets pygame started up"

## Pygame display info: https://www.pygame.org/docs/ref/display.html#pygame.display.init
width = 900
height = 600
main_display = pygame.display.set_mode((width, height)) 
#this creates a screen, set_mode specifically

pygame.display.set_caption("Game name")
#this gives the window a name

clock = pygame.time.Clock() #caps the framerate, Otherwise it runs infinitely fast

def in_frame_checker(name, height, width):
    if name.rect.bottom >= height:
        name.rect.bottom = height
        name.direction.y *= -1
    if name.rect.top <= 0:
        name.rect.top = 0 #gets rid of pesky bugs
        name.direction.y *= -1
    if name.rect.right >= width:
        name.rect.right = width
        name.direction.x *= -1        
    if name.rect.left <= 0:
        name.rect.left = 0
        name.direction.x *= -1

#making groups/classes/sprites
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        #this is like refering that you have parents I guess?
        #parent in this case is group
        w = 50
        h = 80
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_frect(topleft = (10,10))
        self.direction = pygame.math.Vector2(1, 1) #defult
        self.speed = 300

    def update(self):
        #update() will run this
        keys = pygame.key.get_pressed() #this is a dictionary of all the keys
        self.direction.x = keys[pygame.K_RIGHT]-keys[pygame.K_LEFT] #this jsut turns True -> 1, crazy
        self.rect.center += self.direction * self.speed * delta_time #can control speed
        in_frame_checker(player, height, width) #makes sure its in frame

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("pew")

class Object1(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        #question if you grandparent gets updated then do you also update
        # self.image = pygame.image.load(join("images", "Japanese_rock_pillar1.png")).convert_alpha()
        #import every time, inefficient time
        
        self.image = image

        self.image = pygame.transform.scale(self.image, (100, 150))
        #bahahahhahaha you can squish the import
        # self.rect = self.image.get_bounding_rect() This is what i should use honestly OR just fix the art from the beginning
        self.rect = self.image.get_frect(midbottom = (randint(0, width), ground.top + 30))
        # its currently transparent so i need to move it down, hardcoded

            
all_sprites = pygame.sprite.Group()
#holds and manages all sprites, grand master

grey = (71, 68, 72)
#colors the screen main_display.fill(grey). But i wanna do it constantly so into the game

#Makes the floor rectangle
floor_color = (45, 35, 46)
ground = pygame.Rect(0, 400, 900, 500)


#creating objects, order matter.
#   created first -> gets covered
japanese_pillar_1_surf = pygame.image.load(join("images", "Japanese_rock_pillar1.png")).convert_alpha()
for i in range(10):
    Object1(all_sprites, japanese_pillar_1_surf)
player = Player(all_sprites)

# pygame.FRect((0, 520), (900, 300))
you_wanna_learn = False
if you_wanna_learn:
    pass
    #FRects are rectangles but with decimals -> more precise
    #Rectangles can give you acess to a bunch of useful points of the rectangle -> less math
    #for storing coordinates


#load images FUTURE FIX
# bg = pygame.image.load("C:\Users\Hanna\Pictures\Screenshots\Screenshot2026-01-17223534.png")
#ok nvm that didnt work. One way: Be in the code folder
#convertion for higher framerate, .convert() if no transparency, .convert_alpha() if transparent pixels

frames = 60
# i = 0
running = True
while running:
    delta_time = clock.tick(frames)/1000
    # print(clock.get_fps())
    if you_wanna_learn:
        pass
        #to make sure everyone moves the same speed and not make one persons game much faster cause they got more framse
        # -> math and delta_time (how long time (ms) to render one frame)

    #getting all sprites up to date
    all_sprites.update()

    #making display
    if you_wanna_learn:
        pass
        #pygame.key
        #pygame.mouse
    main_display.fill(grey)
    # pygame.Surface.blit(ground)
    pygame.draw.rect(main_display, floor_color, ground) #i draw rect here but define rect outside

    #event loop
    if you_wanna_learn: #info about event actions
        pass
        ##Pygame event info https://www.pygame.org/docs/ref/event.html?highlight=pygame%20event#module-pygame.event
        # lmao this is just a trick to save space
        # pygame.event.pump() can be used when you dont want wasted memeory and dont want event inputs, ex cutscenes ig
        # pygame.event.poll() - wwaits for specific event, if none then it returns none i guess  
    queue = pygame.event.get() #gets event from queue (takes every input as a list then clears all input)
    for event in queue: #in here you check for all input
        if event.type == pygame.QUIT:
            running = False
        
    # input()
    if you_wanna_learn:
        pass #moved it into a sprite
        # https://www.pygame.org/docs/ref/key.html
        # print(pygame.mouse.get_pressed()) or [0]
        # if pygame.mouse.get_pressed()[0]:
        #     player_rect.center = event.
        # print(keys)
        # if keys[pygame.K_1]:
        #     print(f"you are pressing down {1} for the {i}th time")
        #     i+= 1
        
        #if you wanna go up and down too diagonals need this fix
        # player_rect.center += player_direction.normalize() if player_direction else player_direction
        # keys = pygame.key.get_pressed() #this is a dictionary of all the keys
        # player_direction.x = keys[pygame.K_RIGHT]-keys[pygame.K_LEFT] #this jsut turns True -> 1, crazy
        # if keys[pygame.K_RIGHT]:
        #     player_direction.x = 1
        # else:
        #     player_direction.x = 0
        # if event.type == pygame.KEYDOWN: #checks if anything is pressed
        #     if event.key == pygame.K_a:
        #         print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos
        #downsidechecks it once, only checks for the action of something
    



    all_sprites.draw(main_display)
    if you_wanna_learn:
        pass
        #.update() - updates every spite, inbyggd in sprite to appear or something
        #.draw() blit the sprite images
        #gets everything in the group to appear i guess

    pygame.display.update()
    #updates background every loop

    if you_wanna_learn: #my mistakes and previous deleted code
        pass
        # if pygame.event.get() == pygame.QUIT:
        #     this wont work since pygame.event.get() returns a list and pygame.QUIT is an "element"
        #     break

        # main_display.blit(player, player_rect) #this is our player

        #check if in frame?
        # if player.rect.bottom >= height:
        #     player.rect.bottom = height
        #     player.direction.y *= -1
        # if player.rect.top <= 0:
        #     player.rect.top = 0 #gets rid of pesky bugs
        #     player.direction.y *= -1
        # if player.rect.right >= width:
        #     player.rect.right = width
        #     player.direction.x *= -1        
        # if player.rect.left <= 0:
        #     player.rect.left = 0
        #     player.direction.x *= -1

pygame.quit()