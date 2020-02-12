from tunastream import Tuna

while True:
    Tuna.send(18650, 'ltp', 'largeImg.png')
    print('Sent')
