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
    def __init__(self, pos, groups):
        font = pygame.font.Font(join("images", "times.ttf"), 50)
        text_surf = font.render("Text", True, "red")


        self.image =pygame.image.load(join("images", "Textbox.png")).convert_alpha()
        self.scalar = 0.16
        self.image = pygame.transform.smoothscale_by(self.image, self.scalar)
        self.image.blit(text_surf)
        super().__init__(pos, self.image, groups)



    
