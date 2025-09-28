print("Please wait, loading the Shell...")

dbg = False

from startup import while_loading
import multiprocessing

lp = multiprocessing.Process(target=while_loading, kwargs={"dbg":dbg,"pict":"shell-logo.png"})

import gui

from chore.mos import MOS


def load_gui():
    os = MOS()
    root = gui.init(dbg=dbg)
    # Kill loading screen
    lp.kill()
    # Show main window
    gui.run(screen=root)

if __name__ == "__main__":
    # Start loading Screen
    lp.start()
    # Initialize GUI
    gui.startup()
    # After GUI is loaded, load the OS
    load_gui()