from common.logging import *

from tkinter import *
from tkinter import ttk

import tkinter
import time

qubit_radius = 30
movement_step_time = 1000

class GUI:
	def __init__(self, window_width=800, window_height=600):
		self.window_width = window_width
		self.window_height = window_height

	def construct_window(self):
		self.window = tkinter.Tk()
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

		blue_button = Button(self.window, command=self.load_circuit_composer, text="Circuit Composer", font=("Arial", 18), width=15, height=1)
		blue_button.pack(side=TOP, padx=10, pady=5)

		return True
	
	def load_circuit_composer(self):
		self.clear_frame()

		header_label = Label(self.window, text="Circuit Composer", width=50, height=30)
		header_label.pack()

		return True
	
	def construct_visualization_canvas(self):
		self.canvas = tkinter.Canvas(self.window)
		self.canvas.configure(bg="black")
		self.canvas.pack(fill="both", expand=True)

		return True

	def prepare_qubit(self, initial_position):
		qubit = self.canvas.create_oval(initial_position[0] - qubit_radius,
			initial_position[1] - qubit_radius,
			initial_position[0] + qubit_radius,
			initial_position[1] + qubit_radius,
			fill="springgreen", outline="greenyellow", width=4)
		
		return qubit
	
	def transport_qubit(self, qubit, movements):
		for m, movement in enumerate(movements):
			self.window.after(movement_step_time * (m+1), lambda : self.canvas.move(qubit, movement[0], movement[1]))

			# self.window.update()
			# time.sleep(movement_step_time)
