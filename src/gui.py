import numpy as np
from threading import Lock
import datetime

from tkinter import *

import hardware_presets
from simulation import Simulation
from logging import *

viz_length_scale = 1E-6/10
viz_time_scale = 10E-6 * 1000

viz_offset_horizontal = 100
viz_offset_vertical = 75
viz_offset_vector = np.array([viz_offset_horizontal, viz_offset_vertical])

qubit_radius = 1E-6/viz_length_scale
movement_step_time = 1

class GUI:
	def __init__(self, window_width=800, window_height=600):
		self.window_width = window_width
		self.window_height = window_height

		self.temporaryStorage = {}

		self.lock = Lock()

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
		circuit = [[{"instruction": "CZ", "qubits": [0, 1]}]]
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

		# self.lock.acquire()

		current_experiment = self.temporaryStorage["current_experiment"]
		simulation = Simulation(current_experiment, self)

		# self.lock.release()

		simulation.run_experiment()

		return True

	def construct_visualization_canvas(self):
		# print("received a construction call, waiting for lock")
		# with self.lock:
		# self.lock.acquire()
		# print("acquired lock")

		self.visualization_canvas = Canvas(self.window)
		self.visualization_canvas.configure(bg="black")
		self.visualization_canvas.pack(fill="both", expand=True)

		# print("finished construction call")
		# self.lock.release()
		# print("released lock")

		return True

	def prepare_qubit_widget(self, initial_position):
		# print("received a preparation call, waiting for lock")
		# self.lock.acquire()
		# print("acquired lock")

		initial_position = initial_position/viz_length_scale + viz_offset_vector

		qubit = self.visualization_canvas.create_oval(initial_position[0] - qubit_radius,
			initial_position[1] - qubit_radius,
			initial_position[0] + qubit_radius,
			initial_position[1] + qubit_radius,
			fill="springgreen", outline="greenyellow", width=4)
		
		print(f"new qubit @ {initial_position} @ {datetime.datetime.now()}")
		
		# print("finished preparation call")
		# self.lock.release()
		# print("released lock")

		return qubit

	def transport_qubit_widget(self, movements):
		# print("received a transport call, waiting for lock")
		# self.lock.acquire()
		# print("acquired lock")

		for m, movement in enumerate(movements):
			total_movement_vector = movement["movement"]/viz_length_scale
			total_movement_distance = np.linalg.norm(total_movement_vector)

			if total_movement_distance == 0:
				print("ignoring movement with distance 0")
				continue

			# print(viz_length_scale/movement_step_time)

			movement_speed = np.linalg.norm(movement["movement_velocity"]) #/ viz_length_scale
			print(movement_speed)
			time_needed = total_movement_distance/movement_speed
			steps_needed = int(np.ceil(time_needed/movement_step_time))
			movement_step_size = total_movement_distance/steps_needed
			
			unit_movement_vector = total_movement_vector/np.linalg.norm(total_movement_vector)
			step_movement_vector = movement_step_size * unit_movement_vector

			print(total_movement_vector, total_movement_distance, time_needed)

			for step in range(steps_needed):
				self.window.after(movement_step_time * (step + 1), lambda : self.visualization_canvas.move(movement["qubit"], *step_movement_vector))
				# self.visualization_canvas.move(movement["qubit"], *step_movement_vector)

		# print("finished transport call")
		# self.lock.release()
		# print("released lock")
		
		return True
	
	def expel_qubit_widget(self, qubit):
		self.visualization_canvas.delete(qubit)

		return True
	
	def enqueue(self, method, arguments):
		self.lock.acquire()

		method(arguments)

		self.lock.relase()

		return True
