import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QColor


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.check_status = None
        self.label = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Server Status')
        self.setGeometry(100, 100, 1920, 1080)

        # Set background color to light brown
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(204, 204, 102))
        self.setPalette(p)

        # Create label and output window
        self.label = QLabel('Server Status: Unknown', self)
        output_window = QWidget(self)
        output_window.setWindowTitle('Server Status Output')
        output_window.setGeometry(200, 200, 400, 600)
        output_window.setAutoFillBackground(True)
        p = output_window.palette()
        p.setColor(output_window.backgroundRole(), QColor(0, 0, 0))
        output_window.setPalette(p)
        output_label = QLabel(self.get_server_status(), output_window)
        output_label.setStyleSheet('color: rgb(255, 255, 255);')

        # Create a vertical layout manager
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(output_window)

        # Apply the layout manager to the window
        self.setLayout(vbox)

    def get_server_status(self):
        # Run ServerStatusTest.py and get output
        output = subprocess.check_output(['python', 'ServerStatusTest.py'])
        output_str = output.decode()
        return output_str


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
