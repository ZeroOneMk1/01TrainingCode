import time
import datetime

for _ in range(10):
    a = datetime.datetime.now()
    time.sleep(1/70)
    print(datetime.datetime.now() - a)

a = datetime.datetime.now()
time.sleep(1)
print(datetime.datetime.now() - a)