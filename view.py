import sys

import requests
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

device = {}
users = ['Sergey', 'Sam', 'Cabinet']


class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("user_cloud.ui", self)

        # Add user button
        self.add_new_user_button.clicked.connect(lambda: self.add_new_user())

        # Populate user picker with user list
        with open('users.txt', 'r') as f:
            for line in f:
                self.user_picker.addItem(line.strip())
            f.close()

        # Open device list button
        self.login_button.clicked.connect(lambda: self.open_devices_list())

    def add_new_user(self):
        print("Add new user button clicked")
        create_user_window = CreateUserWindow()
        widget.addWidget(create_user_window)
        widget.setFixedHeight(800)
        widget.setFixedWidth(1200)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def open_devices_list(self):
        print("Login button clicked")
        user = self.user_picker.currentText()
        if len(user) == 0:
            self.error_text.setText("You should pick a user")
        else:
            main_window = MainWindow()
            widget.addWidget(main_window)
            widget.setFixedHeight(800)
            widget.setFixedWidth(1200)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            device['owner'] = user


class CreateUserWindow(QDialog):
    def __init__(self):
        super(CreateUserWindow, self).__init__()
        loadUi("create_user.ui", self)

        self.back_button.setIcon(QIcon('icons/arrow-left.svg'))

        self.create_new_user_button.clicked.connect(lambda: self.add_new_user())
        self.back_button.clicked.connect(lambda: self.go_back())

    def add_new_user(self):
        if len(self.user_name_input.text()) == 0:
            self.error_text.setText("Name should not be empty")
        else:
            # users.append(self.user_name_input.text())
            with open('users.txt', 'a') as f:
                f.write('\n')
                f.write(''.join(self.user_name_input.text()))
                f.close()
            print(users)

    def go_back(self):
        print("Going back to login window")
        login_window = LoginWindow()
        widget.addWidget(login_window)
        widget.setFixedHeight(850)
        widget.setFixedWidth(1120)
        widget.setCurrentIndex(widget.currentIndex() + 1)


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

        self.tableWidget.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, selected):
        for index in selected.indexes():
            print(f'selected cell location row is {index.row()}, Column is {index.column()}')
            url = f"http://127.0.0.1:8000/get-item/{index.row() + 1}"
            res = requests.get(url)
            chosen_device = res.json()
            print(f'device is {chosen_device}')
            device["device"] = chosen_device["device"]
            device["owner"] = chosen_device["owner"]
            device["os_version"] = chosen_device["os_version"]
            device["comments"] = chosen_device["comments"]
            print(device)
            self.open_device_info()

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

    def open_device_info(self):
        print("Open Device info button clicked")
        device_info = DeviceInfo()
        widget.addWidget(device_info)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog1(QDialog):
    def __init__(self):
        super(DeviceDialog1, self).__init__()
        loadUi("add_device1.ui", self)

        # Back button
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

        confirmation_screen = ConfirmationDialogue()
        widget.addWidget(confirmation_screen)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)

        device['not_compatible_with'] = self.dropdown.currentText()

    def go_back(self):
        print("Going back to screen 3")
        add_device3 = DeviceDialog3()
        widget.addWidget(add_device3)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ConfirmationDialogue(QDialog):

    def __init__(self):
        super(ConfirmationDialogue, self).__init__()
        loadUi("add_device_confirmation.ui", self)

        text = ''

        for key, value in device.items():
            text += ("{}: {}".format(key, value) + '\n')

        self.confirm_text.setText(f'Are you sure you want to add this \ndevice? \n\n{text}')

        self.confirm_button.clicked.connect(lambda: self.add_device())
        self.back_button.clicked.connect(lambda: self.go_back())

    def add_device(self):
        self.request_add_device()
        # print device fields
        for key in device.keys():
            print(device.get(key))

        print(device)

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

        self.open_devices_list()

    def open_devices_list(self):
        main_window = MainWindow()
        widget.addWidget(main_window)
        widget.setFixedHeight(800)
        widget.setFixedWidth(1200)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_back(self):
        print("Going back to screen 4")
        add_device4 = DeviceDialog4()
        widget.addWidget(add_device4)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceInfo(QDialog):
    def __init__(self):
        super(DeviceInfo, self).__init__()
        loadUi("device_info.ui", self)
        widget.setFixedHeight(430)
        widget.setFixedWidth(1120)

        self.back_button.setIcon(QIcon('icons/arrow-left.svg'))
        self.back_button.clicked.connect(lambda: self.go_back())

        self.device_name.setText(device["device"])
        self.owner.setText(device["owner"])
        self.os_version.setText(device["os_version"])
        self.comments.setText(device["comments"])

    def take_device(self):
        print("Add new user button clicked")
        # TODO: change device owner
        # TODO: open cabinet

    def change_device_info(self):
        print("Add new user button clicked")
        # TODO: open device fields

    def go_back(self):
        print("Going back to main window")
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setFixedHeight(850)
        widget.setFixedWidth(1120)
        widget.setCurrentIndex(widget.currentIndex() + 1)


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
