import Definds

class Background:
    def __init__(self, mode, colors: list[tuple[int]] = None, file = None):
        self.mode = mode
        self.colors = colors
        self.file = file
        pass

    def render_bg(self,screen: Definds.Surface):
        match(self.mode):
            case "solid":
                screen.fill(self.colors[0])
            case "gradient":
                pass
            case "picture":
                pass
        return screen
    
    def update(setting):
        pass