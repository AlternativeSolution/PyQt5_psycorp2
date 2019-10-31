#!/usr/bin/python3
# -*- coding: utf-8 -*-

import psycopg2
import sys
import main_window_design
import child_window_design

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidgetItem,
                             QMainWindow, QMessageBox, QAbstractItemView)

connection_data = "host='localhost' \n\
            dbname='lab_db' user='postgres' password='123'"


class child_window(QWidget, child_window_design.Ui_Dialog):
    def create_window(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.show()
        self.buttonBox.rejected.connect(self.quit)
        self.buttonBox.accepted.connect(self.insert_record)

    def insert_stud(self):
        pass

    @pyqtSlot()
    def quit(self):
        self.close()

    def insert_record(self):
        name = self.tableWidget.item(0, 0)
        name = str(name.text())
        second_name = self.tableWidget.item(0, 1)
        second_name = str(second_name.text())
        middle_name = self.tableWidget.item(0, 2)
        middle_name = str(middle_name.text())
        group_id = self.tableWidget.item(0, 3)
        group_id = str(group_id.text())
        address = self.tableWidget.item(0, 4)
        address = str(address.text())
        course = self.tableWidget.item(0, 5)
        course = str(course.text())

        try:
            con = psycopg2.connect(connection_data)
            cur = con.cursor()

            cur.execute("INSERT INTO student(first_name, second_name, \n\
                        middle_name, id_group, address, cource) \n\
                        VALUES (%s, %s, %s, %s, %s, %s);",
                        (name, second_name, middle_name,
                         group_id, address, course,))

            con.commit()
            QMessageBox.information(self, 'Sucses', "Record sucsesfuly insert",
                                    QMessageBox.Ok, QMessageBox.Ok)
            self.quit()

        except psycopg2.DatabaseError as er:
            err = er.diag.message_primary
            QMessageBox.information(self, 'Error', err, QMessageBox.Ok,
                                    QMessageBox.NoButton)
        finally:
            if con:
                con.rollback()
                con.close()


class main_window(QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_add.clicked.connect(self.on_btn_add_click)
        self.btn_remove.clicked.connect(self.on_btn_remove_click)
        self.table1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.read_table()
        self.show()

    def read_table(self, table_name='student'):
        try:
            con = psycopg2.connect(connection_data)
            cur = con.cursor()

            # set table size
#              cur.execute("SELECT count(1) from %s", (table_name, ))
            cur.execute("SELECT count(1) from " + table_name)
            amountRows = cur.fetchone()
            #  cur.execute("select count(1) from (select column_name from\n\
            #  information_schema.columns where table_schema = 'public' \n\
            #              and table_name = '%s') as numcol;", (table_name,))
            cur.execute("select count(1) from (select column_name from\n\
            information_schema.columns where table_schema = 'public' \n\
                        and table_name = '" + table_name + "') as numcol;")
            amountColums = cur.fetchone()
            amountRows = int(amountRows[0])
            amountColums = int(amountColums[0])
            self.table1.setRowCount(amountRows)
            self.table1.setColumnCount(amountColums)

            hor_label = ["ID", "Name", "Second Name", "Middle Name",
                         "Group ID", "Address", "Course"]
            self.table1.setHorizontalHeaderLabels(hor_label)
            cur.execute("SELECT * FROM " + table_name)

            i = 0
            for i in range(amountRows):
                row = cur.fetchone()

                if row is None:
                    break
                for j in range(amountColums):
                    self.table1.setItem(i, j, QTableWidgetItem(str(row[j])))

        except psycopg2.DatabaseError as er:
            err = er.diag.message_primary
            QMessageBox.information(self, 'Error', err, QMessageBox.Ok,
                                    QMessageBox.NoButton)
            if con:
                con.rollback()

        finally:
            if con:
                con.close()

    def create_child_window(self):
        self.child_window = child_window()
        self.child_window.create_window()
        self.child_window.show()
        self.read_table()

    @pyqtSlot()
    def on_menuExit_click(self):
        answer = QMessageBox.question(self, 'Exit', "You are shure?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.Yes)

        if answer == QMessageBox.Yes:
            pass

    def on_btn_add_click(self):
        self.create_child_window()
        self.read_table()

    def on_btn_remove_click(self):
        removedItemName = "current item"
        try:
            con = psycopg2.connect(connection_data)
            cur = con.cursor()

            idToDelete = self.table1.item(self.table1.currentRow(), 0)
            tmpStr = str(idToDelete.text())
            cur.execute("SELECT * FROM student where id = %s;", (tmpStr,))

            row = cur.fetchone()
            removedItemName = str(row[1]) + " " + str(row[2])

            con.commit()
        except psycopg2.DatabaseError:
            if con:
                con.rollback()
                con.close()

        answer = QMessageBox.question(self, 'Remove', "Remove " +
                                      removedItemName + "?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)

        if answer == QMessageBox.Yes:
            try:
                cur.execute("delete from student where id = %s", (tmpStr,))

                con.commit()

            except psycopg2.Error as er:  # todo
                err = er.diag.message_primary
                QMessageBox.information(self, 'Error', err, QMessageBox.Ok,
                                        QMessageBox.NoButton)
                if con:
                    con.rollback()

            finally:
                if con:
                    con.close()
        self.read_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    sys.exit(app.exec_())
