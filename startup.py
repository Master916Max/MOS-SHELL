import pygame
import sys
import math
import time

def while_loading(dbg=False,pict: str=None):
    pygame.init()
    if dbg:
        screen = pygame.display.set_mode((1080, 720))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    if pict:
        pict = pygame.image.load(pict)

    font = pygame.font.Font(None, 50)  # Default font, size 74
    center = screen.get_rect().center
    loading_text = font.render("Loading", True, (255, 255, 255))
    clock = pygame.time.Clock()
    angle = 0
    tick = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Simulate loading process
        if not pict:
            screen.fill((000, 100, 200))
            screen.blit(loading_text, (center[0] - loading_text.get_width() // 2,center[1] - 60 - loading_text.get_height() // 2))
            # Loading Throttle

            end_angle = angle + math.pi / 4  # quarter circle arc
            pygame.draw.arc(screen,(255, 255, 255),(center[0] - 40, center[1] - 40, 40 * 2, 40 * 2),angle,end_angle, 5)
            pygame.draw.arc(screen,(255, 255, 255),(center[0] - 40, center[1] - 40, 40 * 2, 40 * 2),angle,end_angle, 6)
            pygame.draw.arc(screen,(255, 255, 255),(center[0] - 40, center[1] - 40, 40 * 2, 40 * 2),angle,end_angle, 4)

            pygame.display.flip()
            angle += 0.1  # rotation speed
            clock.tick(60)
        else:
            screen.fill((0, 0, 0))
            screen.blit(loading_text, (center[0] - loading_text.get_width() // 2,center[1] - 60 - loading_text.get_height() // 2 + pict.get_height() // 2))
            pict_rect = pict.get_rect(center=center)
            pict_rect = pict_rect.move(0, 0 - pict.get_height() // 2)
            screen.blit(pict, pict_rect)
        pygame.display.flip()


if __name__ == "__main__":
    #logo = pygame.image.load("mos-os-logo.png")
    logo = pygame.image.load("shell-logo.png")
    while_loading(dbg=False, pict=logo)
    time.sleep(1)
