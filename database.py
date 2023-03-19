import sqlite3

from model import Device

conn = sqlite3.connect('devices.db')
conn.row_factory = sqlite3.Row
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


def build_device_from_db(device_row):
    device = Device(
        device_name=device_row[0],
        brand=device_row[1],
        os_name=device_row[2],
        os_version=device_row[3],
        cpu=device_row[4],
        owner=device_row[5],
        snipe_it=device_row[6],
        serial_number=device_row[7],
        identifier=device_row[8],
        comment=device_row[9]
    )

    return device


def get_all_devices():
    with conn:
        c.execute("SELECT * FROM devices")
        devices = c.fetchall()

        device_list = []

        for row in devices:
            device_obj = build_device_from_db(row)
            device_list.append(device_obj)

        return device_list


def get_devices_by_os(os):
    with conn:
        c.execute("SELECT * FROM devices WHERE os_name LIKE?", (os,))
        devices = c.fetchall()

        device_list = []

        for row in devices:
            device_obj = build_device_from_db(row)
            device_list.append(device_obj)

        return device_list


# get_devices_by_os("Android")


def get_device_by_name(device_name):
    c.execute("SELECT * FROM devices WHERE device_name LIKE?", (device_name,))
    device = c.fetchone()
    # TODO call method parse device and Return result of call

    print(device)


# get_device_by_name("iphone 8")


def get_device_by_row(row_id):
    c.execute("SELECT * FROM devices WHERE rowid LIKE?", (row_id,))
    db_result = c.fetchone()
    device_obj = build_device_from_db(db_result)

    # print(device_obj.device_name)

    return device_obj


# get_device_by_row(1)

# device_1 = Device('iphone 14', 'Apple', 'iOS', '15', 'cpu', 'cabinet', '45254435', 'DDDS123432', '1', 'no comments')
# device_2 = Device('iphone 8', 'Apple', 'iOS', '13', 'cpu', 'cabinet', '1234556', 'FDDS123432', '123',
#                   'Screen was replaced')


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

        conn.commit()


# add_device(device_2)


def change_owner(device):
    pass


def update_device(new_value, serial_number):
    with conn:
        c.execute("UPDATE devices SET identifier=? WHERE serial_number=?", (new_value, serial_number))


# update_device("1433", "FDDS123432")


def delete_device(serial_number):
    with conn:
        c.execute("DELETE FROM devices WHERE serial_number=?", (serial_number,))

# delete_device("FDDS123432")
