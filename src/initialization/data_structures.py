import numpy as np

from common.constants import PROG_EPSILON

class Circuit:
    def __init__(self):
        self.n_qubits = 1
        self.qubits = np.ones((1, self.n_qubits), dtype=complex) * PROG_EPSILON
    
    def add_qubit(self, pos=-1):
        self.n_qubits += 1

        if pos == -1:
            self.qubits = np.append(self.qubits, PROG_EPSILON)
        else:
            self.qubits = np.insert(self.qubits, pos, PROG_EPSILON)
