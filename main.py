import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QInputDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.delete_button.clicked.connect(self.delete_row)
        self.add_button.clicked.connect(self.add_row)

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.load_data()

    def load_data(self):
        res = self.cur.execute(f'select * from coffee').fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'sort', 'degree', 'moloti',
                                                    'about', 'price', 'volume'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(list(row)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def add_row(self):
        sort, ok1 = QInputDialog.getText(self, 'Input', 'Enter sort:')
        degree, ok2 = QInputDialog.getText(self, 'Input', 'Enter degree:')
        moloti, ok3 = QInputDialog.getText(self, 'Input', 'Enter moloti:')
        about, ok4 = QInputDialog.getText(self, 'Input', 'Enter about:')
        price, ok5 = QInputDialog.getDouble(self, 'Input', 'Enter price:')
        volume, ok6 = QInputDialog.getDouble(self, 'Input', 'Enter volume:')

        if ok1 and ok2 and ok3 and ok4 and ok5 and ok6:
            self.cur.execute(
                'INSERT INTO coffee (sort, degree, moloti, about, price, volume) VALUES (?, ?, ?, ?, ?, ?)',
                (sort, degree, moloti, about, price, volume))
            self.con.commit()
            self.load_data()

    def delete_row(self):
        current_row = self.tableWidget.currentRow()
        if current_row >= 0:
            item = self.tableWidget.item(current_row, 0)
            if item is not None:
                coffee_id = item.text()
                self.cur.execute('DELETE FROM coffee WHERE id = ?', (coffee_id,))
                self.con.commit()
                self.load_data()
        else:
            QMessageBox.warning(self, 'Warning', 'No row selected!')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()

    sys.exit(app.exec())
