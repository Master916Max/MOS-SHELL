from time import strftime
import pygame

class TaskBar:
    def __init__(self):
        pass

    def display(self, screen, TBC, menuf):
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
        taskbar = self.handle_task_bar(taskbar)

            #
            # Drawing Clock
            #

            #Clock Surface
        clock_s = pygame.Surface((150,50), pygame.SRCALPHA)

            # Clock Text
        clock_txt = menuf.render(strftime("%H:%M:%S"),True,(255,255,255))

        pygame.draw.rect(clock_s, (20, 41, 68,127), pygame.Rect(0, 0, 10, 50))
        clock_rect = clock_txt.get_rect()
        clock_rect.center = (80,25)
        clock_s.blit(clock_txt, clock_rect)
        taskbar.blit(clock_s, (screen.get_width()- clock_s.get_width(), 0))
            
        screen.blit(taskbar, (0, screen.get_height()- 50))
        return screen
    
    def handle_task_bar(self, taskbar):
        return taskbar
        x_offset = 50
        for app in open_apps:
            if app in app_icons:
                icon = pygame.transform.scale(app_icons[app], (40,40))
                taskbar.blit(icon, (x_offset, 5))
                x_offset += 45
        return taskbar