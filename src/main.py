from common.gui import GUI
from common.experiment import Experiment
from common.logging import *

def main():
    log("INFO", "Running main process")

    gui = GUI()

    gui.construct_window()

    gui.load_main_menu()

    gui.window.mainloop()

    return 0

if __name__ == "__main__":    
    main()
