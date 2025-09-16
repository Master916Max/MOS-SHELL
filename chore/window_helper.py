from Components.mos_terminal import MosTerminal
from Components.mos_window import MosWindow
from chore.mos import mos_app


class WindowHelper:
    @staticmethod
    def init_window(window_config: dict):
        if window_config.get("type_id") == "TERMINAL":
            window = MosTerminal(window_config)
        else:
            window = MosWindow(window_config)
        mos_app.add_window(window)
        return window

    @staticmethod
    def destroy_window(window):
        mos_app.remove_window(window)
