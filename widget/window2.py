import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QLabel, QMessageBox, QWidget, QMainWindow, QHeaderView, QPushButton, \
    QLineEdit, QAbstractItemView, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QDesktopWidget
from PyQt5.QtCore import Qt


class Window2(QMainWindow):
    verifySignal = QtCore.pyqtSignal()

    def __init__(self, matrix):
        super().__init__()
        self.rotation = 0
        self.pattern = None
        self.matrix = matrix
        self.widget = QWidget()
        self.Init_UI()

        self.button.clicked.connect(self.on_button_clicked)
        self.patternWidg.returnPressed.connect(self.on_button_clicked)
        self.clearButton.clicked.connect(self.reset_matrix)

    def Init_UI(self):
        self.setWindowTitle("findPatterDNA")

        # set stylesheet
        self.setStyleSheet("QLabel {"
                           "font: arial, 15px;"
                           "}"
                           "QPushButton {"
                           "margin: 10 px;"
                           "font: arial, 15px; "
                           "}")

        # default error popup
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Warning!")

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setGeometry(400, 250, 900, 500)

        self.patternLabel = QLabel("Pattern to find:")
        self.patternWidg = QLineEdit()
        self.button = QPushButton("Go")
        self.clearButton = QPushButton("Clear")
        self.resultLabel = QLabel()

        self.table = QTableWidget()
        self.table.setRowCount(len(self.matrix))
        self.table.setColumnCount(len(self.matrix[0]))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setMinimumSectionSize(1)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.clicked.connect(self.change_bit)

        self.vBoxLayout = QHBoxLayout()
        self.box1 = QVBoxLayout()
        self.box2 = QVBoxLayout()
        self.box3 = QVBoxLayout()

        self.box1.addWidget(self.patternLabel)
        self.box1.addWidget(self.patternWidg)
        self.box1.addWidget(self.button)
        self.box1.addWidget(self.clearButton)

        self.box2.addWidget(self.resultLabel)

        self.box3.addLayout(self.box1)
        self.box3.addLayout(self.box2)

        self.vBoxLayout.addWidget(self.table, 8)
        self.vBoxLayout.addLayout(self.box3, 2)

        self.widget.setLayout(self.vBoxLayout)
        self.setCentralWidget(self.widget)

    def print_matrix(self):
        if len(self.matrix) > len(self.matrix[0]):
            self.table.setRowCount(len(self.matrix))
            self.table.setColumnCount(len(self.matrix[0]))
            self.setGeometry(400, 250, 500, 900)
        else:
            self.table.setRowCount(len(self.matrix))
            self.table.setColumnCount(len(self.matrix[0]))
            self.setGeometry(400, 250, 900, 500)


        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
                self.table.item(i, j).setTextAlignment(Qt.AlignCenter)


    def set_cell(self, x, y, value):
        self.table.item(x, y).setText(str(value))

    def on_button_clicked(self):
        if self.patternWidg.text() == "":
            self.msg.setText("No pattern selected!")
            self.msg.exec()
            return

        if len(self.patternWidg.text()) != 1:
            self.msg.setText("Too much input pattern!")
            self.msg.exec()
            return

        if not self.patternWidg.text().isalpha():
            self.msg.setText("Input pattern isn't valid!")
            self.msg.exec()
            return

        self.pattern = self.patternWidg.text()

        self.verifySignal.emit()
        self.patternWidg.clear()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def change_bit(self, index):
        if self.matrix[index.row()][index.column()] == "0":
            self.matrix[index.row()][index.column()] = "1"
            self.table.item(index.row(), index.column()).setText(str("1"))
        elif self.matrix[index.row()][index.column()] == "1":
            self.matrix[index.row()][index.column()] = "0"
            self.table.item(index.row(), index.column()).setText(str("0"))

    def change_background_color(self, px, py, color):
        self.table.item(px, py).setBackground(color)

    def set_result_label(self, result):
        self.resultLabel.setText(result)

    def reset_matrix(self):
        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[0])):
                self.matrix[j][i] = "0"
                self.table.item(j, i).setText(str("0"))
                self.change_background_color(j, i, Qt.white)
                self.set_result_label("")

        if self.rotation % 2 == 1:
            self.matrix = np.rot90(self.matrix)

        self.print_matrix()


