import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = pygame.mouse.get_pos()
        self.rect.center = (self.pos[0], self.pos[1])
        self.rect.center = (x, y)

    def update(self):

        self.pos = pygame.mouse.get_pos()
        self.rect.center = (self.pos[0], self.pos[1])

