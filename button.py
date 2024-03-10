import pygame

class Button():
    def __init__(self, text_input, font, text_color, position):
        self.position = position
        self.text_input = text_input
        self.font = font
        self.text_color = text_color
        self.text_surface = self.font.render(self.text_input, 'AA', text_color) 
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.position


        self.surface = pygame.Surface((275, 75))
        self.surface.fill((68, 170, 153))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = self.position

    def update(self, screen):
        screen.blit(self.surface, self.surface_rect)
        screen.blit(self.text_surface, self.text_rect)

    def check_for_click(self, mouse_pos):
        return(self.surface_rect.collidepoint(mouse_pos))