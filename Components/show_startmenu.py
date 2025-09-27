import os
import pygame

def read_version() -> str:
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent
    return path.joinpath("VERSION").read_text().strip()

def build_release(default="Beta") -> str:
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent
    return path.joinpath("RELEASE").read_text().strip() or default

__version__ = read_version()

class Startmenu:
    def __init__(self, theme, user:str):
        self.is_visible = False
        self.theme = theme
        self.user_name = user
        self.searchbar_txt = ""
        
    def draw(self, screen: pygame.Surface, menuf: pygame.font.Font):
        left = pygame.font.Font(None, 24)
        #First Calc Dimensions
        build_type = build_release()
        build_str = f"{__version__}" if build_type == "Stable" else f"{__version__}-{build_type}"
        logo = menuf.render(f"MOS-V{build_str}", True, (255,255,255))
        width = logo.get_height() + 20
        height = logo.get_width() + 20
        logo = pygame.transform.rotate(logo, 90)

        l_width = width
        l_height = height
        logo = pygame.transform.rotate(logo, -90)
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

        width = l_width + max(searchbar_txt.get_width(),calc_button_dimensions("Shutdown",left,20)[0]) + 20 + 10
        height = max(height *1.5, screen.get_height() // 2)


        rounding =  25
        menu_color = (12, 121, 145)
        bg_color = min(menu_color[0] *1.5,255), min(menu_color[1] *1.5,255), min(menu_color[2] *1.5,255)

        # Right Menu Items

        Terminal = MenuItem("Terminal", os.path.join("Resources","icons","terminal_sys.png"), lambda: print("Terminal"))
        Settings = MenuItem("Settings", os.path.join("Resources","icons","einstellungen_sys.png"), lambda: print("Settings"))
        New_Window = MenuItem("New Window", os.path.join("Resources","icons","fenster_sys.png"), lambda: print("New Window"))

        items = [Terminal, Settings, New_Window]
        item_surfaces = [item.render(left) for item in items]

        added_left = max(item_surfaces[0].get_width(),item_surfaces[1].get_width(),item_surfaces[2].get_width()) + 20

        width = width + added_left + added_left // 2#, screen.get_width() // 4)
        #print(width,added_left, height)

        # Create Surface
        menu = pygame.Surface((width, height), pygame.SRCALPHA)

        #Draw Background
        pygame.draw.circle(menu, menu_color,(rounding,rounding),rounding,0 )
        pygame.draw.circle(menu, menu_color,(width-rounding,rounding),rounding,0 )
        pygame.draw.rect(menu, menu_color,(rounding,0,width-rounding*2,rounding*2),0 )
        pygame.draw.rect(menu, menu_color,(0,rounding,width,height-rounding),0 )
        
        
        #Last Draw everything
        menu.blit(logo, ( width - logo.get_width() - 10,10))
        pygame.draw.rect(menu,(100,100,100), (l_width , height - searchbar_txt.get_height() - 10, searchbar_txt.get_width() + 20 + added_left //2, searchbar_txt.get_height() +2), 0)
        pygame.draw.rect(menu,(200,200,200), (l_width , height - searchbar_txt.get_height() - 10 + searchbar_txt.get_height()-3, searchbar_txt.get_width() + added_left //2, 5), 0)
        menu.blit(searchbar_txt, (l_width , height - searchbar_txt.get_height() - 10))
        pygame.draw.circle(menu, (125,125,125), (20, 10 +( (u_height - 10) // 2)), 10, 0)
        menu.blit(user_txt, (35,10))

        # Draw Items/Menus
        i_m_bg = self.theme["syscolor"]
        
        pygame.draw.rect(menu, i_m_bg, pygame.Rect(l_width - 10,u_height +10, width - l_width - added_left + 10,height - u_height - searchbar_txt.get_height() - 30), border_radius=rounding)


        pygame.draw.rect(menu, bg_color, pygame.Rect(width - added_left + 10, u_height +10 , added_left - 20, height - 20 - u_height - u_height), border_radius=rounding)

        for i, item_surface in enumerate(item_surfaces):
            y_pos = 10 + i * (item_surface.get_height() + 10) + u_height + 10
            rect = item_surface.get_rect(bottomleft=(width - added_left + 10, y_pos+ item_surface.get_height()))
            rect.height = 2
            rect.width = item_surface.get_width() - 60
            rect.bottomleft = (width - added_left + 60, y_pos+ item_surface.get_height() -10)
            pygame.draw.rect(menu,(255,255,255), rect)
            menu.blit(item_surface, (width - added_left + 10, y_pos))

        draw_button(menu, "Shutdown", (width - added_left + 10, height - calc_button_dimensions("Shutdown",left,20)[1] - 10), left, (200,0,0), (255,255,255), padding=20, border_radius=10)

        self.menu = menuf

        screen.blit(menu, (0, screen.get_height() - height - 50))

    def handle(self, pos: tuple):
        left = pygame.font.Font(None, 24)
        #First Calc Dimensions
        build_type = build_release()
        build_str = f"{__version__}" if build_type == "Stable" else f"{__version__}-{build_type}"
        logo = self.menuf.render(f"MOS-V{build_str}", True, (255,255,255))
        width = logo.get_height() + 20
        height = logo.get_width() + 20
        logo = pygame.transform.rotate(logo, 90)

        l_width = width
        l_height = height
        logo = pygame.transform.rotate(logo, -90)
        if self.searchbar_txt == "":
            searchbar_txt = self.menuf.render("Search...", True, (200,200,200))
        else:
            searchbar_txt = self.menuf.render(self.searchbar_txt, True, (200,200,200))
        if searchbar_txt.get_width() + 20 > 100:
            height += searchbar_txt.get_height() + 10
            width += 100
        else:
            width += searchbar_txt.get_width() + 20
            height += searchbar_txt.get_height() + 10

        user_txt = self.menuf.render(f"{self.user_name}", True, (255,255,255))
        u_height = user_txt.get_height() + 10

        width = l_width + max(searchbar_txt.get_width(),calc_button_dimensions("Shutdown",left,20)[0]) + 20 + 10
        height = max(height *1.5, screen.get_height() // 2)


        rounding =  25
        menu_color = (12, 121, 145)
        bg_color = min(menu_color[0] *1.5,255), min(menu_color[1] *1.5,255), min(menu_color[2] *1.5,255)

        # Right Menu Items

        Terminal = MenuItem("Terminal", os.path.join("Resources","icons","terminal_sys.png"), lambda: print("Terminal"))
        Settings = MenuItem("Settings", os.path.join("Resources","icons","einstellungen_sys.png"), lambda: print("Settings"))
        New_Window = MenuItem("New Window", os.path.join("Resources","icons","fenster_sys.png"), lambda: print("New Window"))

        items = [Terminal, Settings, New_Window]
        item_surfaces = [item.render(left) for item in items]

        added_left = max(item_surfaces[0].get_width(),item_surfaces[1].get_width(),item_surfaces[2].get_width()) + 20

        width = width + added_left + added_left // 2#, screen.get_width() // 4)
        #print(width,added_left, height)

        # Create Surface
        menu = pygame.Surface((width, height), pygame.SRCALPHA)

        #Draw Background
        pygame.draw.circle(menu, menu_color,(rounding,rounding),rounding,0 )
        pygame.draw.circle(menu, menu_color,(width-rounding,rounding),rounding,0 )
        pygame.draw.rect(menu, menu_color,(rounding,0,width-rounding*2,rounding*2),0 )
        pygame.draw.rect(menu, menu_color,(0,rounding,width,height-rounding),0 )
        
        
        #Last Draw everything
        menu.blit(logo, ( width - logo.get_width() - 10,10))
        pygame.draw.rect(menu,(100,100,100), (l_width , height - searchbar_txt.get_height() - 10, searchbar_txt.get_width() + 20 + added_left //2, searchbar_txt.get_height() +2), 0)
        pygame.draw.rect(menu,(200,200,200), (l_width , height - searchbar_txt.get_height() - 10 + searchbar_txt.get_height()-3, searchbar_txt.get_width() + added_left //2, 5), 0)
        menu.blit(searchbar_txt, (l_width , height - searchbar_txt.get_height() - 10))
        pygame.draw.circle(menu, (125,125,125), (20, 10 +( (u_height - 10) // 2)), 10, 0)
        menu.blit(user_txt, (35,10))

        # Draw Items/Menus
        i_m_bg = self.theme["syscolor"]
        
        pygame.draw.rect(menu, i_m_bg, pygame.Rect(l_width - 10,u_height +10, width - l_width - added_left + 10,height - u_height - searchbar_txt.get_height() - 30), border_radius=rounding)


        pygame.draw.rect(menu, bg_color, pygame.Rect(width - added_left + 10, u_height +10 , added_left - 20, height - 20 - u_height - u_height), border_radius=rounding)

        for i, item_surface in enumerate(item_surfaces):
            y_pos = 10 + i * (item_surface.get_height() + 10) + u_height + 10
            rect = item_surface.get_rect(bottomleft=(width - added_left + 10, y_pos+ item_surface.get_height()))
            rect.height = 2
            rect.width = item_surface.get_width() - 60
            rect.bottomleft = (width - added_left + 60, y_pos+ item_surface.get_height() -10)
            pygame.draw.rect(menu,(255,255,255), rect)
            menu.blit(item_surface, (width - added_left + 10, y_pos))

        draw_button(menu, "Shutdown", (width - added_left + 10, height - calc_button_dimensions("Shutdown",left,20)[1] - 10), left, (200,0,0), (255,255,255), padding=20, border_radius=10)

        #screen.blit(menu, (0, screen.get_height() - height - 50))
        pass

def draw_button(surface:pygame.Surface, text: str, pos:tuple, font: pygame.font.Font, bg_color:tuple, fg_color:tuple, padding:int=20, border_radius:int=0) -> pygame.Rect:
    button_width, button_height = calc_button_dimensions(text, font, padding)
    button_rect = pygame.Rect(pos[0], pos[1], button_width, button_height)
    pygame.draw.rect(surface, bg_color, button_rect, border_radius=border_radius)
    text_surf = font.render(text, True, fg_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    return button_rect

def calc_button_dimensions(text:str, font: pygame.font.Font, padding:int=20):
    text_surf = font.render(text, True, (255,255,255))
    width = text_surf.get_width() + padding
    height = text_surf.get_height() + padding // 2
    return width, height






# 
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


