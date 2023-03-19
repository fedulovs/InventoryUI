class Device:
    """id text primary key,
       device_name text,
       brand text,
       os_name text,
       os_version text,
       cpu text,
       owner text,
       snipe_it text,
       serial_number text,
       identifier text,
       comment text"""

    def __init__(self, device_name, brand, os_name, os_version, cpu, owner, snipe_it, serial_number, identifier,
                 comment, image_url):
        self.device_name = device_name
        self.brand = brand
        self.os_name = os_name
        self.os_version = os_version
        self.cpu = cpu
        self.owner = owner
        self.snipe_it = snipe_it
        self.serial_number = serial_number
        self.identifier = identifier
        self.comment = comment
        self.image_url = image_url

    @property
    def full_os(self):
        return f'{self.os_name} {self.os_version}'
