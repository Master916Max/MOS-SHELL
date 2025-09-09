from Components.mos_window import MosWindow


class MosTerminal(MosWindow):
    def __init__(self, title, width, height, logo=None, parent=None, zlayer=None, type_id='TERMINAL'):
        super().__init__(title, width, height, logo, parent, zlayer, type_id)
