import numpy as np
import time

from PyQt5.QtCore import Qt

import utility.find_matrix_engine
from widget.window2 import Window2
from widget.window1 import Window1


class Controller:
    def __init__(self):
        self.patterEngine = None
        self.window1 = Window1()
        self.window2 = None

        # parameter attribute
        self.matrixRow = None

        # game attribute
        self.matrix = None

        # pattern attribute
        self.pattern = None

        self.init()

    def init(self):
        self.window1.verifySignal.connect(self.set_up)

    def run(self):
        self.window1.show()

    def set_up(self):
        self.matrixRow = int(self.window1.matrixRow)
        self.matrixCol = int(self.window1.matrixCol)

        self.matrix = [['0' for x in range(self.matrixCol)] for y in range(self.matrixRow)]
        self.window2 = Window2(self.matrix)
        self.window2.verifySignal.connect(self.on_search)
        self.window2.print_matrix()

        self.window2.show()
        self.window1.hide()

    def on_search(self):
        self.pattern = self.window2.pattern
        self.matrix = self.window2.matrix
        self.patterEngine = utility.find_matrix_engine.FindMatrixEngine(self.matrix, self.matrixRow, self.matrixCol)
        result = self.patterEngine.search_patter(self.pattern)
        if result[0] == 1:
            arr1 = result[1]
            self.window2.set_result_label("Pattern found!")
            self.window2.rotation = result[2]

            for y in range(result[2]):
                self.window2.matrix = np.rot90(self.window2.matrix)
                self.window2.print_matrix()

            for x in arr1:
                self.window2.change_background_color(x[0], x[1], Qt.green)

        elif result[0] == -1:
            self.window2.set_result_label("No 1-bit found!")
        else:
            self.window2.set_result_label("Pattern not found!")
