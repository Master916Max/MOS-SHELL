from .system import *
from .windows import *

def main():
    mwch: WCH   = create_window_class("Test", titel="Test Windows")
    mwh: WH     =create_window(mwch)
    open_window(mwh)
    sleep(1)
    close_window(mwh)
    destroy_window(mwh)
    delete_window_class(mwch)

def window_handler(event,**kwargs):
    if event == WM_PAINT:
        kwargs["screen"].fill(WHITE)
    else:
        return
        DefaultWMHandler(event, kwargs)
