from client.Components.mos_window_base import MosWindowBase


class MosWindow(MosWindowBase):
    def handle_custom_input(self, event):
        pass

    def draw_content(self):
        pass

    def __init__(self, config):
        super().__init__(config)