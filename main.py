import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("devices.ui", self)

        self.setStyleSheet("background-color: white;")

        # set the title
        self.setWindowTitle("Device inventory")

        # setting  the geometry of window
        self.setGeometry(0, 0, 900, 1300)

        self.tableWidget.resize(1000, 700)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 120)
        self.tableWidget.setColumnWidth(5, 190)
        self.load_data()

    def load_data(self):
        devices = [{"brand": "Samsung", "device": "Galaxy S10", "os version": "Android 11", "owner": "Jack",
                    "comment": "", "not compatible with": "Guitar tuna"},
                   {"brand": "Xiaomi", "device": "Redmi Note 8T", "os version": "Android 9", "owner": "Cabinet",
                    "comment": "", "not compatible with": ""},
                   {"brand": "Huawei", "device": "P40 Lite", "os version": "Android 11", "owner": "Sergey",
                    "comment": "", "not compatible with": "Guitar tuna"},
                   {"brand": "Xiaomi", "device": "Redmi Note 7", "os version": "Android 10", "owner": "Cabinet",
                    "comment": "Lost since 12.8.22", "not compatible with": ""},
                   {"brand": "Xiaomi", "device": "Redmi Note 8T", "os version": "Android 9", "owner": "Cabinet",
                    "comment": "", "not compatible with": ""},
                   {"brand": "Xiaomi", "device": "Redmi Note 7", "os version": "Android 10", "owner": "Cabinet",
                    "comment": "Lost since 12.8.22", "not compatible with": ""},
                   {"brand": "Xiaomi", "device": "Redmi Note 8T", "os version": "Android 9", "owner": "Cabinet",
                    "comment": "", "not compatible with": ""}]
        row = 0
        self.tableWidget.setRowCount(len(devices))
        for device in devices:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(device["brand"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(device["device"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(device["os version"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(device["owner"]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(device["comment"]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(device["not compatible with"]))
            row = row+1




app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1120)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("exiting")
