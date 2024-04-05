import numpy as np
import random

class Experiment:
    """
    Experiments are the primary product of the initialization stage,
    composed of (i) the circuit to be run and (ii) experiment parameters,
    such as atom array options and performance metrics
    """

    def __init__(self):
        self.n_qubits = 1
        self.qubits = np.zeros((1, self.n_qubits), dtype=complex)

        self.circuit = []

        self.performance_metrics = {}
    
    def add_qubit(self, index=-1):
        self.n_qubits += 1

        if index == -1:
            self.qubits = np.append(self.qubits, 0)
        else:
            self.qubits = np.insert(self.qubits, index, 0)
    
    def qasm_to_circuit(self):
        return NotImplemented
    
    def circuit_to_qasm(self):
        # Base string
        circuit_qasm_str = f"OPENQASM 3;\n\ninclude \"stdgates.inc\";\n\n"

        # Declare qubits
        circuit_qasm_str = f"qubit[{self.n_qubits}] qr;\n\n"

        # Append operations
        for operation in self.circuit:
            instruction = operation["instruction"].lower()
            qubits = "], qr[".join([str(qubit) for qubit in operation["qubits"]])

            circuit_qasm_str += f"{instruction} qr[{qubits}];\n"

        return circuit_qasm_str

class AtomArray:
    def __init__(self, gui, n_rows=16, sites_per_row=16, row_spacing=4, site_spacing=4):
        # @TODO - load/store the other important variables that the user can give us

        # GUI handler
        self.gui = gui

        # Initial position parameters
        self.n_rows = n_rows
        self.sites_per_row = sites_per_row
        self.n_qubits = n_rows * sites_per_row
        self.row_spacing = row_spacing
        self.site_spacing = site_spacing

        self.performance_metrics = {}

        # Initialize all qubits randomly
        self.qubits = []
        for i in range(0, n_rows):
            for j in range(0, sites_per_row):
                default_position = (np.random.uniform(0, j*site_spacing), np.random.uniform(0, i*row_spacing))
                default_state = np.array([1+0j, 1+0j])/np.sqrt(2)

                qubit = gui.prepare_qubit(default_position)

                self.qubits.append({
                    "position": default_position,
                    "state": default_state,
                    "graphics": qubit,
                })
        
        # Variables for use during experiment
        active_transports = 0
    
    def prepare_qubit_positions(self, target_qubits=[], initial_positions=[]):
        if len(target_qubits) == 0 or len(initial_positions) == 0:
            # Prepare all qubits in a rectangular grid
            target_qubits = self.qubits

            for i in range(0, self.n_rows):
                for j in range(0, self.sites_per_row):
                    position_row = i * self.row_spacing
                    position_site = j * self.site_spacing

                    initial_positions.append((position_row, position_site))

        for q in target_qubits:
            if random.random() <= self.performance_metrics["epsilon_fill"]:
                break

            initial_position_raw = initial_positions[q]

            for i in range(0, self.n_rows):
                for j in range(0, self.sites_per_row):
                    initial_position_row = initial_position_raw[0] + \
                        self.performance_metrics["delta_y"] * (np.random.randint(2) - 0.5)*2
                    initial_position_site = initial_position_raw[1] + \
                        self.performance_metrics["delta_x"] * (np.random.randint(2) - 0.5)*2

            delta_position = self.qubits[q]["position"] - (initial_position_row, initial_position_site)
            
            self.qubits[q]["position"] = (initial_position_row, initial_position_site)
            self.gui.transport_qubit(self.qubits[q]["qubit"], delta_position)
        
        return True
    
    def prepare_qubit_states(self, target_qubits=[], initial_states=[]):
        if len(target_qubits) == 0:
            # Prepare all qubits
            target_qubits = self.qubits
        
        if len(initial_states) == 0:
            # All start in the 0 state
            initial_states = [np.array([1+0j, 0+0j]) for q in range(self.n_qubits)]

        for q in target_qubits:
            initial_state_raw = initial_states[q]

            # @TODO - incorporate state preparation error
            initial_state = initial_state_raw

            self.qubits[q].state = initial_state
        
        return True
    
    def transport_qubits(self, movements=[]):
        if len(movements) == 0:
            # Movements must be specified!
            return False
        
        for movement in movements:
            for target_qubit in movement["target_qubits"]:
                # @TODO - Computations


                # Visualization updates
                self.gui.transport_qubit(target_qubit, movement["movement"])

        return True
    
    def H(self, target_qubits):
        return NotImplemented
    
    def RotX(self, target_qubits):
        return NotImplemented
    
    def RotY(self, target_qubits):
        return NotImplemented
    
    def RotZ(self, target_qubits):
        return NotImplemented
    
    def PauliX(self, target_qubits):
        return NotImplemented
    
    def PauliY(self, target_qubits):
        return NotImplemented
    
    def PauliZ(self, target_qubits):
        return NotImplemented
    
    def CX(self, target_qubits):
        return NotImplemented
    
    def CY(self, target_qubits):
        return NotImplemented
    
    def CZ(self, target_qubits):
        for qubit in target_qubits[0]:
            pass

        return True

    def measure_all(self):
        return NotImplemented

    def run_experiment(self, experiment):
        self.performance_metrics = experiment.performance_metrics

        for operation in experiment.circuit:
            match operation["instruction"]:
                case "H":
                    pass

        return True
