import gui
import pygame

from components.mos_window import MosWindow
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
    root = gui.init()
    gui.create_msg_box(f"Welcome to MOS-{gui.version}", "You can close this PopUp.", "Go to the Settings to personelize your PC.", 0, 1, root=root)
    gui.run()

if __name__ == "__main__":
    load_gui()
