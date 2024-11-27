import io
import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        # f = io.StringIO(templ)
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        res = cur.execute(f'select * from coffee').fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'sort', 'degree', 'molotiy',
                                                    'about', 'price', 'volume'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(list(row)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()

    sys.exit(app.exec())
