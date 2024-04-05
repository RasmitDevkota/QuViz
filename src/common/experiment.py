import numpy as np

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
