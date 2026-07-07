import sys
import os
import json

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtGui import QPixmap, QShortcut
from PyQt6.QtCore import QSettings
from PIL import Image, ImageQt

from ui_converter import UiMainWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MyApp", "RatesConverter")
        self.rates = None
        self.reply = None
        self._setup_ui()
        self._bind_signals()
        self.theme_now = 'black'

    def _setup_ui(self):
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        geometry = self.settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
        self.ui.input_amount.setMinimum(0.0)
        self.ui.input_amount.setMaximum(9.9e45)
        self.ui.input_amount.setSpecialValueText(' ')

    def _bind_signals(self):
        self._data_layer()

        self.ui.btn_swap.clicked.connect(self.click_on_reverse)
        self.ui.combo_from.currentTextChanged.connect(self._logic)
        self.ui.combo_to.currentTextChanged.connect(self._logic)
        self.ui.input_amount.valueChanged.connect(self._logic)
        self._logic()

        self.ui.btn_swap.setShortcut('Space')
        shortcut_theme = QShortcut("Ctrl+T", self)
        shortcut_theme.activated.connect(self._toggle_theme)  

    def closeEvent(self, event):
        self.reply = QMessageBox.question(self, 'EXIT', 'Are you sure?',
                                          (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No))
        if self.reply == QMessageBox.StandardButton.Yes:
            self.settings.setValue("window_geometry", self.saveGeometry())
            event.accept()
        else:
            event.ignore()

    def _data_layer(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'data', 'rates.json')) as data:
                self.rates = json.load(data)['rates']
        except FileNotFoundError:
            QMessageBox.critical(self, 'Critical ERROR', 'rates.json is not found')
            sys.exit()
        self.ui.combo_to.addItems(self.rates.keys())
        self.ui.combo_from.addItems(self.rates.keys())

    def click_on_reverse(self):
        word = self.ui.combo_from.currentText()
        self.ui.combo_from.setCurrentText(self.ui.combo_to.currentText())
        self.ui.combo_to.setCurrentText(word)

    def _logic(self):
        currency_from = self.ui.combo_from.currentText()
        currency_to = self.ui.combo_to.currentText()
        image_path_from = os.path.join(os.path.dirname(__file__), "assets", f"{currency_from.lower()}.png")
        image_path_to = os.path.join(os.path.dirname(__file__), "assets", f"{currency_to.lower()}.png")

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

        if currency_to in self.rates and currency_from in self.rates:

            amount = self.ui.input_amount.value()
            rate = (1 / self.rates[currency_from]) * self.rates[currency_to]

            if amount >= 0 and rate > 0:
                result = amount * rate
                self.ui.label_result.setText(f'{result:.2f}'.replace('.', ','))
            else:
                self.ui.label_result.setText("0,00")
        else:
            self.ui.label_result.setText("0,00")

    def _apply_theme(self):
        if self.theme_now == 'white':
            try:
                with open(os.path.join(os.path.dirname(__file__), 'data', 'light_theme.css'), 'r') as theme:
                    self.setStyleSheet(theme.read())
            except FileNotFoundError:
                QMessageBox.warning(self, 'Warning', 'light_theme.css is not found')
        else:
            try:
                with open(os.path.join(os.path.dirname(__file__), 'data', 'black_theme.css'), 'r') as theme:
                    self.setStyleSheet(theme.read())
            except FileNotFoundError:
                QMessageBox.warning(self, 'Warning', 'black_theme.css is not found')

    def _toggle_theme(self):
        if self.theme_now == 'black':
            self.theme_now = 'white'
            self._apply_theme()
        else:
            self.theme_now = 'black'
            self._apply_theme()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
