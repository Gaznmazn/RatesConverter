import sys
import json
from ui_converter import UiMainWindow
from PyQt6.QtWidgets import (QApplication, QWidget)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.rates = None
        self._setup_ui()
        self._bind_signals()

    def _setup_ui(self):
        self.ui = UiMainWindow()
        self.ui.setupUi(self)

    def _bind_signals(self):
        self.list_of_country()
        self.ui.btn_swap.clicked.connect(self.click_on_reverse)
        self.ui.combo_from.currentTextChanged.connect(self.count_course)
        self.ui.combo_to.currentTextChanged.connect(self.count_course)
        self.ui.input_amount.valueChanged.connect(self.count_course)
        self.count_course()

    def closeEvent(self, event):
        pass

    def list_of_country(self):
        with open('data/rates.json') as data:
            self.rates = json.load(data)['rates']
            self.ui.combo_to.addItems([val for val in self.rates.keys()])
            self.ui.combo_from.addItems([val for val in self.rates.keys()])

    def click_on_reverse(self):
        word = self.ui.combo_from.currentText()
        self.ui.combo_from.setCurrentText(self.ui.combo_to.currentText())
        self.ui.combo_to.setCurrentText(word)

    def count_course(self):
        course_from = self.ui.combo_from.currentText()
        course_to = self.ui.combo_to.currentText()
        input_count = self.ui.input_amount.value()
        result = f'{(input_count / self.rates[course_from]) * self.rates[course_to]:.2f}'.replace('.', ',')
        self.ui.label_result.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
