from settings import *
import pygame

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
    def __init__(self, pos, groups, text):
        self.font = pygame.font.Font(join("images", "times.ttf"), 20)
        text_surf = self.font.render(text, True, "black")
        self.text = text

        self.image = pygame.image.load(join("images", "Textbox.png")).convert_alpha()
        self.scalar = 0.16
        self.image = pygame.transform.smoothscale_by(self.image, self.scalar)
        self.image.blit(text_surf, dest=(10,50))
        super().__init__(pos, self.image, groups)

def texts_init(self):
    self.keys = pygame.key.get_pressed()
    self.text_num = 1
    self.texts_time = pygame.time.get_ticks()
    self.textbox = Textbox(texts[self.text_num][0], (self.textboxes, self.all_sprites),texts[self.text_num][1])

def texts_update(self, dt):
    if pygame.time.get_ticks()-self.texts_time >= 5/dt:
        if self.keys[text_key]:
            self.texts_time = pygame.time.get_ticks()
            next_text(self)

def next_text(self):
    if self.text_num == 3:
        return
    self.text_num += 1
    if not self.text_num == 0:
        self.textbox.kill()
    self.textbox = Textbox(texts[self.text_num][0], (self.textboxes, self.all_sprites),texts[self.text_num][1])


texts = [[(850,1000),"test text which is\nvery long now"],[(900,1000),"test text which is\nvery long now"],[(950,1000),"test text which is\nvery long now"]]

    
