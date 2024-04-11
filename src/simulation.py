import numpy as np
from threading import Lock

import datetime
import time

class Simulation:
	def __init__(self, experiment, gui):
		# @TODO - load/store the other important variables that the user can give us

		self.lock = Lock()

		# GUI handler
		self.gui = gui

		# Load experiment
		self.load_experiment(experiment)

		# Variables for running experiments
		self.layer_op_counter = 0

		self.layer_deletion_lock = Lock()
		self.layer_queue = []
	
	def run_method_lambda(self, o, method_lambda):
		method_lambda()

		print("running method lambda:", method_lambda)

		self.layer_queue[0][o] = None

		if self.layer_deletion_lock.acquire(False):
			if not any(self.layer_queue[0]):
				self.layer_queue.pop(0)

				if len(self.layer_queue) > 0:
					self.execute_next_layer()
			
			self.layer_deletion_lock.release()
	
	def schedule_operation(self, _o, _method_lambda, delay):
		self.gui.window.after(delay * 1000, lambda o=_o, method_lambda=_method_lambda : self.run_method_lambda(o, method_lambda))
		return True
	
	def push_operation(self, _method_lambda, _delay):
		self.layer_queue[-1].append(lambda layer_op_counter=self.layer_op_counter, method_lambda=_method_lambda, delay=_delay: self.schedule_operation(layer_op_counter, method_lambda, delay))
		self.layer_op_counter += 1
	
	def execute_next_layer(self):
		print("executing next layer...")

		layer_ops = self.layer_queue[0]
		for layer_op in layer_ops:
			print("executing layer operation:", layer_op)
			layer_op()
	
	def load_experiment(self, experiment = None):
		# @TODO - Verify experiment (e.g. cannot have more qubits than storage sites)

		self.n_qubits = experiment["n_qubits"]
		self.qubits = []

		self.circuit = experiment["circuit"]

		self.parameters = experiment["parameters"]

		# Universal zone parameters
		self.zone_margin_vertical = self.parameters["zone_margin_vertical"]
		self.zone_padding = np.array([self.parameters["zone_padding_horizontal"], self.parameters["zone_padding_vertical"]])

		# Storage zone parameters
		self.n_rows_storage = self.parameters["n_rows_storage"]
		self.sites_per_row_storage = self.parameters["sites_per_row_storage"]
		self.row_spacing_storage = self.parameters["row_spacing_storage"]
		self.site_spacing_storage = self.parameters["site_spacing_storage"]

		self.storage_zone_width = 2 * self.zone_padding[0] + (self.sites_per_row_storage - 1) * self.site_spacing_storage
		self.storage_zone_height = 2 * self.zone_padding[1] + (self.n_rows_storage - 1) * self.row_spacing_storage

		self.storage_zone_begin = np.array([0, 0])
		self.storage_zone_end = self.storage_zone_begin + np.array([self.storage_zone_width, self.storage_zone_height])

		# Entanglement zone parameters
		self.n_rows_entanglement = self.parameters["n_rows_entanglement"]
		self.sites_per_row_entanglement = self.parameters["sites_per_row_entanglement"]
		self.row_spacing_entanglement = self.parameters["row_spacing_entanglement"]
		self.site_spacing_entanglement = self.parameters["site_spacing_entanglement"]

		self.rydberg_blockade_radius = self.parameters["rydberg_blockade_radius"]
		
		self.entanglement_zone_width = 2 * self.zone_padding[0] + (self.sites_per_row_entanglement - 1) * (self.site_spacing_entanglement + self.rydberg_blockade_radius)
		self.entanglement_zone_height = 2 * self.zone_padding[1] + (self.n_rows_entanglement - 1) * self.row_spacing_entanglement

		self.entanglement_zone_begin = self.storage_zone_begin + np.array([0, self.storage_zone_height + self.zone_margin_vertical])
		self.entanglement_zone_end = self.entanglement_zone_begin + np.array([self.entanglement_zone_width, self.entanglement_zone_height])

		# Readout zone parameters
		self.n_rows_readout = self.parameters["n_rows_readout"]
		self.sites_per_row_readout = self.parameters["sites_per_row_readout"]
		self.row_spacing_readout = self.parameters["row_spacing_readout"]
		self.site_spacing_readout = self.parameters["site_spacing_readout"]
		
		self.readout_zone_width = 2 * self.zone_padding[0] + (self.sites_per_row_readout - 1) * self.site_spacing_readout
		self.readout_zone_height = 2 * self.zone_padding[1] + (self.n_rows_readout - 1) * self.row_spacing_readout
		
		self.readout_zone_begin = self.entanglement_zone_begin + np.array([0, self.entanglement_zone_height + self.zone_margin_vertical])
		self.readout_zone_end = self.readout_zone_begin + np.array([self.readout_zone_width, self.readout_zone_height])

		# Transport parameters
		self.transport_axis_offset = self.parameters["transport_axis_offset"]
		self.max_transport_speed = self.parameters["max_transport_speed"]
		self.min_transport_speed = self.parameters["min_transport_speed"]

		# Full atom array parameters
		self.array_width = max(self.storage_zone_width, self.entanglement_zone_width, self.readout_zone_width)
		self.array_height = self.storage_zone_height + self.entanglement_zone_height + self.readout_zone_height + self.zone_margin_vertical * 2

		# Zone visualization parameters
		self.storage_zone_begin_viz = self.storage_zone_begin/self.gui.viz_length_scale + self.gui.viz_offset_vector
		self.storage_zone_end_viz = self.storage_zone_end/self.gui.viz_length_scale + self.gui.viz_offset_vector
		self.entanglement_zone_begin_viz = self.entanglement_zone_begin/self.gui.viz_length_scale + self.gui.viz_offset_vector
		self.entanglement_zone_end_viz = self.entanglement_zone_end/self.gui.viz_length_scale + self.gui.viz_offset_vector
		self.readout_zone_begin_viz = self.readout_zone_begin/self.gui.viz_length_scale + self.gui.viz_offset_vector
		self.readout_zone_end_viz = self.readout_zone_end/self.gui.viz_length_scale + self.gui.viz_offset_vector

		self.gui.visualization_canvas.create_rectangle(*self.storage_zone_begin_viz, *self.storage_zone_end_viz, outline='purple')
		self.gui.visualization_canvas.create_rectangle(*self.entanglement_zone_begin_viz, *self.entanglement_zone_end_viz, outline='salmon')
		self.gui.visualization_canvas.create_rectangle(*self.readout_zone_begin_viz, *self.readout_zone_end_viz, outline='darkturquoise')

		# Physical parameters
		self.T1_time = self.parameters["T1_time"]
		self.T2_time = self.parameters["T2_time"]
		self.atom_loss_pre = self.parameters["atom_loss_pre"]
		self.atom_loss_post = self.parameters["atom_loss_post"]
		self.measurement_fidelity = self.parameters["measurement_fidelity"]

		print(self.storage_zone_begin/self.gui.viz_length_scale, self.storage_zone_end/self.gui.viz_length_scale)
		print(self.entanglement_zone_begin/self.gui.viz_length_scale, self.entanglement_zone_end/self.gui.viz_length_scale)
		print(self.readout_zone_begin/self.gui.viz_length_scale, self.readout_zone_end/self.gui.viz_length_scale)
	
	def prepare_qubit_positions(self, target_qubits=[], initial_positions=[]):
		if len(target_qubits) == 0 or len(initial_positions) == 0:
			if len(self.qubits) == 0:
				for _ in range(self.n_qubits):
					random_initial_position = np.array([
						0, 0
						# np.random.normal(loc=self.array_width/2, scale=self.array_width/2**0.5),
						# np.random.normal(loc=self.array_height/2, scale=self.array_height/2**0.5)
					])

					self.qubits.append({
						"position": random_initial_position,
						"widget": self.prepare_qubit_widget(random_initial_position)
					})
			
			target_qubits = [q for q in range(len(self.qubits))]

			sites_filled = 0
			for i in range(0, self.n_rows_storage):
				for j in range(0, self.sites_per_row_storage):
					position_row = i * self.row_spacing_storage
					position_site = j * self.site_spacing_storage

					initial_position = np.array([position_site, position_row]) + self.storage_zone_begin + self.zone_padding

					initial_positions.append(initial_position)

					sites_filled += 1

					if sites_filled >= len(target_qubits):
						break
				else:
					continue

				break

		for i, tq in enumerate(target_qubits):
			initial_position_raw = initial_positions[i]

			initial_position = initial_position_raw + np.array([np.random.normal(scale=self.parameters["delta_x"]), np.random.normal(scale=self.parameters["delta_y"])])

			delta_position = initial_position - self.qubits[tq]["position"]
			
			self.qubits[tq]["position"] = initial_position

			self.transport_qubit_widget([{
				"qubit": self.qubits[tq]["widget"],
				"movement": delta_position,
				"movement_velocity": self.max_transport_speed * np.array([1, 1])
			}])
		
		return True
	
	# @TODO - Reformulate using Statevector
	def prepare_qubit_states(self, target_qubits=[], initial_states=[]):
		if len(target_qubits) == 0:
			# Prepare all qubits
			target_qubits = self.qubits
		
		if len(initial_states) == 0:
			# All (ideally) start in the 0 state
			initial_states = [np.array([1+0j, 0+0j]) for q in range(self.n_qubits)]

		for q in target_qubits:
			initial_state_raw = initial_states[q]

			# @TODO - Incorporate state preparation error
			initial_state = initial_state_raw

			self.qubits[q]["state"] = initial_state
		
		return True
	
	# @TODO - Reformulate using Statevector
	def apply_unitary(self, qubit, theta, alpha, beta):
		unitary_matrix = np.array([
			[np.cos(theta/2), -np.exp(1j * beta) * np.sin(theta/2)],
			[np.exp(1j * alpha) * np.sin(theta/2), np.exp(1j * (alpha + beta)) * np.cos(theta/2)]
		])

		self.qubits[qubit]["state"] = np.matmul(unitary_matrix, self.qubits[qubit]["state"])

		return True
	
	# @TODO - Reformulate using Statevector
	def measure_qubits(self, qubits=[]):
		# Loop through each qubit
		for qubit in qubits:
			if np.random.random() <= self.atom_loss_post:
				probability_0 = 0
			else:
				probability_0 = np.abs(self.qubits[qubit]["state"][0])**2
			
			# Collapse state to 0 probabilistically, also accounting for measurement fidelity
			if np.random.random() <= probability_0 and np.random.random() <= self.measurement_fidelity:
				self.qubits[qubit]["state"] = np.array([1, 0])
			else:
				self.gui.expel_qubit_widget(self.qubits[qubit]["widget"])
				
				self.qubits[qubit]["state"] = np.array([0, 1])

		return True

	def prepare_qubit_widget(self, initial_position):
		initial_position = initial_position/self.gui.viz_length_scale + self.gui.viz_offset_vector

		qubit = self.gui.visualization_canvas.create_oval(initial_position[0] - self.gui.qubit_radius,
			initial_position[1] - self.gui.qubit_radius,
			initial_position[0] + self.gui.qubit_radius,
			initial_position[1] + self.gui.qubit_radius,
			fill="springgreen", outline="greenyellow", width=4)
		
		print("placed qubit!")

		return qubit

	def transport_qubit_widget(self, movements):
		# @TODO - Solve scale issues
		for m, movement in enumerate(movements):
			total_movement_vector = movement["movement"]/self.gui.viz_length_scale
			total_movement_distance = np.linalg.norm(total_movement_vector)

			movement_speed = np.linalg.norm(movement["movement_velocity"]) #/ self.gui.viz_length_scale
			time_needed = total_movement_distance/movement_speed
			steps_needed = int(np.ceil(time_needed/self.gui.movement_step_time))
			movement_step_size = total_movement_distance/steps_needed
			
			unit_movement_vector = total_movement_vector/np.linalg.norm(total_movement_vector)
			step_movement_vector = movement_step_size * unit_movement_vector

			for step in range(steps_needed):
				method_lambda = lambda: self.gui.visualization_canvas.move(movement["qubit"], *step_movement_vector)

				self.push_operation(method_lambda, self.gui.movement_step_time * (step + 1))
		
		return True
	
	def expel_qubit_widget(self, qubit):
		method_lambda = lambda: self.visualization_canvas.delete(qubit)
		self.push_operation(method_lambda, 0)

		return True
	
	def compile_experiment(self, experiment = None):
		next_empty_row = 0
		next_empty_site = 0

		if experiment:
			self.load_experiment(experiment)
		
		self.layer_queue.append([])
		self.prepare_qubit_positions(target_qubits=[], initial_positions=self.parameters["initial_positions"] if "initial_positions" in self.parameters.keys() else [])

		for layer in self.circuit:
			self.layer_queue.append([])
			self.layer_op_counter = 0

			# @TODO - Schedule calculations instead of performing immediately
			for operation in layer:
				match operation["instruction"]:
					case "H":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, np.pi/2, 0, np.pi)
					case "S":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, 0, 0, np.pi/2)
					case "Sdg":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, 0, 0, -np.pi/2)
					case "T":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, 0, 0, np.pi/4)
					case "RX":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, operation["parameters"]["theta"], -np.pi/2, np.pi/2)
					case "RY":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, operation["parameters"]["theta"], 0, 0)
					case "RX":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, 0, 0, operation["parameters"]["theta"])
					case "X":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, np.pi, 0, np.pi)
					case "Y":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, np.pi, np.pi/2, np.pi)
					case "Z":
						for qubit in operation["qubits"]:
							self.apply_unitary(qubit, 0, 0, np.pi)
					case "CZ":
						# Offset all qubits before transport
						transport_offset = min(1E-6, int(np.ceil(self.site_spacing_storage/5)))

						# Calculate transport duration such that all qubits arrive at the same time

						displacement_vectors = []
						for i, q in enumerate(operation["qubits"]):
							next_empty_position_center = np.array([next_empty_site * self.site_spacing_entanglement, next_empty_row * self.row_spacing_entanglement])
							next_empty_position_relative = next_empty_position_center + self.rydberg_blockade_radius * np.array([q % 2 - 0.5, 0])
							next_empty_position = next_empty_position_relative + self.entanglement_zone_begin + self.zone_padding

							displacement_vector = next_empty_position - self.qubits[q]["position"]
							displacement_vectors.append(displacement_vector)

							if i % 2 == 1:
								next_empty_site += 1
								if next_empty_site >= self.sites_per_row_entanglement:
									next_empty_row += 1
									next_empty_site = 0

						L1_distances = [sum(abs(displacement_vector)) for displacement_vector in displacement_vectors]
						max_L1_distance = max(L1_distances)
						
						transport_duration = max_L1_distance/self.max_transport_speed

						# Offset
						for i, q in enumerate(operation["qubits"]):
							self.transport_qubit_widget([{
								"qubit": self.qubits[q]["widget"],
								"movement": np.array([transport_offset, transport_offset]),
								"movement_velocity": self.max_transport_speed * np.array([1, 1])
							}])

						# Move horizontally
						for i, q in enumerate(operation["qubits"]):
							self.transport_qubit_widget([{
								"qubit": self.qubits[q]["widget"],
								"movement": np.array([displacement_vectors[i][0], 0]),
								"movement_velocity": L1_distances[i]/transport_duration
							}])
						
						# Move vertically
						for i, q in enumerate(operation["qubits"]):
							self.transport_qubit_widget([{
								"qubit": self.qubits[q]["widget"],
								"movement": np.array([0, displacement_vectors[i][1]]),
								"movement_velocity": L1_distances[i]/transport_duration
							}])

						# Undo offset
						for i, q in enumerate(operation["qubits"]):
							self.transport_qubit_widget([{
								"qubit": self.qubits[q]["widget"],
								"movement": -1 * np.array([transport_offset, transport_offset]),
								"movement_velocity": self.max_transport_speed * np.array([1, 1])
							}])
						
						# # Offset
						# for i, q in enumerate(operation["qubits"]):
						# 	self.transport_qubit_widget([{
						# 		"qubit": self.qubits[q]["widget"],
						# 		"movement": np.array([transport_offset, transport_offset]),
						# 		"movement_velocity": self.max_transport_speed * np.array([1, 1])
						# 	}])
						
						# # Move back horizontally
						# for i, q in enumerate(operation["qubits"]):
						# 	self.transport_qubit_widget([{
						# 		"qubit": self.qubits[q]["widget"],
						# 		"movement": -1 * np.array([displacement_vectors[i][0], 0]),
						# 		"movement_velocity": L1_distances[i]/transport_duration
						# 	}])
						
						# # Move back vertically
						# for i, q in enumerate(operation["qubits"]):
						# 	self.transport_qubit_widget([{
						# 		"qubit": self.qubits[q]["widget"],
						# 		"movement": -1 * np.array([0, displacement_vectors[i][1]]),
						# 		"movement_velocity": L1_distances[i]/transport_duration
						# 	}])

						# # Undo offset
						# for i, q in enumerate(operation["qubits"]):
						# 	self.transport_qubit_widget([{
						# 		"qubit": self.qubits[q]["widget"],
						# 		"movement": -1 * np.array([transport_offset, transport_offset]),
						# 		"movement_velocity": self.max_transport_speed * np.array([1, 1])
						# 	}])
					case _:
						continue

		print("finished compiling experiment")

		return True

	def run_experiment(self, experiment = None):
		if experiment:
			self.load_experiment(experiment)
			self.compile_experiment(experiment)
		
		print("running experiment")
		
		self.execute_next_layer()

		print("finished running experiment")

		return True
