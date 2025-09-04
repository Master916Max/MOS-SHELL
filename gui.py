from pydoc import text
import pygame
import random
import json
from time import strftime, sleep
import threading
import os
import sys

from Components.Window import Window
#from Modules import Input,Button
from Modules import *

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
    try:
        with open("Settings.json", "r") as f:
            datal = json.load(f)
    except Exception as e:
        print(e)
        datal = json.loads(basi_json)   

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
textbutton : ButtonField
textinput  : InputField
screen : pygame.Surface
lscreen : pygame.Surface
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
Secure_Screen : pygame.Surface
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

def _init_d(version: str):
    global build_id, test_build, build_str, menuf,textcolor
    build_id = version
    test_build = True
    build_str = menuf.render(f"Build {build_id}", True, textcolor)
    init()

def init():
    global screen, Secure_Screen, textbutton, lscreen, textinput, menuf
    lscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.Surface((lscreen.get_width(), lscreen.get_height()), pygame.SRCALPHA)
    pygame.display.set_caption("MOS-Py-GUI")
    Secure_Screen = pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
    textbutton  = ButtonField("Test", screen, 250,50, 150,50,fgcolor=textcolor, bgcolor=syscolor)
    textinput = InputField(screen, 50, 50, 150, 50, fgcolor=textcolor, bgcolor=syscolor, txtfont=menuf)
    return screen


class MSG_Box:
    def __init__(self,Titel, ContentL1,ContentL2,Buttons, Type, root = None, Logo = None):
        self.titel = Titel
        self.line1 = ContentL1
        self.line2 = ContentL2
        self.calc_dims()
        self.Buttons = Buttons
        self.Type = Type
        self.x = screen.get_width()  // 2 - self.width  // 2
        self.y = screen.get_height() // 2 - self.height // 2
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
        titel = menuf.render(self.titel,True,textcolor)
        if img.get_width() + 60 > line2.get_width() + 60:
            self.width = img.get_width() + 80
        else:
            self.width = line2.get_width() + 80
        if titel.get_width() + 90 > self.width:
            self.width = titel.get_width() + 90
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
        _draw_Text(self.titel, menuf, textcolor, self.x + 30, self.y + 2.5)
        if self.Type == 1:
            pygame.draw.circle(screen, (0,0,255),    (self.x + 40,self.y +(self.line1_height)//2 + 50), 25)
            pygame.draw.circle(screen, (255,255,255),(self.x + 40,self.y +(self.line1_height)//2 + 50), 22)
            pygame.draw.circle(screen, (0,0,255),    (self.x + 40,self.y +(self.line1_height)//2 + 50), 20)
            pygame.draw.circle(screen, (255,255,255),(self.x + 40,self.y +(self.line1_height)//2 + 60), 3)
            pygame.draw.line(  screen, (255,255,255),(self.x + 39,self.y +(self.line1_height)//2 + 37),(self.x + 39,self.y +(self.line1_height)//2 + 52), 4)
        _draw_Text(self.line1, menuf, msgtextcolor, self.x + 75, self.y + 35)
        _draw_Text(self.line2, menuf, msgtextcolor, self.x + 75, self.y + 35 + self.line1_height + 5)
        self.ok.draw(x=self.x + self.width // 2 - 75, y=self.y + self.height - 60)
        return 0

def Create_MSG_Box(Titel, ContentL1,ContentL2,Buttons, Type, root = None):
    msg = MSG_Box(Titel, ContentL1,ContentL2,Buttons, Type, root)
    zlayer.insert(0,msg)
    return 0 , msg

def Draw_Shutdown_Text(sceen: pygame.Surface):
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
                    hit =  _hit_list(("New-Window","Apps","System"), menuf, (((213,189,175),textcolor),((250,237,205),textcolor),((212,163,115),textcolor)),10, screen.get_height() - (Menu_Height + 40) + Menu_Text.get_height() + 10, 5, event.pos)
                    if hit == "New-Window":
                        w = random.randint(200,500)
                        # TODO: do not pass in zlayer because the window should not have any idea where its getting handled in terms of layering
                        # we need something like an event listener in gui that can handle child events like window.close and do the necessary stuff
                        # like removing the window from zlayer etc
                        new_window = Window(f"New Window", w,w, None, screen=screen, zlayer=zlayer)
                        zlayer.insert(0,new_window)
                    elif hit == "Apps":
                        print("Showing Apps")
                    elif hit == "System":
                        print("Showing System Apps")
                    if pygame.Rect(25, screen.get_height()- (Menu_Height - Menu_Text.get_height() * 6), Menu_Width - 50,Menu_Text.get_height()).collidepoint(event.pos[0],event.pos[1]):
                        sss = True
                        cd -= 1
                elif textbutton.mouse_down(event.pos):
                    continue     
                else:
                    menu_opend = False
                    inwin = False
                    for window in zlayer:
                        if window.in_window(event.pos[0],event.pos[1]) and not inwin:
                            inwin = True
                            zlayer.remove(window)
                            zlayer.insert(0,window)
                            selected_window = True
                    if not inwin:
                        selected_window = False
                    if len(zlayer) != 0 and len(zlayer) >= 0 + 1 and selected_window:
                        zlayer[0].handel_input("m",(event.pos[0],event.pos[1]))
            elif event.type == pygame.MOUSEMOTION:
                if mousbuttondown:
                    if len(zlayer) != 0 and len(zlayer) >= 0 + 1:
                        if not zlayer[0].update_x_y(event.rel, event.pos):
                            selected_window = False
                data = event.pos
                mouspos = event.pos
                mouserel = event.rel
            elif event.type == pygame.MOUSEBUTTONUP:
                if textbutton.mouse_up(event.pos):
                    pass
                mousbuttondown = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    if menu_opend:
                        menu_opend = False
                elif event.key == pygame.K_RETURN:
                    textinput.input += "\n"
                else:
                    if selected_window and len(zlayer) != 0 and len(zlayer) >= 0 + 1:
                        if zlayer[0].handler:
                            zlayer[0].handler(event.key, event.unicode)
                        else:
                            if event.unicode.isprintable():
                                zlayer[0].screen.blit(menuf.render(event.unicode, True, textcolor), (10, 10))
                            else:
                                print(f"Key {event.key} pressed but no handler defined.")
                    else:
                        textinput.handle(event)
        # Bildschirm aktualisieren
        if not error and not sss:

            screen.fill(BG)
            _draw_Desktop()
            _draw_Content()

            pygame.draw.rect(screen, (30, 61, 88, 125), pygame.Rect(0, screen.get_height()- 50, screen.get_width(), 50))
            logo = pygame.Surface((30,30), pygame.SRCALPHA)
            pygame.draw.rect(screen, (TBC[0] * 1.2,TBC[1] * 1.2,TBC[2]*1.2), pygame.Rect(5,screen.get_height()- 45, 40,40) )
            pygame.draw.rect(logo, (255,0,0), (0,0, 15,15))
            pygame.draw.rect(logo, (255,255,0), (15,0, 15,15))
            pygame.draw.rect(logo, (0,0,255), (0,15, 15,15))
            pygame.draw.rect(logo, (0,255,255), (15,15, 15,15))
            d_logo = pygame.transform.rotate(logo,45)
            screen.blit(d_logo,(5,screen.get_height()- 45))

            _draw_TaskBar()

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
            Secure_Screen_Handle = Draw_Shutdown_Text
            SecureScreen()
            if cd == 0:
                running = False
        if error:
            screen.fill((58,58,255))
            _draw_Text(errormsg,menuf,(235,235,255),50,50)
        
        lscreen.blit(screen,(0,0))

        pygame.display.flip()

    pygame.quit()


# Need to Export
def _draw_menu():

    pygame.draw.rect(screen, syscolor,pygame.Rect(0,screen.get_height() - (Menu_Height + 50), Menu_Width,Menu_Height))

    pygame.draw.rect(screen, (175,0,0), pygame.Rect(25, screen.get_height() - (Menu_Height - Menu_Text.get_height() * 6), Menu_Width - 50, Menu_Text.get_height()))
    #pygame.draw.rect(screen, (175,175,0), pygame.Rect(15, screen.get_height() - (Menu_Height - Menu_Text.get_height() * 1), Menu_Width - 25, Menu_Text.get_height()))
    
    _draw_list(("New-Window","Apps","System"), menuf, (((213,189,175),textcolor),((250,237,205),textcolor),((212,163,115),textcolor)),10, screen.get_height() - (Menu_Height + 40) + Menu_Text.get_height() + 10, 5)

    _draw_Text("Shutdown", menuf, (255,255,255), 30, screen.get_height() - (Menu_Height - Menu_Text.get_height() * 6 - 2.5),)
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

def _draw_Text(txt, font: pygame.font.Font, col, x, y):
    img = font.render(txt, True, col)
    screen.blit(img,(x,y))

def _draw_Content():
    zlayer.reverse()
    for window in zlayer:
        window.draw(screen)
    zlayer.reverse()

def _draw_TaskBar():
    global tb_offset
    tb_offset = 0
    ooo = 0
    if len(zlayer) != 0 and len(zlayer) >= 1 and selected_window:
        u_txt = menuf.render(f"{zlayer[0].titel}",True,(255,255,255))

            
    for window in zlayer:
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

def _draw_Desktop():
    global dt_items, dt_item_size, dt_offset, dt_font, textcolor, textbutton, textinput
    for item in dt_items:
        if not item.isspace():
            titel = dt_font.render(item,True,textcolor)
            ly = (dt_items.index(item)+1) * dt_item_size + dt_offset * (dt_items.index(item)+1) + dt_items.index(item) *titel.get_height()
            ry = (dt_items.index(item)+1) * dt_item_size + dt_offset * (dt_items.index(item)+2) + dt_items.index(item) *titel.get_height() - titel.get_height()
            pygame.draw.rect(screen, syscolor,(5+ (dt_item_size-5)//2, ry - dt_item_size, dt_item_size-5,dt_item_size-5))
            #print((dt_item_size //2 - titel.get_width()//2,ly))
            screen.blit(titel,(dt_item_size - titel.get_width()//2,ly))
    textbutton.draw()
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
    global Secure_Screen, screen, BG, TBC, Secure_Screen_Handle
    screen.fill(BG)
    pygame.draw.rect(screen, TBC, pygame.Rect(0, screen.get_height()- 50, screen.get_width(), 50))
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(10,screen.get_height()- 40, 30,30) )
    clock_txt = menuf.render(strftime("%H:%M:%S"),True,(255,255,255))

    pygame.draw.rect(screen, TBC, pygame.Rect(screen.get_width()- clock_txt.get_width() - 20, screen.get_height()- 50, clock_txt.get_width()+20, 50))
    pygame.draw.rect(screen, (20, 41, 68), pygame.Rect(screen.get_width()- clock_txt.get_width() - 20, screen.get_height()- 50, 5, 50))
    screen.blit(clock_txt, (screen.get_width()- clock_txt.get_width() -10, screen.get_height()- (50 - clock_txt.get_height()//2)))

    #BG /\ FG\/
    pygame.draw.rect(Secure_Screen,(0,0,0, 125),(0,0,screen.get_width(),screen.get_height()))
    if Secure_Screen_Handle:
        sceen = pygame.Surface((screen.get_width(),screen.get_height()), pygame.SRCALPHA)
        sceen.fill((0,0,0,0))
        Secure_Screen_Handle(sceen)
        Secure_Screen.blit(sceen, (0,0))
    screen.blit(Secure_Screen,(0,0))



# Running
if __name__ == "__main__":
    from Modules.Build import next_build_version, get_build_version
    _init_d(str(next_build_version()))



    if datal["SYS"]["First"]:
        datal["SYS"]["First"] = False
        Create_MSG_Box(f"Welcome to MOS-{version}","You can close this PopUp.","Go to the Settings to personelize your PC.", 0,1,None)
        first_time = False
    run()



    #with open("Settings.json","w") as f:
    #    json.dump(datal,f)
