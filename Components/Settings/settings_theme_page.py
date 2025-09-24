from .settings_base_page import SettingsPageBase as SPB

class SettingsThemePage(SPB):
    def __init__(self):
        super().__init__()
        self.themes = []


    def load_settings(self):
        pass

    def save_settings(self):
        # Save theme settings to a file or database
        pass

    def reload_themes(self):
        pass

    def draw_page(self):
        # Draw the theme settings page
        #print(f"Drawing Theme Settings Page with theme: {self.theme}")