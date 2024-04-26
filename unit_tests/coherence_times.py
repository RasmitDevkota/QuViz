import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

t0 = 0.1E-6
T1 = int(15E-6/t0)
T2 = int(7.5E-6/t0)

Omega2pi = 4.6E6

basis_gates = ["id", "u", "cz", "ccz", "cp"]

coherence_error_id = thermal_relaxation_error(T1,  T2, 0/t0)
coherence_error_1q = thermal_relaxation_error(T1,  T2, 1/Omega2pi/t0)
coherence_error_2q = thermal_relaxation_error(T1,  T2, 1.207/Omega2pi/t0)
coherence_error_3q = thermal_relaxation_error(T1,  T2, 1.751/Omega2pi/t0)

noise_model = NoiseModel(basis_gates=basis_gates)
noise_model.add_all_qubit_quantum_error(coherence_error_id, ["id"])
noise_model.add_all_qubit_quantum_error(coherence_error_1q, ["u"])

print(noise_model)

noisy_sim = AerSimulator(noise_model=noise_model)

n_steps = 2 * T1
simulation_runtime = round(2 * n_steps * 1/Omega2pi/t0)
shots = 8000

times = 1/Omega2pi/t0 * np.array(list(range(n_steps)))/T1
observed_counts_list = []
expected_counts_list = []

print(T1, T2, n_steps, simulation_runtime, 1/Omega2pi/t0)
for t in range(n_steps):
    qc = QuantumCircuit(1, 1)

    for i in range(t):
        qc.x(0)
        qc.x(0)

    qc.measure(0, 0)

    noisy_circuit_transpiled = transpile(qc, noisy_sim, basis_gates=basis_gates, optimization_level=0)
    result = noisy_sim.run(noisy_circuit_transpiled, shots=shots).result()
    counts = result.get_counts(noisy_circuit_transpiled)

    if t == 0:
        noisy_circuit_transpiled.draw("mpl", filename="images/decoherence_experiment.png")

    expected_counts = np.exp(-t/T1) * shots
    expected_counts_list.append(expected_counts)

    observed_counts = counts['0'] if '0' in counts else shots - counts['1']
    observed_counts_list.append(observed_counts)

    # print(f"Time {t}: {observed_counts} vs. {expected_counts}")

fig, ax = plt.subplots()
ax.scatter(times, np.array(observed_counts_list)/shots, s=5, c="red")
# ax.plot(times, expected_counts_list, c="green", label="Expected P(0)")
ax.plot(times, [0.5 for _ in range(len(times))], linestyle="--", c="blue")
plt.title("Ground state probability vs. T1-normalized simulation time", fontsize="18")
ax.set_xlabel(r'$t/T_1$', fontsize="18")
ax.set_ylabel(r'$P(0)$', fontsize="18")
ax.set_xlim([0, list(times)[-1]])
ax.set_ylim([0, 1])
plt.show()