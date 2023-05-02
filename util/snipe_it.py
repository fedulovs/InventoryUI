import requests
from decouple import config

from model import Device

last_response_code = ''

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

    return devices


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


def change_device_field(device_id, field, value):
    url = config('HARDWARE_URL') + '/' + str(device_id)
    payload = {
        field: value
    }

    print(url)

    response = requests.patch(url, json=payload, headers=headers)
    print(response.text)

    global last_response_code
    last_response_code = response.status_code


def change_owner(device_id, user):
    ready_for_deploy_status_id = 2
    # status_id = 2 - ready for deploy
    # checkout_to_type = user / location / asset
    # assigned_user - user to whom the asset should be assigned to
    # iphone13 id 974
    # qa department id 243
    # rory = 96

    url = config('HARDWARE_URL') + '/' + str(device_id) + '/checkout'

    payload = {
        "checkout_to_type": "user",
        "status_id": ready_for_deploy_status_id,
        "assigned_user": user
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


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
