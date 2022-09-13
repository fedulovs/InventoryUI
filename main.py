import sys

import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("devices.ui", self)

        self.setStyleSheet("background-color: white;")

        # set the title
        self.setWindowTitle("Device inventory")

        # setting the geometry of window
        self.setGeometry(0, 0, 900, 2000)

        # button settings
        self.addDevice.setStyleSheet(
            "border-radius : 50; border: 2 px solid black; background-color : blue; color: white")
        self.addDevice.setGeometry(200, 150, 100, 100)
        self.addDevice.move(1000, 700)
        self.addDevice.clicked.connect(lambda: self.add_device())

        self.tableWidget.resize(950, 700)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setColumnWidth(5, 190)
        self.load_data()

    def load_data(self):
        url = "http://127.0.0.1:8000/get-items"
        res = requests.get(url)
        devices = res.json()
        row = 0
        self.tableWidget.setRowCount(len(devices))
        for device in devices:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(device["brand"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(device["device"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(device["os_version"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(device["owner"]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(device["comments"]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(device["not_compatible_with"]))
            row = row + 1

    def add_device(self):
        print("clicked")


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
