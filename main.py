import sys
from PyQt5.QtWidgets import QApplication
from controller.controller import Controller
import numpy as np

if __name__ == '__main__':
    app = QApplication([])
    c = Controller()
    c.run()

    sys.exit(app.exec())


