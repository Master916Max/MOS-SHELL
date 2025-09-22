import pygame, random, json
from time import strftime

from Components.mos_terminal import MosTerminal
from Components.mos_window import MosWindow
from Modules import *
from chore.mos import mos_app
from chore.window_helper import WindowHelper

#
# GUI Services
#
from Theme.Service import ThemeService

#
# Init Services
#
Theme_Service = ThemeService()


pygame.init()
MSG_Box = object
#Input Variabeln
mousbuttondown = False
mouspos = None
lastmousepos = (0,0)
mouserel = (0,0)

basi_json = """{
    "GUI":{
        "BG": [87, 168, 168],
        "TBC": [30, 61, 88],
        "window_select_color": [0, 0, 168],
        "syscolor": [192, 199, 200],
        "textcolor": [0,0,0],
        "msgtextcolor": [0, 0, 0],
        "noneselectcolor": [100, 100, 100]
    },
    "SYS":{
        "First":true
    }

}"""

datal: any

def load_settings():
    global datal
    #try:
    #    with open("Settings.json", "r") as f:
    #        datal = json.load(f)
    #except Exception as e:
    #    print(e)
    datal = json.loads(basi_json)
    gui : dict =  Theme_Service.get_manager().get_theme("Solarized Dark")
    print(gui)
    if gui:
        datal["GUI"] = gui
        

load_settings()

# System Variabeln
syscolor = datal["GUI"]["syscolor"]
BG = datal["GUI"]["BG"]
TBC = datal["GUI"]["TBC"]
noneselectcolor =  datal["GUI"]["noneselectcolor"]
textcolor =  datal["GUI"]["textcolor"]
msgtextcolor =  datal["GUI"]["msgtextcolor"]
window_select_color =  datal["GUI"]["window_select_color"]

#Desktop Variabeln
dt_item_size = 64
dt_font = pygame.font.Font(None, 24)
dt_items = ["My PC","System-Settings","Test.txt"]
dt_offset = 20

#Other Variabeln
test_build = True
build_id = "0001"
version = "V-1.0.0"
text_button : ButtonField
textinput  : InputField
display : pygame.Surface
error, errormsg = False , ""
data = "N\\A"
wdata = ""
tb_offset = 0
selected_window = False
cd = 100
sss = False
zlayer = []
#build_str : str = ""


#Secure Screen Variabeln
secure_screen : pygame.Surface
Secure_Screen_Handle : any = None

#Menu Variabeln
menuf = pygame.font.Font(None,45)
Menu_Text = menuf.render(f"MOS-{version}", True, textcolor)

Menu_Height = Menu_Text.get_height() * 8 + 50
Menu_Width = Menu_Text.get_width() + 50

build_str = menuf.render(f"Build {build_id}", True, textcolor)

apps = {"Ordner": "Games",
        "App"   : "Emails",
        "App"   : "Brave"} 

root : pygame.Surface

def init():
    # TODO: do only use globals for constants
    global secure_screen, text_button, textinput,root, menuf,build_id, test_build, build_str
    build_id = version
    test_build = True
    build_str = menuf.render(f"Build {build_id}", True, textcolor)
    root = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("MOS-Py-GUI")
    secure_screen = pygame.Surface((root.get_width(), root.get_height()), pygame.SRCALPHA)
    text_button  = ButtonField("Test", root, 250, 50, 150, 50, fgcolor=textcolor, bgcolor=syscolor)
    textinput = InputField(root, 50, 50, 150, 50, fgcolor=textcolor, bgcolor=syscolor, txtfont=menuf)
    return root

screen = init()

class MsgBox:
    def __init__(self,title, ContentL1,ContentL2,Buttons, Type, root = None, Logo = None):
        self.title = title
        self.line1 = ContentL1
        self.line2 = ContentL2
        self.calc_dims()
        self.Buttons = Buttons
        self.Type = Type
        if root is None:
            raise Exception("No Root Surface given")
        self.x = root.get_width()  // 2 - self.width  // 2
        self.y = root.get_height() // 2 - self.height // 2
        if root:
            self.screen = root
        else: self.screen = screen
        self.logo = Logo
        if Type == 1:
            self.ok = ButtonField("OK", self.screen, self.x + self.width // 2 - 75, self.y + self.height , 150, 50, fgcolor=textcolor, bgcolor=syscolor)
            self.height += 50

    def calc_dims(self):
        img = menuf.render(self.line1, True, textcolor)
        line2 = menuf.render(self.line2, True, textcolor)
        title = menuf.render(self.title,True,textcolor)
        if img.get_width() + 60 > line2.get_width() + 60:
            self.width = img.get_width() + 80
        else:
            self.width = line2.get_width() + 80
        if title.get_width() + 90 > self.width:
            self.width = title.get_width() + 90
        self.height = img.get_height() + 40 + 10 + line2.get_height()
        self.line1_height = img.get_height()

    def update_x_y(self,rel, mousepos):
        if pygame.Rect(self.x + rel[0],self.y + rel[1],self.width,70).collidepoint(mousepos):
            self.x = self.x + rel[0]
            if self.x < 0:
                self.x = 0
            if self.x + self.width > screen.get_width():
                self.x = screen.get_width() - self.width
            self.y = self.y + rel[1]
            if self.y < 0:
                self.y = 0
            return True
        return False

    def in_window(self,x,y):
        return pygame.Rect(self.x,self.y,self.width,self.height).collidepoint(x,y)
    
    def handel_input(self, type : str, dat):
        global data, wdata
        if type == "m":
            if pygame.Rect(self.x + 5,self.y+30 ,self.width- 10,self.height- 35).collidepoint(dat[0], dat[1]): pass
                #if self.func:
                    #self.func(type,dat)
            elif pygame.Rect(self.x,self.y,self.width,30).collidepoint(dat[0], dat[1]):
                if _colide_in_cy(self.x + 15 , self.y+ 15, 10, dat[0], dat[1]):
                    zlayer.remove(self)
                self.offsetx = (self.x - dat[0])
                self.offsety = (self.y - dat[1])
        
    def draw(self, sreen: pygame.Surface = None):
        # if ms.index(self) != selected_window:
        #     pygame.draw.rect(self.screen, (175,175,175), pygame.Rect(self.x,self.y,self.width,self.height))
        # else:
        pygame.draw.rect(  self.screen, (0,0,0), pygame.Rect(self.x-1,self.y-1,self.width+2,self.height+2))        
        pygame.draw.rect(  self.screen, syscolor, pygame.Rect(self.x,self.y,self.width,self.height))
        pygame.draw.rect(  self.screen, (255,255,255), pygame.Rect(self.x + 5,self.y+30 ,self.width- 10,self.height- 35))
        pygame.draw.circle(screen,(255,0,0), (self.x + 15 , self.y+ 15),10)
        #pygame.draw.circle(screen,(0,255,0), (self.x + 40 , self.y+ 15),10)
       # pygame.draw.circle(screen,(0,0,255), (self.x + 65 , self.y+ 15),10)
        _draw_text(self.title, menuf, textcolor, self.x + 30, self.y + 2.5)
        if self.Type == 1:
            pygame.draw.circle(screen, (0,0,255),    (self.x + 40,self.y +(self.line1_height)//2 + 50), 25)
            pygame.draw.circle(screen, (255,255,255),(self.x + 40,self.y +(self.line1_height)//2 + 50), 22)
            pygame.draw.circle(screen, (0,0,255),    (self.x + 40,self.y +(self.line1_height)//2 + 50), 20)
            pygame.draw.circle(screen, (255,255,255),(self.x + 40,self.y +(self.line1_height)//2 + 60), 3)
            pygame.draw.line(  screen, (255,255,255),(self.x + 39,self.y +(self.line1_height)//2 + 37),(self.x + 39,self.y +(self.line1_height)//2 + 52), 4)
        _draw_text(self.line1, menuf, msgtextcolor, self.x + 75, self.y + 35)
        _draw_text(self.line2, menuf, msgtextcolor, self.x + 75, self.y + 35 + self.line1_height + 5)
        self.ok.draw(x=self.x + self.width // 2 - 75, y=self.y + self.height - 60)
        return 0

def create_msg_box(titel, content_l1, content_l2, buttons, type, root = None):
    msg = MsgBox(titel, content_l1, content_l2, buttons, type, root)
    zlayer.insert(0,msg)
    return 0 , msg

def draw_shutdown_text(sceen: pygame.Surface):
    img = menuf.render("Shuting Down", True, (255,255,255))
    sceen.blit(img,(sceen.get_width()//2 - img.get_width()//2, sceen.get_height()//2 - img.get_height()//2))

def run():
    global selected_window, data, mousbuttondown, mouspos, lastmousepos, mouserel, sss, cd, Secure_Screen_Handle, BG, TBC, textinput
    #TaskBar List Background Color

    running = True
    menu_opend = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousbuttondown = True
                if pygame.Rect(10,screen.get_height()- 40, 30,30).collidepoint(event.pos[0],event.pos[1]):
                    menu_opend = not menu_opend
                elif pygame.Rect(0, screen.get_height()- (Menu_Height + 50), Menu_Width,Menu_Height).collidepoint(event.pos[0],event.pos[1]) and menu_opend:
                    menu_opend = True
                    hit =  _hit_list(("New-Window","Terminal","System"), menuf, (((213,189,175),textcolor),((250,237,205),textcolor),((212,163,115),textcolor)),10, screen.get_height() - (Menu_Height + 40) + Menu_Text.get_height() + 10, 5, event.pos)
                    if hit == "New-Window":
                        w = random.randint(200,500)
                        # TODO: do not pass in zlayer because the window should not have any idea where its getting handled in terms of layering
                        # we need something like an event listener in gui that can handle child events like window.close and do the necessary stuff
                        # like removing the window from zlayer etc
                        window_config = {
                            'title': f"New Window",
                            'logo': None,
                            'width': w,
                            'height': w,
                            'parent': screen,
                            'zlayer': zlayer,
                        }
                        new_window = WindowHelper.init_window(window_config)
                        zlayer.insert(0,new_window)
                    elif hit == "Terminal":
                        w = random.randint(200,500)
                        window_config = {
                            'title': f"New Terminal",
                            'logo': None,
                            'width': w,
                            'height': w,
                            'parent': screen,
                            'zlayer': zlayer,
                            'type_id': 'TERMINAL'
                        }
                        new_window = WindowHelper.init_window(window_config)
                        #new_window = MosWindow(f"New Terminal", w,w, None, parent=screen, zlayer=zlayer, type_id='TERMINAL')
                        zlayer.insert(0,new_window)
                    elif hit == "System":
                        print("Showing System Apps")
                    if pygame.Rect(25, screen.get_height()- (Menu_Height - Menu_Text.get_height() * 6), Menu_Width - 50,Menu_Text.get_height()).collidepoint(event.pos[0],event.pos[1]):
                        sss = True
                        cd -= 1
                elif text_button.mouse_down(event.pos):
                    continue     
                else:
                    menu_opend = False
                    inwin = False
                    for window in zlayer:
                        if window.in_window(event.pos[0],event.pos[1]) and not inwin:
                            mos_app.set_active(window)
                            inwin = True
                            zlayer.remove(window)
                            zlayer.insert(0,window)
                            selected_window = True
                    if not inwin:
                        selected_window = False
                    if len(zlayer) >= 1 and selected_window:
                        if type(zlayer[0]) == MosWindow or type(zlayer[0]) == MosTerminal:
                            zlayer[0].handle_input(event)
                        else: zlayer[0].handel_input("m", (event.pos[0], event.pos[1]))
            elif event.type == pygame.MOUSEMOTION:
                if mousbuttondown:
                    if len(zlayer) != 0 and len(zlayer) >= 0 + 1:
                        if not zlayer[0].update_x_y(event.rel, event.pos):
                            selected_window = False
                data = event.pos
                mouspos = event.pos
                mouserel = event.rel
            elif event.type == pygame.MOUSEBUTTONUP:
                if text_button.mouse_up(event.pos):
                    pass
                mousbuttondown = False
            elif event.type == pygame.KEYDOWN:
                try:
                    zlayer[0].handel_input(event)
                except Exception as e:
                    zlayer[0].handle_input(event)

        # Bildschirm aktualisieren
        if not error and not sss:
            screen.fill(BG)
            _draw_desktop()
            _draw_content()

            pygame.draw.rect(screen, (30, 61, 88, 125), pygame.Rect(0, screen.get_height()- 50, screen.get_width(), 50))
            logo = pygame.Surface((30,30), pygame.SRCALPHA)
            pygame.draw.rect(screen, (TBC[0] * 1.2,TBC[1] * 1.2,TBC[2]*1.2), pygame.Rect(5,screen.get_height()- 45, 40,40) )
            pygame.draw.rect(logo, (255,0,0), (0,0, 15,15))
            pygame.draw.rect(logo, (255,255,0), (15,0, 15,15))
            pygame.draw.rect(logo, (0,0,255), (0,15, 15,15))
            pygame.draw.rect(logo, (0,255,255), (15,15, 15,15))
            d_logo = pygame.transform.rotate(logo,45)
            screen.blit(d_logo,(5,screen.get_height()- 45))

            #_draw_task_bar()
            _handle_task_bar()

            #_draw_list(("New-Window","Apps","System"), menuf, (((213,189,175),textcolor),((250,237,205),textcolor),((212,163,115),textcolor)),500, 500, 5)

            clock_txt = menuf.render(strftime("%H:%M:%S"),True,(255,255,255))

            pygame.draw.rect(screen, TBC, pygame.Rect(screen.get_width()- clock_txt.get_width() - 20, screen.get_height()- 50, clock_txt.get_width()+20, 50))
            pygame.draw.rect(screen, (20, 41, 68), pygame.Rect(screen.get_width()- clock_txt.get_width() - 20, screen.get_height()- 50, 5, 50))
            screen.blit(clock_txt, (screen.get_width()- clock_txt.get_width() -10, screen.get_height()- (50 - clock_txt.get_height()//2)))
            screen.blit(build_str, (screen.get_width()- build_str.get_width() - 10, screen.get_height()- 60-(build_str.get_height()//2)))

            if menu_opend:
                _draw_menu()
        if not error and sss:
            cd -= 1
            Secure_Screen_Handle = draw_shutdown_text
            SecureScreen()
            if cd == 0:
                running = False
        if error:
            screen.fill((58,58,255))
            _draw_text(errormsg, menuf, (235, 235, 255), 50, 50)
        
        root.blit(screen, (0, 0))

        pygame.display.flip()

    pygame.quit()


# Need to Export
def _draw_menu():

    pygame.draw.rect(screen, syscolor,pygame.Rect(0,screen.get_height() - (Menu_Height + 50), Menu_Width,Menu_Height))

    pygame.draw.rect(screen, (175,0,0), pygame.Rect(25, screen.get_height() - (Menu_Height - Menu_Text.get_height() * 6), Menu_Width - 50, Menu_Text.get_height()))
    #pygame.draw.rect(screen, (175,175,0), pygame.Rect(15, screen.get_height() - (Menu_Height - Menu_Text.get_height() * 1), Menu_Width - 25, Menu_Text.get_height()))
    
    _draw_list(("New-Window","Terminal","System"), menuf, (((213,189,175),textcolor),((250,237,205),textcolor),((212,163,115),textcolor)),10, screen.get_height() - (Menu_Height + 40) + Menu_Text.get_height() + 10, 5)

    _draw_text("Shutdown", menuf, (255, 255, 255), 30, screen.get_height() - (Menu_Height - Menu_Text.get_height() * 6 - 2.5), )
    screen.blit(Menu_Text, (25,screen.get_height()- (Menu_Height + 25)))

def _draw_list(items: tuple[str],font: pygame.font.Font,colors: tuple[tuple],x: int,y: int, offset:int, background = (125, 125, 125)):
    longestx = 0
    height = 0
    for item in items: 
        text = font.render(item,True,colors[items.index(item)][1])
        height += text.get_height()
        if longestx < text.get_width():
            longestx = text.get_width()
    pygame.draw.rect(screen, background,pygame.Rect(x, y, longestx + 20, height + offset * (len(items) + 1)))
    for item in items:
        text = font.render(item,True,colors[items.index(item)][1])
        xoff = (text.get_height() + offset)* items.index(item) + offset
        pygame.draw.rect(screen, colors[items.index(item)][0],pygame.Rect(x+10, y + xoff, longestx, text.get_height()))
        screen.blit(text, ((x + 10 + (longestx // 2 - text.get_width()//2)), y + xoff))

def _draw_text(txt, font: pygame.font.Font, col, x, y):
    img = font.render(txt, True, col)
    screen.blit(img,(x,y))

def _draw_content():
    zlayer.reverse()
    for window in mos_app.open_windows:
        window.draw(screen)
    #for window in zlayer:
    #    window.draw(screen)
    zlayer.reverse()

def _handle_task_bar():

    global tb_offset
    tb_offset = 0
    ooo = 0
    for window in mos_app.open_windows:
        if mos_app.active == window:
            u_txt = menuf.render(f"{zlayer[0].title}", True, (255, 255, 255))
            pygame.draw.rect(screen, (58,58,255), pygame.Rect(50+ 40*tb_offset + ooo,screen.get_height()- 40, 30,30))
            pygame.draw.rect(screen, (60, 91, 118), pygame.Rect(50+ 40*(tb_offset + 1) - 5 , screen.get_height()- (55 - u_txt.get_height()//2),u_txt.get_width(), 30))
            screen.blit(u_txt, (50+ 40*(tb_offset + 1) - 5 , screen.get_height()- (55 - u_txt.get_height()//2)))
            ooo = u_txt.get_width() + 10
        else:
            pygame.draw.rect(screen, window.logo or syscolor, pygame.Rect(50+ 40*tb_offset + ooo,screen.get_height()- 40, 30,30))


        tb_offset +=1

def _draw_task_bar():
    global tb_offset
    tb_offset = 0
    ooo = 0
    if len(zlayer) != 0 and len(zlayer) >= 1 and selected_window:
        u_txt = menuf.render(f"{zlayer[0].title}", True, (255, 255, 255))

            
    for window in mos_app.open_windows:
        if selected_window and zlayer.index(window)== 0:
            if window.logo and type(window.logo) == pygame.Surface:
                screen.blit(window.logo,(50+ 40*tb_offset + ooo,screen.get_height()- 40))
            else:
                pygame.draw.rect(screen, (58,58,255), pygame.Rect(50+ 40*tb_offset + ooo,screen.get_height()- 40, 30,30))
            pygame.draw.rect(screen, (60, 91, 118), pygame.Rect(50+ 40*(tb_offset + 1) - 5 , screen.get_height()- (55 - u_txt.get_height()//2),u_txt.get_width(), 30))
            screen.blit(u_txt, (50+ 40*(tb_offset + 1) - 5 , screen.get_height()- (55 - u_txt.get_height()//2)))
            ooo = u_txt.get_width() + 10
        else:
            pygame.draw.rect(screen, window.logo or syscolor, pygame.Rect(50+ 40*tb_offset + ooo,screen.get_height()- 40, 30,30))
            
                
        tb_offset +=1

def _draw_desktop():
    global dt_items, dt_item_size, dt_offset, dt_font, textcolor, text_button, textinput
    for item in dt_items:
        if not item.isspace():
            titel = dt_font.render(item,True,textcolor)
            ly = (dt_items.index(item)+1) * dt_item_size + dt_offset * (dt_items.index(item)+1) + dt_items.index(item) *titel.get_height()
            ry = (dt_items.index(item)+1) * dt_item_size + dt_offset * (dt_items.index(item)+2) + dt_items.index(item) *titel.get_height() - titel.get_height()
            pygame.draw.rect(screen, syscolor,(5+ (dt_item_size-5)//2, ry - dt_item_size, dt_item_size-5,dt_item_size-5))
            #print((dt_item_size //2 - titel.get_width()//2,ly))
            screen.blit(titel,(dt_item_size - titel.get_width()//2,ly))
    text_button.draw()
    textinput.draw()

def _hit_list(items: tuple[str],font: pygame.font.Font,colors: tuple[tuple],x: int,y: int, offset:int,mousepos, background = (125, 125, 125)):
    longestx = 0
    height = 0
    hit = None
    for item in items: 
        text = font.render(item,True,colors[items.index(item)][1])
        height += text.get_height()
        if longestx < text.get_width():
            longestx = text.get_width()
    pygame.draw.rect(screen, background,pygame.Rect(x, y, longestx + 20, height + offset * (len(items) + 1)))
    for idx,item in enumerate(items):
        text = font.render(item,True,colors[items.index(item)][1])
        xoff = (text.get_height() + offset)* items.index(item) + offset
        if pygame.Rect(x+10, y + xoff, longestx, text.get_height()).collidepoint(mousepos[0], mousepos[1])	:
            hit = item
    return hit 

#Buttons
def _colide_in_cy(x,y,radius,x1,y1):
    return (((x1 - x)**2+(y1-y)**2)**0.5 <= radius)



# Secure Screen
def SecureScreen():
    global secure_screen, screen, BG, TBC, Secure_Screen_Handle
    screen.fill(BG)
    pygame.draw.rect(screen, TBC, pygame.Rect(0, screen.get_height()- 50, screen.get_width(), 50))
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(10,screen.get_height()- 40, 30,30) )
    clock_txt = menuf.render(strftime("%H:%M:%S"),True,(255,255,255))

    pygame.draw.rect(screen, TBC, pygame.Rect(screen.get_width()- clock_txt.get_width() - 20, screen.get_height()- 50, clock_txt.get_width()+20, 50))
    pygame.draw.rect(screen, (20, 41, 68), pygame.Rect(screen.get_width()- clock_txt.get_width() - 20, screen.get_height()- 50, 5, 50))
    screen.blit(clock_txt, (screen.get_width()- clock_txt.get_width() -10, screen.get_height()- (50 - clock_txt.get_height()//2)))

    #BG /\ FG\/
    pygame.draw.rect(secure_screen, (0, 0, 0, 125), (0, 0, screen.get_width(), screen.get_height()))
    if Secure_Screen_Handle:
        sceen = pygame.Surface((screen.get_width(),screen.get_height()), pygame.SRCALPHA)
        sceen.fill((0,0,0,0))
        Secure_Screen_Handle(sceen)
        secure_screen.blit(sceen, (0, 0))
    screen.blit(secure_screen, (0, 0))
