from threading import RLock


class MOS(object):
    """
    Class to handle OS initialization and management.
    """
    def __init__(self):
        self.name = "MOS"
        self.version = "0.1"
        self.author = "Your Name"
        self.open_windows = list([])
        self._lock = RLock()          # optional
        self._active = None           # the “pointer” to the active item

        for it in self.open_windows:
            if it.is_active:
                if self._active is None:
                    self._active = it
                else:
                    it.is_active = False  # demote extras

    @property
    def active(self):
        return self._active

    def add_window(self, window):
        self.open_windows.append(window)
        print(f"Added window: {window.id}")
        # set the new window active
        self._set_active_locked(window)

    def remove_window(self, window):
        if window in self.open_windows:
            self.open_windows.remove(window)
            print(f"Removed window: {window}")
        else:
            print(f"Window not found: {window}")
        self.clear_active()

    def set_active(self, window):
        with self._lock:
            if window not in self.open_windows:
                print("Item is not managed by this manager.")
            self._set_active_locked(window)

    def clear_active(self):
        with self._lock:
            if self._active is not None:
                self._active.is_active = False
                self._active = None

    def _set_active_locked(self, window):
        if self._active is window:
            return
        if self._active is not None:
            self._active.is_active = False
        window.is_active = True
        self._active = window


mos_app = MOS()
