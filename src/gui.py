import numpy as np
from threading import Lock
import datetime

from tkinter import *

import hardware_presets
from simulation import Simulation

from qiskit import QuantumCircuit, qasm3
from qiskit.circuit import CircuitInstruction

class GUI:
	def __init__(self, window_width=800, window_height=800):
		self.window_width = window_width
		self.window_height = window_height
		
		self.viz_length_scale = 1E-6/5
		self.viz_time_scale = 10E-6 * 1000

		self.viz_offset_horizontal = 75
		self.viz_offset_vertical = 75
		self.viz_offset_vector = np.array([self.viz_offset_horizontal, self.viz_offset_vertical])

		self.qubit_radius = 1E-6/self.viz_length_scale
		self.movement_step_time = 1

		self.qasm_text = None

		self.temporaryStorage = {}

	def construct_window(self):
		self.window = Tk()
		self.window.title("QuViz")
		self.window.geometry(f'{self.window_width}x{self.window_height}')

		return True

	def clear_frame(self):
		for widget in self.window.winfo_children():
			widget.destroy()

	def load_main_menu(self):
		self.clear_frame()

		header_label = Label(self.window, text="QuViz", font=("Arial", 36), width=20, height=10)
		header_label.pack()

		circuit_composer_button = Button(self.window, command=self.load_circuit_composer, text="Circuit Composer", font=("Arial", 18), width=18, height=1)
		circuit_composer_button.pack(side=TOP, padx=10, pady=5)

		return True

	def load_circuit_composer(self):
		self.clear_frame()

		header_label = Label(self.window, text="Circuit Composer", width=50, height=10, font=("Arial", 18))
		header_label.pack()
		
		self.qasm_text = Text(self.window, height=20, width=150, font=("Arial", 16))
		self.qasm_text.pack(side=TOP, padx=10, pady=5)

		compile_experiment_button = Button(self.window, command=self.compile_experiment, text="Compile Experiment", font=("Arial", 16), width=18, height=1)
		compile_experiment_button.pack(side=LEFT, padx=30, pady=5)

		visualize_experiment_button = Button(self.window, command=self.load_visualizer, text="Visualize Experiment", font=("Arial", 16), width=18, height=1)
		visualize_experiment_button.pack(side=RIGHT, padx=30, pady=5)

		return True

	def compile_experiment(self):
		# @TODO - parse number of qubits
		n_qubits = 0

		# # Parse circuit input into Qiskit QuantumCircuit
		# qasm_str = ""
		# if self.qasm_text:
		# 	qasm_str = self.qasm_text.get(1.0, "end-1c")

		# try:
		# 	original_circuit = qasm3.loads(qasm_str)
		# except qasm3.QASM3ImporterError:
		# 	print("Failed to compile OpenQASM3 input! Please check your syntax.")

		# 	return
		
		# basis_gate_operations = []
		
		# # @TODO - Decompose QuantumCircuit into program-native circuit
		# native_circuit_data = []
		# for l in range(len(original_circuit.depth())):
		# 	# Get the circuit instruction(s?) at this position
		# 	circuit_instruction = original_circuit.data[l]
		# 	print(circuit_instruction)
			
		# 	if circuit_instruction.operation in basis_gate_operations:
		# 		native_circuit_data.append(circuit_instruction)
		# 	else:
		# 		# @TODO - Decompose non-basis gate into basis gates
		# 		pass
		
		# # Create a new QuantumCircuit with the basis gate-decomposed circuit
		# native_circuit = QuantumCircuit(n_qubits)
		# native_circuit.data = native_circuit_data

		circuit = []
  
		# @TODO - parse other experiment parameters
		parameters = {}

		##########################################################################################
  		# TEST EXPERIMENT START
		n_qubits = 11
		circuit = [
			[{"instruction": "CZ", "qubits": [0, 1]}],
			# [{"instruction": "CZ", "qubits": [0, 1]}, {"instruction": "CZ", "qubits": [2, 3]}],
			[{"instruction": "CZ", "qubits": [2, 3]}],
			[{"instruction": "CZ", "qubits": [1, 2]}],
			# [{"instruction": "CZ", "qubits": [i, i+1]}] for i in range(9)
			# [{"instruction": "H", "qubits": [0]}],
			# [{"instruction": "CZ", "qubits": [0, 1]}],
			# [{"instruction": "H", "qubits": [0]}],
			# [{"instruction": "CCZ", "qubits": [2, 3, 4]}],
			# [{"instruction": "H", "qubits": [2, 4]}],
			# [{"instruction": "CCCZ", "qubits": [5, 6, 7, 8]}],
			# [{"instruction": "CCCCZ", "qubits": [3, 4, 5, 6, 7]}],
			# [{"instruction": "CCCCCZ", "qubits": [0, 2, 4, 6, 8, 9]}],
   			# [{"instruction": "CP", "qubits": [9, 10]}],
		]
		parameters = hardware_presets.DEFAULT
		# TEST EXPERIMENT STOP
		##########################################################################################

		# @TODO - turn into experiment
		current_experiment = {
			"n_qubits": n_qubits,
			"circuit": circuit,
			"parameters": parameters,
		}

		self.temporaryStorage["current_experiment"] = current_experiment

		return True

	def load_visualizer(self):
		self.compile_experiment()

		self.clear_frame()

		self.construct_visualization_canvas()

		current_experiment = self.temporaryStorage["current_experiment"]
		simulation = Simulation(current_experiment, self)
		simulation.compile_experiment()
		simulation.run_experiment()



		return True
	
	def load_output(self):
		self.clear_frame()
    	

	
		text_label = Label(self.window, text="", wraplength=400, width=100, height=40)
		text_label.pack(pady=10)
		text_label.config(text="Filler text!!! \nLorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.")

		main_menu_button = Button(self.window, text="Main Menu", command=self.load_main_menu, font=("Arial", 18), width=18, height=1)
		main_menu_button.pack(side=TOP, padx=10, pady=5)

		return True
	
	def show_continue_button(self):
		output_button = Button(self.window, command=self.load_output, text="See output state vector!", font=("Arial", 18), width=18, height=1)
		output_button.pack(side=TOP, padx=10, pady=5)
		
		return True


	def construct_visualization_canvas(self):
		self.visualization_canvas = Canvas(self.window)
		self.visualization_canvas.configure(bg="black")
		self.visualization_canvas.pack(fill="both", expand=True)

		return True

