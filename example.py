import time
from xiaomi.mijiadaemon import MijiaDaemon

def callback(tag, is_new=False):
    print(tag)

m = MijiaDaemon(callback=callback)
m.start()
try:
    while True:
        time.sleep(30)
finally:
    m.stop()
