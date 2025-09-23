class ThemeMGR:
    def __init__(self):
        self.themes = {}
        self.defaultTheme = {"name": "Basic", "bg_color": (30, 30, 30), "fg_color": (200, 200, 200), "font": "Fira Code",
                             "font_size": 15, "syscolor": (192, 199, 200), "BG": (87,168,168), "TBC": (30,61,88),
                             "textcolor": (0, 0, 0), "noneselectcolor": (100, 100, 100),
                             "window_select_color": (0, 0, 168),
                             "msgtextcolor": (0, 0, 0), "msgbgcolor": (240, 240, 240), "msgbuttoncolor": (200, 200, 200),}
        self.enabledTheme = self.defaultTheme
        self.themes["Basic"] = self.defaultTheme
        self.themes["Dark"] = {"name": "Dark", "bg_color": (20, 20, 20), "fg_color": (220, 220, 220),
                               "font": "Courier New", "font_size": 16}

    def add_theme(self, name, theme):
        self.themes[name] = theme

    def get_theme(self, name):
        return self.themes.get(name, None)

    def list_themes(self):
        return list(self.themes.keys())

    def enable_theme(self, name):
        if name in self.themes:
            self.enabledTheme = self.themes[name]
            return True
        return False

    def get_enabled_theme(self):
        return self.enabledTheme

    def reset_to_default(self):
        self.enabledTheme = self.defaultTheme

    def remove_theme(self, name):
        if name in self.themes and name != "Basic":
            del self.themes[name]
            return True
        return False

    def update_theme(self, name, theme):
        if name in self.themes:
            self.themes[name] = theme
            return True
        return False

    def is_theme_enabled(self, name):
        return self.enabledTheme["name"] == name


theme_mgr = ThemeMGR()
