
class SettingsPageBase:
    def __init__(self):
        pass

    def load_settings(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def save_settings(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def draw(self, screen):
        self.screen = screen
        self.draw_page()
        return self.screen

    @abstractmethod
    def draw_page(self):
        pass    
    