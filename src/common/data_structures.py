import numpy as np

from common.constants import PROG_EPSILON

class Experiment:
    """
    Experiments are the primary product of the initialization stage,
    composed of (i) the circuit to be run and (ii) experiment parameters,
    such as atom array options and performance metrics
    """

    def __init__(self):
        self.n_qubits = 1
        self.qubits = np.ones((1, self.n_qubits), dtype=complex) * PROG_EPSILON
    
    def add_qubit(self, index=-1):
        self.n_qubits += 1

        if index == -1:
            self.qubits = np.append(self.qubits, PROG_EPSILON)
        else:
            self.qubits = np.insert(self.qubits, index, PROG_EPSILON)
    
    def qasm_to_circuit(self):
        return NotImplemented
    
    def circuit_to_qasm(self):
        return NotImplemented

class AtomArray:
    def __init__(self, n_rows=16, sites_per_row=16, row_spacing=4, site_spacing=4):
        # @TODO - load/store the other important variables that the user can give us

        # @TODO - allow for non-rectangular grids
        self.n_rows = n_rows
        self.sites_per_row = sites_per_row
        self.n_qubits = n_rows * sites_per_row
        self.row_spacing = row_spacing
        self.site_spacing = site_spacing

        self.qubits = []
        for i in range(0, n_rows):
            for j in range(0, sites_per_row):
                self.qubits.append({
                    "position": (i*row_spacing, j*site_spacing),
                    "state": complex(PROG_EPSILON, PROG_EPSILON)
                })
    
    def prepare_qubits(self, target_qubits=[], initial_states=[]):
        if len(qubit_list) == 0:
            # Prepare all qubits
            qubit_list = [q for q in range(self.n_qubits)]

        for q in qubit_list:
            initial_state_raw = initial_states[q]

            # @TODO - incorporate State Preparation error
            initial_state = initial_state_raw

            self.qubits[q].state = initial_state

    def measure_all(self):
        return NotImplemented

    def run_experiment(self, experiment):
        return NotImplemented
