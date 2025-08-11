import pygame

class Text():
    def __init__(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.surface = None
        self.rect = None
        self.update()
    
    def update(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
    #X and Y are the coordinates of the top left corner of the text
    def drawtl(self, surface, x, y):
        self.rect.topleft = (x, y)
        surface.blit(self.surface, self.rect)
    #X and Y are the coordinates of the center of the text
    def drawm(self, surface, x ,y):
        self.rect.center = (x, y)
        surface.blit(self.surface, self.rect)
