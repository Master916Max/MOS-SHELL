from audioop import add
import os
import pathlib
import sys
from turtle import width
from typing import ItemsView
import pygame

def read_version() -> str:
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent
    return path.joinpath("VERSION").read_text().strip()

class Startmenu:
    def __init__(self, theme, user:str):
        self.is_visible = False
        self.theme = theme
        self.user_name = user
        self.searchbar_txt = ""
        
    def draw(self, screen: pygame.Surface, menuf: pygame.font.Font):
        pass
        #First Calc Dimensions
        logo = menuf.render(f"MOS-V{read_version()}", True, (255,255,255))
        width = logo.get_height() + 20
        height = logo.get_width() + 20
        logo = pygame.transform.rotate(logo, 90)

        l_width = width
        l_height = height
        if self.searchbar_txt == "":
            searchbar_txt = menuf.render("Search...", True, (200,200,200))
        else:
            searchbar_txt = menuf.render(self.searchbar_txt, True, (200,200,200))
        if searchbar_txt.get_width() + 20 > 100:
            height += searchbar_txt.get_height() + 10
            width += 100
        else:
            width += searchbar_txt.get_width() + 20
            height += searchbar_txt.get_height() + 10

        user_txt = menuf.render(f"{self.user_name}", True, (255,255,255))
        u_height = user_txt.get_height() + 10

        width = l_width +searchbar_txt.get_width() + 20 + 10
        height = max(height *1.5,screen.get_height() // 2)


        rounding =  25
        menu_color = (4, 73, 10)
        bg_color = min(menu_color[0] *2,255), min(menu_color[1] *2,255), min(menu_color[2] *2,255)

        # Right Menu Items
        left = pygame.font.Font(None, 24)

        Terminal = MenuItem("Terminal", os.path.join("Resources","icons","terminal_sys.png"), lambda: print("Terminal"))
        Settings = MenuItem("Settings", os.path.join("Resources","icons","einstellungen_sys.png"), lambda: print("Settings"))
        New_Window = MenuItem("New Window", os.path.join("Resources","icons","fenster_sys.png"), lambda: print("New Window"))

        items = [Terminal, Settings, New_Window]
        item_surfaces = [item.render(left) for item in items]

        added_left = max(item_surfaces[0].get_width(),item_surfaces[1].get_width(),item_surfaces[2].get_width()) + 20

        width = width + added_left + added_left // 2
        #print(width,added_left, height)

        # Create Surface
        menu = pygame.Surface((width, height), pygame.SRCALPHA)

        #Draw Background
        pygame.draw.circle(menu, menu_color,(rounding,rounding),rounding,0 )
        pygame.draw.circle(menu, menu_color,(width-rounding,rounding),rounding,0 )
        pygame.draw.rect(menu, menu_color,(rounding,0,width-rounding*2,rounding*2),0 )
        pygame.draw.rect(menu, menu_color,(0,rounding,width,height-rounding),0 )
        
        
        #Last Draw everything
        menu.blit(logo, (10, height - logo.get_height() - 10 - searchbar_txt.get_height() - 10))
        pygame.draw.rect(menu,(100,100,100), (l_width + added_left//4 , height - searchbar_txt.get_height() - 10, searchbar_txt.get_width() + 20, searchbar_txt.get_height() +2), 0)
        pygame.draw.rect(menu,(200,200,200), (l_width + added_left//4 , height - searchbar_txt.get_height() - 10 + searchbar_txt.get_height()-3, searchbar_txt.get_width() + 20, 5), 0)
        menu.blit(searchbar_txt, (l_width + added_left//4 , height - searchbar_txt.get_height() - 10))
        pygame.draw.circle(menu, (125,125,125), (20, 10 +( (u_height - 10) // 2)), 10, 0)
        menu.blit(user_txt, (35,10))

        # Draw Items/Menus
        i_m_bg = self.theme["syscolor"]
        #pygame.draw.rect(menu,i_m_bg, )

        #pygame.draw.rect(menu,bg_color, (width - added_left + 10, 10 + u_height, added_left - 20, height - 20 - u_height), 0)
        draw_rounded_rect(menu, bg_color, pygame.Rect(width - added_left + 10, 10 , added_left - 20, height - 20 - u_height), 20)

        for i, item_surface in enumerate(item_surfaces):
            y_pos = 10 + i * (item_surface.get_height() + 10)
            rect = item_surface.get_rect(bottomleft=(width - added_left + 10, y_pos+ item_surface.get_height()))
            rect.height = 2
            rect.width = item_surface.get_width() - 60
            rect.bottomleft = (width - added_left + 60, y_pos+ item_surface.get_height() -10)
            pygame.draw.rect(menu,(255,255,255), rect)
            menu.blit(item_surface, (width - added_left + 10, y_pos))

        screen.blit(menu, (0, screen.get_height() - height - 50))

class MenuItem:
    def __init__(self, name:str, icon_path:str, action):
        self.name = name
        self.icon_path = icon_path
        self.action = action
        self.icon = pygame.image.load(icon_path)
        self.icon = pygame.transform.scale(self.icon, (32,32))

    def render(self, font: pygame.font.Font):
        self.item_txt = font.render(self.name, True, (255,255,255))
        surface = pygame.Surface((self.item_txt.get_width() + 60, max(40, self.item_txt.get_height() + 10)), pygame.SRCALPHA)
        surface.blit(self.icon, (10, (surface.get_height() - self.icon.get_height()) // 2))
        surface.blit(self.item_txt, (50, (surface.get_height() - self.item_txt.get_height()) // 2))
        return surface
    
class Button:
    def __init__(self, rect:pygame.Rect, color, text:str, font: pygame.font.Font, action):
        self.rect = rect
        self.color = color
        self.text = text
        self.font = font
        self.action = action

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, (255,255,255))
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)