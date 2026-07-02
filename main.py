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
        self.ui.input_amount.setMinimum(0.0)
        self.ui.input_amount.setMaximum(9999999999999999999999999999999999999999999999.0)

    def _bind_signals(self):
        self._data_layer()
        self.ui.btn_swap.clicked.connect(self.click_on_reverse)
        self.ui.combo_from.currentTextChanged.connect(self._logic)
        self.ui.combo_to.currentTextChanged.connect(self._logic)
        self.ui.input_amount.valueChanged.connect(self._logic)
        self._logic()

    def closeEvent(self, event):
        event.accept()

    def _data_layer(self):
        with open('data/rates.json') as data:
            self.rates = json.load(data)['rates']
        self.ui.combo_to.addItems([val for val in self.rates.keys()])
        self.ui.combo_from.addItems([val for val in self.rates.keys()])

    def click_on_reverse(self):
        word = self.ui.combo_from.currentText()
        self.ui.combo_from.setCurrentText(self.ui.combo_to.currentText())
        self.ui.combo_to.setCurrentText(word)

    def _logic(self):
        image_path = ''
        currency_from = self.ui.combo_from.currentText()
        currency_to = self.ui.combo_to.currentText()
        amount = self.ui.input_amount.value()
        rate = (1 / self.rates[currency_from]) * self.rates[currency_to]

        if amount >= 0 and rate > 0:
            result = amount * rate
            self.ui.label_result.setText(f'{result:.2f}'.replace('.', ','))
        else:
            self.ui.label_result.setText("0,00")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
