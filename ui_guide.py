from PyQt5.QtCore import QCoreApplication, QMetaObject, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(400, 220)

        self.centralwidget = QWidget(MainWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)

        fontTitle = QFont()
        fontTitle.setPointSize(16)
        fontTitle.setBold(True)

        fontBody = QFont()
        fontBody.setPointSize(12)

        self.label_title = QLabel("ENCODING FILE")
        self.label_title.setFont(fontTitle)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_title)

        # Input
        self.layout_input = QHBoxLayout()
        self.label_input = QLabel("INPUT")
        self.label_input.setFont(fontBody)
        self.Input_text = QLineEdit()
        self.Input_text.setFont(fontBody)
        self.Button_input = QPushButton("Chọn")
        self.Button_input.setFont(fontBody)
        self.layout_input.addWidget(self.label_input)
        self.layout_input.addWidget(self.Input_text)
        self.layout_input.addWidget(self.Button_input)
        self.verticalLayout.addLayout(self.layout_input)

        # Output
        self.layout_output = QHBoxLayout()
        self.label_output = QLabel("OUTPUT")
        self.label_output.setFont(fontBody)
        self.output_text = QLineEdit()
        self.output_text.setFont(fontBody)
        self.Button_output = QPushButton("Chọn")
        self.Button_output.setFont(fontBody)
        self.layout_output.addWidget(self.label_output)
        self.layout_output.addWidget(self.output_text)
        self.layout_output.addWidget(self.Button_output)
        self.verticalLayout.addLayout(self.layout_output)

        # Controls
        self.layout_controls = QHBoxLayout()
        self.Funtion_choice = QComboBox()
        self.Funtion_choice.setFont(fontBody)
        self.Funtion_choice.addItem("Mã Hóa")
        self.Funtion_choice.addItem("Biên Dịch")
        self.Button_Run = QPushButton("RUN")
        self.Button_Run.setFont(fontBody)
        self.Button_Cancel = QPushButton("CANCEL")
        self.Button_Cancel.setFont(fontBody)
        self.layout_controls.addWidget(self.Funtion_choice)
        self.layout_controls.addWidget(self.Button_Run)
        self.layout_controls.addWidget(self.Button_Cancel)
        self.verticalLayout.addLayout(self.layout_controls)

        # Status label
        self.label_status = QLabel("")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_status)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        QMetaObject.connectSlotsByName(MainWindow)
