import sys
import json
from ui_converter import UiMainWindow
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QComboBox, QDoubleSpinBox, QMenu)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

    def _setup_ui(self):
        pass

    def _bind_signals(self):
        pass

    def closeEvent(self, event):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


