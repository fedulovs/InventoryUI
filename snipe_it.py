import requests
from decouple import config

from model import Device

TEST_API_KEY = config('TEST_API_KEY')
API_KEY = config('API_KEY')

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": API_KEY
}


def get_all_devices():
    response = requests.get(config('HARDWARE_URL'), headers=headers)

    json_response = response.json()
    devices = json_response['rows']

    # print(devices)
    return devices

    # model[name] = device_name i.e. Samsung Galaxy S22+
    # model_number = "S22+"
    # asset_tag = snipe_it
    # category["name"] = "Smart phone"
    # manufacturer["name"] = Apple / Samsung
    # notes = comments
    # image = image
    # assigned_to[username], [name], [first_name], [last_name]
    # Color[value] = black
    # id = snipe_it_id
    # serial = serial_number

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


def get_devices_number():
    response = requests.get(config('HARDWARE_URL'), headers=headers)

    json_response = response.json()
    devices_count = json_response['total']

    return devices_count


def get_device_by_row(row):
    devices = get_all_devices()
    return devices[row]


def build_device_from_json(device):
    device = Device(
        device_name=device['model']['name'],
        brand=device['manufacturer']['name'],
        os_name='',
        os_version='',
        cpu='',
        owner=device['assigned_to']['username'],
        snipe_it=device['asset_tag'],
        serial_number=device['serial'],
        identifier='',
        comment=device['notes'],
        image_url=device['image'])

    return device


def add_device_to_snipe_it():
    url = config('HARDWARE_URL')

    payload = {
        "archived": False,
        "warranty_months": None,
        "depreciate": False,
        "supplier_id": None,
        "requestable": False,
        "rtd_location_id": None,
        "last_audit_date": "null",
        "location_id": None,
        "asset_tag": "1",
        "status_id": 2,
        "model_id": 3
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


# get_devices_number()
get_all_devices()
# add_device_to_snipe_it()
