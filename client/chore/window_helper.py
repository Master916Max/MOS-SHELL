from client.Components.mos_terminal import MosTerminal
from client.Components.mos_window import MosWindow
from client.Components.mos_settings import MosSettings
from client.chore.mos import mos_app


class WindowHelper:
    @staticmethod
    def init_window(window_config: dict):
        if window_config.get("type_id") == "TERMINAL":
            window = MosTerminal(window_config)
        elif window_config.get("type_id") == "SETTINGS":
            window = MosSettings(window_config)
        else:
            window = MosWindow(window_config)
        mos_app.add_window(window)
        return window

    @staticmethod
    def destroy_window(window):
        mos_app.remove_window(window)
