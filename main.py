import sys

import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

device = {}


class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("login_screen.ui", self)

        self.login_button.clicked.connect(lambda: self.open_devices_list())

    def open_devices_list(self):
        print("Login button clicked")
        main_window = MainWindow()
        widget.addWidget(main_window)
        widget.setFixedHeight(800)
        widget.setFixedWidth(1200)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        device['owner'] = self.login_input.text()


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("devices.ui", self)

        self.setWindowTitle("Device inventory")

        # Add button settings
        self.add_device_button.setGeometry(200, 150, 100, 100)
        self.add_device_button.move(1000, 600)
        self.add_device_button.clicked.connect(lambda: self.add_device())

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
        print("Open Device button clicked")
        add_device1 = DeviceDialog1()
        widget.addWidget(add_device1)
        widget.setFixedHeight(500)
        widget.setFixedWidth(400)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog1(QDialog):
    def __init__(self):
        super(DeviceDialog1, self).__init__()
        loadUi("add_device1.ui", self)

        # Back button
        self.backButton.setStyleSheet(
            "border-radius : 50; border: 2 px solid black; color: black")
        self.backButton.setGeometry(10, 10, 100, 100)
        self.backButton.clicked.connect(lambda: self.go_back())

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_os_input())

    def open_os_input(self):
        print("Open OS button clicked")
        add_device2 = DeviceDialog2()
        widget.addWidget(add_device2)
        widget.setFixedHeight(500)
        widget.setFixedWidth(400)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        device['brand'] = self.brandInput.text()
        device['device'] = self.deviceInput.text()

    def go_back(self):
        print("Going back to main window")
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setFixedHeight(850)
        widget.setFixedWidth(1120)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog2(QDialog):
    def __init__(self):
        super(DeviceDialog2, self).__init__()
        loadUi("add_device2.ui", self)

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_comments_input())

        # Back button
        self.backButton.setGeometry(10, 10, 100, 100)
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_comments_input(self):
        print("Open Comments button clicked")
        add_device3 = DeviceDialog3()
        widget.addWidget(add_device3)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        device['os_version'] = self.osInput.text()

    def go_back(self):
        print("Going back to screen 1")
        add_device1 = DeviceDialog1()
        widget.addWidget(add_device1)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog3(QDialog):
    def __init__(self):
        super(DeviceDialog3, self).__init__()
        loadUi("add_device3.ui", self)

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_not_compatible_input())

        # Back button
        self.backButton.setGeometry(10, 10, 100, 100)
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_not_compatible_input(self):
        print("Open Not compatible button clicked")
        add_device4 = DeviceDialog4()
        widget.addWidget(add_device4)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        device['comments'] = self.commentsInput.toPlainText()

    def go_back(self):
        print("Going back to screen 2")
        add_device2 = DeviceDialog2()
        widget.addWidget(add_device2)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog4(QDialog):
    def __init__(self):
        super(DeviceDialog4, self).__init__()
        loadUi("add_device4.ui", self)

        self.dropdown.addItem('-')
        self.dropdown.addItem('Guitar Tuna')
        self.dropdown.addItem('Yousician')
        self.dropdown.addItem('Campfire')
        self.dropdown.addItem('Lessons')

        # Add device button
        self.nextButton.clicked.connect(lambda: self.open_confirmation_screen())

        # Back button
        self.backButton.setGeometry(10, 10, 100, 100)
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_confirmation_screen(self):
        print("Confirmation button clicked")
        device['not_compatible_with'] = self.dropdown.currentText()
        self.request_add_device()

        # print device fields
        for key in device.keys():
            print(device.get(key))

        print(device)

    def go_back(self):
        print("Going back to screen 3")
        add_device3 = DeviceDialog3()
        widget.addWidget(add_device3)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def request_add_device(self):
        # {
        #     "brand": "string",
        #     "device": "string",
        #     "owner": "string",
        #     "os_version": "string",
        #     "comments": "string",
        #     "not_compatible_with": "string"
        # }

        url = "http://127.0.0.1:8000/create-item"
        res = requests.post(url, json=device)
        print(res.json())


app = QApplication(sys.argv)

login_window = LoginWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login_window)

widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
