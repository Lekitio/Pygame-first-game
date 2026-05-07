from settings import *
import pygame
from player import Player
from texts import *

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

class Textbox(VisualSprite):
    def __init__(self, groups, texts, text_num=-1):
        self.text_num = text_num +1
        self.font = pygame.font.Font(join("images", "times.ttf"), 20)
        self.texts = texts
    
        text_surf = self.font.render(texts[self.text_num][1], True, "black")
        self.image = pygame.image.load(join("images", "Textbox.png")).convert_alpha()
        self.scalar = 0.16
        self.image = pygame.transform.smoothscale_by(self.image, self.scalar)
        self.image.blit(text_surf, dest=(10,50))
        super().__init__(self.texts[self.text_num][0], self.image, groups)

        self.texts_time = pygame.time.get_ticks()
    
    def update(self, dt):
        # checks for right key_press
        self.keys = pygame.key.get_pressed()
        if self.keys[text_key]:
            # checks if delta x,y < 500
            if abs(self.player.rect.center[0] - self.textbox.rect.center[0]) < 500 and abs(self.player.rect.center[1] - self.textbox.rect.center[1]) < 500:
                # creates a cooldown between switches
                if pygame.time.get_ticks()-self.texts_time >= 5/dt:
                    self.texts_time = pygame.time.get_ticks()
                    next_text(self)
                    

def texts_init(self):
    self.textbox = Textbox((self.textboxes, self.all_sprites), text1)

def texts_update(self, dt):
    # checks for right key_press
    self.keys = pygame.key.get_pressed()
    if self.keys[text_key]:
        # checks if delta x,y < 500
        if abs(self.player.rect.center[0] - self.textbox.rect.center[0]) < 500 and abs(self.player.rect.center[1] - self.textbox.rect.center[1]) < 500:
            # creates a cooldown between switches
            if pygame.time.get_ticks()-self.texts_time >= 5/dt:
                self.texts_time = pygame.time.get_ticks()
                next_text(self)

# kills old textbox and creates a new one with new pos & text
def next_text(self):
    if self.text_num == len(text1)-1:
        return
    self.text_num += 1
    self.textbox.kill()

    self.textbox = Textbox(text1[self.text_num][0], (self.textboxes, self.all_sprites),text1[self.text_num][1])



    
