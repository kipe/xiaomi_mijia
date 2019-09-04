import threading
from math import isfinite

from bluepy import btle
from xiaomi.mijia import Mijia


class MijiaDaemon(threading.Thread):
    '''A threaded scanner for Mijias.'''

    class ScanDelegate(btle.DefaultDelegate):
        '''
        Custom delegate to receive btle scan results,
        used internally to notify MijiaDaemon.

        Keyword arguments:
                interface_index (int): the index of bluetooth device to use.
                    Defaults to 0.
                callback: function to call when receiving data.
                    Defaults to None.
                    Function signature is callback(tag, is_new: False)
        '''
        def __init__(self, daemon, *args, **kwargs):
            self.daemon = daemon
            # Use old style class to initialize,
            # as that's required by btle ":D"
            btle.DefaultDelegate.__init__(self, *args, **kwargs)

        def handleDiscovery(self, device, is_new_device, is_new_data):
            ''' Call update_tag method from MijiaDaemon. '''
            # try:
            adv_data = device.getValueText(0x16)
            if adv_data is not None and '95fe' in adv_data:
                self.daemon.update_tag(device, adv_data)
            # except:
            #     pass

    def __init__(self, interface_index=0, callback=None, *args, **kwargs):
        self.__stop = threading.Event()
        self.interface_index = interface_index
        self.callback_function = callback
        self.tags = {}
        self.__new_devices_found = threading.Event()
        super(MijiaDaemon, self).__init__(*args, **kwargs)

    def run(self):
        '''Main-loop of the daemon, started via daemon.start().'''
        scanner = btle.Scanner().withDelegate(MijiaDaemon.ScanDelegate(self))
        scanner.start(passive=True)

        while not self.__stop.is_set():
            scanner.process(timeout=0.5)

        scanner.stop()

    def stop(self):
        '''Used to stop the (running) daemon.'''
        self.__stop.set()

    def update_tag(self, device, adv_data):
        '''Updates the Mijia, based on the information received from
        ScanDelegate.handleDiscovery.'''
        try:
            tag = Mijia.parse(device.addr, adv_data)
        except:
            tag = None

        if not tag:
            return

        is_new = False
        if tag.address not in self.tags:
            self.tags[tag.address] = tag
            is_new = True

        self.tags[tag.address].update(
            **tag.as_dict(),
            update_last_seen=isfinite(tag.temperature),
        )
        self.callback(self.tags[tag.address], is_new=is_new)

    def callback(self, tag, is_new=False):
        '''Callback to run when a broadcast from a Mijia has been
        received.'''
        if self.callback_function:
            self.callback_function(tag, is_new=is_new)
