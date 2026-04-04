import pygame

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


#making groups/classes/sprites
class Player(pygame.sprite.Sprite):



grey = (71, 68, 72)
#colors the screen

floor_color = (45, 35, 46)
# pygame.FRect((0, 520), (900, 300))
you_wanna_learn = False
if you_wanna_learn:
    pass
    #FRects are rectangles but with decimals -> more precise
    #Rectangles can give you acess to a bunch of useful points of the rectangle -> less math
    #for storing coordinates


#Making the player

player_color = (241, 240, 234)
w = 50
h = 80
player = pygame.Surface((w, h))

#another use of rectangle is knowing player pos
player_rect = player.get_frect(topleft = (10,10))
player_direction = pygame.math.Vector2(1, -1) #2d
player_speed = 300

#load images FUTURE FIX
# bg = pygame.image.load("C:\Users\Hanna\Pictures\Screenshots\Screenshot2026-01-17223534.png")
#ok nvm that didnt work. One way: Be in the code folder
#convertion for higher framerate, .convert() if no transparency, .convert_alpha() if transparent pixels

frames = 60
i = 0
running = True
while running:
    delta_time = clock.tick(frames)/1000
    # print(clock.get_fps())
    if you_wanna_learn:
        pass
        #to make sure everyone moves the same speed and not make one persons game much faster cause they got more framse
        # -> math and delta_time (how long time (ms) to render one frame)

    #making display
    if you_wanna_learn:
        pass
        #pygame.key
        #pygame.mouse
    main_display.fill(grey)
    ground = pygame.draw.rect(main_display, floor_color, [0, 400, 900, 300]) #rect has other benefits too
    main_display.blit(player, player_rect) #this is our player
    player_rect.center += player_direction * player_speed * delta_time #can control speed

    #check if in frame?
    if player_rect.bottom >= height:
        player_rect.bottom = height
        player_direction.y *= -1
    if player_rect.top <= 0:
        player_rect.top = 0 #gets rid of pesky bugs
        player_direction.y *= -1
    if player_rect.right >= width:
        player_rect.right = width
        player_direction.x *= -1        
    if player_rect.left <= 0:
        player_rect.left = 0
        player_direction.x *= -1

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
        # if event.type == pygame.KEYDOWN: #checks if anything is pressed
        #     if event.key == pygame.K_a:
        #         print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos
        #downsidechecks it once, only checks for the action of something
    
    # input()
    if you_wanna_learn:
        pass
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
    keys = pygame.key.get_pressed() #this is a dictionary of all the keys
    player_direction.x = keys[pygame.K_RIGHT]-keys[pygame.K_LEFT] #this jsut turns True -> 1, crazy
    # if keys[pygame.K_RIGHT]:
    #     player_direction.x = 1
    # else:
    #     player_direction.x = 0

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print("pew")

    pygame.display.update()
    #updates background every loop

    if you_wanna_learn: #my mistakes
        pass
        # if pygame.event.get() == pygame.QUIT:
        #     this wont work since pygame.event.get() returns a list and pygame.QUIT is an "element"
        #     break


pygame.quit()