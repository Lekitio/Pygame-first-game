from settings import *
import pygame
from texts import *
from math import *

from operator import sub #for debug text

class VisualSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Spirit(VisualSprite):
    def __init__(self, groups, parent, spirit_id, pos=(1800,800)):
        self.scalar = 2
        self.image = pygame.image.load(join("images", "spirit.png")).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, self.scalar)
        super().__init__(pos, self.image, groups)

        self.spirit_id = spirit_id
        self.parent = parent
        self.collectable = True

        self.x_dir = 0
        self.x_speed_max,self.y_speed_max = 600,600
        self.speed_div = float(0.5)

    def update(self, dt):
        # handles collection of spirits and movement after
        if self.rect.colliderect(self.parent.player.rect) and self.collectable:
            self.collectable = False
            self.parent.spirit_sprites.spirit_order[self.spirit_id] = max(self.parent.spirit_sprites.spirit_order)+1 # sets the spirit's order of collection based on its id
        if not self.collectable:
            self.move(dt)


    def move(self, dt):
        # sets position to aim for to an offset based on movement direction and spirit count (independetly)
        self.player_pos = self.parent.player.rect.center
        self.player_pos = (self.player_pos[0]+60*self.x_dir*self.parent.spirit_sprites.spirit_order[self.spirit_id], self.player_pos[1])

        # calculate speed
        # x
        if abs(self.player_pos[0]-self.rect.center[0]) > self.speed_div*self.x_speed_max:
            if self.player_pos[0] > self.rect.center[0]:
                self.x_speed = self.x_speed_max
            else:
                self.x_speed = -self.x_speed_max
        else:
            self.x_speed = (self.player_pos[0] - self.rect.center[0])/self.speed_div
        # y
        if abs(self.player_pos[1]-self.rect.center[1]) > self.speed_div*self.y_speed_max:
            if self.player_pos[1] > self.rect.center[1]:
                self.y_speed = self.y_speed_max
            else:
                self.y_speed = -self.y_speed_max
        else:
            self.y_speed = (self.player_pos[1]-self.rect.center[1])/self.speed_div

        # removes infinite smoothing
        if abs(self.x_speed) < 5 and (self.x_speed <= 5 or self.x_speed >= 5):
            self.x_speed = 0 
        if abs(self.y_speed) < 5 and (self.y_speed <= 5 or self.y_speed >= 5):
            self.y_speed = 0 

        # check for which side to stay on
        if self.parent.player.velocity.x >0.9:
            self.x_dir = -1
        if self.parent.player.velocity.x <-0.9:
            self.x_dir = 1

        self.rect.center = (self.rect.center[0]+self.x_speed*dt, self.rect.center[1]+self.y_speed*dt)




class Textbox(VisualSprite):
    def __init__(self, groups, texts, textbox_id, parent, text_num=-1):
        self.text_num = text_num +1 #updates which text in the list to display
        self.textbox_id = textbox_id
        self.parent = parent #reference to parent self; game
        self.groups = groups
        self.texts = texts #list of texts to display

        self.scalar = 0.16
        self.font = pygame.font.Font(join("images", "times.ttf"), 20)

        # Creates the image and text
        text_surf = self.font.render(texts[self.text_num][1], True, "black")
        self.image = pygame.image.load(join("images", "Textbox.png")).convert_alpha()
        self.image = pygame.transform.smoothscale_by(self.image, self.scalar)
        self.image.blit(text_surf, dest=(10,50))
        
        super().__init__(self.texts[self.text_num][0], self.image, self.groups)

        self.texts_time = pygame.time.get_ticks()


    def update(self, dt):
        player_pos = self.parent.player.rect.center

        # checks for the right key_press
        self.keys = pygame.key.get_pressed()
        if self.keys[text_key]:
            # checks if delta x,y < 500
            if abs(player_pos[0] - self.rect.center[0]) < 500 and abs(player_pos[1] - self.rect.center[1]) < 500:
                # creates a cooldown between switches
                if pygame.time.get_ticks()-self.texts_time >= 5/dt:
                    # checks if it's the last text of the list
                    if not self.text_num == len(self.texts)-1:
                        self.texts_time = pygame.time.get_ticks() # updates time 
                        
                        # kills self and creates new textbox with the next phrase
                        self.kill()
                        self.parent.textboxes[self.textbox_id] = Textbox(self.groups, self.texts, self.textbox_id,self.parent, self.text_num)


def texts_init(self):
    textbox_groups = (self.textboxes_sprites, self.all_sprites)
    self.textboxes = [Textbox(textbox_groups, text1, 0, self), Textbox(textbox_groups, text2, 1, self)]

    self.debug_text_line = "null"
    self.debug_text = DebugText(self, (self.all_sprites), self.player.rect.center)


class DebugText(VisualSprite):
    def __init__(self, parent, groups, pos):
        self.parent = parent
        self.groups = groups
        font = pygame.font.Font(join("images", "times.ttf"), 50)
        if self.parent.debug_text_line == "null":
            text_surf = font.render("", True, "red")
        else:
            text_surf = font.render(self.parent.debug_text_line, True, "red")
        super().__init__(pos, text_surf, self.groups)   
            


    def update(self, dt):
        self.kill()
        self.parent.debug_text = DebugText(self.parent, self.groups, tuple(map(sub, self.parent.player.rect.bottomright, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))))
    