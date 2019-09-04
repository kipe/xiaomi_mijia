import pendulum
from math import isfinite

from bluepy import btle
from bitstring import BitArray


class Mijia(object):
    # '''An instance of Mijia. Usually created by Mijia.scan().'''
    def __init__(self,
                 address,
                 temperature=float('nan'),
                 humidity=float('nan'),
                 battery_level=float('nan')):
        '''Initialize an instance of Mijia.
        Ususally created by Mijia.scan().

        Args:
            address (str): the MAC address of the Mijia

        Keyword args:
            temperature (float): temperature. Defaults to NaN.
            humidity (float): humidity. Defaults to NaN.
            battery_level (float): pressure. Defaults to NaN.
        '''

        #: pendulum.instance: datetime of last update
        self.last_seen = pendulum.now()
        self.address = address
        self.temperature = temperature
        self.humidity = humidity
        self.battery_level = battery_level

    def __repr__(self):
        return '<Mijia %s %.02fc, %.02f%%, %.0f%%, %s>' % (
            self.address,
            self.temperature,
            self.humidity,
            self.battery_level,
            self.last_seen.isoformat()
        )

    def update(self,
               temperature=None,
               humidity=None,
               battery_level=None,
               update_last_seen=True,
               **kwargs):
        '''Update the Mijia instance.

        Updates last_seen and sets movement_detected, if value differs from
        previous.

        Keyword args:
            temperature (float): temperature. Defaults to previous value
            humidity (float): humidity. Defaults to previous value
            battery_level (float): battery_level. Defaults to previous value

            update_last_seen (boolean): should the last_seen value be updated? Defaults to True
        '''

        if update_last_seen:
            self.last_seen = pendulum.now()

        self.temperature = temperature if isfinite(temperature) else self.temperature
        self.humidity = humidity if isfinite(humidity) else self.humidity
        self.battery_level = battery_level if isfinite(battery_level) else self.battery_level

    def as_dict(self):
        '''Returns all (significant) values as a dictionary.'''
        values = {
            'address': self.address,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'battery_level': self.battery_level,
            'last_seen': self.last_seen,
        }
        return values

    @classmethod
    def parse(cls, address, data):
        '''Used to parse data received from Mijia.
        Currently supports versions 3 and 5 of the protocol.

        Arguments:
            address (str): MAC address of Mijia.
            data (bytes): received data in bytes.
        '''
        b = BitArray(bytes=bytearray.fromhex(data))

        if len(b) == 160:
            uuid, flag, id, index, mac, datatype, length, temperature, humidity = b.unpack(
                'uintle:16, uintle:16, uintle:16, uintle:8, uintle:48, uintle:16, uintle:8, intle:16, intle:16'
            )
            temperature /= 10.0
            humidity /= 10.0
            return cls(
                address,
                temperature=float(temperature),
                humidity=float(humidity),
            )
        if len(b) == 136:
            uuid, flag, id, index, mac, datatype, length, battery_level = b.unpack(
                'uintle:16, uintle:16, uintle:16, uintle:8, uintle:48, uintle:16, uintle:8, uintle:8'
            )
            return cls(
                address,
                battery_level=float(battery_level),
            )

    # @classmethod
    # def scan(cls, interface_index=0, timeout=2):
    #     '''Scan for Mijias. Yields Mijias as they're found.

    #     Keyword arguments:
    #             interface_index: The index of bluetooth device to use.
    #                 Defaults to 0
    #             timeout (float): Timeout for the scan. Defaults to 2.0.
    #     '''
    #     for device in btle.Scanner(interface_index).scan(timeout):
    #         try:
    #             # print(device.scanData)
    #             tag = cls.parse(device.addr, device.getValueText(0x16))
    #             if tag:
    #                 yield tag
    #         except:
    #             pass
