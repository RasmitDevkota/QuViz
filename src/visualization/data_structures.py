import numpy as np

from common.constants import PROG_EPSILON

class AtomArray:
    def __init__(self, rows, cols):
        # @TODO - Load/store the other important variables that the user can give us
        self.isotope_list = ["Rb_87"]
        self.state_array = np.ones((rows,cols), dtype=complex) * PROG_EPSILON
