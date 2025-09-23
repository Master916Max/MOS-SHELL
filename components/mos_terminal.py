import pygame

from components.mos_window import MosWindow
from components.mos_window_base import MosWindowBase


class MosTerminal(MosWindowBase):
    def __init__(self, config: dict):
        super().__init__(config)
        self.terminal_lines = []
        self.command_buffer = ""
        self.cursor_pos = 0
        self.command_history = []
        self.font_size = 20
        self.line_spacing = 5
        self.text_color = (0, 0, 0)

    
    def draw_content(self):
        font = pygame.font.Font(None, self.font_size)
        visible_lines = self.terminal_lines[-20:]  # Show last 20 lines
        total_height = self.height - self.title_height - 20  # Reserve space for prompt
        line_height = font.get_height() + self.line_spacing
        top_padding = 10
        content_height = (len(visible_lines) + 1) * line_height  # +1 for prompt

        # Calculate initial y_offset to position content at top or scrolled position
        y_offset = self.title_height + top_padding
        if content_height > total_height:
            y_offset = self.height - content_height - top_padding

        for line in visible_lines:
            text = font.render(line, True, self.text_color)
            self.surface.blit(text, (10, y_offset))
            y_offset += line_height

        prompt = "$ " + self.command_buffer
        if pygame.time.get_ticks() % 1000 < 500:  # Blinking cursor
            prompt = prompt[:self.cursor_pos + 2] + "|" + prompt[self.cursor_pos + 2:]

        input_text = font.render(prompt, True, self.text_color)
        self.surface.blit(input_text, (10, y_offset))

    def handle_custom_input(self, event):
        if self.type_id == 'TERMINAL' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.command_buffer:
                    self.terminal_lines.append(f"$ {self.command_buffer}")
                    self._execute_command(self.command_buffer)
                    self.command_history.append(self.command_buffer)
                    self.command_buffer = ""
                    self.cursor_pos = 0
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.command_buffer = (self.command_buffer[:self.cursor_pos - 1] +
                                           self.command_buffer[self.cursor_pos:])
                    self.cursor_pos -= 1
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.command_buffer), self.cursor_pos + 1)
            elif event.unicode.isprintable():
                self.command_buffer = (self.command_buffer[:self.cursor_pos] +
                                       event.unicode +
                                       self.command_buffer[self.cursor_pos:])
                self.cursor_pos += 1

    def _execute_command(self, command):
        try:
            import subprocess
            output = subprocess.check_output(command.split(),
                                             stderr=subprocess.STDOUT,
                                             text=True,
                                             shell=True)
            self.terminal_lines.extend(output.splitlines())
        except Exception as e:
            self.terminal_lines.append(f"Error: {str(e)}")
