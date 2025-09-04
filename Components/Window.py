import pygame

"""
TODO: read fooColor from a global ENUM to get rid of "magic numbers"
example usage: 
    Color.SYSCOLOR -> (200, 200, 200)
"""
class Window:
    def __init__(self, titel, width, height, Logo=None, syscolor=(192, 199, 200), window_select_color=(0, 0, 168), menuf = None, textcolor=(0, 0, 0), zlayer=None, screen=None):
        # layering from the parent but could also be inside of the window itself because of rendering other windows or elements
        if zlayer is None:
            self.zlayer = []
        else:
            self.zlayer = zlayer
        self.width = width
        self.height = height
        if screen is None:
            self.screen = pygame.Surface((self.width- 10,self.height- 45))
        else:
            self.screen = screen
        self.titel = titel
        self.x = self.screen.get_width()  // 2 - width  // 2
        self.y = self.screen.get_height() // 2 - height // 2
        self.logo = Logo
        self.func = None
        self.drawer = None
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

    def add_input_handler(self,func):
        self.handler = func

    def add_screen_drawer(self, name_func):
        self.drawer = name_func

    def run(self):
        while True:
            self.draw(self.lastframe)

    def draw(self,screen: pygame.Surface, syscolocr=None) -> int:
        pygame.draw.rect(  self.screen, (0,0,0), pygame.Rect(self.x-1,self.y-1,self.width+2,self.height+2))
        pygame.draw.rect(  self.screen, self.syscolor, pygame.Rect(self.x,self.y,self.width,self.height))
        pygame.draw.rect(  self.screen, self.window_select_color, pygame.Rect(self.x + 5,self.y+5 ,self.width- 10,30))
        pygame.draw.rect(  self.screen, (255,255,255), pygame.Rect(self.x + 5,self.y+40 ,self.width- 10,self.height- 45))
        if self.drawer:
            self.drawer(0,self.screen)
            self.screen.blit(self.screen,(self.x + 5,self.y+40))
        pygame.draw.circle(screen,(255,0,0), (self.x + 15 , self.y+ 17.5),10)
        pygame.draw.circle(screen,(0,255,0), (self.x + 40 , self.y+ 17.5),10)
        pygame.draw.circle(screen,(0,0,255), (self.x + 65 , self.y+ 17.5),10)
        self._draw_text(self.titel, self.menuf, self.textcolor, self.x + 100, self.y + 7.5)
        return 0

    def in_window(self,x,y):
        return pygame.Rect(self.x,self.y,self.width,self.height).collidepoint(x,y)

    def update_x_y(self,rel, mousepos):
        if pygame.Rect(self.x + rel[0],self.y + rel[1],self.width,70).collidepoint(mousepos):
            self.x = self.x + rel[0]
            if self.x < 0:
                self.x = 0
            if self.x + self.width > self.screen.get_width():
                self.x = self.screen.get_width() - self.width
            self.y = self.y + rel[1]
            if self.y < 0:
                self.y = 0
            return True
        return False

    def handel_input(self, type : str, dat):
        global data, wdata
        if type == "m":
            if pygame.Rect(self.x + 5,self.y+30 ,self.width- 10,self.height- 35).collidepoint(dat[0], dat[1]):
                if self.func:
                    self.func(type,dat)
            elif pygame.Rect(self.x,self.y,self.width,30).collidepoint(dat[0], dat[1]):
                if self._collide_in_cy(self.x + 15 , self.y + 15, 10, dat[0], dat[1]):
                    self.zlayer.remove(self)
                self.offsetx = (self.x - dat[0])
                self.offsety = (self.y - dat[1])

    @staticmethod
    def _collide_in_cy(x, y, radius, x1, y1):
        return ((x1 - x) ** 2 + (y1 - y) ** 2)**0.5 <= radius

    def _draw_text(self, txt, font: pygame.font.Font, col, x, y):
        img = font.render(txt, True, col)
        self.screen.blit(img,(x,y))