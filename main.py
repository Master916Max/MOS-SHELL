print("Please wait, loading the Shell...")

from startup import while_loading
import multiprocessing
import pygame
import time

lp = multiprocessing.Process(target=while_loading, kwargs={"dbg":False,"pict":"shell-logo.png"})

import gui

from Components.mos_window import MosWindow
from chore.mos import MOS


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
    os = MOS()
    root = gui.init()
    # Kill loading screen
    lp.kill()
    # Show main window
    gui.run(screen=root)

if __name__ == "__main__":
    # Start loading Screen
    lp.start()
    # Initialize GUI
    gui.startup()
    load_gui()