import numpy as np
from threading import Lock
import datetime

from tkinter import *

import hardware_presets
from simulation import Simulation
from logging import *

class GUI:
	def __init__(self, window_width=800, window_height=600):
		self.window_width = window_width
		self.window_height = window_height
		
		self.viz_length_scale = 1E-6/5
		self.viz_time_scale = 10E-6 * 1000

		self.viz_offset_horizontal = 75
		self.viz_offset_vertical = 75
		self.viz_offset_vector = np.array([self.viz_offset_horizontal, self.viz_offset_vertical])

		self.qubit_radius = 1E-6/self.viz_length_scale
		self.movement_step_time = 1

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

		header_label = Label(self.window, text="Circuit Composer", width=50, height=30)
		header_label.pack()

		compile_experiment_button = Button(self.window, command=self.compile_experiment, text="Compile Experiment", font=("Arial", 16), width=18, height=1)
		compile_experiment_button.pack(side=LEFT, padx=10, pady=5)

		visualize_experiment_button = Button(self.window, command=self.load_visualizer, text="Visualize Experiment", font=("Arial", 16), width=18, height=1)
		visualize_experiment_button.pack(side=RIGHT, padx=10, pady=5)

		return True

	def compile_experiment(self):
		# @TODO - parse number of qubits
		n_qubits = 0

		# @TODO - parse circuit input
		circuit = []
  
		# @TODO - parse other experiment parameters
		parameters = {}

		##########################################################################################
  		# TEST EXPERIMENT START
		n_qubits = 10
		circuit = [
			[{"instruction": "CZ", "qubits": [0, 1]}],
			# [{"instruction": "CZ", "qubits": [0, 1]}, {"instruction": "CZ", "qubits": [2, 3]}],
			[{"instruction": "CZ", "qubits": [2, 3]}],
			# [{"instruction": "CZ", "qubits": [1, 2]}],
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
		self.clear_frame()

		self.construct_visualization_canvas()

		current_experiment = self.temporaryStorage["current_experiment"]
		simulation = Simulation(current_experiment, self)
		simulation.compile_experiment()
		simulation.run_experiment()

		return True

	def construct_visualization_canvas(self):
		self.visualization_canvas = Canvas(self.window)
		self.visualization_canvas.configure(bg="black")
		self.visualization_canvas.pack(fill="both", expand=True)

		return True

