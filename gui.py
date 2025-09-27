#
# MOS-Shell
#

#
# Python Imports
#
import pathlib
from re import M
import re
import time
import pygame, random, json
from time import strftime
from typing import Any

#
# Local Imports
#
from Components.mos_terminal import MosTerminal
from Components.mos_window import MosWindow
from Components.mos_settings import MosSettings
from Components.show_taskbar import TaskBar
from Components.show_startmenu import Startmenu
from Components.remote_terminal import start_remote_terminal
from Modules import *
from chore.mos import mos_app
from chore.window_helper import WindowHelper

#
# Services
#
import services

# Pygame Init
pygame.init()

MSG_Box = object
datal: any

#Input Variabeln
mousbuttondown = False

# Colors
syscolor =Any
bg_color =Any
TBC =Any
noneselectcolor =Any
textcolor =Any
msgtextcolor =Any
window_select_color =Any

#Desktop Variabeln
dt_item_size = 64
dt_font = pygame.font.Font(None, 24)
dt_items = ["My PC","System-Settings","Test.txt"]
dt_offset = 20

#Other Variabeln
version = "V-1.0.0"
screen: pygame.Surface = None
error, errormsg = False , ""
selected_window = False
cd = 100
sss = False
zlayer = []
bg_img = pygame.image.load("olopit.png")
remote_pip : Any        = None
remote_process : Any    = None

#Secure Screen Variabeln
secure_screen : pygame.Surface
Secure_Screen_Handle : any = None

#Menu Variabeln
menuf = pygame.font.Font(None,45)
Menu_Text: pygame.Surface

build_str: pygame.Surface

apps = {"Ordner": "Games",
        "App"   : "Emails",
        "App"   : "Brave"} 

root : pygame.Surface

#
# Components
#
task_bar : TaskBar
start_menu : Startmenu

def startup():
    global syscolor, bg_color, TBC, noneselectcolor, textcolor, msgtextcolor, window_select_color, datal
    services.Start_Services()

    Theme_Service = services.services[services.Services.Theme_Service]
    Theme_Pipe, Theme_Return_Pipe = services.get_Theme_Pipes()


    basi_json = """{"SYS":{"First":true}}"""


    def load_settings():
        #try:
        #    with open("Settings.json", "r") as f:
        #        datal = json.load(f)
        #except Exception as e:
        #    print(e)
        datal = json.loads(basi_json)
        Theme_Pipe.send(("GET_ACTIVE_THEME", "1234Trash"))
        #print("Waiting for Theme Service...")
        #print("Reciving Theme...")
        time.sleep(0.5)
        while not Theme_Pipe.poll():
            time.sleep(0.1)
        command, theme = Theme_Pipe.recv()
        if theme:
            #print(theme)
            datal["Theme"] = theme
        else:
            raise Exception("No Active Theme Set\n Please make sure a theme is in the Current Working Directory.")
          
        return datal
    
    datal = load_settings()

    #print(datal)

    # System Variabeln
    syscolor =              datal["Theme"]["syscolor"]
    bg_color =              datal["Theme"]["bg_color"]
    TBC =                   datal["Theme"]["TBC"]
    noneselectcolor =       datal["Theme"]["noneselectcolor"]
    textcolor =             datal["Theme"]["textcolor"]
    msgtextcolor =          datal["Theme"]["msgtextcolor"]
    window_select_color =   datal["Theme"]["window_select_color"]


def read_version() -> str:
    from pathlib import Path
    return Path(__file__).resolve().parent.joinpath("VERSION").read_text().strip()


__version__ = read_version()



def git_short_sha(default="unknown") -> str:
    from git import Repo
    try:
        repo = Repo(search_parent_directories=True)
        return repo.git.rev_parse("--short", "HEAD").strip()
    except Exception:
        return default

def init(dbg:bool=False):
    # TODO: do only use globals for constants
    global secure_screen, text_button, textinput,root, menuf, build_str, Menu_Text, Menu_Height, Menu_Width, task_bar, start_menu, datal, remote_pip, remote_process, zlayer
    #print(textcolor) #                     \/ "-{git_short_sha()}"
    build_str = menuf.render(f"{__version__}-{git_short_sha()}", dbg, textcolor)
    if dbg:
        root = pygame.display.set_mode((1080, 720))
        remote_pip, remote_process = start_remote_terminal()
    else:
        root = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("MOS-Py-GUI")
    secure_screen = pygame.Surface((root.get_width(), root.get_height()), pygame.SRCALPHA)
    text_button  = ButtonField("Test", root, 250, 50, 150, 50, fgcolor=textcolor, bgcolor=syscolor)
    textinput = InputField(root, 50, 50, 150, 50, fgcolor=textcolor, bgcolor=syscolor, txtfont=menuf)
    # Menu \/
    Menu_Text = menuf.render(f"MOS-{__version__}", True, textcolor)
    Menu_Height = Menu_Text.get_height() * 8 + 50
    Menu_Width = Menu_Text.get_width() + 50
    task_bar = TaskBar()
    start_menu = Startmenu(datal["Theme"], "Max")
    return root

def run(screen: pygame.Surface = None):
    global selected_window, mousbuttondown, sss, cd, Secure_Screen_Handle, bg_color, TBC, textinput, datal
    #TaskBar List Background Color
    screen = screen
    running = True
    menu_opend = False
    last_size = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousbuttondown = True
                if pygame.Rect(10,screen.get_height()- 40, 30,30).collidepoint(event.pos[0],event.pos[1]):
                    menu_opend = not menu_opend
                #Will be reworked
                #by Master916Max
                #elif pygame.Rect(0, screen.get_height()- (Menu_Height + 50), Menu_Width,Menu_Height).collidepoint(event.pos[0],event.pos[1]) and menu_opend and False:
                    menu_opend = True
                    hit =  _hit_list(screen,("New-Window","Terminal","Settings","System"), menuf, (((213,189,175),textcolor),((250,237,205),textcolor),((213,189,175),textcolor),((212,163,115),textcolor)),10, screen.get_height() - (Menu_Height + 40) + Menu_Text.get_height() + 10, 5, event.pos)
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
                    elif hit == "Settings":
                        w = 600
                        h = 400
                        window_config = {
                            'title': f"System Settings",
                            'logo': None,
                            'width': w,
                            'height': h,
                            'parent': screen,
                            'zlayer': zlayer,
                            'type_id': 'SETTINGS'
                        }
                        new_window = WindowHelper.init_window(window_config)
                        zlayer.insert(0,new_window)
                    elif hit == "System":
                        print("Showing System Apps")
                        print(last_size)
                    if pygame.Rect(25, screen.get_height()- (Menu_Height - Menu_Text.get_height() * 6), Menu_Width - 50,Menu_Text.get_height()).collidepoint(event.pos[0],event.pos[1]):
                        sss = True
                        cd -= 1    
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
                        elif type(zlayer[0]) == MosWindow or type(zlayer[0]) == MosSettings:
                            zlayer[0].handle_input(event)
                        else: zlayer[0].handel_input("m", (event.pos[0], event.pos[1]))
            elif event.type == pygame.MOUSEMOTION:
                if mousbuttondown:
                    if len(zlayer) != 0 and len(zlayer) >= 0 + 1:
                        if not zlayer[0].update_x_y(event.rel, event.pos):
                            selected_window = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mousbuttondown = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12 or event.key == 1073742051:
                    if menu_opend:
                        menu_opend = False
                    else:
                        menu_opend = True
                else:
                    pass
                    #print(event)
                    #zlayer[0].handle_input(event)
                    
        # Bildschirm aktualisieren
        if not error and not sss:
            check_remote_pipe()
            screen.fill(bg_color)
            tmp = pygame.transform.scale(bg_img, (screen.get_width(), screen.get_height()))
            screen.blit(tmp, (0,0))
            _draw_desktop(screen)
            _draw_content(screen)
            
            screen.blit(build_str, (screen.get_width()- build_str.get_width() - 10, screen.get_height()- 60-(build_str.get_height()//2)))

            screen = task_bar.display(screen, menuf, datal["Theme"], mos_app, zlayer)

            if menu_opend:
                #_draw_menu(screen)
                start_menu.draw(screen, menuf)
        if not error and sss:
            cd -= 1
            Secure_Screen_Handle = draw_shutdown_text
            SecureScreen(screen)
            if cd == 0:
                running = False
        if error:
            screen.fill((58,58,255))
            _draw_text(errormsg, menuf, (235, 235, 255), 50, 50)
        
        root.blit(screen, (0, 0))

        pygame.display.flip()

    pygame.quit()


def check_remote_pipe():
    global remote_pip
    if not remote_pip: return
    if remote_pip.poll():
        command, arg = remote_pip.recv()
        match command:
            case "start_process":
                print(f"Starting Process: {arg}")
            case "kill_process":
                print(f"Killing Process: {arg}")
            case "list_processes":
                print("Listing Processes")
                #remote_pip.send([] for win in mos_app.open_windows if win.type_id == "TERMINAL")
            case _:
                print(f"Unknown Command: {command} with arg: {arg}")

# Need to Export

def _draw_text(screen,txt, font: pygame.font.Font, col, x, y):
    img = font.render(txt, True, col)
    screen.blit(img,(x,y))

def _draw_content(screen):
    zlayer.reverse()
    for window in mos_app.open_windows:
        window.draw(screen)
    zlayer.reverse()



def _draw_desktop(screen):
    global dt_items, dt_item_size, dt_offset, dt_font, textcolor
    for item in dt_items:
        if not item.isspace():
            titel = dt_font.render(item,True,textcolor)
            ly = (dt_items.index(item)+1) * dt_item_size + dt_offset * (dt_items.index(item)+1) + dt_items.index(item) *titel.get_height()
            ry = (dt_items.index(item)+1) * dt_item_size + dt_offset * (dt_items.index(item)+2) + dt_items.index(item) *titel.get_height() - titel.get_height()
            pygame.draw.rect(screen, syscolor,(5+ (dt_item_size-5)//2, ry - dt_item_size, dt_item_size-5,dt_item_size-5))
            #print((dt_item_size //2 - titel.get_width()//2,ly))
            screen.blit(titel,(dt_item_size - titel.get_width()//2,ly))
    #text_button.draw()
    #textinput.draw()

def _hit_list(screen, items: tuple[str],font: pygame.font.Font,colors: tuple[tuple],x: int,y: int, offset:int,mousepos, background = (125, 125, 125)):
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
def SecureScreen(screen):
    global secure_screen, bg_color, TBC, Secure_Screen_Handle
    screen.fill(bg_color)
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

def draw_shutdown_text(sceen: pygame.Surface):
    img = menuf.render("Shuting Down", True, (255,255,255))
    sceen.blit(img,(sceen.get_width()//2 - img.get_width()//2, sceen.get_height()//2 - img.get_height()//2))
