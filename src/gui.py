import numpy as np
import re

from tkinter import *

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

import hardware_presets
from simulation import Simulation

from qiskit import qasm3
from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_aer.noise import NoiseModel, pauli_error, thermal_relaxation_error
from qiskit.exceptions import QiskitError
from qiskit.transpiler.exceptions import CircuitTooWideForTarget

GATE_DIMENSIONS = {
	1: ["H", "X", "Y", "Z"],
	2: ["CX", "CY", "CZ", "CP"],
	3: ["CCZ", "PSCP"],
}

DEFAULT_FONT = ("Arial", 24)
CIRCUIT_COMPOSER_FONT = ("Arial", 16)

class GUI:
	def __init__(self, window_width=800, window_height=800):
		self.window_width = window_width
		self.window_height = window_height

		self.viz_background_color = "black"
		
		self.viz_length_scale = 1E-6/5
		self.viz_time_scale = 10E-6 * 1000

		self.viz_offset_horizontal = 75
		self.viz_offset_vertical = 75
		self.viz_offset_vector = np.array([self.viz_offset_horizontal, self.viz_offset_vertical])

		self.qubit_radius = 1E-6/self.viz_length_scale
		self.movement_step_time = 1

		self.experiment_input_method = None

		self.qubit_count_entry = None
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

		header_label = Label(self.window, text="QuViz", font=("Arial", 36))
		header_label.place(relwidth=0.2, relheight=0.2, relx=0.4, rely=0.2)

		experiment_designer_button = Button(self.window, command=self.load_qasm_editor, text="Experiment Designer", font=DEFAULT_FONT)
		experiment_designer_button.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.6)

		return True

	def load_qasm_editor(self):
		self.clear_frame()

		header_label = Label(self.window, text="OpenQASM3 Editor", font=DEFAULT_FONT)
		header_label.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.05)

		qasm_frame = Frame(self.window, borderwidth=3, background="black")
		# qasm_frame.place(side=TOP, fill="x", padx=500, pady=0)
		qasm_frame.place(relwidth=0.6, relheight=0.65, relx=0.2, rely=0.15)

		#############################################################################################
		preamble_text = Text(qasm_frame, width=150, height=3, font=("Arial", 16), background="white")
		preamble_text.insert(1.0, f"OPENQASM 3;\n\ninclude \"stdgates.inc\";")
		preamble_text.configure(state="disabled", highlightthickness=0, borderwidth=0)
		preamble_text.pack(side=TOP, fill="both", padx=0, pady=0)

		qregister_frame = Frame(qasm_frame, width=150, height=1)
		qregister_frame.pack(side=TOP, fill="both", padx=0, pady=0)

		qregister_pre_label = Label(qregister_frame, width=4, height=1, text="qubit[", font=("Arial", 16), background="white")
		qregister_pre_label.pack(side=LEFT, fill="x", padx=0, pady=0)

		self.qubit_count_var = StringVar()
		self.qubit_count_var.trace_add("write", self.qubit_count_filter)
		self.qubit_count_entry = Entry(qregister_frame, textvariable=self.qubit_count_var, width=3, font=("Arial", 16), highlightthickness=0, borderwidth=0, background="white")
		self.qubit_count_entry.pack(side=LEFT, fill="x", padx=0, pady=0)
		
		qregister_post_label = Label(qregister_frame, width=3, text="] qr;", font=("Arial", 16), background="white")
		qregister_post_label.pack(side=LEFT, fill="x", padx=0, pady=0)

		qregister_postfill_label = Label(qregister_frame, width=140, text="", font=("Arial", 16), background="white")
		qregister_postfill_label.pack(side=LEFT, fill="x", padx=0, pady=0)
		
		self.qasm_text = Text(qasm_frame, undo=True, width=150, height=30, font=("Arial", 16), highlightthickness=0, borderwidth=0)
		self.qasm_text.insert(1.0, f"// Your code starts here!")
		self.qasm_text.pack(side=TOP, fill="both", expand=True, padx=0, pady=0)
		#############################################################################################

		compile_experiment_button = Button(self.window, command=self.compile_experiment, text="Compile Experiment", font=DEFAULT_FONT)
		compile_experiment_button.place(relwidth=0.15, relheight=0.05, relx=0.1, rely=0.85)

		visualize_experiment_button = Button(self.window, command=self.load_visualizer, text="Visualize Experiment", font=DEFAULT_FONT)
		visualize_experiment_button.place(relwidth=0.15, relheight=0.05, relx=0.75, rely=0.85)

		switch_type = Button(self.window, command=self.load_circuit_composer, text="Switch to Circuit Composer", font=DEFAULT_FONT)
		switch_type.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.85)

		self.experiment_input_method = "OpenQASM3 Editor"

		return True
	
	def qubit_count_filter(self, var, index, mode):
		filtered_text = re.sub(r'\D', '', self.qubit_count_var.get()[:3])
		self.qubit_count_var.set(filtered_text)
		return

	def load_circuit_composer(self):
		self.clear_frame()

		header_label = Label(self.window, text="Circuit Composer", font=DEFAULT_FONT)
		header_label.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.05)

		self.circuit_composer_frame = Frame(self.window)
		self.circuit_composer_frame.place(relwidth=0.6, relheight=0.65, relx=0.2, rely=0.15)
		
		self.circuit_composer = CircuitComposer(self.circuit_composer_frame)

		compile_experiment_button = Button(self.window, command=self.compile_experiment, text="Compile Experiment", font=DEFAULT_FONT)
		compile_experiment_button.place(relwidth=0.15, relheight=0.05, relx=0.1, rely=0.85)

		visualize_experiment_button = Button(self.window, command=self.load_visualizer, text="Visualize Experiment", font=DEFAULT_FONT)
		visualize_experiment_button.place(relwidth=0.15, relheight=0.05, relx=0.75, rely=0.85)

		switch_type = Button(self.window, command=self.load_qasm_editor, text="Switch to OpenQASM3 Editor", font=DEFAULT_FONT)
		switch_type.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.85)

		self.experiment_input_method = "Circuit Composer"

		return True

	def compile_experiment(self):
		qubit_mode = "physical"
		
		n_qubits = 0
		if self.experiment_input_method == "OpenQASM3 Editor":
			n_qubits_raw = self.qubit_count_var.get()

			if n_qubits_raw.isdigit():
				n_qubits = int(n_qubits_raw)
		elif self.experiment_input_method == "Circuit Composer":
			n_qubits = len(self.circuit_composer.wires)
		
		if n_qubits == 0:
			print("Cannot compile circuit with no wires!")
			# @ TODO - Communicate compilation error (e.g. popup)
			return False
  
		# @TODO - parse user input for experiment parameters
		parameters = hardware_presets.DEFAULT
		
		# Parse circuit input into Qiskit QuantumCircuit
		qasm_str = f"OPENQASM 3;\n\ninclude \"stdgates.inc\";\nqubit[{n_qubits}] qr;\n"
		if self.experiment_input_method == "OpenQASM3 Editor":
			qasm_str += self.qasm_text.get(1.0, "end-1c")
		elif self.experiment_input_method == "Circuit Composer":
			n_layers = self.circuit_composer.num_segments

			for layer in range(n_layers):
				visited_gates = []

				for wire_index in range(n_qubits):
					if (wire_index, layer) in self.circuit_composer.gates:
						gate_tags = self.circuit_composer.canvas.gettags(self.circuit_composer.gates[(wire_index, layer)][0])
						gate_info = list(filter(lambda gate_tag : True if gate_tag.startswith("@") else False, gate_tags))[0][1:].lower()

						if gate_info in visited_gates:
							continue
						else:
							visited_gates.append(gate_info)

						instruction_name = gate_info.split("|")[0]

						parameters = gate_info.split("|")[1].split(",")

						start_qubit = int(gate_info.split("|")[2].split(":")[0])
						stop_qubit = int(gate_info.split("|")[2].split(":")[1].split(",")[0])+1
						qubits = list(range(start_qubit,stop_qubit))

						qasm_line = f"{instruction_name}"

						if parameters[0] != "":
							parameters = ",".join(parameters)
							qasm_line += f"({parameters})"

						for qubit in qubits:
							qasm_line += f" qr[{qubit}],"

						qasm_line = qasm_line[:-1]
						qasm_line += ";\n"

						qasm_str += qasm_line

		print(f"--------------------------\n{qasm_str}\n--------------------------")

		try:
			original_circuit = qasm3.loads(qasm_str)
		except qasm3.QASM3ImporterError:
			# @ TODO - Communicate compilation error (e.g. popup)
			print("Failed to compile OpenQASM3 input! Please check your syntax.")
			return False
		
		# @TODO - Implement Dynamical Decoupling
  
		basis_gates = ["id", "u", "cz", "ccz", "cp"]

		# @TODO - Implement errors for multi-qubit gates
		pauli_error_x_cz = pauli_error([("X", parameters["Pauli_error_X_CZ"]), ("I", 1 - parameters["Pauli_error_X_CZ"])])
		pauli_error_x_cz = pauli_error_x_cz.tensor(pauli_error_x_cz)
		pauli_error_y_cz = pauli_error([("Y", parameters["Pauli_error_Y_CZ"]), ("I", 1 - parameters["Pauli_error_Y_CZ"])])
		pauli_error_y_cz = pauli_error_y_cz.tensor(pauli_error_y_cz)
		pauli_error_z_cz = pauli_error([("Z", parameters["Pauli_error_Z_CZ"]), ("I", 1 - parameters["Pauli_error_Z_CZ"])])
		pauli_error_z_cz = pauli_error_z_cz.tensor(pauli_error_z_cz)

		decoherence_error_id = thermal_relaxation_error(parameters["T1"],  parameters["T2"], 0)
		decoherence_error_1q = thermal_relaxation_error(parameters["T1"],  parameters["T2"], 1/parameters["Omega2pi"]/self.viz_time_scale)
		decoherence_error_2q = decoherence_error_1q.tensor(decoherence_error_1q)
		decoherence_error_3q = decoherence_error_2q.tensor(decoherence_error_1q)

		try:
			noise_model = NoiseModel(basis_gates=basis_gates)
			noise_model.add_all_qubit_quantum_error(pauli_error_x_cz, ["cz"])
			noise_model.add_all_qubit_quantum_error(pauli_error_y_cz, ["cz"])
			noise_model.add_all_qubit_quantum_error(pauli_error_z_cz, ["cz"])
			noise_model.add_all_qubit_quantum_error(decoherence_error_id, ["id"])
			noise_model.add_all_qubit_quantum_error(decoherence_error_1q, ["u"])
			noise_model.add_all_qubit_quantum_error(decoherence_error_2q, ["u"])
			noise_model.add_all_qubit_quantum_error(decoherence_error_3q, ["u"])

			backend = AerSimulator(noise_model=noise_model)

			decomposed_circuit = transpile(original_circuit, backend, basis_gates=basis_gates, optimization_level=0)
		except (CircuitTooWideForTarget, QiskitError):
			backend = GenericBackendV2(num_qubits=n_qubits)

			decomposed_circuit = transpile(original_circuit, backend, basis_gates=basis_gates, optimization_level=0)

		# @TODO - Save graphics in a more useful location
		decomposed_circuit.draw("mpl", filename="images/decomposed_circuit.png")

		circuit = []

		occupied_qubits = []
		circuit.append([])
		for circuit_instruction in decomposed_circuit.data:
			instruction = circuit_instruction.operation
			instruction_name = instruction.name.upper()
			instruction_parameters = instruction.params
			qubits = [qubit._index for qubit in circuit_instruction.qubits]
			
			# Create new layer if one of the qubits is already occupied in the current layer
			for qubit in qubits:
				if qubit in occupied_qubits:
					circuit.append([])
					occupied_qubits = []
					break
			
			occupied_qubits.extend(qubits)
			
			circuit[-1].append({"instruction": instruction_name, "parameters": instruction_parameters, "qubits": qubits})
		
		print(circuit)

		current_experiment = {
			"qubit_mode": qubit_mode,
			"n_qubits": n_qubits,
			"circuit": circuit,
			"qiskit_circuit": decomposed_circuit,
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
	
		text_label = Label(self.window, text="Experiment results", width=50, height=1, font=DEFAULT_FONT)
		text_label.pack(pady=5)

		output_frame = Frame(self.window, width=150, height=10, borderwidth=3, background="black")
		output_frame.pack(side=TOP, padx=50, pady=0, fill="x", expand=True)
		
		# Display decomposed circuit
		circuit_figure = self.temporaryStorage["current_experiment"]["qiskit_circuit"].draw("mpl")
		circuit_figure_canvas = FigureCanvasTkAgg(circuit_figure, output_frame)
		circuit_figure_canvas.get_tk_widget().pack(side=TOP, padx=0, pady=0, fill="x", expand=True)

		# Display final statevector
		if self.temporaryStorage["current_experiment"]["n_qubits"] <= 16:
			statevector_latex = Statevector(self.temporaryStorage["current_experiment"]["qiskit_circuit"]).draw("latex_source")
			statevector_plaintext = statevector_latex.replace("\\rangle", "⟩").replace("\\frac", "").replace("\\sqrt", "sqrt").replace("}{", "/").replace("{", "").replace("}", "").replace("+", " + ")

			statevector_label = Label(output_frame, text="Final statevector: " + statevector_plaintext, width=50, height=1, font=DEFAULT_FONT)
			statevector_label.pack(side=BOTTOM, padx=0, pady=0, fill="x", expand=True)
		
		# statevector_figure = Figure(figsize=(5, 1), dpi=100, frameon=False)
		# statevector_figure.patch.set_visible(False)

		# statevector_figure_canvas = FigureCanvasTkAgg(statevector_figure, output_frame)
		# statevector_figure_canvas.get_tk_widget().pack(side=BOTTOM, padx=0, pady=0, fill="x", expand=True)

		# statevector_axes = statevector_figure.add_subplot()
		# statevector_axes.get_xaxis().set_visible(False)
		# statevector_axes.get_yaxis().set_visible(False)
		# statevector_axes.spines['top'].set_visible(False)
		# statevector_axes.spines['right'].set_visible(False)
		# statevector_axes.spines['bottom'].set_visible(False)
		# statevector_axes.spines['left'].set_visible(False)
		# statevector_axes.text(0, 0.5, statevector_latex, fontsize=16, ha="center", va="center")

		main_menu_button = Button(self.window, text="Main Menu", command=self.load_main_menu, font=DEFAULT_FONT, width=18, height=1)
		main_menu_button.pack(side=TOP, padx=0, pady=0)

		return True

	def show_continue_button(self):
		output_button = Button(self.window, command=self.load_output, text="Continue to output", font=DEFAULT_FONT, width=18, height=1)
		output_button.pack(side=TOP, padx=10, pady=5)

		return True

	def construct_visualization_canvas(self):
		self.visualization_canvas = Canvas(self.window)
		self.visualization_canvas.configure(bg=self.viz_background_color)
		self.visualization_canvas.pack(fill="both", expand=True)

		return True

class CircuitComposer:
	def __init__(self, master):
		self.master = master

		self.num_segments = 25
		self.gate_size = 30
		self.wire_spacing = 2 * self.gate_size

		self.x_start = 100
		self.x_end = self.num_segments * self.gate_size
		self.y_start = 50

		self.wires = []
		self.gates = {}

		self.selected_gate = None
		
		self.canvas = Canvas(master, width=800, height=600, bg="white")
		self.canvas.pack(side=TOP, fill=BOTH, expand=True)

		self.draw_wires()

		self.draw_gate_buttons()

		self.canvas.bind("<Button-1>", self.place_gate)

	def draw_wires(self):
		for i in range(5):
			label = self.canvas.create_text(
				self.x_start - self.gate_size,
				self.y_start + i * self.wire_spacing,
				text="|0⟩", font=CIRCUIT_COMPOSER_FONT,
				anchor="e", tags=("qubit_label", f"qubit_{i}"),
			)

			# Bind toggle function to labels
			self.canvas.tag_bind(label, "<Button-1>", lambda event, idx=i : self.toggle_qubit(idx))

			wire = self.canvas.create_line(self.x_start, self.y_start + i * self.wire_spacing, self.x_end, self.y_start + i * self.wire_spacing, width=2)
			self.wires.append((self.y_start + i * self.wire_spacing, wire))

	def toggle_qubit(self, idx):
		# Get current text of the clicked label
		current_text = self.canvas.itemcget(f"qubit_{idx}", "text")

		# Toggle the text between "|0>" and "|1>"
		new_text = "|1⟩" if current_text == "|0⟩" else "|0⟩"

		# Update the text of the clicked label
		self.canvas.itemconfigure(f"qubit_{idx}", text=new_text, fill="black")

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
			
			gate_tag = f"@{self.selected_gate}||{wire_index}:{wire_index},{segment_index}"
		
			gate = self.canvas.create_rectangle(
				gate_x - self.gate_size // 2,
				gate_y - self.gate_size // 2,
				gate_x + self.gate_size // 2,
				gate_y + self.gate_size // 2,
				fill="lightblue", tag=(gate_tag,)
			)

			text = self.canvas.create_text(
				gate_x,
				gate_y,
				text=self.selected_gate, tag=(gate_tag,)
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
			
			gate_tag = f"@{self.selected_gate}||{wire_index}:{wire_index+gate_dimension-1},{segment_index}"

			gate = self.canvas.create_rectangle(
				gate_x - self.gate_size // 2,
				gate_y - self.gate_size // 2,
				gate_x + self.gate_size // 2,
				gate_y + self.wire_spacing * (gate_dimension - 1) + self.gate_size // 2,
				fill="lightblue", tag=(gate_tag,)
			)

			text = self.canvas.create_text(
				gate_x,
				gate_y + self.wire_spacing * (gate_dimension - 1) // 2,
				text=self.selected_gate, tag=(gate_tag,)
			)

			for i in range(gate_dimension):
				self.gates[(wire_index + i, segment_index)] = [gate, text]

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
