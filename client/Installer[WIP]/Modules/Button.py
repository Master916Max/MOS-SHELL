from .Basic import Module
import pygame

class Button(Module):
    def __init__(self, text:str, screen,x,y,width, height, fgcolor = (125,125,125), bgcolor = (255,255,255)):
        super().__init__()
        self.text = text
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fgcolor
        self.bg = bgcolor
        self.clicked = False
        self.light = (self.bg[0] * 1.2, self.bg[1] * 1.2, self.bg[2] * 1.2)
        self.dark = (self.bg[0] * 0.6, self.bg[1] * 0.6, self.bg[2] * 0.6)
        self.was_clicked = False

    def draw(self, x = None, y = None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        Text_Size = 32
        pygame.draw.rect(self.screen,self.bg,(self.x,self.y,self.width,self.height))
        if self.clicked:
            pygame.draw.line(self.screen, self.dark,(self.x, self.y),(self.x+self.width, self.y), 3)
            pygame.draw.line(self.screen, self.dark,(self.x, self.y),(self.x, self.y + self.height), 3)
            pygame.draw.line(self.screen, self.light,(self.x, self.y+self.height),(self.x+self.width, self.y+ self.height), 3)
            pygame.draw.line(self.screen, self.light,(self.x+self.width, self.y),(self.x+self.width, self.y + self.height), 3)
        else:
            pygame.draw.line(self.screen, self.dark,(self.x, self.y+self.height),(self.x+self.width, self.y+ self.height), 3)
            pygame.draw.line(self.screen, self.dark,(self.x+self.width, self.y),(self.x+self.width, self.y + self.height), 3)
            pygame.draw.line(self.screen, self.light,(self.x, self.y),(self.x+self.width, self.y), 3)
            pygame.draw.line(self.screen, self.light,(self.x, self.y),(self.x, self.y + self.height), 3)
            
        font = pygame.font.Font(None, Text_Size)
        text = font.render(self.text, True, self.fg)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        if self.clicked:
            pygame.draw.rect(self.screen, (0,0,0), text_rect.inflate(10, 10))  # Draw background for text
            pygame.draw.rect(self.screen, self.bg, text_rect.inflate(8, 8)) 
        self.screen.blit(text, text_rect)

    def click(self):
        pass

    def mouse_over(self, pos):
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            return True
        return False

    def mouse_down(self, pos):
        if self.mouse_over(pos):
            self.clicked = True
            self.was_clicked = True
            return True
        return False
    
    def mouse_up(self, pos):
        if self.clicked and self.mouse_over(pos):
            self.clicked = False
            return True
        self.clicked = False
        return False

    def mouse_move(self, pos):
        if self.mouse_over(pos):
            pass
        else:
            self.clicked = False
        return self.mouse_over(pos)

        
