from os import listdir
from theme.theme_mgr import theme_mgr
from theme.theme_file_read import read_theme_file


class ThemeService:
    def __init__(self):
        self.mgr = theme_mgr
        try:
            for file in listdir("C:\\Max-U-Soft\\Resources\\Themes"):
                if file.endswith(".theme"):
                    theme_settings = read_theme_file(f"C:\\Max-U-Soft\\Resources\\Themes\\{file}")
                    if "name" in theme_settings:
                        self.mgr.add_theme(theme_settings["name"], theme_settings)
        except Exception as e:
            print(f"Error loading themes: {e}")
        #
        # Load a default theme
        #       
        try:
            default_theme = read_theme_file("Basic.theme")
            if "name" in default_theme:
                self.mgr.add_theme("Basic", default_theme)
        except Exception as e:
            print(f"Error loading default theme: {e}\n\n Make sure Basic.theme is in the working directory.")

    
    def get_manager(self):
        return self.mgr

    def load_theme(self, file_path: str) -> bool:
        theme_settings = read_theme_file(file_path)
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

    def get_theme(self, name: str) -> dict:
        return self.mgr.get_theme(name)

theme_service = ThemeService()