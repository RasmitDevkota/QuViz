import numpy as np
import random

import quantum

class Simulation:
    def __init__(self, experiment: dict, gui):
        # @TODO - load/store the other important variables that the user can give us

        # GUI handler
        self.gui = gui

        # Load experiment if given
        if experiment:
            self.load_experiment(experiment)
    
    def load_experiment(self, experiment: dict = None):
        self.n_qubits = experiment["n_qubits"]
        self.qubits = []

        self.circuit = experiment["circuit"]

        self.parameters = experiment["parameters"]
        
        # Univeral atom array parameters
        self.array_width = self.parameters["array_width"]
        self.array_height = self.parameters["array_height"]
        self.row_spacing = self.parameters["row_spacing"]
        self.site_spacing = self.parameters["site_spacing"]

        # Zone separation
        self.vertical_zone_separation = self.parameters["zone_separation"]

        # Readout zone parameters
        self.n_rows_readout = self.parameters["n_rows_readout"]
        self.sites_per_row_readout = self.parameters["sites_per_row_readout"]
        self.readout_zone_begin = np.array([0, 0])
        self.readout_zone_end = self.readout_zone_begin + np.array([self.sites_per_row_readout * self.site_spacing, self.n_rows_readout * self.row_spacing])

        # Entanglement zone parameters
        self.n_rows_entanglement = self.parameters["n_rows_entanglement"]
        self.sites_per_row_entanglement = self.parameters["sites_per_row_entanglement"]
        self.entanglement_zone_begin = self.readout_zone_end + np.array([0, self.vertical_zone_separation])
        self.entanglement_zone_end = self.entanglement_zone_begin + np.array([self.sites_per_row_entanglement * self.site_spacing, self.n_rows_entanglement * self.row_spacing])

        # Storage zone parameters
        self.n_rows_storage = self.parameters["n_rows_storage"]
        self.sites_per_row_storage = self.parameters["sites_per_row_storage"]
        self.storage_zone_begin = self.entanglement_zone_end + np.array([0, self.vertical_zone_separation])
        self.storage_zone_end = self.storage_zone_begin + np.array([self.array_height, self.n_rows_storage * self.row_spacing])

        # Transport parameters
        self.transport_axis_offset = self.parameters["transport_axis_offset"]
        self.max_transport_speed = self.parameters["max_transport_speed"]
        self.min_transport_speed = self.parameters["min_transport_speed"]

        self.prepare_qubit_positions(
            target_qubits=[],
            initial_positions=(self.parameters["initial_positions"] if "initial_positions" in self.parameters.keys() else [])
        )
    
    def prepare_qubit_positions(self, target_qubits=[], initial_positions=[]):
        if len(target_qubits) == 0 or len(initial_positions) == 0:
            # Prepare all qubits in a rectangular grid
            target_qubits = self.qubits

            for i in range(0, self.n_rows_storage):
                for j in range(0, self.sites_per_row_storage):
                    position_row = i * self.row_spacing
                    position_site = j * self.site_spacing

                    initial_positions.append((position_site, position_row))

        for q in target_qubits:
            if random.random() <= self.parameters["epsilon_fill"]:
                break

            initial_position_raw = initial_positions[q]

            for i in range(0, self.n_rows_storage):
                for j in range(0, self.sites_per_row_storage):
                    initial_position_site = initial_position_raw[0] + np.random.normal(scale=self.parameters["delta_x"])
                    initial_position_row = initial_position_raw[1] + np.random.normal(scale=self.parameters["delta_y"])

            delta_position = self.qubits[q]["position"] - (initial_position_site, initial_position_row)
            
            self.qubits[q]["position"] = (initial_position_site, initial_position_row)
            self.gui.transport_qubit_widget(self.qubits[q]["widget"], delta_position)
        
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

            self.qubits[q]["state"] = initial_state
        
        return True
    
    def parallel_transport(self, movements=[]):
        if len(movements) == 0:
            # Movements must be specified!
            return False
        
        for movement in movements:
            for tq in movement["qubits"]:
                # @TODO - Computations

                # Visualization updates
                self.gui.transport_qubit_widget(self.qubits[tq]["widget"], movement["movement"])

        return True

    def run_experiment(self, experiment: dict = None):
        # @TODO - Integrate with visualizations

        if experiment:
            self.load_experiment(experiment)

        for layer in self.circuit:
            # @TODO - Parallelize visualizations for operations within each layer (as much as possible)
            for operation in layer:
                match operation["instruction"]:
                    case "H":
                        for qubit in operation["qubits"]:
                            self.qubits[qubit]["state"] = np.matmul(quantum.H, self.qubits[qubit]["state"])
                    case "X":
                        for qubit in operation["qubits"]:
                            self.qubits[qubit]["state"] = np.matmul(quantum.PauliX, self.qubits[qubit]["state"])
                    case "Y":
                        for qubit in operation["qubits"]:
                            self.qubits[qubit]["state"] = np.matmul(quantum.PauliY, self.qubits[qubit]["state"])
                    case "Z":
                        for qubit in operation["qubits"]:
                            self.qubits[qubit]["state"] = np.matmul(quantum.PauliZ, self.qubits[qubit]["state"])
                    case "CZ":
                        # Offset all qubits before transport
                        transport_offset = self.parameters["minimum_spacing"]
                        self.parallel_transport([{
                            "qubits": operation["qubits"],
                            "movement": np.array([transport_offset, transport_offset]),
                            "movement_velocity": self.max_transport_speed * np.array([1, 1])
                        }])

                        # Calculate transport duration such that all qubits arrive at the same time
                        next_empty_row = 0
                        next_empty_site = 0

                        max_L1_distance = 0
                        for q in operation["qubits"]:
                            next_empty_position = np.array([next_empty_site * self.site_spacing, next_empty_row * self.row_spacing])
                            L1_distance = sum(abs(next_empty_position - self.qubits[q]["position"]))

                            max_L1_distance = max(max_L1_distance, L1_distance)

                            next_empty_row += 1
                            next_empty_site += 1
                        
                        transport_duration = max_L1_distance/self.max_transport_speed

                        next_empty_row = 0
                        next_empty_site = 0

                        for q in operation["qubits"]:
                            next_empty_position = np.array([next_empty_site * self.site_spacing, next_empty_row * self.row_spacing])
                            displacement_vector = next_empty_position - self.qubits[q]["position"]
                            L1_distance = sum(abs(displacement_vector))

                            # Move horizontally
                            self.parallel_transport([{
                                "qubits": operation["qubits"],
                                "movement": np.array([displacement_vector[0], 0]),
                                "movement_velocity": L1_distance/transport_duration
                            }])

                            # Move vertically
                            self.parallel_transport([{
                                "qubits": operation["qubits"],
                                "movement": np.array([0, displacement_vector[1]]),
                                "movement_velocity": L1_distance/transport_duration
                            }])

                            next_empty_row += 1
                            next_empty_site += 1
                    case _:
                        continue

        return True
