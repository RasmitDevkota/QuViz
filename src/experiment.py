import numpy as np

# Experiments are the primary product of the initialization stage,
# composed of (i) the circuit to be run and (ii) experiment parameters,
# such as atom array options and performance metrics
experiment = {
    "n_qubits": 1,
    "circuit": [],
    "parameters": {},
}

def qasm_to_circuit(circuit_qasm_str):
    return NotImplemented

def circuit_to_qasm(experiment):
    # Base string
    circuit_qasm_str = f"OPENQASM 3;\n\ninclude \"stdgates.inc\";\n\n"

    # Declare qubits
    circuit_qasm_str = f"qubit[{experiment['n_qubits']}] qr;\n\n"

    # Append operations
    for layer in experiment["circuit"]:
        for operation in layer:
            instruction = operation["instruction"].lower()
            qubits = "], qr[".join([str(qubit) for qubit in operation["qubits"]])

            circuit_qasm_str += f"{instruction} qr[{qubits}];\n"

    return circuit_qasm_str
