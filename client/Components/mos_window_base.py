from abc import abstractmethod, ABC
from client.chore.mos import mos_app
import pygame

class MosWindowBase(ABC):
    def __init__(self, config: dict):
        if config is None:
            raise ValueError("config must be a dict")
        self.command_history = []
        self.command_buffer = ""
        self.cursor_pos = 0
        self.scroll_offset = 0
        self.terminal_font = pygame.font.Font(None, 20)
        self.terminal_lines = []
        # layering from the parent but could also be inside of the window itself because of rendering other windows or elements
        self.zlayer = config.get('zlayer', [])
        self.width = config['width']
        self.height = config['height']
        self.parent = config.get('parent',pygame.Surface((self.width- 10,self.height- 45)))
        self.title = config['title']
        self.x = self.parent.get_width()  // 2 - self.width  // 2
        self.y = self.parent.get_height() // 2 - self.height // 2
        self.logo = config['logo']
        self.func = None
        self.lastframe = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        self.syscolor = config.get('syscolor',(192, 199, 200))
        self.window_select_color = config.get('window_select_color',(0,0,168))
        self.menuf = config.get('menuf',pygame.font.Font(None, 24))
        self.textcolor = config.get('textcolor', (0,0,0))
        self.handler = None
        self.surface = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        self.id: str = f"{self.title}_{id(self)}"
        self.type_id = config.get('type_id',None)
        self.dragging = False
        self.drag_offset = (0, 0)
        self.title_height = 30
        self.close_btn_rect = pygame.Rect(self.width - 30, 0, 30, self.title_height)
        self.title_text = self.menuf.render(self.title, True, self.textcolor)

    
    def draw(self,screen: pygame.Surface):
        # Draw window background
        self.surface.fill((240, 240, 240))
        # Draw title bar
        pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.width, self.title_height))
        # Draw title text
        font = pygame.font.Font(None, 24)
        title_text = font.render(self.title, True, (0, 0, 0))
        self.surface.blit(title_text, (5, 5))

        # Draw content area - can be overridden by child classes
        self.draw_content()

        # Draw buttons
        pygame.draw.rect(self.surface, (255, 0, 0), self.close_btn_rect)
        # pygame.draw.rect(self.surface,(0,255,0), self.close_btn_rect)
        # pygame.draw.rect(self.surface,(0,0,255), self.close_btn_rect)
        # Draw X symbol
        x_start = self.width - 25
        x_end = self.width - 5
        pygame.draw.line(self.surface, (255, 255, 255), (x_start, 5), (x_end, 25), 2)
        pygame.draw.line(self.surface, (255, 255, 255), (x_start, 25), (x_end, 5), 2)
        # Draw window to screen
        screen.blit(self.surface, (self.x, self.y))


    def in_window(self,x,y):
        return pygame.Rect(self.x,self.y,self.width,self.height).collidepoint(x,y)

    def update_x_y(self,rel, mousepos):
        if pygame.Rect(self.x + rel[0],self.y + rel[1],self.width,70).collidepoint(mousepos):
            self.x = self.x + rel[0]
            if self.x < 0:
                self.x = 0
            if self.x + self.width > self.parent.get_width():
                self.x = self.parent.get_width() - self.width
            self.y = self.y + rel[1]
            if self.y < 0:
                self.y = 0
            return True
        return False

    def handle_input(self, event):
        self.handle_custom_input(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            relative_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
            
            # Check for close button click
            if self.close_btn_rect.collidepoint(relative_pos):
                self.destroy()

            # Start dragging
            if relative_pos[1] < self.title_height:
                self.dragging = True
                self.drag_offset = relative_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.x = mouse_pos[0] - self.drag_offset[0]
            self.y = mouse_pos[1] - self.drag_offset[1]

    # TODO: make mos handle destroying windows
    def destroy(self):
        mos_app.remove_window(self)
        if self.zlayer and self in self.zlayer:
            self.zlayer.remove(self)

    @staticmethod
    def _collide_in_cy(x, y, radius, x1, y1):
        return ((x1 - x) ** 2 + (y1 - y) ** 2)**0.5 <= radius

    def _draw_text(self, txt, font: pygame.font.Font, col, x, y):
        img = font.render(txt, True, col)
        self.parent.blit(img,(x,y))

    @abstractmethod
    def draw_content(self):
        raise NotImplementedError("draw_content must be implemented by child classes")

    @abstractmethod
    def handle_custom_input(self, event):
        raise NotImplementedError("handle_custom_input must be implemented by child classes")