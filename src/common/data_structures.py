import numpy as np

from common.aquila_specs import delta_x, delta_y

class Experiment:
    """
    Experiments are the primary product of the initialization stage,
    composed of (i) the circuit to be run and (ii) experiment parameters,
    such as atom array options and performance metrics
    """

    def __init__(self):
        self.n_qubits = 1
        self.qubits = np.zeros((1, self.n_qubits), dtype=complex)
    
    def add_qubit(self, index=-1):
        self.n_qubits += 1

        if index == -1:
            self.qubits = np.append(self.qubits, 0)
        else:
            self.qubits = np.insert(self.qubits, index, 0)
    
    def qasm_to_circuit(self):
        return NotImplemented
    
    def circuit_to_qasm(self):
        return NotImplemented

class AtomArray:
    def __init__(self, n_rows=16, sites_per_row=16, row_spacing=4, site_spacing=4):
        # @TODO - load/store the other important variables that the user can give us

        # @TODO - allow for non-rectangular grid parameters
        self.n_rows = n_rows
        self.sites_per_row = sites_per_row
        self.n_qubits = n_rows * sites_per_row
        self.row_spacing = row_spacing
        self.site_spacing = site_spacing

        # Initialize all qubits randomly
        self.qubits = []
        for i in range(0, n_rows):
            for j in range(0, sites_per_row):
                self.qubits.append({
                    "position": (np.random.uniform(0,j*site_spacing), np.random.uniform(0,i*row_spacing)),
                    "state": np.array([1+0j, 1+0j])/np.sqrt(2)
                })
    
    def prepare_qubit_positions(self, target_qubits=[], initial_positions=[]):
        if len(target_qubits) == 0:
            # Prepare all qubits
            target_qubits = [q for q in range(self.n_qubits)]
        
        if len(initial_positions) == 0:
            # All start in a rectangular grid
            for i in range(0, self.n_rows):
                for j in range(0, self.sites_per_row):
                    position_row = i * self.row_spacing
                    position_site = j * self.site_spacing

                    initial_positions.append((position_row, position_site))

        for q in target_qubits:
            initial_position_raw = initial_positions[q]

            for i in range(0, self.n_rows):
                for j in range(0, self.sites_per_row):
                    initial_position_row = initial_position_raw[0] + delta_y * (np.random.randint(2) - 0.5)*2
                    initial_position_site = initial_position_raw[1] + delta_x * (np.random.randint(2) - 0.5)*2

            self.qubits[q].position = (initial_position_row, initial_position_site)
        
        return True
    
    def prepare_qubit_states(self, target_qubits=[], initial_states=[]):
        if len(target_qubits) == 0:
            # Prepare all qubits
            target_qubits = [q for q in range(self.n_qubits)]
        
        if len(initial_states) == 0:
            # All start in the 0 state
            initial_states = [np.array([1+0j, 0+0j]) for q in range(self.n_qubits)]

        for q in target_qubits:
            initial_state_raw = initial_states[q]

            # @TODO - incorporate State Preparation error
            initial_state = initial_state_raw

            self.qubits[q].state = initial_state
        
        return True

    def measure_all(self):
        return NotImplemented

    def run_experiment(self, experiment):
        return NotImplemented
