from . import Theme_MGR, themeFileInt
from os import listdir

class ThemeService:
    def __init__(self):
        self.mgr = Theme_MGR.Theme_MGR()
        for file in listdir("C:\\Max-U-Soft\\Resources\\Themes"):
            if file.endswith(".theme"):
                theme_settings = themeFileInt.read_theme_file(f"C:\\Max-U-Soft\\Resources\\Themes\\{file}")
                if "name" in theme_settings:
                    self.mgr.add_theme(theme_settings["name"], theme_settings)
    
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