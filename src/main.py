from common.gui import GUI
from common.data_structures import Experiment

from common.logging import *

window = None
canvas = None

def main():
    log("INFO", "Running main process")

    gui = GUI()

    gui.construct_window()

    gui.load_main_menu()

    # gui.construct_visualization_canvas()

    # qubits = []
    # for i in range(5):
    #     for j in range(5):
    #         qubit = gui.prepare_qubit((i*100+100, j*100+100))
    #         qubits.append(qubit)
    
    # for qubit in qubits:
    #     gui.transport_qubit(qubit, [(50, 50) for _ in range(10)])
    #     # gui.transport_qubit(qubit, [(50, 50) for _ in range(10)])

    gui.window.mainloop()

    return 0

if __name__ == "__main__":    
    main()
