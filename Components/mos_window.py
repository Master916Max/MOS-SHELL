import pygame

"""
TODO: read fooColor from a global ENUM to get rid of "magic numbers"
example usage: 
    Color.SYSCOLOR -> (200, 200, 200)
"""
class MosWindow(object):
    def __init__(self, title, width, height, Logo=None, syscolor=(192, 199, 200), window_select_color=(0, 0, 168),
                 menuf=None, textcolor=(0, 0, 0), zlayer=None, parent=None, drawer=None, type_id=None):
        # layering from the parent but could also be inside of the window itself because of rendering other windows or elements
        self.zlayer = zlayer if zlayer is not None else []
        self.width = width
        self.height = height
        self.parent = parent if parent is not None else pygame.Surface((self.width- 10,self.height- 45))
        self.title = title
        self.x = self.parent.get_width()  // 2 - width  // 2
        self.y = self.parent.get_height() // 2 - height // 2
        self.logo = Logo
        self.func = None
        self.drawer = drawer if drawer is not None else None
        self.lastframe = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        self.syscolor = syscolor
        self.window_select_color = window_select_color
        if menuf is None:
            pygame.font.init()
            self.menuf = pygame.font.Font(None, 24)
        else:
            self.menuf = menuf
        self.textcolor = textcolor
        self.handler = None
        self.surface = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        self.id: str = f"{self.title}_{id(self)}"
        self.type_id = type_id
        self.dragging = False
        self.drag_offset = (0, 0)
        self.title_height = 30
        self.close_btn_rect = pygame.Rect(width - 30, 0, 30, self.title_height)

    def add_input_handler(self,func):
        self.handler = func

    def add_screen_drawer(self, name_func):
        self.drawer = name_func

    def run(self):
        while True:
            self.draw(self.lastframe)

    def draw(self,screen: pygame.Surface):
        # Draw window background
        self.surface.fill((240, 240, 240))
        # Draw title text
        font = pygame.font.Font(None, 24)
        title_text = font.render(self.title, True, (0, 0, 0))
        self.surface.blit(title_text, (5, 5))

        # TODO: extract this into a subclass of MosWindow smth like MosTerminal
        if self.type_id == 'TERMINAL':
            font = pygame.font.Font(None, 50)
            data_text = font.render(f"{self.x, self.y}", True, (0, 0, 0))
            data1_text = font.render(f"{self.dragging}", True, (0, 0, 0))
            title_bar_height = title_text.get_height()
            self.surface.blit(data_text, (10,  title_text.get_height() + title_text.get_height()+5 if title_text is not None else data_text.get_height() + 5))
            self.surface.blit(data1_text, (10, data_text.get_height() + title_bar_height + data1_text.get_height()))
            #self.surface.blit(wdata_text, (10, data_text.get_height() + 5 + data1_text.get_height() + 5))

        # Draw title bar
        pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.width, self.title_height))
        # Draw buttons
        pygame.draw.rect(self.surface,(255,0,0), self.close_btn_rect)
        #pygame.draw.rect(self.surface,(0,255,0), self.close_btn_rect)
        #pygame.draw.rect(self.surface,(0,0,255), self.close_btn_rect)
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            relative_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)

            # Check for close button click
            if self.close_btn_rect.collidepoint(relative_pos):
                return False

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
        return True

    @staticmethod
    def _collide_in_cy(x, y, radius, x1, y1):
        return ((x1 - x) ** 2 + (y1 - y) ** 2)**0.5 <= radius

    def _draw_text(self, txt, font: pygame.font.Font, col, x, y):
        img = font.render(txt, True, col)
        self.parent.blit(img,(x,y))