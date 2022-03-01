from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout


class Window1(QMainWindow):
    verifySignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.matrixRow = None

        self.widget = QWidget()

        # initilasize UI
        self.init_UI()
        # connect handler
        self.connect_slot()

    def init_UI(self):
        # set window title
        self.setWindowTitle("findPatternDNA")

        # set window dimension
        self.setGeometry(650, 400, 300, 100)

        # set possible error message box
        self.errorMsg = QMessageBox()
        self.errorMsg.setWindowTitle("Error pop up")

        # set stylesheet
        self.setStyleSheet("QLabel {"
                           "font: arial, 15px;"
                           "}"
                           "QPushButton {"
                           "margin: 10 px;"
                           "font: arial, 15px; "
                           "}")

        # defining button
        self.submitButton = QPushButton("Submit")
        self.submitButton.setFixedWidth(100)
        self.submitButton.setFixedHeight(60)

        # defining labels
        label1 = QLabel("Matrix row:")
        label2 = QLabel("Matrix column:")

        # defining text box
        self.textBox1 = QLineEdit()
        self.textBox2 = QLineEdit()


        # defining vertical layout
        box1 = QVBoxLayout()
        box1.addWidget(label1)
        box1.addWidget(self.textBox1)
        box1.addWidget(label2)
        box1.addWidget(self.textBox2)
        box1.addWidget(self.submitButton, alignment=QtCore.Qt.AlignCenter)

        self.widget.setLayout(box1)
        self.setCentralWidget(self.widget)

    def on_button_clicked(self):
        if self.textBox1.text() == "" or self.textBox2.text() == "":
            self.errorMsg.setText("No parameter inserted!")
            self.errorMsg.exec()
            return

        if not self.textBox1.text().isnumeric() or not self.textBox2.text().isnumeric():
            self.errorMsg.setText("Input type isn't valid!")
            self.errorMsg.exec()
            return

        self.matrixRow = self.textBox1.text()
        self.matrixCol = self.textBox2.text()

        # emit a signal to inform controller that he can get the input
        self.verifySignal.emit()

    # clear all textbox
    def clear_texts_boxs(self):
        self.textBox1.clear()

    # connect all textbox to handler
    def connect_slot(self):
        self.submitButton.clicked.connect(self.on_button_clicked)
        self.textBox2.returnPressed.connect(self.on_button_clicked)
