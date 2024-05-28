import numpy as np

n_qubits = 5
circuit = [
    [
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [0]}
    ],
    [
        {'instruction': 'CZ', 'parameters': [], 'qubits': [0, 1]},
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [2]},
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [3]}
    ],
    [
        {'instruction': 'CP', 'parameters': [3.141592653589793], 'qubits': [2, 3]}
    ],
    [
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [3]},
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [4]}
    ]
]

occupied_qubits_list = []
for l, layer in enumerate(circuit):
    occupied_qubits_list.append([])

    for operation in layer:
        occupied_qubits_list[l].extend(operation["qubits"])

    # print(set(occupied_qubits))
    # print(set(range(0, n_qubits)))
    
    unoccupied_qubits = set(range(0, n_qubits)) - set(occupied_qubits_list[l])

    print(f"layer {l} unoccupied_qubits: {unoccupied_qubits}")

    if l > 0:
        doubly_unoccupied_qubits = []
        for unoccupied_qubit in unoccupied_qubits:
            if unoccupied_qubit not in occupied_qubits_list[l-1]:
                print(f"doubly-unoccupied qubit {unoccupied_qubit}, performing DD")
                doubly_unoccupied_qubits.append(unoccupied_qubit)
        
        if len(doubly_unoccupied_qubits) > 0:
            dynamical_decoupling_operation = {
                "instruction": "U",
                "parameters": [0, 0, np.pi],
                "qubits": doubly_unoccupied_qubits
            }
                    
            circuit[l-1].append(dynamical_decoupling_operation)
            circuit[l].append(dynamical_decoupling_operation)

            occupied_qubits_list[l-1].extend(doubly_unoccupied_qubits)
            occupied_qubits_list[l].extend(doubly_unoccupied_qubits)

print(circuit)

"""
result = [
    [
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [0]},
        {'instruction': 'U', 'parameters': [0, 0, 3.141592653589793], 'qubits': [4]}
    ],
    [
        {'instruction': 'CZ', 'parameters': [], 'qubits': [0, 1]},
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [2]},
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [3]},
        {'instruction': 'U', 'parameters': [0, 0, 3.141592653589793], 'qubits': [4]}
    ],
    [
        {'instruction': 'CP', 'parameters': [3.141592653589793], 'qubits': [2, 3]},
        {'instruction': 'U', 'parameters': [0, 0, 3.141592653589793], 'qubits': [0, 1]}
    ],
    [
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [3]},
        {'instruction': 'U', 'parameters': [1.5707963267948966, 0, 3.141592653589793], 'qubits': [4]},
        {'instruction': 'U', 'parameters': [0, 0, 3.141592653589793], 'qubits': [0, 1]}
    ]
]
"""
