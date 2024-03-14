from common.logging import *

from common.gui import load_gui

from common.data_structures import Experiment

def main():
    log("INFO", "Running main process")
    
    # load gui
    gui_handler = load_gui()

    # load to main menu
    gui_handler.load("main_menu")

    return 0

if __name__ == "__main__":    
    main()
