import pygame
import sys
import gui


class Window:
    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

    def __init__(self, title, width, height, x=0, y=0, type_id=None):
        self.title = title
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = pygame.Surface((width, height))
        self.dragging = False
        self.drag_offset = (0, 0)
        self.title_height = 30
        self.close_btn_rect = pygame.Rect(width - 30, 0, 30, self.title_height)
        self.type_id = type_id
        self.children = []

    def draw(self, screen):
        # Draw window background
        self.surface.fill((240, 240, 240))
        # Draw title text
        font = pygame.font.Font(None, 24)
        title_text = font.render(self.title, True, (0, 0, 0))
        self.surface.blit(title_text, (5, 5))

        if self.type_id == 'TERMINAL':
            font = pygame.font.Font(None, 50)
            data_text = font.render(f"{self.x, self.y}", True, (0, 0, 0))
            wdata_text = font.render(f"{gui.wdata}", True, (0, 0, 0))
            data1_text = font.render(f"{self.dragging}", True, (0, 0, 0))
            title_bar_height = title_text.get_height()
            self.surface.blit(data_text, (10,  title_text.get_height() + title_text.get_height()+5 if title_text is not None else data_text.get_height() + 5))
            self.surface.blit(data1_text, (10, data_text.get_height() + title_bar_height + data1_text.get_height()))
            #self.surface.blit(wdata_text, (10, data_text.get_height() + 5 + data1_text.get_height() + 5))

        # Draw title bar
        pygame.draw.rect(self.surface, (200, 200, 200), (0, 0, self.width, self.title_height))
        # Draw close button
        pygame.draw.rect(self.surface, (255, 0, 0), self.close_btn_rect)
        # Draw window to screen
        screen.blit(self.surface, (self.x, self.y))

    def handle_event(self, event):
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
            else:
                # Handle events for children
                for child in reversed(self.children):
                    if not child.handle_event(event):
                        self.children.remove(child)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            # Propagate event to children
            for child in self.children:
                child.handle_event(event)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.x = mouse_pos[0] - self.drag_offset[0]
            self.y = mouse_pos[1] - self.drag_offset[1]
        elif event.type == pygame.MOUSEMOTION:
            # Propagate motion events to children
            for child in self.children:
                child.handle_event(event)

        return True


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Window Manager")
    clock = pygame.time.Clock()

    windows = [
        Window("Window 1", 300, 200, 100, 100, type_id="TERMINAL"),
        Window("Window 2", 400, 300, 200, 150)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, window in enumerate(windows):
                    if window.x <= mouse_pos[0] <= window.x + window.width and \
                            window.y <= mouse_pos[1] <= window.y + window.height:
                        if i != len(windows) - 1:  # Only reorder if not already active
                            windows.append(windows.pop(i))
                        break

            if len(windows) > 0:
                if not windows[-1].handle_event(event):
                    windows.remove(windows[-1])

        screen.fill((128, 128, 128))

        for window in windows:
            window.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
