from time import strftime
import pygame

class TaskBar:
    def __init__(self):
        pass

    def display(self, screen, menuf:pygame.font.Font, theme:dict, mos_app, zlayer):
        self.menuf = menuf
        TBC = theme["TBC"]
        taskbar = pygame.Surface((screen.get_width(), 50), pygame.SRCALPHA)

        pygame.draw.rect(taskbar, (TBC[0],TBC[1],TBC[2],200), pygame.Rect(0, 0, screen.get_width(), 50))
        pygame.draw.rect(taskbar, (TBC[0],TBC[1],TBC[2],225), pygame.Rect(5,5, 40,40) )

            #
            # Drawing Logo
            #
        logo = pygame.Surface((30,30), pygame.SRCALPHA)
        pygame.draw.rect(logo, (255,0,0), (0,0, 15,15))
        pygame.draw.rect(logo, (255,255,0), (15,0, 15,15))
        pygame.draw.rect(logo, (0,0,255), (0,15, 15,15))
        pygame.draw.rect(logo, (0,255,255), (15,15, 15,15))
        d_logo = pygame.transform.rotate(logo,45)
        taskbar.blit(d_logo,(5,5))

            #
            # Drawing Taskbar Items
            #
        taskbar = self.handle_task_bar(taskbar, mos_app, zlayer, theme)

            #
            # Drawing Clock
            #

            #Clock Surface
        clock_s = pygame.Surface((150,50), pygame.SRCALPHA)

            # Clock Text
        clock_txt = self.menuf.render(strftime("%H:%M:%S"),True,(255,255,255))

        pygame.draw.rect(clock_s, (20, 41, 68,127), pygame.Rect(0, 0, 10, 50))
        clock_rect = clock_txt.get_rect()
        clock_rect.center = (80,25)
        clock_s.blit(clock_txt, clock_rect)
        taskbar.blit(clock_s, (screen.get_width()- clock_s.get_width(), 0))
            
        screen.blit(taskbar, (0, screen.get_height()- 50))
        return screen
    
    def handle_task_bar(self, taskbar: pygame.Surface,mos_app, zlayer, theme:dict):
        tb_offset = 0
        active_window_text = 0
        #for window in mos_app.open_windows:
        #    if mos_app.active == window:
        #        u_txt = self.menuf.render(f"{zlayer[0].title}", True, (255, 255, 255))
        #        pygame.draw.rect(taskbar, (58,58,255), pygame.Rect(50+ 40*tb_offset + active_window_text,taskbar.get_height()- 40, 30,30))
        #        pygame.draw.rect(taskbar, (60, 91, 118), pygame.Rect(50+ 40*(tb_offset + 1) - 5 , taskbar.get_height()- (55 - u_txt.get_height()//2),u_txt.get_width(), 30))
        #        taskbar.blit(u_txt, (50+ 40*(tb_offset + 1) - 5 , taskbar.get_height()- (55 - u_txt.get_height()//2)))
        #        active_window_text = u_txt.get_width() + 10
        #    else:
        #        if window.logo:
        #            pygame.draw.rect(taskbar, pygame.transform.scale(window.logo, (30,30)), pygame.Rect(50+ 40*tb_offset + active_window_text,0, 30,30))
        #        pygame.draw.rect(taskbar, theme["syscolor"], pygame.Rect(50+ 40*tb_offset + active_window_text,0, 30,30))


        tb_offset +=1

        size = taskbar.get_height() * 0.6

        for win in mos_app.open_windows:
            
            if mos_app.active != win:
                if win.logo:
                    taskbar.blit()
                    pygame.draw.rect(taskbar, pygame.transform.scale(win.logo, (size,size)), pygame.Rect(50+ 40*tb_offset + active_window_text,taskbar.get_height()- 40, size,size))
                    tb_offset +=1
                    continue
                pygame.draw.rect(taskbar, theme["syscolor"], pygame.Rect(50+ 40*tb_offset + active_window_text,10, size,size))
                tb_offset +=1
            else:
                u_text = self.menuf.render(f"{win.title}", True, (255, 255, 255))
                active_window_text = u_text.get_width() + 10
                pygame.draw.rect(taskbar, (58,58,255), pygame.Rect(50+ 40*tb_offset ,taskbar.get_height()- 40, size,size))
                pygame.draw.rect(taskbar, (60, 91, 118), pygame.Rect(50+ 40*(tb_offset + 1) - 5 , taskbar.get_height()- (55 - u_text.get_height()//2),u_text.get_width(), size))
                taskbar.blit(u_text, (50+ 40*(tb_offset + 1) - 5 , taskbar.get_height()- (55 - u_text.get_height()//2)))
                tb_offset +=1

        return taskbar