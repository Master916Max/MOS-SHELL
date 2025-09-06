from typing import List, Tuple

from Components.mos_window import MosWindow


class MOS(object):
    """
    Class to handle OS initialization and management.
    """
    def __init__(self):
        self.name = "MOS"
        self.version = "0.1"
        self.author = "Your Name"
        self.open_windows:List[Tuple[str, MosWindow]] = []

    def start(self):
        print(f"Starting {self.name} version {self.version} by {self.author}")
        # Add more startup logic here

    def open_window(self, window):
        self.open_windows.append((window.id, window))
        print(f"Opened window: {window.id}")

    def close_window(self, window):
        if (window.id, window) in self.open_windows:
            self.open_windows.remove(window)
            print(f"Closed window: {window}")
        else:
            print(f"Window not found: {window}")