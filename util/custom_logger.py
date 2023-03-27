import datetime


def write_to_custom_log(message):
    with open("device-logs.txt", mode='a') as file:
        file.write(f'{datetime.datetime.now()} - {message}\n')
