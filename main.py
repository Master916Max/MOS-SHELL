#import multiprocessing
import gui
import pygame

def terminal(window,screen: pygame.Surface):
    screen.fill((200,200,200))
    #screen_width, screen_height = screen.get_size()
    font = pygame.font.Font(None, 50)  # Default font, size 74
    data_text = font.render(f"{gui.data}", True, (0,0,0))
    wdata_text = font.render(f"{gui.wdata}", True, (0,0,0))
    data1_text = font.render(f"{gui.mousbuttondown}", True, (0,0,0))
    screen.blit(data_text, (0, 0))
    screen.blit(data1_text,(0, data_text.get_height()+5))
    screen.blit(wdata_text,(0, data_text.get_height()+5 + data1_text.get_height() + 5))
    return window


def load_gui():
    gui.init()
    gui.zlayer.append(gui.Window("Terminal", 500,500, Logo=(0,0,0)))
    gui.zlayer[0].add_screen_drawer(terminal)
    gui.zlayer[0].x = 100
    gui.zlayer[0].y = 50
    gui.zlayer.append(gui.Window("Terminal2", 300,300, None))
    gui.zlayer[1].add_screen_drawer(terminal)
    gui.zlayer.append(gui.Window("Window", 250,250, None))
    gui.Create_MSG_Box(f"Welcome to MOS-{gui.version}","You can close this PopUp.","Go to the Settings to personelize your PC.", 0,1,None)
    gui.run()

load_gui()
