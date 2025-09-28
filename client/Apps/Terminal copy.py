from .Definds import *

def Terminal_Drawer(window,surface: pygame.Surface): 
    surface.fill((0,0,0))
    return window
def Terminal_Handler(window,type,data):
    return window
def Window_SetUp() -> Window:
    logo = pygame.Surface((30,30),pygame.SRCALPHA)
    pygame.draw.rect(logo, (255,255,255) (0,0,30,30))
    return Window("MUS-OS-Terminal", 720,480,logo)