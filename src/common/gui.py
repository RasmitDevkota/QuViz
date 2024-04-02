from common.logging import *

from tkinter import *
from tkinter import ttk

import tkinter
import time

window_width = 800
window_height = 600

qubit_radius = 30
movement_step_time = 0.1

def construct_window():
  window = tkinter.Tk()
  window.title("QuViz")
  window.geometry(f'{window_width}x{window_height}')
  return window
 
def construct_visualization_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="black")
  canvas.pack(fill="both", expand=True)
  return canvas

def place_qubit(window, canvas, initial_position):
    qubit = canvas.create_oval(initial_position[0] - qubit_radius,
        initial_position[1] - qubit_radius,
        initial_position[0] + qubit_radius,
        initial_position[1] + qubit_radius,
        fill="springgreen", outline="greenyellow", width=4)
    
    return qubit
 
def move_qubit(window, canvas, qubit, movements):
    for movement in movements:
        canvas.move(qubit, movement[0], movement[1])

        window.update()

        time.sleep(movement_step_time)
