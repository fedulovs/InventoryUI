import sqlite3

from model import Device

conn = sqlite3.connect('devices.db')

c = conn.cursor()


# Create table
# c.execute("""CREATE TABLE devices (
#             device_name text,
#             brand text,
#             os_name text,
#             os_version text,
#             cpu text,
#             owner text,
#             snipe_it text,
#             serial_number text,
#             identifier text,
#             comment text
#             )""")


def get_all_devices(device_id):
    c.execute("SELECT * FROM devices WHERE device_id = :device_id")
    c.fetchone()
    # c.fetchall()


def get_device_by_id():
    pass


device_1 = Device('iphone 14', 'Apple', 'iOS', '15', 'cpu', 'cabinet', '45254435', 'DDDS123432', 'no comments', '12')


def add_device(device):
    with conn:
        c.execute("""INSERT INTO devices VALUES (
        :device_name, 
        :brand, 
        :os_name, 
        :os_version, 
        :cpu,
        :owner, 
        :snipe_it, 
        :serial_number, 
        :identifier, 
        :comment)""", {'device_name': device.device_name, 'brand': device.brand, 'os_name': device.os_name,
                       'os_version': device.os_version, 'cpu': device.cpu, 'owner': device.owner,
                       'snipe_it': device.snipe_it, 'serial_number': device.serial_number,
                       'identifier': device.identifier, 'comment': device.comment})


add_device(device_1)


def change_owner(device):
    pass


def update_device(device):
    pass


conn.close()
