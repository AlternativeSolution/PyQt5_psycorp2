#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QPushButton, QMainWindow)


class child_window(QWidget):
    def create_window(self):
        super(child_window, self).__init__(None)
        self.setGeometry(200, 200, 800, 200)
        self.setWindowTitle('Child window')


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Main window')
        btn_show_child = QPushButton('Show Child', self)
        btn_show_child.move(200, 200)
        btn_show_child.clicked.connect(self.on_click)
        self.show()

    def create_child_window(self):
        self.child_window = child_window()
        self.child_window.create_window()
        self.child_window.show()

    @pyqtSlot()
    def on_click(self):
        self.create_child_window()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    sys.exit(app.exec_())
