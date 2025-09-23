from . import Theme_MGR, themeFileInt
from multiprocessing.connection import PipeConnection
from os import listdir

class ThemeService:
    def __init__(self, theme_pipe : PipeConnection = None, theme_return_pipe : PipeConnection = None):
        self.mgr = Theme_MGR.Theme_MGR()
        self.theme_pipe = theme_pipe
        self.theme_return_pipe = theme_return_pipe
        try:
            for file in listdir("C:\\Max-U-Soft\\Resources\\Themes"):
                if file.endswith(".theme"):
                    theme_settings = themeFileInt.read_theme_file(f"C:\\Max-U-Soft\\Resources\\Themes\\{file}")
                    if "name" in theme_settings:
                        self.mgr.add_theme(theme_settings["name"], theme_settings)
        except Exception as e:
            print(f"Error loading themes: {e}")
        #
        # Load a default theme
        #       
        try:
            default_theme = themeFileInt.read_theme_file("Basic.theme")
            if "name" in default_theme:
                self.mgr.add_theme("Basic", default_theme)
        except Exception as e:
            raise Exception(f"Error loading default theme: {e}\n\n Make sure Basic.theme is in the working directory.")

    
    def get_manager(self):
        return self.mgr

    def load_theme(self, file_path: str) -> bool:
        theme_settings = themeFileInt.read_theme_file(file_path)
        if "name" in theme_settings:
            self.mgr.add_theme(theme_settings["name"], theme_settings)
            return True
        return False

    def save_theme(self, name: str, file_path: str) -> bool:
        theme = self.mgr.get_theme(name)
        if theme:
            try:
                with open(file_path, "w") as f:
                    for key, value in theme.items():
                        if isinstance(value, tuple):
                            value = ",".join(map(str, value))
                        f.write(f"{key}={value}\n")
                return True
            except IOError:
                return False
        return False
    
    def run(self):
        while True:
            if self.theme_pipe.poll():
                command, data = self.theme_pipe.recv()
                if command == "LOAD_THEME":
                    success = self.load_theme(data)
                    self.theme_return_pipe.send(("LOAD_THEME_RESPONSE", success))
                elif command == "SAVE_THEME":
                    name, file_path = data
                    success = self.save_theme(name, file_path)
                    self.theme_return_pipe.send(("SAVE_THEME_RESPONSE", success))
                elif command == "LIST_THEMES":
                    themes = self.mgr.list_themes()
                    self.theme_return_pipe.send(("LIST_THEMES_RESPONSE", themes))
                elif command == "GET_ACTIVE_THEME":
                    theme = self.mgr.get_enabled_theme()
                    if theme:
                        self.theme_return_pipe.send(("GET_THEME_RESPONSE", theme))
                    else:
                        self.theme_return_pipe.send(("GET_THEME_RESPONSE", None))
                elif command == "UNLOAD_THEME":
                    theme_name = data
                    self.mgr.remove_theme(theme_name)
                    self.theme_return_pipe.send(("UNLOAD_THEME_RESPONSE", True))
                elif command == "SHUTDOWN":
                    break