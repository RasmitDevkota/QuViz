import numpy as np
from threading import Lock
import datetime

from tkinter import *

import hardware_presets
from simulation import Simulation

from qiskit import QuantumCircuit, qasm3
from qiskit.circuit import CircuitInstruction

GATE_DIMENSIONS = {
	1: ["H", "X", "Y", "Z"],
	2: ["CX", "CY", "CZ", "CP"],
	3: ["CCZ", "PSCP"],
}

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

		experiment_designer_button = Button(self.window, command=self.load_qasm_editor, text="Experiment Designer", font=("Arial", 24), width=18, height=1)
		experiment_designer_button.pack(side=TOP, padx=10, pady=5)

		return True

	def load_qasm_editor(self):
		self.clear_frame()

		header_label = Label(self.window, text="OpenQASM3 Input", width=50, height=6, font=("Arial", 16))
		header_label.pack()

		qasm_frame = Frame(self.window, width=150, height=50)
		qasm_frame.pack(side=LEFT, fill="x", padx=500, pady=0)

		preamble_text = Text(qasm_frame, width=150, height=3, font=("Arial", 16), background="white")
		preamble_text.insert(1.0, f"OPENQASM 3;\n\ninclude \"stdgates.inc\";")
		preamble_text.configure(state="disabled", highlightthickness=0, borderwidth=0)
		preamble_text.pack(side=TOP, fill="both", padx=0, pady=0)

		qregister_frame = Frame(qasm_frame, width=150, height=1)
		qregister_frame.pack(side=TOP, fill="both", padx=0, pady=0)

		qregister_pre_label = Label(qregister_frame, width=4, height=1, text="qubit[", font=("Arial", 16), background="white")
		qregister_pre_label.pack(side=LEFT, fill="x", padx=0, pady=0)

		qregister_in_text = Text(qregister_frame, width=3, height=1, font=("Arial", 16), highlightthickness=0, borderwidth=0, background="white")
		qregister_in_text.bind('<<Modified>>', lambda *args: qregister_in_text.set(qregister_in_text.get()[:4]))
		qregister_in_text.pack(side=LEFT, fill="x", padx=0, pady=0)
		
		qregister_post_label = Label(qregister_frame, width=5, text="]  qr;", font=("Arial", 16), background="white")
		qregister_post_label.pack(side=LEFT, fill="x", padx=0, pady=0)

		qregister_postfill_label = Label(qregister_frame, width=135, text="", font=("Arial", 16), background="white")
		qregister_postfill_label.pack(side=LEFT, fill="x", padx=0, pady=0)
		
		self.qasm_text = Text(qasm_frame, undo=True, width=150, height=30, font=("Arial", 16), highlightthickness=0, borderwidth=0)
		self.qasm_text.insert(1.0, f"// Your code starts here!")
		self.qasm_text.pack(side=TOP, padx=0, pady=0)

		compile_experiment_button = Button(self.window, command=self.compile_experiment, text="Compile Experiment", font=("Arial", 16), width=18, height=1)
		compile_experiment_button.pack(side=LEFT, padx=30, pady=5)

		visualize_experiment_button = Button(self.window, command=self.load_visualizer, text="Visualize Experiment", font=("Arial", 16), width=18, height=1)
		visualize_experiment_button.pack(side=RIGHT, padx=30, pady=5)

		switch_type = Button(self.window, command=self.load_circuit_composer, text="Switch to Circuit Composer", font=("Arial", 24), width=24, height=1)
		switch_type.pack(padx=30, pady=5)

		return True
	
	def load_circuit_composer(self):
		self.clear_frame()

		header_label = Label(self.window, text="Circuit Composer", width=50, height=10, font=("Arial", 18))
		header_label.pack()

		self.circuit_composer_frame = Frame(self.window)
		self.circuit_composer_frame.pack()
		
		self.circuit_composer = CircuitComposer(self.circuit_composer_frame)

		compile_experiment_button = Button(self.window, command=self.compile_experiment, text="Compile Experiment", font=("Arial", 16), width=18, height=1)
		compile_experiment_button.pack(side=LEFT, padx=30, pady=5)

		visualize_experiment_button = Button(self.window, command=self.load_visualizer, text="Visualize Experiment", font=("Arial", 16), width=18, height=1)
		visualize_experiment_button.pack(side=RIGHT, padx=30, pady=5)

		switch_type = Button(self.window, command=self.load_qasm_editor, text="Switch to OpenQASM input", font=("Arial", 24), width=24, height=1)
		switch_type.pack(padx=30, pady=5)

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

		main_menu_button = Button(self.window, text="Main Menu", command=self.load_main_menu, font=("Arial", 24), width=18, height=1)
		main_menu_button.pack(side=TOP, padx=10, pady=5)

		return True
	
	def show_continue_button(self):
		output_button = Button(self.window, command=self.load_output, text="See output state vector!", font=("Arial", 24), width=18, height=1)
		output_button.pack(side=TOP, padx=10, pady=5)

		return True

	def construct_visualization_canvas(self):
		self.visualization_canvas = Canvas(self.window)
		self.visualization_canvas.configure(bg="black")
		self.visualization_canvas.pack(fill="both", expand=True)

		return True

class CircuitComposer:
	def __init__(self, master):
		self.master = master
		
		self.canvas = Canvas(master, width=600, height=400, bg="white")
		self.canvas.pack(side=TOP, fill=BOTH, expand=True)

		self.x_start = 100
		self.x_end = 500
		self.y_start = 50
		self.wire_spacing = 60

		self.wires = []
		self.gate_size = 30
		self.gates = {}
		self.num_segments = 10

		self.grid_size = (10, 6)

		self.selected_gate = None
		self.drag_data = {"item": None, "x": 0, "y": 0}

		self.draw_wires()

		self.draw_gate_buttons()

		self.canvas.bind("<Button-1>", self.place_gate)

	def draw_wires(self):
		for i in range(5):
			wire_id = self.canvas.create_line(self.x_start, self.y_start + i * self.wire_spacing, self.x_end, self.y_start + i * self.wire_spacing, width=2)
			self.wires.append((self.y_start + i * self.wire_spacing, wire_id))

	def draw_gate_buttons(self):
		gates = ["H", "X", "Y", "Z", "CX", "CY", "CZ", "CP", "CCZ"]
		self.buttons = []
		for gate in gates:
			button = Button(self.master, text=gate, command=lambda g=gate: self.select_gate(g))
			button.pack(side=TOP, padx=10, pady=5, fill=X)
			self.buttons.append(button)

		# add_wire_button = Button(self.master, text="Add Wire", command=self.add_wire)
		# add_wire_button.pack(side=TOP, padx=10, pady=5, fill=X)
		# self.buttons.append(add_wire_button)

		# remove_wire_button = Button(self.master, text="Remove Wire", command=self.remove_wire)
		# remove_wire_button.pack(side=TOP, padx=10, pady=5, fill=X)
		# self.buttons.append(remove_wire_button)

	def select_gate(self, gate):
		self.selected_gate = gate

	def place_gate(self, event):
		if event.x < self.x_start or event.x > self.x_end or event.y < self.y_start or event.y > self.y_start + len(self.wires) * self.wire_spacing:
			return

		if not self.selected_gate:
			return
		
		wire_index = round((event.y - self.y_start)/self.wire_spacing)
		segment_index = round((event.x - self.x_start)/self.gate_size)

		gate_x = self.x_start + segment_index * self.gate_size
		gate_y = self.y_start + wire_index * self.wire_spacing

		if self.selected_gate in GATE_DIMENSIONS[1]:
			if (wire_index, segment_index) in self.gates:
				for widget in self.gates[(wire_index, segment_index)]:
					for related_widget in self.canvas.gettags(widget):
						print(related_widget)
						if related_widget != "current":
							self.canvas.delete(related_widget)
					
					self.canvas.delete(widget)
				
				del self.gates[(wire_index, segment_index)]
				
				return
		
			gate = self.canvas.create_rectangle(
				gate_x - self.gate_size // 2,
				gate_y - self.gate_size // 2,
				gate_x + self.gate_size // 2,
				gate_y + self.gate_size // 2,
				fill="lightblue", tag=(f"{wire_index}:{wire_index},{segment_index}",)
			)

			text = self.canvas.create_text(
				gate_x,
				gate_y,
				text=self.selected_gate, tag=(f"{wire_index}:{wire_index},{segment_index}",)
			)
			
			self.gates[(wire_index, segment_index)] = [gate, text]
		else:
			gate_dimension = 0

			for d, gates in GATE_DIMENSIONS.items():
				if self.selected_gate in gates:
					gate_dimension = d
			
			if wire_index + gate_dimension > len(self.wires):
				return

			for i in range(gate_dimension):
				if (wire_index + i, segment_index) in self.gates:
					print(self.gates[(wire_index + i, segment_index)])
					for widget in self.gates[(wire_index + i, segment_index)]:
						for related_widget in self.canvas.gettags(widget):
							if related_widget != "current":
								self.canvas.delete(related_widget)
						
						self.canvas.delete(widget)
					
					del self.gates[(wire_index + i, segment_index)]

			gate = self.canvas.create_rectangle(
				gate_x - self.gate_size // 2,
				gate_y - self.gate_size // 2,
				gate_x + self.gate_size // 2,
				gate_y + self.wire_spacing * (gate_dimension - 1) + self.gate_size // 2,
				fill="lightblue", tag=(f"{wire_index}:{wire_index+gate_dimension-1},{segment_index}",)
			)

			text = self.canvas.create_text(
				gate_x,
				gate_y + self.wire_spacing * (gate_dimension - 1) // 2,
				text=self.selected_gate, tag=(f"{wire_index}:{wire_index+gate_dimension-1},{segment_index}",)
			)

			for i in range(gate_dimension):
				self.gates[(wire_index + i, segment_index)] = [gate, text]
			
			# self.gates[(wire_index, segment_index)] = [gate, text]

		return True

	# def add_wire(self):
	#     y = self.wires[-1][0] + 60
	#     wire_id = self.canvas.create_line(100, y, 500, y, width=2)
	#     self.wires.append((y, wire_id))

	# def remove_wire(self):
	#     if len(self.wires) > 1:
	#         _, wire_id = self.wires.pop()
	#         self.canvas.delete(wire_id)
	#         for segment in self.gates.copy():
	#             if segment[0] == len(self.wires):
	#                 self.canvas.delete(self.gates.pop(segment))
