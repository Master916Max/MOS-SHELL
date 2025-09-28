
import pygame

from client.Components.mos_window import MosWindow


class MosSettings(MosWindow):
    def __init__(self, config: dict):
        super().__init__(config)
        self.pages = []
        self.current_page = 0
        self.page_history = []
        self.font_size = 20
        self.text_color = (0, 0, 0)

    
    def draw_content(self):
        font = pygame.font.Font(None, self.font_size)
        
        Title = font.render("Settings", True, self.text_color)

        self.surface.blit(Title, (10, 10))

    def handle_custom_input(self, event):
        if self.type_id == 'TERMINAL' and event.type == pygame.KEYDOWN:
            pass