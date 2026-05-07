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
    def __init__(self, groups, texts, textbox_id, game, text_num=-1):
        self.text_num = text_num +1
        self.textbox_id = textbox_id
        self.game = game #reference to parent self; game
        self.groups = groups
        self.texts = texts

        self.scalar = 0.16
        self.font = pygame.font.Font(join("images", "times.ttf"), 20)

        text_surf = self.font.render(texts[self.text_num][1], True, "black")
        self.image = pygame.image.load(join("images", "Textbox.png")).convert_alpha()
        self.image = pygame.transform.smoothscale_by(self.image, self.scalar)
        self.image.blit(text_surf, dest=(10,50))
        
        super().__init__(self.texts[self.text_num][0], self.image, self.groups)

        self.texts_time = pygame.time.get_ticks()



    def update(self, dt):
        player_pos = self.game.player.rect.center

        # checks for right key_press
        self.keys = pygame.key.get_pressed()
        if self.keys[text_key]:
            # checks if delta x,y < 500
            if abs(player_pos[0] - self.rect.center[0]) < 500 and abs(player_pos[1] - self.rect.center[1]) < 500:
                # creates a cooldown between switches
                if pygame.time.get_ticks()-self.texts_time >= 5/dt:
                    # checks if it's the last text
                    if not self.text_num == len(self.texts)-1:
                        self.texts_time = pygame.time.get_ticks() # updates time 
                        
                        # kills self and creates new textbox with the next phrase
                        self.kill()
                        self.game.textboxes[self.textbox_id] = Textbox(self.groups, self.texts, self.textbox_id,self.game, self.text_num)

    


                    

def texts_init(self):
    textbox_groups = (self.textboxes_sprites, self.all_sprites)
    self.textboxes = [Textbox(textbox_groups, text1, 0, self), Textbox(textbox_groups, text2, 1, self)]
