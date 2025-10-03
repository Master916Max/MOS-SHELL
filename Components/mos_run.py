
from encodings.punycode import T
from operator import le
from turtle import left
import pygame
import os

from Components.mos_window_base import MosWindowBase


class MosRunDialog(MosWindowBase):
    def __init__(self, config: dict):
        cfg = {
            "width": 300,
            "height": 200,
            "title": "MOS Run Dialog",
            "parent": config.get("parent", None),
            "zlayer": config.get("zlayer", 1),
            "logo": None   

        }
        super().__init__(cfg)
        self.font_size = 16
        self.text_color = (0, 0, 0)
        self.text = ""
        

    
    def draw_content(self):
        font = pygame.font.match_font('arial', bold=True)
        font = pygame.font.Font(font, self.font_size)
        y_offset = self.title_height + 10
        Title = font.render(f"Type any Window Type and", True, self.text_color)
        Title2 = font.render(f" MOS will open it for you.", True, self.text_color)
        left_icon = pygame.image.load(os.path.join("Resources","icons","run_sys.png"))
        left_icon = pygame.transform.scale(left_icon, (32, 32))
        left_icon_width = left_icon.get_width()

        pygame.draw.rect(self.surface, (200, 200, 200), (0, self.height - 50, self.width, 50))

        self.surface.blit(left_icon, (10, 10 + y_offset))

        self.surface.blit(Title, (left_icon_width + 20, 10 + y_offset))
        self.surface.blit(Title2, (left_icon_width + 20, 20 + y_offset + Title.get_height()))

    def handle_custom_input(self, event):
        pass