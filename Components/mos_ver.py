from.mos_window import MosWindow
import pygame

def read_version() -> str:
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent
    return path.joinpath("VERSION").read_text().strip()

def read_build_id() -> str:
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent
    return path.joinpath("build_version.txt").read_text().strip()


#print("Version:", read_version())
#print("Build ID:", read_build_id())

class MosSettings(MosWindow):
    def __init__(self, configl: dict):
        self.logo = pygame.Surface()
        config ={
            'title': f"System Settings",
            'logo': None,
            'width': 400,
            'height': 400,
            'parent': configl['parent'],
            'zlayer': configl['zlayer'],
            'type_id': 'INFO'
        }
        super().__init__(config)
        

    
    def draw_content(self):
        font = pygame.font.Font(None, self.font_size)
        
        Title = font.render("Settings", True, self.text_color)

        self.surface.blit(Title, (10, 10))

    def handle_custom_input(self, event):
        if self.type_id == 'TERMINAL' and event.type == pygame.KEYDOWN:
            pass
