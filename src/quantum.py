import numpy as np

H = 1/(2**0.5) * np.array([
    [1, 1],
    [1, -1]
])

PauliX = np.array([
    [0, 1],
    [1, 0]
])

PauliY = np.array([
    [0, 1j],
    [-1j, 0]
])

PauliZ = np.array([
    [1, 0],
    [0, -1]
])
