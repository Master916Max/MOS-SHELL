from . import Basic
import pygame

class Input(Basic.Module):
    def __init__(self, screen,x,y,width, height, fgcolor = (125,125,125), bgcolor = (255,255,255), txtfont = None):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fgcolor
        self.bg = bgcolor
        self.input = "Test"
        self.font = txtfont if txtfont else pygame.font.Font(None, 32)

    def draw(self):
        pygame.draw.rect(self.screen,(0,0,0),(self.x,self.y,self.width,self.height))
        pygame.draw.rect(self.screen,self.bg,(self.x+1,self.y+1,self.width-2,self.height-2))
        text = self.font.render(str(self.input), True, self.fg)
        # Top Left corner of the input box
        text_rect = text.get_rect(topleft=(self.x + 2, self.y + (self.height // 2) -( text.get_height() // 2)))
        self.screen.blit(text, text_rect)

    def handle(self,event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input = self.input[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                self.input += event.unicode