import sys
import os
import json
from ui_converter import Ui_main_window
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPixmap
from PIL import Image, ImageQt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.rates = None
        self._setup_ui()
        self._bind_signals()

    def _setup_ui(self):
        self.ui = Ui_main_window()
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
        currency_from = self.ui.combo_from.currentText()
        currency_to = self.ui.combo_to.currentText()
        image_path_from = f'{os.path.join(os.path.dirname(__file__), "assets", f"{currency_from.lower()}.png")}'
        image_path_to = f'{os.path.join(os.path.dirname(__file__), "assets", f"{currency_to.lower()}.png")}'

        if os.path.exists(image_path_from):
            image_from = Image.open(image_path_from).resize((32, 32))
            image_from_pixmap = QPixmap.fromImage(ImageQt.ImageQt(image_from))
            self.ui.label_icon_from.setPixmap(image_from_pixmap)
        else:
            self.ui.label_icon_from.clear()

        if os.path.exists(image_path_to):
            image_to = Image.open(image_path_to).resize((32, 32))
            image_to_pixmap = QPixmap.fromImage(ImageQt.ImageQt(image_to))
            self.ui.label_icon_to.setPixmap(image_to_pixmap)
        else:
            self.ui.label_icon_to.clear()

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
