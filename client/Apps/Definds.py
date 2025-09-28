import pygame

class MSG_Box:
    def __init__(self,Titel, ContentL1,ContentL2,Buttons, Type, root = None, Logo = None):pass
    def calc_dims(self):pass
    def update_x_y(self,rel, mousepos):pass
    def in_window(self,x,y):pass
    def handel_input(self, type : str, dat):pass
    def draw(self, sreen: pygame.Surface = None):pass

class Window:
    def __init__(self, titel, width,height, Logo=None):pass 
    def add_input_handler(self,func):pass 
    def add_screen_drawer(self, name_func):pass
    def draw(self,sreen: pygame.Surface):pass
    def in_window(self,x,y):pass
    def update_x_y(self,rel, mousepos):pass
    def handel_input(self, type : str, dat):pass