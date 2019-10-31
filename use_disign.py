#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import main_window_design
import child_window_design
import psycopg2

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidgetItem,
                             QMainWindow, QMessageBox)


class child_window(QWidget, child_window_design.Ui_Dialog):
    def create_window(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.buttonBox.clicked.connect()

    def insert_stud(self):
        pass


class main_window(QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_add.clicked.connect(self.on_btn_add_click)
        self.btn_remove.clicked.connect(self.on_btn_remove_click)
        self.show()

    def create_child_window(self):
        self.child_window = child_window()
        self.child_window.create_window()
        self.child_window.exec_()
        self.read_table()

    @pyqtSlot()
    def on_menuExit_click(self):
        answer = QMessageBox.question(self, 'Exit', "You are shure?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.Yes)

        if answer == QMessageBox.Yes:
            pass            # todo

    def on_btn_add_click(self):
        self.create_child_window()
        #  self.setWindowModality(ApplicationModal)
        #

    def on_btn_remove_click(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    sys.exit(app.exec_())
