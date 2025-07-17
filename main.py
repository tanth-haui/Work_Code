import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_guide import Ui_MainWindow
from controller import MainController

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller = MainController(self.ui)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
