import pygame
from random import randrange

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, color_dict, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.color = list(color_dict.values())[randrange(0, len(color_dict) - 2)]
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
    
    def update(self):
        self.rect.centery += self.speed

    def show(self):
        print(self.color)