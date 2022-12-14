import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QHeaderView
from PyQt5.uic import loadUi

import database as db
from model import Device

device = {}
new_device = {}
row = None


class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("layouts/user_cloud.ui", self)

        # Add user button
        self.add_new_user_button.clicked.connect(lambda: self.add_new_user())

        # Populate user picker with user list
        with open('data/users.txt', 'r') as f:
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
        global user_name
        user_name = user
        if len(user) == 0:
            self.error_text.setText("You should pick a user")
        else:
            main_window = MainWindow()
            widget.addWidget(main_window)
            widget.setFixedHeight(800)
            widget.setFixedWidth(1200)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            new_device['owner'] = user


class CreateUserWindow(QDialog):
    def __init__(self):
        super(CreateUserWindow, self).__init__()
        loadUi("layouts/create_user.ui", self)

        self.back_button.setIcon(QIcon('icons/arrow-left.svg'))

        self.create_new_user_button.clicked.connect(lambda: self.add_new_user())
        self.back_button.clicked.connect(lambda: self.go_back())

    def add_new_user(self):
        if len(self.user_name_input.text()) == 0:
            self.error_text.setText("Name should not be empty")
        else:
            with open('data/users.txt', 'a') as f:
                f.write('\n')
                f.write(''.join(self.user_name_input.text()))
                f.close()

    def go_back(self):
        print("Going back to login window")
        login_window = LoginWindow()
        widget.addWidget(login_window)
        widget.setFixedHeight(800)
        widget.setFixedWidth(1200)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("layouts/devices_screen.ui", self)

        self.user_name.setText(user_name)

        self.profile_button.setIcon(QIcon('icons/user.svg'))

        # Add button settings
        self.add_device_button.setGeometry(200, 150, 100, 100)
        self.add_device_button.clicked.connect(lambda: self.add_device())

        # self.tableWidget.setColumnWidth(5, 250)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

        self.load_data()

        self.tableWidget.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, selected):
        for index in selected.indexes():
            print(f'selected cell location row is {index.row()}, Column is {index.column()}')
            global row
            global device
            row = index.row() + 1
            device = db.get_device_by_row(index.row() + 1)
            self.open_device_info()
            # TODO Think how to assign parameters to device

    # device['device_name'] = row[0] +
    # device['brand'] = row[1] +
    # device['os_name'] = row[2] +
    # device['os_version'] = row[3] +
    # device['cpu'] = row[4]
    # device['owner'] = row[5]
    # device['snipe_it'] = row[6] +
    # device['serial_number'] = row[7] +
    # device['identifier'] = row[8] +
    # device['comment'] = row[9]

    def load_data(self):
        devices = db.get_all_devices()
        row = 0
        self.tableWidget.setRowCount(len(devices))
        for item in devices:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(item.device_name))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(item.brand))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{item.os_name} {item.os_version}"))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(item.cpu))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(item.owner))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(item.comment))
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
        loadUi("layouts/add_device1.ui", self)

        # Back button
        self.backButton.setIcon(QIcon('icons/arrow-left.svg'))
        self.backButton.clicked.connect(lambda: self.go_back())

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_os_input())

    def open_os_input(self):
        print("Open OS info button clicked")
        add_device2 = DeviceDialog2()
        widget.addWidget(add_device2)
        widget.setFixedHeight(500)
        widget.setFixedWidth(400)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        new_device['device_name'] = self.device_input.text()
        new_device['brand'] = self.brand_input.text()

    def go_back(self):
        print("Going back to main window")
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setFixedHeight(800)
        widget.setFixedWidth(1200)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog2(QDialog):
    def __init__(self):
        super(DeviceDialog2, self).__init__()
        loadUi("layouts/add_device2.ui", self)

        self.os_dropdown.addItem('Android')
        self.os_dropdown.addItem('iOS')
        self.os_dropdown.addItem('Windows')
        self.os_dropdown.addItem('macOS')

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_identifiers_input())

        # Back button
        self.backButton.setIcon(QIcon('icons/arrow-left.svg'))
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_identifiers_input(self):
        print("Open identifiers button clicked")
        add_device3 = DeviceDialog3()
        widget.addWidget(add_device3)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        new_device['os_name'] = self.os_dropdown.currentText()
        new_device['os_version'] = self.os_version_input.text()

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
        loadUi("layouts/add_device3.ui", self)

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_not_compatible_input())

        # Back button
        self.backButton.setIcon(QIcon('icons/arrow-left.svg'))
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_not_compatible_input(self):
        print("Open comments button clicked")
        add_device4 = DeviceDialog4()
        widget.addWidget(add_device4)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)

        new_device['snipe_it'] = self.snipe_it_input.text()
        new_device['serial_number'] = self.serial_number_input.text()
        new_device['identifier'] = self.identifier_input.text()

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
        loadUi("layouts/add_device4.ui", self)

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_cpu_input())

        # Back button
        self.backButton.setIcon(QIcon('icons/arrow-left.svg'))
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_cpu_input(self):
        print("Open cpu button clicked")
        add_device5 = DeviceDialog5()
        widget.addWidget(add_device5)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        new_device['comment'] = self.comments_input.toPlainText()
        print(new_device)

    def go_back(self):
        print("Going back to screen 3")
        add_device3 = DeviceDialog3()
        widget.addWidget(add_device3)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog5(QDialog):
    def __init__(self):
        super(DeviceDialog5, self).__init__()
        loadUi("layouts/add_device5.ui", self)

        # Next button
        self.nextButton.clicked.connect(lambda: self.open_confirmation_screen())

        # Back button
        self.backButton.setIcon(QIcon('icons/arrow-left.svg'))
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_confirmation_screen(self):
        print("Open not compatible with input")
        confirmation_screen = ConfirmationDialogue()
        widget.addWidget(confirmation_screen)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        new_device['cpu'] = self.cpu_input.text()

    def go_back(self):
        print("Going back to screen 4")
        add_device4 = DeviceDialog4()
        widget.addWidget(add_device4)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class DeviceDialog6(QDialog):
    def __init__(self):
        super(DeviceDialog6, self).__init__()
        loadUi("layouts/add_device6.ui", self)

        self.dropdown.addItem('-')
        self.dropdown.addItem('Guitar Tuna')
        self.dropdown.addItem('Yousician')
        self.dropdown.addItem('Campfire')

        # Add device button
        self.nextButton.clicked.connect(lambda: self.open_confirmation_screen())

        # Back button
        self.backButton.setIcon(QIcon('icons/arrow-left.svg'))
        self.backButton.clicked.connect(lambda: self.go_back())

    def open_confirmation_screen(self):
        print("Confirmation button clicked")
        confirmation_screen = ConfirmationDialogue()
        widget.addWidget(confirmation_screen)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        new_device['not_compatible_with'] = self.dropdown.currentText()
        print(new_device)

    def go_back(self):
        print("Going back to screen 5")
        add_device5 = DeviceDialog5()
        widget.addWidget(add_device5)
        widget.setFixedHeight(501)
        widget.setFixedWidth(411)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ConfirmationDialogue(QDialog):

    def __init__(self):
        super(ConfirmationDialogue, self).__init__()
        loadUi("layouts/add_device_confirmation.ui", self)

        text = ''

        for key, value in new_device.items():
            text += ("{}: {}".format(key, value) + '\n')

        self.confirm_text.setText(f'Are you sure you want to add this \ndevice? \n\n{text}')

        self.confirm_button.clicked.connect(lambda: self.add_device())
        self.back_button.clicked.connect(lambda: self.go_back())

    def add_device(self):
        device_1 = Device('iphone 14', 'Apple', 'iOS', '15', 'cpu', 'cabinet', '45254435', 'DDDS123432', '1',
                          'no comments')

        device_object = Device(
            device_name=new_device['device_name'],
            brand=new_device['brand'],
            os_name=new_device['os_name'],
            os_version=new_device['os_version'],
            cpu=new_device['cpu'],
            owner=new_device['owner'],
            snipe_it=new_device['snipe_it'],
            serial_number=new_device['serial_number'],
            identifier=new_device['identifier'],
            comment=new_device['comment'])
        db.add_device(device_object)
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
        loadUi("layouts/device_info.ui", self)
        widget.setFixedHeight(430)
        widget.setFixedWidth(1120)

        self.back_button.setIcon(QIcon('icons/arrow-left.svg'))
        self.back_button.clicked.connect(lambda: self.go_back())

        db_device = db.get_device_by_row(row)

        self.device_name.setText(db_device.device_name)
        self.cpu.setText(db_device.cpu)
        self.owner.setText(db_device.owner)
        self.os_version.setText(f"{db_device.os_name} {db_device.os_version}")
        self.snipe_it.setText(db_device.snipe_it)
        self.serial_number.setText(db_device.serial_number)
        self.identifier.setText(db_device.identifier)
        self.comments.setText(db_device.comment)

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
        widget.setFixedHeight(800)
        widget.setFixedWidth(1200)
        widget.setCurrentIndex(widget.currentIndex() + 1)


app = QApplication(sys.argv)

login_window = LoginWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login_window)

widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.setWindowTitle("Device inventory")
widget.setWindowIcon(QIcon('icons/phone_iphone.svg'))

widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
