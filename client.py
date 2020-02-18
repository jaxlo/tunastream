from tunastream import Tuna
from timeit import default_timer as timer

start = timer()
Tuna.sendFile(18650, '120.0.0.1', '/home/jax/Downloads/manjaro-xfce-18.1.4-191210-linux54.iso')
print(timer() - start)
