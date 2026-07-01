import sys
import json
from ui_converter import UiMainWindow
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QComboBox, QDoubleSpinBox, QMenu)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._bind_signals()

    def _setup_ui(self):
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

    def _bind_signals(self):
        self.list_of_country()

    def closeEvent(self, event):
        pass

    def list_of_country(self):
        with open('data/rates.json') as data:
            data = json.load(data)['rates']
            course = [cour for cour in data.values()]
            self.ui.combo_to.addItems([val for val in data.keys()])
            self.ui.combo_from.addItems([val for val in data.keys()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


