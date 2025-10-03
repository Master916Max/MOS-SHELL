from chore.mos import mos_app


class WindowHelper:
    @staticmethod
    def init_window(window_config: dict):
        if window_config.get("type_id") == "TERMINAL":
            from Components.mos_terminal import MosTerminal
            window = MosTerminal(window_config)
        elif window_config.get("type_id") == "SETTINGS":
            from Components.mos_settings import MosSettings
            window = MosSettings(window_config)
        elif window_config.get("type_id") == "RUN_DIALOG":
            from Components.mos_run import MosRunDialog
            window = MosRunDialog(window_config)
        else:
            from Components.mos_window import MosWindow
            window = MosWindow(window_config)
        mos_app.add_window(window)
        return window

    @staticmethod
    def destroy_window(window):
        mos_app.remove_window(window)
