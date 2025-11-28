import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow
from calculator import Calculator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.calculator = Calculator(self.ui)
        
    def keyPressEvent(self, event):
        self.calculator.keyPressEvent(event)
 

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.setWindowTitle("Калькулятор")
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()