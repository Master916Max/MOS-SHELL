
class Theme_MGR:
    def __init__(self):
        self.themes = {}
        self.defaultTheme = {"name": "Basic", "bg_color": (30, 30, 30), "fg_color": (200, 200, 200), "font": "Arial", "font_size": 14}
        self.enabledTheme = self.defaultTheme
        self.themes["Basic"] = self.defaultTheme
        self.themes["Dark"] = {"name": "Dark", "bg_color": (20, 20, 20), "fg_color": (220, 220, 220), "font": "Courier New", "font_size": 16}

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